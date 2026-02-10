import heapq
import time
from constantes import OBSTACULOS, COSTO, INICIO, META, CAMINO, VISITADO

class CalculadoraAEstrella:
    def __init__(self, mapa):
        self.mapa = mapa

    def es_impasable(self, valor):
        return valor in OBSTACULOS

    def vecinos(self, f, c):
        return [(f-1, c), (f+1, c), (f, c-1), (f, c+1)]

    def heuristica(self, a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def reconstruir_camino(self, predecesor, inicio, meta):
        nodo = meta
        camino = []
        while nodo != inicio:
            camino.append(nodo)
            nodo = predecesor.get(nodo)
            if nodo is None:
                return []
        camino.append(inicio)
        camino.reverse()
        return camino

    def calcular(self):
        inicio = self.mapa.encontrar(INICIO)
        meta   = self.mapa.encontrar(META)
        if not inicio or not meta:
            return False, "Falta inicio 🚩 o meta 🏁"

        si, sj = inicio
        mi, mj = meta
        if self.es_impasable(self.mapa.matriz[si][sj]):
            return False, "Inicio sobre obstáculo"
        if self.es_impasable(self.mapa.matriz[mi][mj]):
            return False, "Meta sobre obstáculo"

        abiertos = []
        g_score = {inicio: 0}
        f_score = {inicio: self.heuristica(inicio, meta)}
        predecesor = {}
        cerrados = set()
        heapq.heappush(abiertos, (f_score[inicio], 0, inicio))

        while abiertos:
            _, g_actual, actual = heapq.heappop(abiertos)
            if actual in cerrados:
                continue
            cerrados.add(actual)

            af, ac = actual
            if (af, ac) not in (inicio, meta):
                self.mapa.matriz[af][ac] = VISITADO
                self.mapa.imprimir()
                time.sleep(0.05)

            if actual == meta:
                camino = self.reconstruir_camino(predecesor, inicio, meta)
                self.mapa.limpiar_camino()
                for (fi, ci) in camino:
                    if (fi, ci) not in (inicio, meta):
                        self.mapa.matriz[fi][ci] = CAMINO
                self.mapa.imprimir()
                return True, f"Camino encontrado con {len(camino)-1} pasos"

            for nf, nc in self.vecinos(af, ac):
                if not (0 <= nf < self.mapa.filas and 0 <= nc < self.mapa.columnas):
                    continue
                celda = self.mapa.matriz[nf][nc]
                if self.es_impasable(celda) and (nf, nc) != meta:
                    continue

                costo = self.mapa.costo_celda(nf, nc)
                tentative_g = g_actual + costo

                if tentative_g < g_score.get((nf, nc), float("inf")):
                    predecesor[(nf, nc)] = actual
                    g_score[(nf, nc)] = tentative_g
                    f_total = tentative_g + self.heuristica((nf, nc), meta)
                    f_score[(nf, nc)] = f_total
                    heapq.heappush(abiertos, (f_total, tentative_g, (nf, nc)))

        return False, "No hay camino disponible"
