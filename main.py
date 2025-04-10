import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime
import subprocess

def generar_graficos(similitudes):
    if not similitudes:
        print("[ERROR] La lista de similitudes está vacía. No se puede generar gráfico.")
        return

    # Obtener todos los documentos únicos
    nombres_documentos = sorted(list(set(doc for par in similitudes for doc in par[:2])))
    index_map = {nombre: i for i, nombre in enumerate(nombres_documentos)}
    n = len(nombres_documentos)

    # Crear matriz de similitud (n x n)
    matriz = np.zeros((n, n))

    for doc1, doc2, sim in similitudes:
        i, j = index_map[doc1], index_map[doc2]
        matriz[i, j] = sim * 100
        matriz[j, i] = sim * 100  # Asegurar simetría

    # Calcular similitud promedio por documento
    promedio_similitud = matriz.mean(axis=1)

    # Ordenar índices por similitud promedio descendente
    orden_indices = np.argsort(-promedio_similitud)

    # Reordenar matriz y nombres
    matriz_ordenada = matriz[orden_indices, :][:, orden_indices]
    nombres_ordenados = [nombres_documentos[i] for i in orden_indices]

    # Crear carpeta si no existe
    os.makedirs('resultados/graficos', exist_ok=True)

    # Crear heatmap
    plt.figure(figsize=(1.5 * n, 1.2 * n))
    sns.set(font_scale=0.9)

    ax = sns.heatmap(
        matriz_ordenada,
        annot=True,
        fmt=".1f",
        cmap="YlOrRd",
        xticklabels=nombres_ordenados,
        yticklabels=nombres_ordenados,
        linewidths=0.5,
        linecolor='gray',
        cbar_kws={'label': 'Similitud (%)'}
    )

    plt.title("Mapa de Calor de Similitud entre Documentos (Ordenado)", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

    # Guardar imagen
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'resultados/graficos/heatmap_similitud_ordenado_{timestamp}.png'
    plt.savefig(filename, dpi=300, facecolor='white')
    plt.close()
    print(f"[✔] Imagen guardada en: {filename}")

    # Abrir imagen automáticamente (Windows)
    try:
        subprocess.run(['start', filename], shell=True)
    except Exception as e:
        print(f"[ERROR] No se pudo abrir la imagen automáticamente: {e}")

# 📌 Ejemplo con más documentos
similitudes = [
    ("doc1.txt", "doc2.txt", 0.75),
    ("doc1.txt", "doc3.txt", 0.50),
    ("doc2.txt", "doc3.txt", 0.85),
    ("doc1.txt", "doc4.txt", 0.30),
    ("doc3.txt", "doc4.txt", 0.60),
    ("doc2.txt", "doc4.txt", 0.20),
    ("doc1.txt", "doc5.txt", 0.65),
    ("doc2.txt", "doc5.txt", 0.70),
    ("doc3.txt", "doc5.txt", 0.40),
    ("doc4.txt", "doc5.txt", 0.10),
    ("doc1.txt", "doc6.txt", 0.90),
    ("doc2.txt", "doc6.txt", 0.80),
    ("doc3.txt", "doc6.txt", 0.75),
    ("doc4.txt", "doc6.txt", 0.50),
    ("doc5.txt", "doc6.txt", 0.30),
]

# Ejecutar función
generar_graficos(similitudes)
