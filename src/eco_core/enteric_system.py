"""
Compatibilidad para el orquestador entérico E.C.O.

La implementación principal vive en `enteric_orchestrator.py`.
Este archivo conserva los imports históricos:

    from src.eco_core.enteric_system import EntericSystem

sin romper scripts ni pruebas anteriores.
"""

from .enteric_orchestrator import EntericDecision, EntericHomeostasis, EntericSystem

__all__ = ["EntericDecision", "EntericHomeostasis", "EntericSystem"]
