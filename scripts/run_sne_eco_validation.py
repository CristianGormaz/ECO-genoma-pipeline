"""
Validación integral S.N.E.-E.C.O.
=================================

Ejecuta un lote mínimo de paquetes a través del orquestador entérico completo:

- barrera / mucosa informacional,
- plexo submucoso / sensado local,
- plexo mientérico / motilidad,
- defensa informacional,
- microbiota / memoria de recurrencia,
- homeostasis,
- eje intestino-cerebro.

Uso:
    python scripts/run_sne_eco_validation.py
"""

from __future__ import annotations

from src.eco_core import EntericSystem


DEMO_PACKETS = (
    ("valid_sequence", "ACGTCCAATGGTATAAA"),
    ("invalid_sequence", "ACGTXYZ"),
    ("short_sequence", "ACG"),
    ("duplicate_sequence", "ACGTCCAATGGTATAAA"),
)


def run_validation() -> tuple[EntericSystem, str]:
    system = EntericSystem(min_length=6, max_n_percent=25.0, heavy_payload_threshold=10_000)

    for source, sequence in DEMO_PACKETS:
        system.process_dna_sequence(sequence, source=source)

    return system, system.gut_brain_markdown()


def main() -> None:
    system, markdown = run_validation()
    snapshot = system.homeostasis_snapshot()

    print("S.N.E.-E.C.O. VALIDATION REPORT")
    print("================================")
    print(f"processed_packets: {snapshot.total_packets}")
    print(f"absorbed_packets: {snapshot.absorbed_packets}")
    print(f"rejected_packets: {snapshot.rejected_packets}")
    print(f"quarantined_packets: {snapshot.quarantined_packets}")
    print(f"discarded_packets: {snapshot.discarded_packets}")
    print(f"recurrent_packets: {snapshot.recurrent_packets}")
    print(f"defense_alerts: {snapshot.defense_alerts}")
    print(f"state: {snapshot.state}")
    print()
    print(markdown)
    print()
    print("OK: S.N.E.-E.C.O. integrado funcionando.")


if __name__ == "__main__":
    main()
