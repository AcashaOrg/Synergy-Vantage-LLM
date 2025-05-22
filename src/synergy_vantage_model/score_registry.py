"""
Score Registry for the Synergy‑Vantage project.

This module defines the ScoreRegistry class, responsible for logging and
storing the evaluation scores of candidate solutions.
"""
import datetime

class ScoreRegistry:
    """
    A simple in-memory registry for storing evaluation scores.

    This class acts as a placeholder for a more robust score logging and
    auditing system. Currently, it stores scores in a list in memory and
    does not persist them.
    """

    def __init__(self):
        """
        Initialize the ScoreRegistry.

        Sets up an in-memory list to store score entries.
        """
        self.scores = []  # In-memory list to store score data
        print("ScoreRegistry initialized.")

    def log_scores(self, evaluated_candidates):
        """
        Log evaluation results for a list of candidates.

        NOTE: This is a MOCK implementation. It appends score information for
        each candidate to an in-memory list. Each entry includes the candidate's
        ID, their score, and a timestamp.

        Args:
            evaluated_candidates (list): A list of candidate dictionaries.
                Each dictionary is expected to have an "id" (or defaults to "N/A")
                and a "score" (or defaults to 0.0).
        """
        print(f"ScoreRegistry: Logging scores for {len(evaluated_candidates)} candidates.")
        for candidate in evaluated_candidates:
            # Extract candidate ID, defaulting if not present
            candidate_id = candidate.get("id", "N/A")
            # Extract score, defaulting if not present
            score = candidate.get("score", 0.0)
            # Append score entry with a timestamp
            self.scores.append({
                "id": candidate_id,
                "score": score,
                "timestamp": datetime.datetime.now().isoformat()
            })
        print(f"ScoreRegistry state (in-memory): {self.scores}")


if __name__ == "__main__":
    # Example usage of the mock ScoreRegistry
    registry = ScoreRegistry()
    example_evals = [
        {"id": "cand_A", "score": 0.85},
        {"id": "cand_B", "score": 0.4},
    ]
    registry.log_scores(example_evals)
    example_evals_no_id = [
        {"score": 0.99},
    ]
    registry.log_scores(example_evals_no_id)
