
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. Load Human Protein Atlas RNA tissue data
# ============================================================

# Expected columns:
# "Gene name", "Tissue", and either "nTPM" or "TPM"
hpa_file = "rna_tissue_consensus.tsv"

hpa = pd.read_csv(
    hpa_file,
    sep="\t"
)


# ============================================================
# 2. Define the 40 SBMA-associated genes
# ============================================================

gene_order = [
    "CKM",
    "MYL2",
    "ALDOA",
    "TNNI2",
    "MYL3",
    "KLHL41",
    "MYBPC2",
    "PDLIM3",
    "RPL30",
    "HSPB6",
    "ACTN2",
    "CSRP3",
    "ADSS1",
    "PDLIM5",
    "ATP5PF",
    "TTN",
    "CAPN3",
    "CHCHD10",
    "APOBEC2",
    "FBP2",
    "MYL6B",
    "GPD1",
    "MYOM2",
    "MYOM3",
    "ACYP2",
    "HSPA2",
    "ART3",
    "RGMA",
    "PCBD1",
    "CKB",
    "DMD",
    "UBE2S",
    "ENPP5",
    "MSTN",
    "CACNB3",
    "GDF11",
    "INHBA",
    "USP29",
    "SLC26A7",
    "MYBPC3"
]


# ============================================================
# 3. Identify the relevant column names
# ============================================================

if "Gene name" in hpa.columns:
    gene_column = "Gene name"
elif "Gene" in hpa.columns:
    gene_column = "Gene"
else:
    raise ValueError(
        "The dataset must contain either a 'Gene name' or 'Gene' column."
    )

if "Tissue" not in hpa.columns:
    raise ValueError(
        "The dataset must contain a 'Tissue' column."
    )

if "nTPM" in hpa.columns:
    expression_column = "nTPM"
elif "TPM" in hpa.columns:
    expression_column = "TPM"
else:
    raise ValueError(
        "The dataset must contain either an 'nTPM' or 'TPM' column."
    )


# ============================================================
# 4. Extract the selected genes
# ============================================================

selected_data = hpa[
    hpa[gene_column].isin(gene_order)
].copy()

selected_data[expression_column] = pd.to_numeric(
    selected_data[expression_column],
    errors="coerce"
)


# Report genes that were not found in the HPA dataset
detected_genes = set(selected_data[gene_column].dropna())

missing_genes = [
    gene for gene in gene_order
    if gene not in detected_genes
]

if missing_genes:
    print("Genes not found in the dataset:")
    print(missing_genes)


# ============================================================
# 5. Create the gene-by-tissue expression matrix
# ============================================================

expression_matrix = selected_data.pivot_table(
    index=gene_column,
    columns="Tissue",
    values=expression_column,
    aggfunc="mean"
)


# Arrange tissues alphabetically
tissue_order = sorted(expression_matrix.columns)

# Reorder genes and tissues
expression_matrix = expression_matrix.reindex(
    index=gene_order,
    columns=tissue_order
)


# ============================================================
# 6. Apply the log2(TPM + 1) transformation
# ============================================================

log2_expression = np.log2(
    expression_matrix + 1
)


# Save the plotted data if needed
log2_expression.to_csv(
    "HPA_40_genes_log2_TPM.csv"
)


# ============================================================
# 7. Generate the grayscale heatmap
# ============================================================

fig, ax = plt.subplots(
    figsize=(12, 5.5)
)

sns.heatmap(
    log2_expression,
    cmap="Greys",
    vmin=0,
    vmax=15,
    linewidths=0.15,
    linecolor="#dddddd",
    xticklabels=True,
    yticklabels=True,
    cbar_kws={
        "label": "log2(TPM+1)",
        "ticks": [0, 5, 10, 15]
    },
    ax=ax
)


# ============================================================
# 8. Format the figure
# ============================================================

ax.set_title(
    "Human Protein Atlas RNA Expression "
    "(40 genes, log2(TPM+1)) - Grayscale",
    fontsize=12
)

ax.set_xlabel("")
ax.set_ylabel("")

plt.setp(
    ax.get_xticklabels(),
    rotation=60,
    ha="right",
    rotation_mode="anchor",
    fontsize=8
)

plt.setp(
    ax.get_yticklabels(),
    rotation=0,
    fontsize=8
)

ax.tick_params(
    axis="both",
    length=0
)

plt.tight_layout()


# ============================================================
# 9. Save and display the figure
# ============================================================

plt.savefig(
    "HPA_RNA_expression_40_genes_grayscale.png",
    dpi=300,
    bbox_inches="tight"
)

plt.savefig(
    "HPA_RNA_expression_40_genes_grayscale.pdf",
    bbox_inches="tight"
)

plt.show()
