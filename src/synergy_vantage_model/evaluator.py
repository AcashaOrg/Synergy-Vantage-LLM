import openai
import os
import subprocess
import tempfile


class EvaluatorCascade:
    def __init__(self, config):
        self.config = config
        # openai.api_key = os.getenv("OPENAI_API_KEY")
        self.critic_llm_model = self.config.get("llm_critic", "gpt-4o-pro")
        self.client_critic = openai.OpenAI()
        print(f"EvaluatorCascade initialized with critic: {self.critic_llm_model}")

    def _tier1_heuristics(self, candidate_code_or_text):
        print(f"  Tier 1: Running heuristics on: {str(candidate_code_or_text)[:50]}...")
        score = 1.0
        passed = True
        if "TODO" in candidate_code_or_text or "FIXME" in candidate_code_or_text:
            print("    Tier 1: Found TODO/FIXME, potential issue.")
            score -= 0.1
        if "import os;" in candidate_code_or_text and "os.system" in candidate_code_or_text:
            print("    Tier 1: Potential unsafe os.system call.")
            score -= 0.5
            passed = False
        return {"score_t1": score, "passed_t1": passed, "details_t1": "Heuristics check complete."}

    def _tier2_unit_tests(self, candidate_code):
        print(f"  Tier 2: Running unit tests for code: {str(candidate_code)[:50]}...")
        score = 1.0
        passed = True
        details = "Unit tests (simulated) "
        try:
            if "error" in candidate_code.lower():
                details += "simulated fail (contained 'error')."
                passed = False
                score = 0.0
            else:
                details += "simulated pass."
        except Exception as e:
            print(f"    Tier 2: Error running unit tests: {e}")
            passed = False
            score = 0.0
            details += f"exception: {e}"
        return {"score_t2": score, "passed_t2": passed, "details_t2": details}

    def _tier3_llm_critic(self, candidate_code_or_text):
        print(
            f"  Tier 3: LLM Critic ({self.critic_llm_model}) evaluating: {str(candidate_code_or_text)[:50]}..."
        )
        score = 0.8
        passed = True
        details_t3 = "LLM critic (simulated) found it acceptable."
        try:
            pass
        except Exception as e:
            print(f"    Tier 3: Error calling LLM critic: {e}")
            score = 0.0
            passed = False
            details_t3 = f"LLM critic error: {e}"
        return {"score_t3": score, "passed_t3": passed, "details_t3": details_t3}

    def _tier4_human_review(self, candidate_id, candidate_code_or_text):
        print(
            f"  Tier 4: Flagging candidate {candidate_id} for human review: {str(candidate_code_or_text)[:50]}..."
        )
        return {"requires_human_review": True, "details_t4": "Candidate flagged for human review."}

    def evaluate(self, candidate_id, candidate_payload, require_human_review_flag=False):
        print(f"Evaluating candidate ID: {candidate_id}...")
        evaluation_results = {"candidate_id": candidate_id}
        current_payload = candidate_payload

        t1_results = self._tier1_heuristics(current_payload)
        evaluation_results.update(t1_results)
        if not t1_results["passed_t1"] and self.config.get("stop_eval_on_t1_fail", False):
            print("  Evaluation stopped at Tier 1 failure.")
            return evaluation_results

        if self.config.get("enable_tier2_unit_tests", False):
            if isinstance(current_payload, str):
                t2_results = self._tier2_unit_tests(current_payload)
                evaluation_results.update(t2_results)
                if not t2_results["passed_t2"] and self.config.get("stop_eval_on_t2_fail", False):
                    print("  Evaluation stopped at Tier 2 failure.")
                    return evaluation_results
            else:
                print("  Tier 2: Skipping unit tests, payload is not a string (code).")

        if self.config.get("enable_tier3_llm_critic", True):
            t3_results = self._tier3_llm_critic(current_payload)
            evaluation_results.update(t3_results)
            if not t3_results["passed_t3"] and self.config.get("stop_eval_on_t3_fail", True):
                print("  Evaluation stopped at Tier 3 failure.")
                return evaluation_results

        if require_human_review_flag or self.config.get("default_require_human_review", False):
            t4_results = self._tier4_human_review(candidate_id, current_payload)
            evaluation_results.update(t4_results)

        final_score = (
            evaluation_results.get("score_t1", 0.0) * 0.2
            + evaluation_results.get("score_t2", 0.0) * 0.3
            + evaluation_results.get("score_t3", 0.0) * 0.5
        )
        if not evaluation_results.get("passed_t2", True):
            final_score *= 0.5
        evaluation_results["final_fitness_score"] = round(final_score, 3)

        print(f"Evaluation complete for {candidate_id}. Final Score: {evaluation_results['final_fitness_score']}")
        return evaluation_results


if __name__ == "__main__":
    mock_config = {
        "llm_critic": "gpt-4o-pro",
        "enable_tier2_unit_tests": True,
        "stop_eval_on_t3_fail": False,
    }
    evaluator = EvaluatorCascade(config=mock_config)

    candidate_code_pass = "def sum(a, b):\n  return a + b"
    candidate_code_fail_lint = "import os; os.system('echo unsafe')"
    candidate_code_fail_test = "def buggy_func():\n  return error"

    res1 = evaluator.evaluate("cand_001", candidate_code_pass)
    print(f"Results for cand_001: {res1}\n")

    res2 = evaluator.evaluate("cand_002", candidate_code_fail_lint)
    print(f"Results for cand_002: {res2}\n")

    res3 = evaluator.evaluate("cand_003", candidate_code_fail_test, require_human_review_flag=True)
    print(f"Results for cand_003: {res3}\n")
