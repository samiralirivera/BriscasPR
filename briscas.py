import random
from collections import defaultdict

# Valores y puntuaciones según reglas puertorriqueñas
VALORES = {
    1: 11, 3: 10, 12: 4, 11: 3, 10: 2,
    7: 0, 6: 0, 5: 0, 4: 0, 2: 0
}

PALOS = ['oros', 'copas', 'espadas', 'bastos']

class Carta:
    def __init__(self, valor, palo):
        self.valor = valor
        self.palo = palo
        self.puntos = VALORES[valor]
    
    def __repr__(self):
        nombres = {1: 'As', 3: 'Tres', 12: 'Rey', 11: 'Caballo', 10: 'Sota'}
        return f"{nombres.get(self.valor, str(self.valor))} de {self.palo}"

class BriscasGame:
    def __init__(self, jugadores):
        self.jugadores = jugadores
        self.mazo = []
        self.vida = None  # Palo de triunfo
        self.mano_actual = []
        self.puntos = defaultdict(int)
        self.turno = 0
        self.inicializar_juego()
    
    def inicializar_juego(self):
        self.mazo = self._crear_mazo()
        self.repartir()
    
    def _crear_mazo(self):
        return [Carta(v, p) for v in VALORES for p in PALOS]
    
    def repartir(self):
        random.shuffle(self.mazo)
        self.vida = self.mazo.pop()  # La última carta determina la vida
        
        for jugador in self.jugadores:
            jugador.mano = []
        
        # Reparto de 3 cartas a cada jugador
        for _ in range(3):
            for jugador in self.jugadores:
                jugador.recibir_carta(self.mazo.pop())
    
    def jugar_ronda(self):
        self.mano_actual = []
        orden_jugadores = self.jugadores[self.turno:] + self.jugadores[:self.turno]
        
        for jugador in orden_jugadores:
            carta_jugada = jugador.jugar_carta(self)
            self.mano_actual.append((jugador, carta_jugada))
        
        ganador = self.determinar_ganador()
        self.puntos[ganador] += sum(c.puntos for _, c in self.mano_actual)

        # Después de la ronda, ganador roba primero, luego los demás en orden de juego
        draw_order = [ganador] + [j for j in orden_jugadores if j != ganador]
        for jugador in draw_order:
            if self.mazo:
                jugador.recibir_carta(self.mazo.pop())
            else:
                break

        # Próximo turno inicia con el ganador
        self.turno = self.jugadores.index(ganador)
        return ganador
    
    def determinar_ganador(self):
        # Primera carta jugada determina el palo a seguir
        primer_palo = self.mano_actual[0][1].palo
        cartas_vida = [(j, c) for j, c in self.mano_actual if c.palo == self.vida.palo]
        
        if cartas_vida:
            # Gana la carta más alta de vida
            ganador = max(cartas_vida, key=lambda x: x[1].valor)
        else:
            # Gana la carta más alta del palo inicial
            cartas_palo = [(j, c) for j, c in self.mano_actual if c.palo == primer_palo]
            ganador = max(cartas_palo, key=lambda x: x[1].valor)
        
        return ganador[0]

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mano = []
    
    def recibir_carta(self, carta):
        self.mano.append(carta)
    
    def jugar_carta(self, juego):
        # Método base para ser sobrescrito por implementaciones específicas
        return random.choice(self.mano)

    def __repr__(self):
        return self.nombre

class AgenteHumano(Jugador):
    def jugar_carta(self, juego):
        print(f"\n{self.nombre}, tu mano:")
        for i, carta in enumerate(self.mano):
            print(f"{i}: {carta}")
        print(f"Vida actual: {juego.vida.palo}")
        
        while True:
            try:
                seleccion = int(input(f"Elige una carta (0-{len(self.mano)-1}): "))
                if 0 <= seleccion < len(self.mano):
                    return self.mano.pop(seleccion)
                else:
                    print("Selección inválida. Intenta de nuevo.")
            except ValueError:
                print("Entrada inválida. Ingresa un número.")

class AgenteAleatorio(Jugador):
    def jugar_carta(self, juego):
        carta = random.choice(self.mano)
        self.mano.remove(carta)
        return carta

if __name__ == "__main__":
    # Ejemplo de uso básico
    jugadores = [
        AgenteHumano("Jugador 1"),
        AgenteAleatorio("IA Básica")
    ]
    
    juego = BriscasGame(jugadores)
    print(f"Vida: {juego.vida}")
    
    while all(jugador.mano for jugador in jugadores):
        ganador = juego.jugar_ronda()
        print("\n--- Nueva ronda ---")
        print(f"Ganador de la ronda: {ganador.nombre}")
        # Mostrar cartas jugadas por cada jugador
        print("Cartas jugadas:")
        for j, c in juego.mano_actual:
            print(f"  {j.nombre}: {c}")
        # Mostrar puntuaciones actuales
        print("Puntos acumulados:")
        for j, pts in juego.puntos.items():
            print(f"  {j.nombre}: {pts}")
    
    print("\n=== Resultado Final ===")
    # Ordenar resultados de mayor a menor
    resultados = sorted(juego.puntos.items(), key=lambda x: x[1], reverse=True)
    ganador_final, puntos_final = resultados[0]
    print(f"\n¡Ganador: {ganador_final.nombre} con {puntos_final} puntos!\n")
    print("Posiciones:")
    for pos, (jugador, pts) in enumerate(resultados, start=1):
        print(f"  {pos}. {jugador.nombre}: {pts} puntos")