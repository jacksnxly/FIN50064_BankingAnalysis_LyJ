# Banking Balance Sheet Analysis

FIN50064 Money & Banking
Author: Jackson Ly

## Project Overview

Analysis of historical and modern bank balance sheet structures, comparing financial ratios across different time periods and with Deutsche Bank's current position.

## Repository Structure

project_root/
├─ data/
│ ├─ raw/
│ │ ├─ occ-balance-sheets_fall2024.csv
│ │ └─ Annual-Financial-Statements-of-Deutsche-Bank-AG-2023.pdf
│ └─ processed/ # Processed data files (if any)
├─ notebooks/
│ ├─ bank_ratio_analysis.ipynb # Main analysis notebook for Questions 1-4
│ └─ question5_analysis.ipynb # Analysis notebook for Question 5
├─ output/
│ ├─ summary_statistics.csv # Output of summary stats from main analysis
│ ├─ ratio_distributions.png # Distribution plot of ratios
│ └─ question5_failure_probabilities.csv # Probability of failure by category (Q5)
├─ src/
│ ├─ **init**.py
│ ├─ question2_analysis.py # Core analysis code (calculating ratios, etc.)
│ ├─ utils.py # Utility functions (data loading, cleaning)
│ └─ question5_analysis.py # Standalone script for Question 5 analysis
├─ requirements.txt
└─ README.md

## Setup and Installation

1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Run analysis:
   Ensure you have Python 3.8+ installed. From the project root directory:
   python3 -m venv .venv
   source .venv/bin/activate # On Windows: .venv\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   Running Main Analysis
   jupyter lab
   Open and run notebooks/bank_ratio_analysis.ipynb
   Open and run notebooks/question5_analysis.ipynb

## Data Sources

- Annual-Financial-Statements-of-Deutsche-Bank-AG-2023.pdf
- occ-balance-sheets_fall2024.csv
