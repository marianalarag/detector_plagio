import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from datetime import datetime

def generar_graficos(similitudes, max_docs=5):
    # Limitar el número de pares de documentos a comparar
    similitudes = similitudes[:max_docs * (max_docs - 1) // 2]

    # Obtener lista única de documentos
    documentos = sorted(set([doc for sim in similitudes for doc in sim[:2]]))[:max_docs]

    # Crear matriz de similitud (llenar con ceros inicialmente)
    matriz = np.zeros((len(documentos), len(documentos)))

    doc_index = {doc: idx for idx, doc in enumerate(documentos)}

    for doc1, doc2, score in similitudes:
        if doc1 in doc_index and doc2 in doc_index:
            i, j = doc_index[doc1], doc_index[doc2]
            matriz[i][j] = score * 100  # Convertir a porcentaje
            matriz[j][i] = score * 100  # Simetría

    # Ordenar por promedio de similitud de mayor a menor
    promedios = matriz.mean(axis=1)
    indices_ordenados = np.argsort(-promedios)  # Negativo para orden descendente

    matriz_ordenada = matriz[indices_ordenados, :][:, indices_ordenados]
    documentos_ordenados = [documentos[i] for i in indices_ordenados]

    # Crear el directorio si no existe
    os.makedirs('resultados/graficos', exist_ok=True)

    # Configurar tamaño del gráfico en función de la cantidad de documentos
    plt.figure(figsize=(1.5 * len(documentos), 1.2 * len(documentos)))

    # Generar heatmap con anotaciones
    ax = sns.heatmap(
        matriz_ordenada,
        xticklabels=documentos_ordenados,
        yticklabels=documentos_ordenados,
        annot=True,
        fmt=".1f",
        cmap="YlGnBu",
        cbar_kws={'label': 'Similitud (%)'},
        linewidths=0.5,
        linecolor='gray'
    )

    plt.title("Mapa de Calor de Similitud entre Documentos (Ordenado)", fontsize=14)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.yticks(rotation=0, fontsize=10)

    # Ajustar el diseño
    plt.tight_layout()

    # Guardar con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'resultados/graficos/heatmap_similitud_{timestamp}.png'
    plt.savefig(filename, dpi=300, facecolor='white')
    plt.close()
    print(f"[✔] Imagen guardada en: {filename}")
