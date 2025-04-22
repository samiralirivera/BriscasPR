# Briscas de Puerto Rico

Juego de cartas Briscas con reglas puertorriqueñas implementado en Python con interfaz Tkinter.

## Características
- Lógica completa de Briscas (mazo, reparto, rondas, determinación de ganador).
- Interfaz gráfica con imágenes de cartas y marcador en tiempo real.
- Intercambio del **2 de vida** en la primera ronda.
- Intercambio del **7 de vida** a partir de la segunda ronda.
- Botón **Reset** para reiniciar la partida en cualquier momento.

## Requisitos
- Python 3.7 o superior
- tkinter (incluido en la mayoría de distribuciones de Python)
- Pillow (para manejo de imágenes)

## Instalación
```bash
git clone https://github.com/usuario/briscas-pr.git
cd briscas-pr
python -m venv venv         # opcional
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Uso
```bash
python briscas_gui.py
```
- Al inicio se reparte la mano (3 cartas). La **última carta** de la pila determina el palo de triunfo.
- Durante la **primera ronda**, si tienes el **2** del palo de triunfo, aparece un botón `2↔` junto a esa carta para intercambiarla por la carta de triunfo.
- En rondas posteriores, si posees el **7** del palo de triunfo, aparece un botón `7↔` para intercambiarlo.
- Haz clic en la carta que deseas jugar; el sistema mostrará la jugada de la IA y actualizará el marcador.
- La partida termina cuando se acaben las cartas o se alcance el umbral de puntos.
- Usa **Reset** en la esquina superior para empezar una nueva partida en cualquier momento.

## Estructura del proyecto
```
Briscas/                # Carpeta raíz
├── briscas.py           # Lógica del juego y reglas
├── briscas_gui.py       # Interfaz Tkinter y manejo de eventos
├── images/              # Carpeta de imágenes (placeholders si faltan)
├── images/recortar_briscas.py # Herramienta para generar imágenes de cartas
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documentación del proyecto
```

## Licencia
MIT 2025
