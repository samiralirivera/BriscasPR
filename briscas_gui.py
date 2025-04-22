import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

from briscas import BriscasGame, AgenteAleatorio, Jugador, VALORES, PALOS

# Map card values to face names for placeholder generation
CARD_NAMES = {1: 'As', 3: 'Tres', 12: 'Rey', 11: 'Caballo', 10: 'Sota'}

class BriscasGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Briscas GUI")
        # Initialize game with human and AI
        human = Jugador("Tú")
        ai = AgenteAleatorio("IA Básica")
        self.game = BriscasGame([human, ai])
        self.load_images()
        self.setup_ui()
        # Flags for exchange rules
        self.round_count = 0
        self.exchanged_two = False
        self.exchanged_seven = False
        self.update_view()

    def load_images(self):
        # Expect images in ./images; auto-generate placeholders if missing
        self.images = {}
        if not os.path.exists("images"):
            os.makedirs("images")
        for v in VALORES:
            for p in PALOS:
                filename = f"{v}_{p}.png"
                path = os.path.join("images", filename)
                if not os.path.isfile(path):
                    # create placeholder image
                    img0 = Image.new("RGB", (100, 150), "white")
                    draw = ImageDraw.Draw(img0)
                    font = ImageFont.load_default()
                    nombre = CARD_NAMES.get(v, str(v))
                    text = f"{nombre} de {p}"
                    # Measure text size using textbbox (Pillow >=8.0)
                    bbox = draw.textbbox((0, 0), text, font=font)
                    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    draw.text(((100 - w) / 2, (150 - h) / 2), text, fill="black", font=font)
                    img0.save(path)
                img = Image.open(path).resize((100, 150), Image.LANCZOS)
                self.images[(v, p)] = ImageTk.PhotoImage(img)
        # Generate back-of-card image for opponent hand
        back0 = Image.new("RGB", (100, 150), "navy")
        db = ImageDraw.Draw(back0)
        db.rectangle([5, 5, 95, 145], fill="navy", outline="white", width=4)
        self.card_back = ImageTk.PhotoImage(back0)

    def setup_ui(self):
        # Reset button at top-right corner
        tk.Button(self.root, text="Reset", command=self.restart, font=("Arial",10)).pack(anchor='ne', padx=5, pady=5)
        self.vida_label = tk.Label(self.root, text="Triunfo")
        self.vida_label.pack(pady=10)
        # Opponent hand (face-down)
        self.opponent_label = tk.Label(self.root, text="Mano oponente")
        self.opponent_label.pack()
        self.opponent_frame = tk.Frame(self.root)
        self.opponent_frame.pack(pady=5)
        # Human hand
        self.hand_label = tk.Label(self.root, text="Tu mano")
        self.hand_label.pack()
        self.hand_frame = tk.Frame(self.root)
        self.hand_frame.pack(pady=5)
        # Info area
        self.info_label = tk.Label(self.root, text="")
        self.info_label.pack(pady=10)
        # Table for played cards
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(pady=5)
        # Score display
        self.score_label = tk.Label(self.root, text="", font=("Arial",12,"bold"))
        self.score_label.pack(pady=5)

    def update_view(self):
        # Show trump card
        vida = self.game.vida
        img = self.images[(vida.valor, vida.palo)]
        self.vida_label.config(image=img, text=f"Triunfo: {vida}", compound='top')
        self.vida_label.image = img

        # Show opponent hand as face-down cards
        for w in self.opponent_frame.winfo_children():
            w.destroy()
        ai = self.game.jugadores[1]
        for _ in ai.mano:
            back_img = self.card_back
            lbl = tk.Label(self.opponent_frame, image=back_img)
            lbl.image = back_img
            lbl.pack(side='left', padx=5)

        # Show human hand as buttons with swap options
        for widget in self.hand_frame.winfo_children():
            widget.destroy()
        human = self.game.jugadores[0]
        vida = self.game.vida
        for idx, card in enumerate(human.mano):
            container = tk.Frame(self.hand_frame)
            container.pack(side='left', padx=5)
            img = self.images[(card.valor, card.palo)]
            btn = tk.Button(container, image=img, command=lambda i=idx: self.play(i))
            btn.image = img
            btn.pack()
            # Swap 2 for trump on first round
            if card.valor == 2 and card.palo == vida.palo and self.round_count == 0 and not self.exchanged_two:
                tk.Button(container, text="2↔", command=lambda i=idx: self.exchange_two(i), font=("Arial",8)).pack()
            # Swap 7 for trump after first round
            elif card.valor == 7 and card.palo == vida.palo and self.round_count >= 1 and not self.exchanged_seven:
                tk.Button(container, text="7↔", command=lambda i=idx: self.exchange_seven(i), font=("Arial",8)).pack()
        # Update initial score
        human, ai = self.game.jugadores
        sc = self.game.puntos
        self.score_label.config(text=f"Puntos: {human.nombre} {sc.get(human,0)} - {ai.nombre} {sc.get(ai,0)}")
        # Show played cards in table
        for w in self.table_frame.winfo_children():
            w.destroy()
        if self.game.mano_actual:
            img_h = self.images[(self.game.mano_actual[0][1].valor, self.game.mano_actual[0][1].palo)]
            lbl_h = tk.Label(self.table_frame, image=img_h)
            lbl_h.image = img_h
            lbl_h.pack(side='left', padx=10)
            img_ai = self.images[(self.game.mano_actual[1][1].valor, self.game.mano_actual[1][1].palo)]
            lbl_ai = tk.Label(self.table_frame, image=img_ai)
            lbl_ai.image = img_ai
            lbl_ai.pack(side='left', padx=10)
        # Show round winner
        if self.game.mano_actual:
            winner = self.game.determinar_ganador()
            self.info_label.config(text=f"Ganó la ronda: {winner.nombre}")
        # Update or finish: continuar solo si ambos tienen cartas
        if human.mano and ai.mano:
            self.round_count += 1
        else:
            self.show_final()

    def play(self, idx):
        human, ai = self.game.jugadores
        # Human plays
        card_h = human.mano.pop(idx)
        # AI plays
        card_ai = ai.jugar_carta(self.game)
        # Register round
        self.game.mano_actual = [(human, card_h), (ai, card_ai)]
        winner = self.game.determinar_ganador()
        self.game.puntos[winner] += sum(c.puntos for _, c in self.game.mano_actual)
        # Show played cards in table
        for w in self.table_frame.winfo_children():
            w.destroy()
        img_h = self.images[(card_h.valor, card_h.palo)]
        lbl_h = tk.Label(self.table_frame, image=img_h)
        lbl_h.image = img_h
        lbl_h.pack(side='left', padx=10)
        img_ai = self.images[(card_ai.valor, card_ai.palo)]
        lbl_ai = tk.Label(self.table_frame, image=img_ai)
        lbl_ai.image = img_ai
        lbl_ai.pack(side='left', padx=10)
        # Show round winner
        self.info_label.config(text=f"Ganó la ronda: {winner.nombre}")
        # Update score
        self.score_label.config(text=f"Puntos: {human.nombre} {self.game.puntos.get(human,0)} - {ai.nombre} {self.game.puntos.get(ai,0)}")
        # Draw cards: winner first, then other
        draw_order = [winner] + [j for j in [human, ai] if j != winner]
        for jugador in draw_order:
            if self.game.mazo:
                jugador.recibir_carta(self.game.mazo.pop())
        # Update or finish: continuar solo si ambos tienen cartas
        if human.mano and ai.mano:
            self.round_count += 1
            self.update_view()
        else:
            self.show_final()

    def show_final(self):
        # Remove only non-table elements and show final below last table
        self.root.title("Resultado Final")
        # Destroy control frames except table_frame
        self.vida_label.destroy()
        self.opponent_label.destroy()
        self.opponent_frame.destroy()
        self.hand_label.destroy()
        self.hand_frame.destroy()
        self.score_label.destroy()
        # Repurpose info_label as header
        self.info_label.config(text="¡Juego Terminado!", font=("Arial",24,"bold"))
        self.info_label.pack(pady=20)
        resultados = sorted(self.game.puntos.items(), key=lambda x: x[1], reverse=True)
        for pos, (jug, pts) in enumerate(resultados, start=1):
            tk.Label(self.root, text=f"{pos}. {jug.nombre}: {pts} puntos", font=("Arial",18)).pack(pady=5)
        tk.Button(self.root, text="Salir", command=self.root.destroy, font=("Arial",14)).pack(pady=20)

    def restart(self):
        # Reset game state and rebuild UI
        human = Jugador("Tú")
        ai = AgenteAleatorio("IA Básica")
        self.game = BriscasGame([human, ai])
        self.load_images()
        # Recreate UI
        for w in self.root.winfo_children():
            w.destroy()
        self.root.title("Briscas GUI")
        self.setup_ui()
        self.update_view()

    def exchange_two(self, idx):
        human, ai = self.game.jugadores
        card = human.mano.pop(idx)
        old_vida = self.game.vida
        human.mano.append(old_vida)
        self.game.vida = card
        self.exchanged_two = True
        self.update_view()

    def exchange_seven(self, idx):
        human, ai = self.game.jugadores
        card = human.mano.pop(idx)
        old_vida = self.game.vida
        human.mano.append(old_vida)
        self.game.vida = card
        self.exchanged_seven = True
        self.update_view()

def main():
    app = BriscasGUI()
    app.root.mainloop()

if __name__ == "__main__":
    main()
