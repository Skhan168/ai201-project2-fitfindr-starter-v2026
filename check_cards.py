import glob, re

path = sorted(glob.glob("results/run_*_before.md"))[-1]
text = open(path, encoding="utf-8").read()

sec3 = text.split("### state: selected item reaches suggest_outfit")[1].split("### fit card")[0]
print("Criterion 3 selected_item per try:")
for i, line in enumerate(re.findall(r"- selected_item: (.*)", sec3), 1):
    print(f"  try {i}: {line}")

sec4 = text.split("### fit card: same item five times")[1].split("### empty wardrobe")[0]
cards = re.findall(r"Fit card:\n\n```\n(.*?)\n```", sec4, re.S)
print("\nCriterion 4 fit cards (slip dress, price $30):")
for i, c in enumerate(cards, 1):
    ok = len(c) < 300 and ("$30" in c) and len(c.strip()) > 0
    print(f"  try {i}: {len(c)} chars | has $30: {'$30' in c} | {'PASS' if ok else 'FAIL'}")
    print(f"    {c}")
print("\nAll identical:", len(set(cards)) == 1)