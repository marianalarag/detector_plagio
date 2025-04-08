import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime
import subprocess

def generar_graficos(similitudes, max_documentos=15):
    # Verificar si la lista de similitudes no está vacía
    if not similitudes:
        print("[ERROR] La lista de similitudes está vacía. No se puede generar gráfico.")
        return

    # Limitar a un número máximo de documentos si es necesario
    similitudes = similitudes[:max_documentos]

    # Obtener los nombres de los documentos únicos
    nombres_documentos = sorted(list(set([doc for par in similitudes for doc in par[:2]])))
    index_map = {nombre: i for i, nombre in enumerate(nombres_documentos)}
    
    # Crear la matriz de similitudes
    matriz = np.zeros((len(nombres_documentos), len(nombres_documentos)))

    for doc1, doc2, sim in similitudes:
        i, j = index_map[doc1], index_map[doc2]
        matriz[i, j] = sim * 100
        matriz[j, i] = sim * 100

    # Verificar la matriz de similitudes
    print(f"Matriz de similitudes:\n{matriz}")

    # Crear el directorio para los gráficos si no existe
    os.makedirs('resultados/graficos', exist_ok=True)

    # Crear la figura para el gráfico
    plt.figure(figsize=(12, 10))
    sns.set(font_scale=0.9)

    # Generar el mapa de calor (heatmap)
    ax = sns.heatmap(
        matriz,
        annot=True,
        fmt=".1f",
        cmap="YlOrRd",  # Cambia el mapa de colores si prefieres otro
        xticklabels=nombres_documentos,
        yticklabels=nombres_documentos,
        linewidths=0.5,
        linecolor='gray',
        cbar_kws={'label': 'Similitud (%)'}
    )

    # Título del gráfico
    plt.title("Mapa de Calor de Similitudes entre Documentos", fontsize=14)
    plt.tight_layout()

    # Crear un nombre único para el archivo de salida
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'resultados/graficos/heatmap_similitudes_{timestamp}.png'

    # Intentar guardar el gráfico
    try:
        plt.savefig(filename, dpi=300, facecolor='white')
        print(f"[✔] Imagen guardada correctamente en: {filename}")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar la imagen: {e}")
        return

    # Cerrar la figura de matplotlib
    plt.close()

    # Intentar abrir la imagen automáticamente
    try:
        subprocess.run(['start', filename], shell=True)
        print(f"[✔] Imagen abierta en el visor predeterminado.")
    except Exception as e:
        print(f"[ERROR] No se pudo abrir automáticamente la imagen: {e}")

# Ejemplo de llamada a la función con datos de similitudes
similitudes = [
    ("doc1.txt", "doc2.txt", 0.75),
    ("doc1.txt", "doc3.txt", 0.50),
    ("doc2.txt", "doc3.txt", 0.85),
    ("doc1.txt", "doc4.txt", 0.30),
    ("doc3.txt", "doc4.txt", 0.60),
    ("doc2.txt", "doc4.txt", 0.20),
    # Añadir más similitudes según sea necesario
]

# Llamar a la función para generar el gráfico
generar_graficos(similitudes)
