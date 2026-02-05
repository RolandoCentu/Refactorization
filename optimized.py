import os
import heapq
import time

# Emojis
BORDE       = "🟫"
CELDA_VACIA = "⬜"
AGUA        = "🌊"
EDIFICIO    = "🏢"
BLOQUEADO   = "⛔"
INICIO      = "🚩"
META        = "🏁"
CAMINO      = "🟢"
VISITADO    = "👣"

# Costos
COSTO = {
    CELDA_VACIA: 1,
    AGUA: 3,
}

class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = self._crear_mapa

    def _crear_mapa(self):
        mapa = []
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                if i == 0 or i == self.filas-1 or j == 0 or j == self.columnas-1:
                    fila.append(BORDE)
                else:
                    fila.append(CELDA_VACIA)
            mapa.append(fila)
        return mapa

        
