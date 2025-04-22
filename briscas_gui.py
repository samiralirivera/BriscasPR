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

    def setup_ui(self):
        self.vida_label = tk.Label(self.root, text="Triunfo")
        self.vida_label.pack(pady=10)
        self.hand_frame = tk.Frame(self.root)
        self.hand_frame.pack(pady=10)
        self.info_label = tk.Label(self.root, text="")
        self.info_label.pack(pady=10)

    def update_view(self):
        # Show trump card
        vida = self.game.vida
        img = self.images[(vida.valor, vida.palo)]
        self.vida_label.config(image=img, text=f"Triunfo: {vida}", compound='top')
        self.vida_label.image = img

        # Show human hand as buttons
        for widget in self.hand_frame.winfo_children():
            widget.destroy()
        human = self.game.jugadores[0]
        for idx, card in enumerate(human.mano):
            img = self.images[(card.valor, card.palo)]
            btn = tk.Button(self.hand_frame, image=img, command=lambda i=idx: self.play(i))
            btn.image = img
            btn.pack(side='left', padx=5)

    def play(self, idx):
        human, ai = self.game.jugadores
        # Human plays
        card_h = human.mano.pop(idx)
        # AI plays
        card_ai = ai.jugar_carta(self.game)
        # Display played cards
        played = f"Tú jugaste: {card_h}\nIA jugó: {card_ai}"
        self.info_label.config(text=played)
        # Register round
        self.game.mano_actual = [(human, card_h), (ai, card_ai)]
        winner = self.game.determinar_ganador()
        self.game.puntos[winner] += sum(c.puntos for _, c in self.game.mano_actual)
        # Draw cards: winner first
        draw_order = [winner] + [j for j in [human, ai] if j != winner]
        for jugador in draw_order:
            if self.game.mazo:
                jugador.recibir_carta(self.game.mazo.pop())
        # Update or finish
        if human.mano:
            self.update_view()
        else:
            results = "\n".join(f"{p.nombre}: {pts}" for p, pts in self.game.puntos.items())
            messagebox.showinfo("Resultado Final", results)
            self.root.destroy()

def main():
    app = BriscasGUI()
    app.root.mainloop()

if __name__ == "__main__":
    main()
