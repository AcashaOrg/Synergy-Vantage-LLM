"""
Evolution orchestrator for the Synergy‑Vantage project.

This module defines the EvolutionOrchestrator class, which is the central
component responsible for managing the main "propose -> score -> evolve"
loop of the evolutionary system. It coordinates the interactions between
the ProposerEnsemble, EvaluatorCascade, ProgramDB, and ScoreRegistry.
"""

import yaml
from .proposer import ProposerEnsemble  # Placeholder for future import
from .evaluator import EvaluatorCascade  # Placeholder for future import
from .program_db import ProgramDB
from .score_registry import ScoreRegistry


class EvolutionOrchestrator:
    """
    Manages the evolutionary loop: proposing candidates, evaluating them,
    and evolving the population based on scores.
    """
    def __init__(self, config_path="configs/default.yaml"):
        """
        Initialize the EvolutionOrchestrator.

        This involves loading the main configuration file and setting up
        the core components: Proposer, Evaluator, ProgramDB, and ScoreRegistry.

        Args:
            config_path (str): Path to the YAML configuration file.
        """
        self.config = self._load_config(config_path)
        # Instantiate core components with the loaded configuration
        self.proposer = ProposerEnsemble(self.config)
        self.evaluator = EvaluatorCascade(self.config)
        self.program_db = ProgramDB(self.config.get("program_db_config"))
        self.score_registry = ScoreRegistry()
        self.current_iteration = 0  # Initialize iteration counter
        print(
            f"EvolutionOrchestrator initialized with config: {self.config.get('llm_proposer_breadth')}"
        )

    def _load_config(self, config_path):
        """
        Load YAML configuration from the specified path.

        Args:
            config_path (str): The path to the YAML configuration file.

        Returns:
            dict: The loaded configuration data as a dictionary, or an empty
                  dictionary if loading fails.
        """
        try:
            with open(config_path, "r") as f:
                config_data = yaml.safe_load(f)
            print(f"Configuration loaded successfully from {config_path}")
            return config_data
        except FileNotFoundError:
            print(f"Error: Configuration file {config_path} not found.")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML configuration: {e}")
            return {}

    def run_evolution_loop(self):
        """
        Execute the main "propose -> score -> evolve" process.

        This loop iterates for a configured number of times (max_iterations).
        In each iteration, it:
        1. Samples prompts and mutation strategies.
        2. Generates new candidate solutions using the ProposerEnsemble.
        3. Evaluates these candidates using the EvaluatorCascade.
        4. Selects the top-performing candidates (winners).
        5. Logs scores of all evaluated candidates.
        6. Promotes winners to the ProgramDB.
        7. Checks termination conditions.
        """
        print("Starting Propose -> Score -> Evolve loop...")
        if not self.config: # Basic check for configuration presence
            print("Cannot run evolution loop without a valid configuration.")
            return

        # 1. Seed Program DB (if needed, or load existing)
        print("Step 1: Seeding/Loading Program DB...")
        # self.program_db.seed_or_load() # Placeholder for initial DB seeding

        max_iterations = self.config.get("max_iterations", 10)
        for i in range(max_iterations):
            self.current_iteration = i + 1 # Update current iteration number
            print(f"\nIteration {self.current_iteration}/{max_iterations}")

            # Step 2: Sample prompts and mutation strategies
            print("Step 2: Sampling prompts & hyper-mutations...")
            prompts, mutations = self._sample_prompts_and_mutations()

            # Step 3: Generate candidate solutions
            # The number of candidates to generate is read from config.
            num_candidates_to_generate = self.config.get('candidate_generation_N', 10)
            print(
                f"Step 3: Generating {num_candidates_to_generate} candidates..."
            )
            candidates = self.proposer.generate_candidates(prompts, mutations)

            # Step 4: Evaluate each generated candidate
            print("Step 4: Evaluating candidates...")
            evaluated_candidates = [self.evaluator.evaluate(c) for c in candidates]

            # Step 5: Select top 'k' candidates by fitness and archive others
            # The number of top candidates to select (k) is read from config.
            top_k_selection = self.config.get('top_k_selection', 3)
            print(
                f"Step 5: Selecting top {top_k_selection} candidates..."
            )
            winners, failures = self._select_and_archive(evaluated_candidates)
            # Log scores for all evaluated candidates for audit/analysis
            self.score_registry.log_scores(evaluated_candidates)

            # Step 6: Promote winning candidates to the ProgramDB
            print("Step 6: Promoting winners to Program DB...")
            self.program_db.promote(winners)
            # self._maybe_emit_pr(winners) # Placeholder for optional PR emission

            # Step 7: Check termination conditions for the loop
            print("Step 7: Checking termination conditions...")
            if self._check_termination_conditions():
                print("Termination condition met.")
                break # Exit the loop if conditions are met
        print("Evolution loop finished.")

    def _sample_prompts_and_mutations(self):
        """
        Sample or retrieve initial prompts and mutation strategies.

        NOTE: This is currently a MOCK implementation. In a real system, this
        method might involve complex logic to select diverse and relevant
        prompts and mutation strategies based on the current state of evolution.

        Returns:
            tuple: A tuple containing:
                - prompts (list): A list of prompt strings.
                - mutations (dict): A dictionary of mutation strategies.
        """
        # Mock data for prompts and mutations
        prompts = ["Create a function that adds two numbers", "Write a class for a basic calculator"]
        mutations = ["Slightly modify existing code", "Combine two existing functions"]
        return prompts, mutations

    def _select_and_archive(self, evaluated_candidates):
        """
        Select top-k winning candidates and archive the rest.

        Selection is based on the 'score' attribute of the candidates.
        The number of top candidates to select (k) is determined by the
        'top_k_selection' value in the configuration.

        Args:
            evaluated_candidates (list): A list of candidate dictionaries,
                                         each expected to have a 'score'.

        Returns:
            tuple: A tuple containing:
                - winners (list): A list of the top-k selected candidates.
                - failures (list): A list of the remaining candidates.
        """
        # Sort candidates by score in descending order.
        # Candidates without a score are treated as having a score of 0.
        sorted_candidates = sorted(evaluated_candidates, key=lambda c: c.get("score", 0), reverse=True)
        
        top_k = self.config.get('top_k_selection', 3) # Get k from config
        
        winners = sorted_candidates[:top_k]
        failures = sorted_candidates[top_k:]
        
        print(f"Selected {len(winners)} winners: {winners}")
        print(f"Archived {len(failures)} failures: {failures}")
        return winners, failures

    def _maybe_emit_pr(self, winners):
        """
        Optionally create a pull request for the winning candidates.
        (Placeholder for future implementation)
        """
        # This method would interact with a version control system (e.g., Git)
        # to propose changes based on the 'winners'.
        # For now, it's a no-op.
        pass

    def _check_termination_conditions(self):
        """
        Check if the evolution loop should terminate.

        Currently, termination is based on reaching the maximum number of
        configured iterations. Future implementations might include other
        conditions like convergence (delta-metric below a threshold) or
        resource limits (token budget exhausted).

        Returns:
            bool: True if termination conditions are met, False otherwise.
        """
        # Termination based on current iteration vs max configured iterations
        return self.current_iteration >= self.config.get("max_iterations", 10)


if __name__ == "__main__":
    orchestrator = EvolutionOrchestrator()
    orchestrator.run_evolution_loop()
