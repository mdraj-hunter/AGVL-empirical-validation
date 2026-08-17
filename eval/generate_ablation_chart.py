import matplotlib.pyplot as plt

stages = [
    'Baseline',
    '+ Input\nValidation',
    '+ RAG',
    '+ Chain-of-\nThought',
    '+ Uncertainty\nQuant.',
    '+ Critic\nModel',
    '+ Cross-Model\nConsensus'
]

rates = [62.7, 62.7, 30.7, 35.3, 32.7, 46.7, 32.7]

# Color code: green for improvements, red for regressions, gray for no-op
colors = []
for i in range(len(rates)):
    if i == 0:
        colors.append('#888888')  # baseline, neutral
    elif rates[i] < rates[i-1]:
        colors.append('#4CAF50')  # improvement
    elif rates[i] > rates[i-1]:
        colors.append('#E57373')  # regression
    else:
        colors.append('#888888')  # no-op

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.bar(stages, rates, color=colors, edgecolor='black', linewidth=0.5)

for bar, rate in zip(bars, rates):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{rate}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_ylabel('Hallucination Rate (%)', fontsize=12)
ax.set_title('AGVL Pipeline — Hallucination Rate by Stage\n(150-sample HaluEval QA subset, Llama 3.2 3B + Qwen2.5 3B, local CPU)',
             fontsize=12, fontweight='bold')
ax.set_ylim(0, 70)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig('results/ablation_chart.png', dpi=200, bbox_inches='tight')
print("Saved chart to results/ablation_chart.png")
plt.show()