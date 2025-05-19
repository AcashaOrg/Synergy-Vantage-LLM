import yaml
from synergy_vantage_model.orchestrator import EvolutionOrchestrator


def test_orchestrator_init_and_config_load(tmp_path):
    dummy_config = {"llm_proposer_breadth": "test_mini_model"}
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(dummy_config, f)

    orchestrator = EvolutionOrchestrator(config_path=str(config_file))
    assert orchestrator.config is not None
    assert orchestrator.config["llm_proposer_breadth"] == "test_mini_model"
