import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
from datetime import datetime

def generar_heatmap(similitudes):
    # Extraer nombres únicos de documentos
    nombres = sorted(set([doc for doc1, doc2, _ in similitudes for doc in (doc1, doc2)]))
    n = len(nombres)
    
    # Crear una matriz de similitud inicializada en ceros
    matriz = np.zeros((n, n))

    # Llenar la matriz con los valores de similitud
    for doc1, doc2, score in similitudes:
        i, j = nombres.index(doc1), nombres.index(doc2)
        matriz[i, j] = matriz[j, i] = score * 100  # Simetría

    # Crear el directorio para guardar gráficos si no existe
    os.makedirs('resultados/graficos', exist_ok=True)

    # Configurar el heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(matriz, xticklabels=nombres, yticklabels=nombres, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Similitud (%)'})

    plt.title("Mapa de Calor de Similitud entre Documentos")
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

    # Guardar el gráfico
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'resultados/graficos/heatmap_similitudes_{timestamp}.png'
    plt.savefig(filename)
    plt.show()
