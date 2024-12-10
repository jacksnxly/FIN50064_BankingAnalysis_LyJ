# src/analysis.py
import pandas as pd
import numpy as np
from pathlib import Path

class BankRatioAnalysis:
    """
    A class to analyze historical bank balance sheet ratios.
    
    This class implements methodologies for calculating and analyzing key banking ratios
    from historical OCC balance sheet data, following standard financial accounting practices.
    """
    
    def __init__(self, data_path):
        """Initialize with path to raw banking data."""
        self.df = pd.read_csv(data_path)
        self.ratios = None
        
    def calculate_consolidated_accounts(self):
        """
        Calculate consolidated financial accounts following historical banking standards.
        """
        # Total deposits (including all deposit types)
        self.df['total_deposits'] = (self.df['deposits'].fillna(0) + 
                                   self.df['us_deposits'].fillna(0) + 
                                   self.df['usdo_deposits'].fillna(0))
        
        # Total loans (including overdrafts)
        self.df['total_loans'] = self.df['loans'].fillna(0) + self.df['odraft'].fillna(0)
        
        # Total liquid assets
        self.df['liquid_assets'] = (
            self.df['currency'].fillna(0) +
            self.df['legal_tender'].fillna(0) +
            self.df['checks_and_other'].fillna(0) +
            self.df['bills_sb'].fillna(0) +
            self.df['bills_nb'].fillna(0) +
            self.df['bonds_hand'].fillna(0) +
            self.df['bonds_dep'].fillna(0) +
            self.df['due_from_nb'].fillna(0) +
            self.df['due_from_ra'].fillna(0) +
            self.df['due_from_other_nb'].fillna(0) +
            self.df['due_from_other_nb_and_sb'].fillna(0) +
            self.df['due_from_sb'].fillna(0)
        )
        
        # Total equity
        self.df['total_equity'] = (self.df['capital'].fillna(0) + 
                                 self.df['surplus_fund'].fillna(0) + 
                                 self.df['undivided_profits'].fillna(0))
        
    def calculate_ratios(self):
        """
        Calculate key banking ratios based on consolidated accounts.
        """
        self.calculate_consolidated_accounts()
        
        self.ratios = pd.DataFrame()
        
        # Deposit to asset ratio
        self.ratios['deposit_to_asset'] = self.df['total_deposits'] / self.df['assets']
        
        # Loan to deposit ratio
        self.ratios['loan_to_deposit'] = self.df['total_loans'] / self.df['total_deposits']
        
        # Liquid asset ratio
        self.ratios['liquid_asset_ratio'] = self.df['liquid_assets'] / self.df['assets']
        
        # Equity to asset ratio
        self.ratios['equity_to_asset'] = self.df['total_equity'] / self.df['assets']
        
        # Nominal asset growth rate
        self.ratios['nominal_asset_growth'] = (
            self.df.sort_values('year')
            .groupby('bank_id')['assets']
            .pct_change()
        )
        
    def generate_summary_statistics(self):
        """
        Generate summary statistics for banking ratios.
        
        Returns:
        --------
        pd.DataFrame
            Summary statistics including mean, median, 10th and 90th percentiles
            for all banking ratios.
        """
        if self.ratios is None:
            self.calculate_ratios()
            
        stats_df = pd.DataFrame(
            index=['Mean', 'Median', '10th percentile', '90th percentile']
        )
        
        for column in self.ratios.columns:
            stats = self.ratios[column].describe(percentiles=[0.1, 0.5, 0.9])
            stats_df[column] = [
                stats['mean'],
                stats['50%'],
                stats['10%'],
                stats['90%']
            ]
        
        return stats_df.round(4)