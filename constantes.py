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

# Conjunto de obstáculos impasables
IMPASABLE = {BORDE, EDIFICIO, BLOQUEADO}

# Diccionario de costos de paso (solo para celdas transitables)
COSTO = {
    CELDA_VACIA: 1,
    AGUA: 3,
}

