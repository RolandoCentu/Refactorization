import os
from constantes import BORDE, CELDA_VACIA, AGUA, EDIFICIO, BLOQUEADO, INICIO, META, CAMINO, VISITADO, IMPASABLE, COSTO

class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.matriz = self._crear_mapa()
        self.entrada = None
        self.salida = None
        self.obstaculos = set()
        
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

    def imprimir(self):  #mostrar mapa
        os.system("cls" if os.name == "nt" else "clear")
        for fila in self.matriz:
            print("".join(fila))


    def encontrar(self, simbolo): #busca simbolo y devuelve coordenadas
        for i, fila in enumerate(self.matriz):
            for j, val in enumerate(fila):
                if val == simbolo:
                    return (i, j)
        return None

    def limpiar_camino(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.matriz[i][j] in (CAMINO, VISITADO):
                    self.matriz[i][j] = CELDA_VACIA

    def meta_final(self, simbolo, fila, columna): #para recalcular un nuevo camino cambiando inicio y fin y que no se dupliquen
        self.limpiar_camino()
        anterior = self.encontrar(simbolo) #busca inicio y meta
        if anterior:
            ai, aj = anterior
            self.matriz[ai][aj] = CELDA_VACIA #reemplaza para que quede limpio
        self.matriz[fila][columna] = simbolo #nueva pos para ini o meta


    def desbloquear_zonas(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.matriz[i][j] == BLOQUEADO:
                    self.matriz[i][j] = CELDA_VACIA

    # Métodos nuevos

    def agregar_obstaculo(self, fila, columna, tipo=EDIFICIO):
        if self.matriz[fila][columna] in (CELDA_VACIA, CAMINO, VISITADO):
            self.matriz[fila][columna] = tipo
            self.obstaculos.add((fila, columna))


    def quitar_obstaculo(self, fila, columna):
        if (fila, columna) in self.obstaculos:
            self.matriz[fila][columna] = CELDA_VACIA
            self.obstaculos.remove((fila, columna))

    def es_accesible(self, fila, columna):
        celda = self.matriz[fila][columna]
        return celda not in IMPASABLE
    
    def costo_celda(self, fila, columna):
        celda = self.matriz[fila][columna]
    # Si no está en COSTO, se asume costo 1
        return COSTO.get(celda, 1)



