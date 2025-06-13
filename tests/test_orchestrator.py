"""
Unit tests for the EvolutionOrchestrator class.

These tests cover the initialization of the orchestrator, configuration loading,
and the execution of the main evolution loop with mocked dependencies.
"""
import os
import sys

# Ensure project root and src on path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(ROOT_DIR, 'src')
sys.path.extend([ROOT_DIR, SRC_DIR])

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - fallback for minimal envs
    import yaml_stub as yaml
from unittest.mock import patch, MagicMock
from synergy_vantage_model.orchestrator import EvolutionOrchestrator
from synergy_vantage_model.program_db import ProgramDB  # Added for autospec
from synergy_vantage_model.score_registry import ScoreRegistry  # Added for autospec


@patch('synergy_vantage_model.proposer.openai.OpenAI')
@patch('synergy_vantage_model.evaluator.openai.OpenAI')
def test_orchestrator_init_and_config_load(mock_OpenAI_evaluator, mock_OpenAI, tmp_path):
    """
    Test that the EvolutionOrchestrator initializes correctly and loads
    its configuration from a YAML file.
    """
    dummy_config = {"llm_proposer_breadth": "test_mini_model", "program_db_config": {}}
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(dummy_config, f)

    orchestrator = EvolutionOrchestrator(config_path=str(config_file))
    assert orchestrator.config is not None
    assert orchestrator.config["llm_proposer_breadth"] == "test_mini_model"


@patch('synergy_vantage_model.proposer.openai.OpenAI')
@patch('synergy_vantage_model.evaluator.openai.OpenAI')
@patch('synergy_vantage_model.orchestrator.EvaluatorCascade')
@patch('synergy_vantage_model.orchestrator.ProposerEnsemble')
def test_run_evolution_loop_mocked(mock_ProposerEnsemble, mock_EvaluatorCascade, mock_OpenAI_evaluator, mock_OpenAI_proposer, tmp_path):
    """
    Test the main `run_evolution_loop` with mocked dependencies.

    This test verifies that the orchestrator correctly calls its components
    (Proposer, Evaluator, ProgramDB, ScoreRegistry) the expected number of
    times and with the correct arguments, based on the test configuration.
    It ensures the core loop logic operates as intended without relying on
    the actual (and potentially complex) behavior of the mocked components.
    """
    # 1. Create a minimal valid test_config.yaml for the orchestrator
    test_config = {
        "max_iterations": 2,  # Number of iterations for the loop
        "candidate_generation_N": 5,
        "top_k_selection": 2,
        "llm_proposer_breadth": "test_model",
        "program_db_config": {} 
    }
    config_file = tmp_path / "test_config.yaml"
    with open(config_file, "w") as f:
        yaml.dump(test_config, f)

    # 2. Instantiate EvolutionOrchestrator
    orchestrator = EvolutionOrchestrator(config_path=str(config_file))

    # 3. Configure mock ProposerEnsemble
    mock_proposer_instance = mock_ProposerEnsemble.return_value
    mock_proposer_instance.generate_candidates.return_value = [{"id": i, "code_sketch": f"sketch {i}"} for i in range(test_config["candidate_generation_N"])]

    # 4. Configure mock EvaluatorCascade
    mock_evaluator_instance = mock_EvaluatorCascade.return_value
    mock_evaluator_instance.evaluate.side_effect = lambda c: {**c, "score": c["id"] * 0.1}
    
    # 5. Mock ProgramDB and ScoreRegistry methods directly on the orchestrator's instances.
    #    This allows us to verify interactions with these components without them
    #    performing their actual (potentially complex or stateful) operations.
    #    Using `spec=ProgramDB` and `spec=ScoreRegistry` ensures that the mocks
    #    will only allow calls to actual methods of these classes, preventing typos.
    orchestrator.program_db = MagicMock(spec=ProgramDB)
    orchestrator.score_registry = MagicMock(spec=ScoreRegistry)

    # 6. Execute the main evolution loop
    orchestrator.run_evolution_loop()

    # 7. Assertions to verify interactions and state
    # Check that ProposerEnsemble's generate_candidates was called once per iteration
    assert mock_proposer_instance.generate_candidates.call_count == test_config["max_iterations"]
    # Check that EvaluatorCascade's evaluate was called for each candidate in each iteration
    assert mock_evaluator_instance.evaluate.call_count == test_config["candidate_generation_N"] * test_config["max_iterations"]
    
    # Assertions for ProgramDB interactions
    assert orchestrator.program_db.promote.call_count == test_config["max_iterations"]
    # Verify that 'promote' was called with the correct number of winners (top_k_selection)
    for call_args in orchestrator.program_db.promote.call_args_list:
        args, _ = call_args # call_args is a tuple (args_tuple, kwargs_dict)
        assert len(args[0]) == test_config["top_k_selection"] # args[0] is the 'winners' list

    # Assertions for ScoreRegistry interactions
    assert orchestrator.score_registry.log_scores.call_count == test_config["max_iterations"]
    # Verify that 'log_scores' was called with all evaluated candidates from that iteration
    for call_args in orchestrator.score_registry.log_scores.call_args_list:
        args, _ = call_args
        assert len(args[0]) == test_config["candidate_generation_N"] # args[0] is 'evaluated_candidates'

    # Check that the orchestrator's iteration counter reached the configured maximum
    assert orchestrator.current_iteration == test_config["max_iterations"]
    
    # Note: We are not checking the *content* of `orchestrator.program_db.programs`
    # because we fully mocked the `promote` method. Verifying the content would require
    # either a more nuanced mock (e.g., one that still appends to a list) or not
    # mocking `promote` if its side effects are simple and desired for the test.
    # For this test, checking call counts and arguments to `promote` is deemed sufficient.
