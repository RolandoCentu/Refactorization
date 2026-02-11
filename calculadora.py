import heapq
import time
from constantes import COSTO, INICIO, META, CAMINO, VISITADO, IMPASABLE

class CalculadoraAEstrella:
    def __init__(self, mapa):
        self.mapa = mapa  # instancia de Mapa

    def es_impasable(self, valor): #devuelve true si la celda es obstaculo
        return valor in IMPASABLE

    def vecinos(self, f, c): #coordenadas arriba,abajo,izquierda, derecha
        return [(f-1, c), (f+1, c), (f, c-1), (f, c+1)]

    def heuristica(self, a, b):
        # Distancia Manhattan
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

        # f(n) = g(n) + h(n)
        abiertos = []  # lista de nodos abiertos a explorar
        g_score = {inicio: 0}  # costo real acumulado desde inicio
        f_score = {inicio: self.heuristica(inicio, meta)} # f es la suma de ambos valores
        predecesor = {} #diccionario para guardar predecesor
        cerrados = set() #conjunto para nodos explorados
        heapq.heappush(abiertos, (f_score[inicio], 0, inicio)) #para anadir un elemnto a la lista

        while abiertos:
            _, g_actual, actual = heapq.heappop(abiertos) #se extrae el nodo con menor fscore
            if actual in cerrados:
                continue
            cerrados.add(actual)

            af, ac = actual # Mostrar exploración paso a paso
            if (af, ac) not in (inicio, meta):
                self.mapa.matriz[af][ac] = VISITADO
                self.mapa.imprimir()
                time.sleep(0.05)

            if actual == meta: # si nodo es la meta se reconstruye el camino con predecesores
                camino = self.reconstruir_camino(predecesor, inicio, meta)
                self.mapa.limpiar_camino()
                for (fi, ci) in camino:
                    if (fi, ci) not in (inicio, meta):
                        self.mapa.matriz[fi][ci] = CAMINO
                self.mapa.imprimir()
                return True, f"Camino encontrado con {len(camino)-1} pasos"

            for nf, nc in self.vecinos(af, ac): # si no es la meta, se exploran los vecinos
                if not (0 <= nf < self.mapa.filas and 0 <= nc < self.mapa.columnas): #validar que este dentro del mapa
                    continue
                celda = self.mapa.matriz[nf][nc] 
                if self.es_impasable(celda) and (nf, nc) != meta: # si la celda es un impasable no se puede pasar 
                    continue

                costo = self.mapa.costo_celda(nf, nc) #calcular costos
                tentative_g = g_actual + costo #costo acumulado desde el inicio hasta ese vecino

                if tentative_g < g_score.get((nf, nc), float("inf")): # se compara, si el nuevo costo es menor, entonces se actualizan
                    predecesor[(nf, nc)] = actual
                    g_score[(nf, nc)] = tentative_g #se actualiza valores de g y f
                    f_total = tentative_g + self.heuristica((nf, nc), meta) #combina costo real y heuristica
                    f_score[(nf, nc)] = f_total
                    heapq.heappush(abiertos, (f_total, tentative_g, (nf, nc))) # se anhade a abierto

        return False, "No hay camino disponible"

