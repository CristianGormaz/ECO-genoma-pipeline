"""
Módulo de ingesta SNE-E.C.O.
===========================

Representa la entrada del alimento informacional: recibe datos crudos y los
convierte en paquetes trazables para el metabolismo E.C.O.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .flow import EcoPacket, route_packet


def ingest_text(text: str, source: str = "manual_input", packet_type: str = "text") -> EcoPacket:
    """Crea un paquete E.C.O. desde texto crudo.

    Args:
        text: Contenido bruto a procesar.
        source: Origen del dato.
        packet_type: Tipo declarativo del paquete.

    Returns:
        EcoPacket con registro inicial de ingesta.
    """
    packet = EcoPacket(payload=text, source=source, packet_type=packet_type)
    return route_packet(packet, stage="ingestion", message="Dato crudo ingerido por E.C.O.")


def ingest_file(path: str | Path, packet_type: Optional[str] = None) -> EcoPacket:
    """Crea un paquete E.C.O. leyendo un archivo de texto.

    Este helper se mantiene simple para no reemplazar todavía los parsers
    especializados de BED/FASTA existentes.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"No existe el archivo de entrada: {file_path}")

    inferred_type = packet_type or file_path.suffix.lstrip(".") or "text"
    content = file_path.read_text(encoding="utf-8")
    packet = EcoPacket(payload=content, source=str(file_path), packet_type=inferred_type)
    return route_packet(packet, stage="ingestion", message=f"Archivo ingerido: {file_path}")
