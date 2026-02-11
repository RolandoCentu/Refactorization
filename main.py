from mapa import Mapa
from calculadora import CalculadoraAEstrella
from constantes import AGUA, EDIFICIO, BLOQUEADO, INICIO, META, CELDA_VACIA, IMPASABLE

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
        print("4) 🚩 Colocar inicio")
        print("5) 🏁 Colocar meta")
        print("6) Borrar obstáculo")
        print("7) Calcular camino")
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
                if objeto == INICIO:
                    if not mapa.es_accesible(x, y):
                        print("No puedes colocar inicio sobre obstáculo")
                        input("Enter para volver al menú")
                        continue
                    mapa.meta_final(INICIO, x, y)
                elif objeto == META:
                    if not mapa.es_accesible(x, y):
                        print("No puedes colocar meta sobre obstáculo")
                        input("Enter para volver al menú")
                        continue
                    mapa.meta_final(META, x, y)
                elif objeto == CELDA_VACIA:
                    mapa.quitar_obstaculo(x, y)
                else:
                    mapa.agregar_obstaculo(x, y, objeto)
        except ValueError:
            pass

if __name__ == "__main__": #Ejecutá main() solo si este archivo se está ejecutando directamente, no si está siendo importado desde otro archivo
    main()

