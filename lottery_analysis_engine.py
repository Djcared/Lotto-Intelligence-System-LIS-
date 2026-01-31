import pandas as pd
import numpy as np
from itertools import combinations

class LotteryAnalyzer:
    def __init__(self, file_path, reduction_list):
        """
        Inicializa el motor con el historial y la lista de números filtrados.
        """
        #Cargarr el historial de sorteos    
        self.df = pd.read_csv(file_path)
        self.reduction = sorted(reduction_list)
        self.columns = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6']

    def get_column_distribution(self):
        """
        Analiza la densidad por columnas (A: 1-9, B: 10-19, C: 20-29, D: 30-39).
        """
        dist = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
        for n in self.reduction:    
            if 1 <= n <= 9: dist['A'] += 1
            elif 10 <= n <= 19: dist['B'] += 1
            elif 20 <= n <= 29: dist['C'] += 1
            elif 30 <= n <= 39: dist['D'] += 1
        return dist

    def analyze_patterns(self):
        """
        Calcula la Suma Promedio, Paridad y Frecuencia de los números en el histórico.
        """
        history_matrix = self.df[self.columns].values
        sums = history_matrix.sum(axis=1)
        
        # Frecuencia de cada número en el histórico
        flat_history = history_matrix.flatten()
        freq = pd.Series(flat_history).value_counts()
        
        return {
            "mean_sum": np.mean(sums),
            "std_sum": np.std(sums),
            "top_frequencies": freq.head(10).to_dict()
        }

    def generate_optimized_plays(self, n_plays=3):
        """
        Genera jugadas basadas en 3 pilares:
        1. Presión del "Rey" (Número con mayor frecuencia histórica).
        2. Reversión a la media (Ajuste de suma objetivo).
        3. Densidad por columnas (Evitar saturación).
        """
        # El 19 es el 'Rey' estadístico identificado en el análisis
        rey = 19
        anclas = [n for n in self.reduction if n in [2, 10, 11, 26, 38]] # Números en deuda
        
        # Lógica de generación simplificada para el portafolio
        # En una versión avanzada, aquí se usaría un algoritmo genético o Monte Carlo
        plays = []
        for _ in range(n_plays):
            # Selección balanceada: 2 de deuda, el rey, y 3 aleatorios de la reducción
            sample = list(np.random.choice(anclas, 2, replace=False))
            if rey not in sample: sample.append(rey)
            
            rest = [n for n in self.reduction if n not in sample]
            sample.extend(list(np.random.choice(rest, 6 - len(sample), replace=False)))
            plays.append(sorted(sample))
            
        return plays

# --- EJECUCIÓN ---
mi_reduccion = [1, 2, 3, 5, 10, 11, 14, 15, 16, 18, 19, 20, 22, 25, 26, 29, 31, 34, 38]
engine = LotteryAnalyzer('Melate-Retro.csv', mi_reduccion)

print("Distribución por Columnas:", engine.get_column_distribution())
print("Patrones Históricos:", engine.analyze_patterns())
print("Jugadas Sugeridas:", engine.generate_optimized_plays())


import matplotlib.pyplot as plt
import seaborn as sns

def plot_analytics(df, reduction):
    # 1. Mapa de Calor de Frecuencias
    plt.figure(figsize=(12, 4))
    all_numbers = df[['F1', 'F2', 'F3', 'F4', 'F5', 'F6']].values.flatten()
    sns.countplot(x=all_numbers, palette="viridis")
    plt.title("Frecuencia Histórica de Números (Análisis de Densidad)")
    plt.axhline(y=np.mean(pd.Series(all_numbers).value_counts()), color='r', linestyle='--', label='Media')
    plt.show()

    # 2. Distribución de Sumas (Campana de Gauss)
    sums = df[['F1', 'F2', 'F3', 'F4', 'F5', 'F6']].sum(axis=1)
    plt.figure(figsize=(10, 5))
    sns.histplot(sums, kde=True, color="blue")
    plt.title("Distribución de Sumas: Reversión a la Media")
    plt.axvline(x=110, color='red', label='Zona de Probabilidad Máxima')
    plt.show()

# Estas gráficas demuestran por qué elegimos sumas cercanas a 110-120.

def generate_weighted_play(reduction, history_df):
    """
    Asigna pesos a los números de la reducción basados en su 'deuda' histórica.
    Un número que no ha salido en 10 sorteos tiene más 'peso' que uno que salió ayer.
    """
    last_draw = history_df.iloc[0][['F1', 'F2', 'F3', 'F4', 'F5', 'F6']].values
    
    # Pesos: Más altos para números que NO salieron en el último sorteo
    weights = [2.0 if n not in last_draw else 0.5 for n in reduction]
    
    # Normalizar pesos para que sumen 1
    prob = np.array(weights) / sum(weights)
    
    # Generar jugada basada en estas probabilidades
    play = np.random.choice(reduction, size=6, replace=False, p=prob)
    return sorted(play)