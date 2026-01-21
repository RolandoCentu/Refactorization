import os
import heapq
import time

class MapaAEstrella:
    # Emojis como atributos de clase
    BORDE       = "🟫"
    CELDA_VACIA = "⬜"
    AGUA        = "🌊"
    EDIFICIO    = "🏢"
    BLOQUEADO   = "⛔"
    INICIO      = "🚩"
    META        = "🏁"
    CAMINO      = "🟢"
    VISITADO    = "👣"

    # Costos de movimiento
    COSTO = {
        CELDA_VACIA: 1,
        AGUA: 3,
    }

    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.mapa = self.crear_mapa()

        def crear_mapa(self):
        mapa = []
        for i in range(self.filas):
            fila = []
            for j in range(self.columnas):
                if i == 0 or i == self.filas-1 or j == 0 or j == self.columnas-1:
                    fila.append(self.BORDE)
                else:
                    fila.append(self.CELDA_VACIA)
            mapa.append(fila)
        return mapa

    def imprimir_mapa(self):
        os.system("cls" if os.name == "nt" else "clear")
        for fila in self.mapa:
            print("".join(fila)
                  
    def encontrar(self, simbolo):
        for i, fila in enumerate(self.mapa):
            for j, val in enumerate(fila):
                if val == simbolo:
                    return (i,j)
        return None

    def limpiar_camino(self):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[0])):
                if self.mapa[i][j] in (self.CAMINO, self.VISITADO):
                    self.mapa[i][j] = self.CELDA_VACIA

    def es_impasable(self, valor):
        return valor in (self.BORDE, self.EDIFICIO, self.BLOQUEADO)

    def vecinos(self, f, c):
        return [(f-1,c),(f+1,c),(f,c-1),(f,c+1)]

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

    # Algoritmo A*
    def a_estrella(self):
        inicio = self.encontrar(self.INICIO)
        meta   = self.encontrar(self.META)
        if not inicio or not meta:
            return False,"Falta inicio 🚩 o meta 🏁"

        si,sj = inicio
        mi,mj = meta
        if self.es_impasable(self.mapa[si][sj]):
            return False,"Inicio sobre obstáculo"
        if self.es_impasable(self.mapa[mi][mj]):
            return False,"Meta sobre obstáculo"

        abiertos = []
        g_score = {inicio:0}
        f_score = {inicio:self.heuristica(inicio,meta)}
        predecesor = {}
        cerrados = set()
        heapq.heappush(abiertos,(f_score[inicio],0,inicio))

        while abiertos:
            _,g_actual,actual = heapq.heappop(abiertos)
            if actual in cerrados: continue
            cerrados.add(actual)

            af,ac = actual
            if (af,ac) not in (inicio,meta):
                self.mapa[af][ac] = self.VISITADO
            self.imprimir_mapa()
            time.sleep(0.05)

            if actual == meta:
                camino = self.reconstruir_camino(predecesor,inicio,meta)
                self.limpiar_camino()
                for (fi,ci) in camino:
                    if (fi,ci) not in (inicio,meta):
                        self.mapa[fi][ci] = self.CAMINO
                self.imprimir_mapa()
                return True,f"Camino encontrado con {len(camino)-1} pasos"
            
            for nf,nc in self.vecinos(af,ac):
                if not (0<=nf<len(self.mapa) and 0<=nc<len(self.mapa[0])): continue
                celda = self.mapa[nf][nc]
                if self.es_impasable(celda) and (nf,nc)!=meta: continue
                costo = self.COSTO.get(celda,1)
                tentative_g = g_actual + costo
                if tentative_g < g_score.get((nf,nc),float("inf")):
                    predecesor[(nf,nc)] = actual
                    g_score[(nf,nc)] = tentative_g
                    f_total = tentative_g + self.heuristica((nf,nc),meta)
                    f_score[(nf,nc)] = f_total
                    heapq.heappush(abiertos,(f_total,tentative_g,(nf,nc)))
        return False,"No hay camino disponible"

    def meta_final(self, simbolo, fila, columna):
        self.limpiar_camino()
        anterior = self.encontrar(simbolo)
        if anterior:
            ai,aj = anterior
            self.mapa[ai][aj] = self.CELDA_VACIA
        self.mapa[fila][columna] = simbolo

    def desbloquear_zonas(self):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[0])):
                if self.mapa[i][j] == self.BLOQUEADO:
                    self.mapa[i][j] = self.CELDA_VACIA

    #Menú 
    def menu(self):
        while True:
            self.imprimir_mapa()
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

            if opcion=="9": break
            elif opcion=="1": objeto=self.AGUA
            elif opcion=="2": objeto=self.EDIFICIO
            elif opcion=="3": objeto=self.BLOQUEADO
            elif opcion=="4": objeto=self.INICIO
            elif opcion=="5": objeto=self.META
            elif opcion=="6": objeto=self.CELDA_VACIA
            elif opcion=="7":
                ok,msg = self.a_estrella()
                self.imprimir_mapa()
                print(msg)
                input("Enter para volver al menu")
                continue
            elif opcion=="8":
                self.desbloquear_zonas()
                print("Zonas ⛔ desbloqueadas.")
                input("Enter para volver al menu")
                continue
            else:
                continue

            try:
                x=int(input(f"Fila (1 a {self.filas-2}): "))
                y=int(input(f"Columna (1 a {self.columnas-2}): "))
                if 1<=x<=self.filas-2 and 1<=y<=self.columnas-2:
                    if objeto in (self.INICIO,self.META):
                        if self.es_impasable(self.mapa[x][y]):
                            print("No puedes colocar inicio/meta sobre obstáculo")
                            input("Enter para volver al menu")
                            continue
                        self.meta_final(objeto,x,y)
                    else:
                        self.limpiar_camino()
                        self.mapa[x][y]=objeto
            except: 
                pass

#input para las dimensiones de la matriz
if __name__=="__main__":
    filas = int(input("Filas: "))
    columnas = int(input("Columnas: "))
    juego = MapaAEstrella(filas,columnas)
    juego.menu()
