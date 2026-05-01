from src.eco_core import EntericLayer, EntericSystem, build_sne_metrics, describe_enteric_layers


def test_sne_metrics_from_stable_enteric_system():
    system = EntericSystem()
    system.process_dna_sequence("ACGTCCAATGGTATAAA", source="valid_sequence")

    metrics = build_sne_metrics(system.homeostasis_report())

    assert metrics.total_packets == 1
    assert metrics.absorption_ratio == 1.0
    assert metrics.immune_load == 0.0
    assert metrics.quarantine_ratio == 0.0
    assert metrics.homeostasis_state == "stable"
    assert metrics.needs_attention is False


def test_sne_metrics_detect_attention_state():
    system = EntericSystem()
    system.process_dna_sequence("ACGTXYZ", source="bad_one")
    system.process_dna_sequence("TTTXYZ", source="bad_two")

    metrics = build_sne_metrics(system.homeostasis_report())

    assert metrics.total_packets == 2
    assert metrics.immune_load == 1.0
    assert metrics.homeostasis_state == "attention"
    assert metrics.needs_attention is True
    assert any("Alta respuesta inmune" in note for note in metrics.notes)


def test_describe_enteric_layers_returns_expected_architecture_names():
    descriptions = describe_enteric_layers(
        [
            EntericLayer.MUCOSA,
            EntericLayer.MYENTERIC_PLEXUS,
            EntericLayer.GUT_BRAIN_AXIS,
        ]
    )

    assert "barrera_mucosa" in descriptions
    assert "plexo_mienterico_motilidad" in descriptions
    assert "eje_intestino_cerebro" in descriptions
    assert "rechaza" in descriptions["barrera_mucosa"]
    assert "Reporte" in descriptions["eje_intestino_cerebro"]
