import pandas as pd
import numpy as np
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    # Define the path to the data file
    data_path = Path('../data/raw/occ-balance-sheets_fall2024.csv')
    df = pd.read_csv(data_path, low_memory=False)
    
    # Calculate Equity
    df['equity'] = df['capital'].fillna(0) + df['surplus_fund'].fillna(0) + df['undivided_profits'].fillna(0)
    
    # Calculate Solvency Proxy
    df['solvency_proxy'] = np.where(df['equity'] > 0, df['undivided_profits'] / df['equity'], np.nan)
    
    # Calculate Funding Vulnerability Proxy
    df['funding_vulnerability'] = np.where(
        df['assets'] > 0,
        (df['bills_payable'].fillna(0) + df['rediscounts'].fillna(0)) / df['assets'],
        np.nan
    )

    # Calculate Quantiles
    solvency_p50 = df['solvency_proxy'].quantile(0.5)
    solvency_p05 = df['solvency_proxy'].quantile(0.05)
    fv_p50 = df['funding_vulnerability'].quantile(0.5)
    fv_p95 = df['funding_vulnerability'].quantile(0.95)

    # Define Categorization Functions
    def categorize_solvency(x):
        if pd.isna(x):
            return np.nan
        if x == 0:
            return np.nan  # Exclude zero observations
        if x > solvency_p50:
            return '>p50'
        elif x > solvency_p05:
            return 'p50-p05'
        else:
            return '<p5'

    def categorize_fv(x):
        if pd.isna(x):
            return np.nan
        if x == 0 or x <= fv_p50:
            return '<p50'
        elif x <= fv_p95:
            return 'p50-p95'
        else:
            return '>p95'

    # Apply Categorization
    df['solvency_cat'] = df['solvency_proxy'].apply(categorize_solvency)
    df['funding_vul_cat'] = df['funding_vulnerability'].apply(categorize_fv)
    
    # Define Categorical Order
    solvency_order = ['>p50', 'p50-p05', '<p5']
    funding_vul_order = ['<p50', 'p50-p95', '>p95']
    
    # Convert to Categorical with Specified Order
    df['solvency_cat'] = pd.Categorical(df['solvency_cat'], categories=solvency_order, ordered=True)
    df['funding_vul_cat'] = pd.Categorical(df['funding_vul_cat'], categories=funding_vul_order, ordered=True)
    
    # Convert 'is_rec' to Numeric
    df['is_rec'] = pd.to_numeric(df['is_rec'], errors='coerce')

    # Group and Calculate Mean Failure Probability
    grouped = df.groupby(['solvency_cat', 'funding_vul_cat'])['is_rec'].mean()
    result_table = grouped.unstack('funding_vul_cat').reindex(index=solvency_order, columns=funding_vul_order)
    
    print("Probability of Failure by Solvency and Funding Vulnerability Categories:")
    print(result_table)
    
    # Generate Heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(result_table, annot=True, fmt=".6f", cmap="YlGnBu", cbar_kws={'label': 'Probability of Failure'})
    plt.title("Probability of Failure by Solvency and Funding Vulnerability Categories")
    plt.xlabel("Funding Vulnerability Proxy")
    plt.ylabel("Solvency Proxy")
    plt.tight_layout()
    
    # Define Output Path
    output_path = Path('../output')
    output_path.mkdir(exist_ok=True)
    
    # Save Heatmap
    heatmap_path = output_path / 'question5_failure_probabilities_heatmap.png'
    plt.savefig(heatmap_path)
    plt.close()
    
    # Save Result Table
    result_table.to_csv(output_path / 'question5_failure_probabilities.csv')

if __name__ == "__main__":
    main()