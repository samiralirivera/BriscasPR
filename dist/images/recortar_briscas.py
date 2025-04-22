from PIL import Image

# Carga la imagen original
img = Image.open("Baraja_española_completa.png")

# Parámetros de la cuadrícula
cartas_por_fila = 12  # columnas
cartas_por_columna = 4  # SOLO las primeras 4 filas (0-3)

ancho_carta = img.width // cartas_por_fila
alto_carta = img.height // 5  # La imagen tiene 5 filas, pero solo usamos 4

# Índices de columnas válidas para Briscas (1-7, 10-12)
indices_briscas = [0, 1, 2, 3, 4, 5, 6, 9, 10, 11]  # columnas para 1-7, 10-12

palos = ['oros', 'copas', 'espadas', 'bastos']
valores = [1,2,3,4,5,6,7,10,11,12]

carta_num = 0
for fila in range(cartas_por_columna):  # SOLO filas 0,1,2,3
    palo = palos[fila]
    for idx, col in enumerate(indices_briscas):
        valor = valores[idx]
        left = col * ancho_carta
        upper = fila * alto_carta
        right = left + ancho_carta
        lower = upper + alto_carta
        carta = img.crop((left, upper, right, lower))
        nombre_archivo = f"{valor}_{palo}.png"
        carta.save(nombre_archivo)
        carta_num += 1

print(f"¡Listo! Se guardaron {carta_num} cartas individuales de Briscas.")
