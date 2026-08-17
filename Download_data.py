import json
import urllib.request
import os

os.makedirs('data', exist_ok=True)

url = 'https://raw.githubusercontent.com/RUCAIBox/HaluEval/main/data/qa_data.json'
dest = 'data/qa_data.json'

urllib.request.urlretrieve(url, dest)
print(f"Downloaded to {dest}")

# Peek at structure
with open(dest, 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f"Total examples: {len(lines)}")
print("First example:", lines[0])