"""
E.C.O. Core
===========

Capa base para convertir el marco conceptual SNE-E.C.O. en módulos técnicos.

Esta carpeta representa la arquitectura entérica del proyecto:

- ingestion: entrada de datos crudos.
- filtering: validación y limpieza inicial.
- flow: trazabilidad y movimiento por etapas.
- absorption: extracción de señales útiles.
- feedback: métricas y aprendizaje del proceso.
- discard: descarte controlado de datos no aprovechables.
- enteric_system: orquestación integrada con sensado, reflejo local,
  motilidad, cuarentena, absorción y homeostasis.
- sne_eco: contratos y métricas explícitas del Sistema Nervioso Entérico E.C.O.

La intención es que esta capa crezca gradualmente sin romper los scripts
funcionales actuales del repositorio.
"""

from .flow import EcoPacket, EcoStageLog, route_packet
from .ingestion import ingest_text
from .filtering import validate_dna_sequence, validate_packet_payload
from .absorption import absorb_sequence_features
from .feedback import EcoFeedback, build_feedback_summary
from .discard import EcoDiscardRecord, discard_packet
from .enteric_system import EntericDecision, EntericHomeostasis, EntericSystem
from .sne_eco import EntericLayer, SNEEcoMetrics, build_sne_metrics, describe_enteric_layers

__all__ = [
    "EcoPacket",
    "EcoStageLog",
    "route_packet",
    "ingest_text",
    "validate_dna_sequence",
    "validate_packet_payload",
    "absorb_sequence_features",
    "EcoFeedback",
    "build_feedback_summary",
    "EcoDiscardRecord",
    "discard_packet",
    "EntericDecision",
    "EntericHomeostasis",
    "EntericSystem",
    "EntericLayer",
    "SNEEcoMetrics",
    "build_sne_metrics",
    "describe_enteric_layers",
]
