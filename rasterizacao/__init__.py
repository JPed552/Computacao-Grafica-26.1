"""Pacote de algoritmos de rasterizacao."""

from .dda import dda
from .bresenham import bresenham, bresenham_geral

__all__ = ["dda", "bresenham", "bresenham_geral"]