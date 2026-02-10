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

    def imprimir(self):
        os.system("cls" if os.name == "nt" else "clear")
        for fila in self.matriz:
            print("".join(fila))
            
    

    def encontrar(self, simbolo):
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

    def meta_final(self, simbolo, fila, columna):
        self.limpiar_camino()
        anterior = self.encontrar(simbolo)
        if anterior:
            ai, aj = anterior
            self.matriz[ai][aj] = CELDA_VACIA
        self.matriz[fila][columna] = simbolo

    def desbloquear_zonas(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.matriz[i][j] == BLOQUEADO:
                    self.matriz[i][j] = CELDA_VACIA


class CalculadoraAEstrella:
    def __init__(self, mapa: Mapa):
        self.mapa = mapa

    def es_impasable(self, valor):
        return valor in (BORDE, EDIFICIO, BLOQUEADO)

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
                costo = COSTO.get(celda, 1)
                tentative_g = g_actual + costo

                if tentative_g < g_score.get((nf, nc), float("inf")):
                    predecesor[(nf, nc)] = actual
                    g_score[(nf, nc)] = tentative_g
                    f_total = tentative_g + self.heuristica((nf, nc), meta)
                    f_score[(nf, nc)] = f_total
                    heapq.heappush(abiertos, (f_total, tentative_g, (nf, nc)))

        return False, "No hay camino disponible"


def main():
    filas = int(input("Filas: "))
    columnas = int(input("Columnas: "))
    mapa = Mapa(filas, columnas)
    calculadora = CalculadoraAEstrella(mapa)

    while True:
        mapa.imprimir()
        print("\nOpciones:")
        print("1) 🌊 Agua")
        print("2) 🏢 Edificio")
        print("3) ⛔ Zona bloqueada temporal")
        print("4) 🚩 Inicio")
        print("5) 🏁 Meta")
        print("6) Borrar")
        print("7) Calcular Camino")
        print("8) Desbloquear zonas ⛔")
        print("9) Salir")
        opcion = input("Elige: ").strip()

        if opcion == "9":
            break
        elif opcion == "1": objeto = AGUA
        elif opcion == "2": objeto = EDIFICIO
        elif opcion == "3": objeto = BLOQUEADO
        elif opcion == "4": objeto = INICIO
        elif opcion == "5": objeto = META
        elif opcion == "6": objeto = CELDA_VACIA
        elif opcion == "7":
            ok, msg = calculadora.calcular()
            mapa.imprimir()
            print(msg)
            input("Enter para volver al menú")
            continue
        elif opcion == "8":
            mapa.desbloquear_zonas()
            print("Zonas ⛔ desbloqueadas.")
            input("Enter para volver al menú")
            continue
        else:
            continue

        try:
            x = int(input(f"Fila (1 a {filas-2}): "))
            y = int(input(f"Columna (1 a {columnas-2}): "))
            if 1 <= x <= filas-2 and 1 <= y <= columnas-2:
                if objeto in (INICIO, META):
                    if calculadora.es_impasable(mapa.matriz[x][y]):
                        print("No puedes colocar inicio/meta sobre obstáculo")
                        input("Enter para volver al menú")
                        continue
                    mapa.meta_final(objeto, x, y)
                else:
                    mapa.limpiar_camino()
                    mapa.matriz[x][y] = objeto
        except:
            pass

if __name__ == "__main__":
    main()
