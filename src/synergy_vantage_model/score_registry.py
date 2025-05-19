import json
import datetime


class ScoreRegistry:
    """Placeholder for storing evaluation scores and ESI metrics."""

    def __init__(self, audit_log_file="logs/audit_scores.jsonl"):
        self.audit_log_file = audit_log_file
        print(f"ScoreRegistry initialized. Logging scores to: {self.audit_log_file}")

    def log_scores(self, evaluated_candidates):
        """Log evaluation results for a list of candidates."""
        timestamp = datetime.datetime.now().isoformat()
        log_entries = []
        for candidate_eval in evaluated_candidates:
            entry = {
                "timestamp": timestamp,
                "candidate_id": candidate_eval.get("candidate_id", "N/A"),
                "final_fitness_score": candidate_eval.get("final_fitness_score"),
                "tier1_score": candidate_eval.get("score_t1"),
                "tier1_passed": candidate_eval.get("passed_t1"),
                "tier2_score": candidate_eval.get("score_t2"),
                "tier2_passed": candidate_eval.get("passed_t2"),
                "tier3_score": candidate_eval.get("score_t3"),
                "tier3_passed": candidate_eval.get("passed_t3"),
                "requires_human_review": candidate_eval.get("requires_human_review", False),
            }
            log_entries.append(entry)

        print(f"Logging scores for {len(evaluated_candidates)} candidates.")
        try:
            with open(self.audit_log_file, "a") as f:
                for log_entry in log_entries:
                    f.write(json.dumps(log_entry) + "\n")
            print(f"Successfully logged scores to {self.audit_log_file}")
        except Exception as e:
            print(f"Error logging scores to {self.audit_log_file}: {e}")


if __name__ == "__main__":
    registry = ScoreRegistry()
    example_evals = [
        {"candidate_id": "cand_A", "final_fitness_score": 0.85, "score_t1": 0.9, "passed_t1": True, "score_t3": 0.8, "passed_t3": True},
        {"candidate_id": "cand_B", "final_fitness_score": 0.4, "score_t1": 0.5, "passed_t1": False, "score_t3": 0.0, "passed_t3": False},
    ]
    registry.log_scores(example_evals)
