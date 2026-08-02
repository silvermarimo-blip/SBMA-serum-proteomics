import pandas as pd
import numpy as np


def log10_transform_csv(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Apply the -log10 transformation to positive numeric values only
    df_transformed = df.applymap(
        lambda x: -np.log10(x)
        if np.issubdtype(type(x), np.number) and x > 0
        else x
    )

    # Save the transformed data to a new CSV file
    df_transformed.to_csv(output_file, index=False)

    print(f"Transformed CSV saved to: {output_file}")


# Example usage
input_file = "q_pvalues_NvsH.csv"  # Path to the input CSV file
output_file = "log10_" + input_file  # Path to the output CSV file

log10_transform_csv(input_file, output_file)
