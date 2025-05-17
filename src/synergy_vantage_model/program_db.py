class ProgramDB:
    """Simple in-memory program database placeholder."""

    def __init__(self, db_config=None):
        self.db_config = db_config
        self.solutions = []
        print(f"ProgramDB initialized. Config: {db_config}")

    def seed_or_load(self, baseline_implementations=None):
        if baseline_implementations:
            for item in baseline_implementations:
                self.solutions.append(item)
            print(f"ProgramDB seeded with {len(baseline_implementations)} baseline implementations.")
        else:
            print("ProgramDB loaded (placeholder - no persistent store yet).")

    def promote(self, winning_candidates):
        for candidate in winning_candidates:
            self.solutions.append(candidate)
            self.solutions.sort(key=lambda x: x.get('score', 0), reverse=True)
        print(f"Promoted {len(winning_candidates)} candidates to ProgramDB.")

    def get_best_solutions(self, k=1):
        print(f"Retrieving top {k} solutions from ProgramDB...")
        return self.solutions[:k]

    def archive_failure(self, candidate_info, reason):
        print(f"Archiving failure for candidate: {candidate_info.get('id', 'N/A')}. Reason: {reason}")


if __name__ == "__main__":
    db = ProgramDB({"path": "data/program_db.jsonl"})
    db.seed_or_load([
        {"id": "baseline_001", "code": "def hello(): print('baseline')", "score": 0.5, "generation": 0}
    ])
    winners_example = [
        {"id": "cand_005", "code": "def hello_optimized(): print('optimized world')", "score": 0.9, "generation": 1},
        {"id": "cand_008", "code": "def hello_v2(): print('hello again')", "score": 0.7, "generation": 1},
    ]
    db.promote(winners_example)
    print("Best solutions:", db.get_best_solutions(k=2))
    db.archive_failure({"id": "cand_001", "code": "..."}, "failed unit tests")
