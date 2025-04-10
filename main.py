import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import random
from datetime import datetime
import subprocess

# Tabla hash para almacenar trigramas de cada documento
tabla_trigramas = {}

# Cargar documentos aleatorios desde un directorio
def cargar_documentos_aleatorios(directorio='documentos', cantidad=5):
    archivos_txt = [f for f in os.listdir(directorio) if f.endswith('.txt')]
    seleccionados = random.sample(archivos_txt, min(cantidad, len(archivos_txt)))

    documentos = {}
    for archivo in seleccionados:
        ruta = os.path.join(directorio, archivo)
        with open(ruta, 'r', encoding='utf-8') as f:
            documentos[archivo] = f.read()
    return documentos

# Generar trigramas y guardarlos en la tabla hash
def generar_trigramas(texto):
    texto = texto.lower().replace('\n', ' ')
    return set([texto[i:i+3] for i in range(len(texto) - 2)])

# Calcular similitud usando trigramas desde la tabla hash
def calcular_similitud(doc1_nombre, doc2_nombre, documentos):
    if doc1_nombre not in tabla_trigramas:
        tabla_trigramas[doc1_nombre] = generar_trigramas(documentos[doc1_nombre])
    if doc2_nombre not in tabla_trigramas:
        tabla_trigramas[doc2_nombre] = generar_trigramas(documentos[doc2_nombre])

    trigrams1 = tabla_trigramas[doc1_nombre]
    trigrams2 = tabla_trigramas[doc2_nombre]
    interseccion = trigrams1 & trigrams2
    union = trigrams1 | trigrams2
    return len(interseccion) / len(union) if union else 0.0

# Comparar todos los pares posibles
def obtener_similitudes(documentos):
    nombres = list(documentos.keys())
    similitudes = []
    for i in range(len(nombres)):
        for j in range(i + 1, len(nombres)):
            doc1 = nombres[i]
            doc2 = nombres[j]
            sim = calcular_similitud(doc1, doc2, documentos)
            similitudes.append((doc1, doc2, sim))
    return similitudes

# Generar gráfico de similitud
def generar_graficos(similitudes):
    if not similitudes:
        print("[ERROR] La lista de similitudes está vacía. No se puede generar gráfico.")
        return

    nombres_documentos = sorted(list(set(doc for par in similitudes for doc in par[:2])))
    index_map = {nombre: i for i, nombre in enumerate(nombres_documentos)}
    n = len(nombres_documentos)
    matriz = np.zeros((n, n))

    for doc1, doc2, sim in similitudes:
        i, j = index_map[doc1], index_map[doc2]
        matriz[i, j] = sim * 100
        matriz[j, i] = sim * 100

    promedio_similitud = matriz.mean(axis=1)
    orden_indices = np.argsort(-promedio_similitud)
    matriz_ordenada = matriz[orden_indices, :][:, orden_indices]
    nombres_ordenados = [nombres_documentos[i] for i in orden_indices]

    os.makedirs('resultados/graficos', exist_ok=True)

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

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'resultados/graficos/heatmap_similitud_ordenado_{timestamp}.png'
    plt.savefig(filename, dpi=300, facecolor='white')
    plt.close()
    print(f"[✔] Imagen guardada en: {filename}")

    try:
        subprocess.run(['start', filename], shell=True)
    except Exception as e:
        print(f"[ERROR] No se pudo abrir la imagen automáticamente: {e}")

# Ejecutar todo
documentos = cargar_documentos_aleatorios(directorio='documentos', cantidad=6)
similitudes = obtener_similitudes(documentos)
generar_graficos(similitudes)
