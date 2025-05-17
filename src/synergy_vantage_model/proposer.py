import openai
import os  # For API key
from dotenv import load_dotenv

load_dotenv()


class ProposerEnsemble:
    def __init__(self, config):
        self.config = config
        # Ensure API key is set, e.g., from environment variable
        # openai.api_key = os.getenv("OPENAI_API_KEY")
        # if not openai.api_key:
        #     print("Warning: OPENAI_API_KEY environment variable not set.")

        self.client_mini = openai.OpenAI()  # Assuming default client setup for GPT-4o-Mini
        self.client_pro = openai.OpenAI()   # Assuming default client setup for GPT-4o-Pro

        self.llm_mini_model = self.config.get("llm_proposer_breadth", "gpt-4o-mini")
        self.llm_pro_model = self.config.get("llm_proposer_depth", "gpt-4o-pro")
        print(
            f"ProposerEnsemble initialized with Mini: {self.llm_mini_model}, Pro: {self.llm_pro_model}"
        )

    def generate_candidates(self, base_solutions_or_prompts, mutation_strategies):
        """Generate candidate solutions using a diversity-first strategy."""
        candidates = []
        print(
            f"Generating candidates based on {len(base_solutions_or_prompts)} inputs and {len(mutation_strategies)} strategies."
        )

        # Example: Use Mini for broad generation
        for base_input in base_solutions_or_prompts:
            for strategy in mutation_strategies.get("breadth_strategies", ["simple_variation"]):
                try:
                    print(
                        f"  Using {self.llm_mini_model} for breadth with strategy: {strategy} on input: {str(base_input)[:50]}..."
                    )
                    response_mini = self.client_mini.chat.completions.create(
                        model=self.llm_mini_model,
                        messages=[
                            {
                                "role": "user",
                                "content": f"Generate a variation of {base_input} using strategy {strategy}"
                            }
                        ],
                    )
                    candidates.append(response_mini.choices[0].message.content)
                except Exception as e:
                    print(f"Error calling {self.llm_mini_model}: {e}")

        # Example: Use Pro for depth on a subset of ideas
        promising_ideas = candidates[: self.config.get("pro_refinement_count", 2)]
        for idea in promising_ideas:
            for strategy in mutation_strategies.get("depth_strategies", ["detailed_elaboration"]):
                try:
                    print(
                        f"  Using {self.llm_pro_model} for depth with strategy: {strategy} on idea: {str(idea)[:50]}..."
                    )
                    response_pro = self.client_pro.chat.completions.create(
                        model=self.llm_pro_model,
                        messages=[
                            {
                                "role": "user",
                                "content": f"Refine this idea: {idea} using strategy {strategy}"
                            }
                        ],
                    )
                    candidates.append(response_pro.choices[0].message.content)
                except Exception as e:
                    print(f"Error calling {self.llm_pro_model}: {e}")

        return candidates


if __name__ == "__main__":
    mock_config = {
        "llm_proposer_breadth": "gpt-4o-mini",
        "llm_proposer_depth": "gpt-4o-pro",
        "pro_refinement_count": 1,
    }
    proposer = ProposerEnsemble(config=mock_config)
    sample_prompts = ["def hello():\n  print('world')", "class MyClass:\n  pass"]
    sample_mutations = {
        "breadth_strategies": ["add_docstring", "rename_variable"],
        "depth_strategies": ["optimize_runtime"],
    }
    generated_candidates = proposer.generate_candidates(sample_prompts, sample_mutations)
    print("\nGenerated Candidates:")
    for cand_idx, cand_code in enumerate(generated_candidates):
        print(f"{cand_idx + 1}: {cand_code}")
