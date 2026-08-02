
from pathlib import Path
import json
import nbformat

src = Path("/mnt/data/貼り付けられたテキスト（1 点）(7).txt")
dst = Path("/mnt/data/ttest_log2FC_english_comments.ipynb")

with src.open("r", encoding="utf-8") as f:
    notebook_dict = json.load(f)

translations = {
    "#後で使う、物質名リストcを取得":
        "# Obtain the list of protein names (c) for later use",
    "#H,N,R,さらにcontrolとsbmaのデータを、SBMAsomascan_all.csvから抽出する形で取得":
        "# Extract the H, N, R, control, and SBMA datasets from SBMAsomascan_all.csv",
    "#t検定実行~ControlとSBMA":
        "# Perform t-tests: Control vs SBMA",
    "#t検定実行~HとR":
        "# Perform t-tests: H vs R",
    "#t検定実行~RとN":
        "# Perform t-tests: R vs N",
    "#t検定実行~NとH":
        "# Perform t-tests: N vs H",
    "#ファイル出力":
        "# Export the results to a CSV file",
    "#以下からFC導出過程":
        "# Calculate fold changes below",
    "#各群の平均値":
        "# Calculate the mean values for each group",
    "#上記で得られた各群の平均値から不要な列削除":
        "# Remove unnecessary columns from the group means calculated above",
    "#log2FCの導出(ここではcon/sbma。同様にして、直上のセルの値を用いて導出。)":
        "# Calculate log2 fold change (Control/SBMA in this example). Other comparisons can be calculated similarly using the mean values obtained above.",
}

for cell in notebook_dict.get("cells", []):
    if cell.get("cell_type") != "code":
        continue

    source = cell.get("source", [])
    if isinstance(source, list):
        translated_lines = []
        for line in source:
            newline = line
            for jp, en in translations.items():
                newline = newline.replace(jp, en)
            translated_lines.append(newline)
        cell["source"] = translated_lines
    else:
        translated_source = source
        for jp, en in translations.items():
            translated_source = translated_source.replace(jp, en)
        cell["source"] = translated_source

# Convert to and validate a proper Jupyter Notebook.
notebook = nbformat.from_dict(notebook_dict)
nbformat.validate(notebook)
nbformat.write(notebook, dst)

# Read back and validate again.
validated = nbformat.read(dst, as_version=4)
nbformat.validate(validated)

print(f"Created and validated: {dst}")
