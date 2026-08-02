from pathlib import Path
import json
import nbformat

source_path = Path("/mnt/data/貼り付けられたテキスト（1 点）(8).txt")
output_path = Path("/mnt/data/volcano_plot_english_comments.ipynb")

with source_path.open("r", encoding="utf-8") as f:
    notebook_data = json.load(f)

translations = {
    "# CSVファイルの読み込み":
        "# Read the CSV files",
    "# log2 fold changeのデータ":
        "# Log2 fold-change data",
    "# -log10 FDRのデータ":
        "# -log10 FDR data",
    "# データが同じインデックス順に並んでいると仮定し、2つのデータフレームを連結":
        "# Concatenate the two data frames, assuming that their rows are in the same order",
    "# 必要に応じて 'ID' や 'Gene' などの共通カラムで結合してください":
        "# If needed, merge the data frames using a shared column such as 'ID' or 'Gene'",
    "# 閾値の設定（例としてlog2FC > 1または< -1、log10FDR > 1.3を有意値と仮定）":
        "# Define significance thresholds (example: log2FC > 1 or < -1 and -log10 FDR > 1.3)",
    "# ボルケーノプロットの作成":
        "# Create the volcano plot",
    "# グレーの点（有意ではないデータポイント）":
        "# Plot non-significant data points in grey",
    "# プラス側の有意なデータポイント（オレンジ色、薄い枠あり）":
        "# Plot significantly increased data points in orange with light borders",
    "# マイナス側の有意なデータポイント（水色、薄い枠あり）":
        "# Plot significantly decreased data points in light blue with light borders",
    "# プロットの調整":
        "# Adjust the plot",
    "#軸ラベルに、何と何の比較なのか示す名前":
        "# Indicate the comparison groups in the axis label",
    "# ラベルとタイトル、フォント設定":
        "# Set the axis labels, title, and font properties",
    "# プロットの表示":
        "# Display the plot",
}

for cell in notebook_data.get("cells", []):
    if cell.get("cell_type") != "code":
        continue

    source = cell.get("source", [])
    if isinstance(source, list):
        updated_lines = []
        for line in source:
            updated_line = line
            for japanese, english in translations.items():
                updated_line = updated_line.replace(japanese, english)
            updated_lines.append(updated_line)
        cell["source"] = updated_lines
    else:
        updated_source = source
        for japanese, english in translations.items():
            updated_source = updated_source.replace(japanese, english)
        cell["source"] = updated_source

notebook = nbformat.from_dict(notebook_data)
nbformat.validate(notebook)
nbformat.write(notebook, output_path)

# Confirm that the saved notebook is valid.
validated_notebook = nbformat.read(output_path, as_version=4)
nbformat.validate(validated_notebook)

print(f"Created and validated: {output_path}")
