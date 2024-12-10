# src/utils.py
import pandas as pd
import numpy as np
from scipy import stats
import os

def load_data(filepath):
    """Load raw banking data."""
    return pd.read_csv(filepath)

def clean_data(df):
    """Clean and preprocess banking data."""
    # Remove invalid entries
    essential_columns = ['assets', 'deposits', 'loans', 'odraft', 'capital', 
                        'surplus_fund', 'undivided_profits']
    df = df.dropna(subset=essential_columns)
    df = df[df['assets'] > 0]
    
    # Winsorize to handle outliers
    for col in essential_columns:
        df[col] = stats.mstats.winsorize(df[col], limits=[0.01, 0.01])
    
    return df

def calculate_consolidated_variables(df):
    """Calculate consolidated financial variables."""
    df['total_deposits'] = (df['deposits'].fillna(0) + 
                          df['us_deposits'].fillna(0) + 
                          df['usdo_deposits'].fillna(0))
    
    df['total_loans'] = df['loans'].fillna(0) + df['odraft'].fillna(0)
    
    df['liquid_assets'] = (df['currency'].fillna(0) + 
                          df['legal_tender'].fillna(0) + 
                          df['checks_and_other'].fillna(0) + 
                          df['bills_sb'].fillna(0) + 
                          df['bills_nb'].fillna(0) + 
                          df['bonds_hand'].fillna(0) + 
                          df['bonds_dep'].fillna(0) + 
                          df['due_from_nb'].fillna(0) + 
                          df['due_from_ra'].fillna(0) + 
                          df['due_from_other_nb'].fillna(0) + 
                          df['due_from_other_nb_and_sb'].fillna(0) + 
                          df['due_from_sb'].fillna(0))
    
    df['total_equity'] = (df['capital'].fillna(0) + 
                         df['surplus_fund'].fillna(0) + 
                         df['undivided_profits'].fillna(0))
    
    return df