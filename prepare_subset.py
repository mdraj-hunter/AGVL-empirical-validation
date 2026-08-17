import json
import random

random.seed(42)  # reproducibility matters for a resume/research project

with open('data/qa_data.json', 'r', encoding='utf-8') as f:
    all_examples = [json.loads(line) for line in f]

subset = random.sample(all_examples, 150)

with open('data/subset_150.json', 'w', encoding='utf-8') as f:
    json.dump(subset, f, indent=2)

print(f"Saved {len(subset)} examples to data/subset_150.json")