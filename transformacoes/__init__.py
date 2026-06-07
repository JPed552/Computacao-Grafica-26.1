"""Pacote de transformacoes geometricas 2D em coordenadas homogeneas."""

from .base import (
    identidade,
    mat_mult,
    aplicar_ponto,
    aplicar_transformacao,
    poligono_regular,
    translacao,
    escala,
    rotacao,
    reflexao,
    cisalhamento,
)

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
