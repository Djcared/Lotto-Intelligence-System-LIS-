# Lotto-Intelligence-System-LIS-
Este proyecto implementa un motor de análisis estadístico diseñado para identificar patrones de distribución y anomalías de frecuencia en el histórico, se sigue trabajando en el y se aceptan adecuaciones.

Proyecto: Motor de Análisis Estadístico para Melate Retro
Este proyecto utiliza técnicas de Data Mining y Análisis Predictivo aplicadas al histórico de sorteos de lotería. El objetivo no es predecir el azar, sino optimizar la selección de números basándose en la Reversión a la Media y la Densidad de Probabilidad.

Metodología Utilizada:
1. Reducción de Dimensiones: Filtramos el universo de 39 números a una "Reducción de Oro" (24 a 15 números) basada en la frecuencia de aparición y ciclos de deuda (ausencia prolongada).

2. Análisis de Cuadrantes (Columnas): Dividimos el tablero en 4 bloques (A, B, C, D). El sistema detecta "vacíos de energía" (columnas que no han salido) para predecir el próximo "latigazo" o rebote estadístico.

3.Identificación de "Números Ancla": Se identificó al 19 como el "Rey del Histórico" por su alta frecuencia acumulada, utilizándolo como base constante en las simulaciones.

4.Optimización de Sumas: Las combinaciones se filtran para que su suma total caiga dentro de una desviación estándar de la media histórica ($110 \pm 15$), descartando combinaciones extremas que rara vez ocurren.

Tecnologías:
Python 3.x| Pandas: Manipulación y limpieza de datos históricos.| Numpy: Cálculos estadísticos y matrices. |Matplotlib/Seaborn: Visualización de la Campana de Gauss y Mapas de Calor de frecuencia.


Visualización de Calor y Campana de Gauss
El modelo incluye un análisis de Transición de Columnas. Si un sorteo satura la Columna A (como el último con el 1, 2, 7), el sistema calcula la probabilidad de 'salto' hacia la Columna B y C. Esto se basa en la observación histórica de que el sistema busca el equilibrio termodinámico, evitando que una zona del tablero permanezca activa por más de 3 ciclos consecutivos."


