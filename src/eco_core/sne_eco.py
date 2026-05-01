"""
S.N.E.-E.C.O. contract layer
===========================

Contratos livianos para expresar el Sistema Nervioso Entérico de E.C.O.
como métricas y capas computacionales estables.

Este módulo no reemplaza `EntericSystem`. Lo complementa: toma el reporte
de homeostasis actual y lo convierte en indicadores explícitos para validar
absorción, carga inmune, cuarentena y estabilidad del flujo.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Tuple

from .enteric_system import EntericHomeostasis


class EntericLayer(str, Enum):
    """Capas entéricas traducidas a arquitectura E.C.O."""

    LUMEN = "lumen_informacional"
    MUCOSA = "barrera_mucosa"
    SUBMUCOSAL_PLEXUS = "plexo_submucoso_sensorial"
    MYENTERIC_PLEXUS = "plexo_mienterico_motilidad"
    MICROBIOTA = "microbiota_informacional"
    IMMUNE_SYSTEM = "sistema_inmune_informacional"
    ABSORPTION = "absorcion"
    HOMEOSTASIS = "homeostasis"
    GUT_BRAIN_AXIS = "eje_intestino_cerebro"


@dataclass(frozen=True)
class SNEEcoMetrics:
    """Indicadores mínimos del estado entérico del pipeline."""

    total_packets: int
    absorption_ratio: float
    immune_load: float
    quarantine_ratio: float
    discard_ratio: float
    duplicate_ratio: float
    homeostasis_state: str
    notes: Tuple[str, ...]

    @property
    def needs_attention(self) -> bool:
        """Indica si el sistema requiere revisión humana o ajuste técnico."""
        return self.homeostasis_state == "attention" or self.immune_load > 0.4 or self.quarantine_ratio > 0.3


def safe_ratio(part: int, total: int) -> float:
    """Calcula proporciones sin romper cuando no hay paquetes procesados."""
    if total <= 0:
        return 0.0
    return round(part / total, 4)


def build_sne_metrics(report: EntericHomeostasis) -> SNEEcoMetrics:
    """Convierte un reporte de homeostasis en métricas S.N.E.-E.C.O."""
    total = report.total_packets
    return SNEEcoMetrics(
        total_packets=total,
        absorption_ratio=safe_ratio(report.absorbed_packets, total),
        immune_load=safe_ratio(report.rejected_packets, total),
        quarantine_ratio=safe_ratio(report.quarantined_packets, total),
        discard_ratio=safe_ratio(report.discarded_packets, total),
        duplicate_ratio=safe_ratio(report.duplicate_packets, total),
        homeostasis_state=report.state,
        notes=tuple(report.notes),
    )


def describe_enteric_layers(layers: Iterable[EntericLayer] | None = None) -> dict[str, str]:
    """Entrega una descripción breve de cada capa entérica computacional."""
    selected_layers = tuple(layers) if layers is not None else tuple(EntericLayer)
    descriptions = {
        EntericLayer.LUMEN: "Entrada cruda del dato antes de ser validado.",
        EntericLayer.MUCOSA: "Barrera selectiva que permite, limita o rechaza entrada.",
        EntericLayer.SUBMUCOSAL_PLEXUS: "Sensado local de calidad, ambigüedad y señales internas.",
        EntericLayer.MYENTERIC_PLEXUS: "Control de movimiento: avanzar, retener, derivar o procesar por lote.",
        EntericLayer.MICROBIOTA: "Memoria y módulos auxiliares que enriquecen o detectan redundancia.",
        EntericLayer.IMMUNE_SYSTEM: "Respuesta defensiva frente a invalidez, ruido o riesgo.",
        EntericLayer.ABSORPTION: "Extracción de nutrientes informacionales convertidos en features.",
        EntericLayer.HOMEOSTASIS: "Lectura del equilibrio general del flujo procesado.",
        EntericLayer.GUT_BRAIN_AXIS: "Reporte trazable hacia usuario, sistema superior o capa interpretativa.",
    }
    return {layer.value: descriptions[layer] for layer in selected_layers}
