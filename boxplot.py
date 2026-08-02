import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. Load the data
# ============================================================

# Dataset containing all protein measurements
df = pd.read_csv("SBMAsomascan_all.csv")

# Proteins identified in the volcano plot analysis
df_p = pd.read_csv("volcano42_p.csv")
df_n = pd.read_csv("volcano42_n.csv")

print(list(df_p["proteins"]))
print(list(df_n["proteins"]))


# ============================================================
# 2. Define the target proteins
# ============================================================

target = [
    "GPD1", "PCBD1", "TTN", "CAPN3", "ACYP2", "MYOM2", "GPD1.1",
    "INHBA", "MYOM3", "SLC26A7", "MYL6B", "CFL2", "ENPP2",
    "UBE2S", "MYL3", "HSPB6", "RPL12", "MUSTN1", "PDLIM3", "SHD",
    "KLHL41", "PDLIM5", "ATF5.1", "CACNB3", "APOBEC2", "MYBPH",
    "MYBPC2", "CKM", "CKB|CKM", "CA3", "TNNT2", "TNNI2", "ALDOA",
    "MYBPC1", "ATP5PF", "CSRP3", "ACTN2", "FBP2", "ART3",
    "GDF11|MSTN", "ENPP5", "ART3.1"
]


# ============================================================
# 3. Extract the target proteins
# ============================================================

existing_targets = [
    protein for protein in target
    if protein in df.columns
]

df_target = df[existing_targets].copy()

# Save the extracted dataset if needed
# df_target.to_csv("0328_vol_42.csv", index=False)


# ============================================================
# 4. Load the SBMA and control datasets
# ============================================================

df1 = pd.read_csv("0328_vol_42_sbma.csv")
df2 = pd.read_csv("0328_vol_42_control.csv")


# ============================================================
# 5. Remove unnecessary columns
# ============================================================

columns_to_drop = [
    "Entrez gene symbol",
    "responder/non-responder",
    "group"
]

df1 = df1.drop(
    columns=columns_to_drop,
    errors="ignore"
)

df2 = df2.drop(
    columns=columns_to_drop,
    errors="ignore"
)


# ============================================================
# 6. Convert the datasets to long format
# ============================================================

df1_long = df1.melt(
    var_name="Variable",
    value_name="Value"
)

df1_long["Dataset"] = "SBMA"


df2_long = df2.melt(
    var_name="Variable",
    value_name="Value"
)

df2_long["Dataset"] = "Control"


# Convert the measurement values to numeric format
df1_long["Value"] = pd.to_numeric(
    df1_long["Value"],
    errors="coerce"
)

df2_long["Value"] = pd.to_numeric(
    df2_long["Value"],
    errors="coerce"
)


# Remove rows containing missing measurement values
df1_long = df1_long.dropna(subset=["Value"])
df2_long = df2_long.dropna(subset=["Value"])


# Combine the SBMA and control datasets
combined_df = pd.concat(
    [df1_long, df2_long],
    ignore_index=True
)


# ============================================================
# 7. Generate the box plots
# ============================================================

plt.figure(figsize=(12, 8))

ax = sns.boxplot(
    data=combined_df,
    x="Variable",
    y="Value",
    hue="Dataset",
    palette="Set3",
    showfliers=False  # Hide outlier symbols
)

plt.title("Boxplot of SBMA vs Control for Each Variable")
plt.xlabel("Variables")
plt.ylabel("Values")
plt.xticks(rotation=90)
plt.legend(title="Dataset")
plt.tight_layout()

plt.show()
