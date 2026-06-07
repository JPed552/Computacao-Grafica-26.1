"""Pacote de transformacoes geometricas 2D em coordenadas homogeneas."""

from homogeneas    import identidade, mat_mult, aplicar_ponto, aplicar_transformacao, poligono_regular
from .translacao   import translacao
from .escala       import escala
from .rotacao      import rotacao
from .reflexao     import reflexao
from .cisalhamento import cisalhamento

__all__ = [
    "identidade",
    "mat_mult",
    "aplicar_ponto",
    "aplicar_transformacao",
    "poligono_regular",
    "translacao",
    "escala",
    "rotacao",
    "reflexao",
    "cisalhamento",
]
