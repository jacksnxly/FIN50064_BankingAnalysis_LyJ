import pandas as pd
import numpy as np

class BankRatioAnalysis:
    def __init__(self, data_path):
        dtypes = {
            'bank_id': str,
            'assets': float,
            'loans': float,
            'deposits': float,
            'us_deposits': float,
            'usdo_deposits': float,
            'capital': float,
            'surplus_fund': float,
            'undivided_profits': float,
            'currency': float,
            'legal_tender': float,
            'checks_and_other': float,
            'bills_sb': float,
            'bills_nb': float,
            'bonds_hand': float,
            'bonds_dep': float,
            'due_from_nb': float,
            'due_from_ra': float,
            'due_from_other_nb': float,
            'due_from_other_nb_and_sb': float,
            'due_from_sb': float,
            'odraft': float,
            'year': int
        }
        self.df = pd.read_csv(data_path, dtype=dtypes, low_memory=False)
        self.ratios = None

    def calculate_consolidated_accounts(self):
        # Calculate total deposits
        self.df['total_deposits'] = (self.df['deposits'].fillna(0) +
                                     self.df['us_deposits'].fillna(0) +
                                     self.df['usdo_deposits'].fillna(0))

        # Calculate total loans
        self.df['total_loans'] = self.df['loans'].fillna(0) + self.df['odraft'].fillna(0)

        # Calculate liquid assets
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

        # Calculate total equity
        self.df['total_equity'] = (self.df['capital'].fillna(0) +
                                   self.df['surplus_fund'].fillna(0) +
                                   self.df['undivided_profits'].fillna(0))

    def calculate_ratios(self, deposit_cutoff=1e-5):
        """
        Calculate the desired ratios. 
        deposit_cutoff: minimum deposit level below which loan-to-deposit ratio is set to NaN
        to avoid extremely large values.
        """
        self.calculate_consolidated_accounts()

        near_zero_deposits = (self.df['total_deposits'] > 0) & (self.df['total_deposits'] < deposit_cutoff)

        self.ratios = pd.DataFrame(index=self.df.index)

        with np.errstate(invalid='ignore', divide='ignore'):
            # Deposit to asset ratio
            self.ratios['deposit_to_asset'] = np.where(
                self.df['assets'] > 0,
                self.df['total_deposits'] / self.df['assets'],
                np.nan
            )

            # Loan to deposit ratio
            self.ratios['loan_to_deposit'] = np.where(
                (self.df['total_deposits'] >= deposit_cutoff),
                self.df['total_loans'] / self.df['total_deposits'],
                np.nan
            )

            # Liquid asset ratio
            self.ratios['liquid_asset_ratio'] = np.where(
                self.df['assets'] > 0,
                self.df['liquid_assets'] / self.df['assets'],
                np.nan
            )

            # Equity to asset ratio
            self.ratios['equity_to_asset'] = np.where(
                self.df['assets'] > 0,
                self.df['total_equity'] / self.df['assets'],
                np.nan
            )

        self.df = self.df.sort_values(['bank_id', 'year'])
        self.ratios['nominal_asset_growth'] = self.df.groupby('bank_id')['assets'].pct_change(fill_method=None)

        self.clean_ratios()

    def clean_ratios(self):
        """Remove extreme values and ensure ratios are within reasonable bounds."""
        self.ratios['deposit_to_asset'] = self.ratios['deposit_to_asset'].clip(0, 1)
        self.ratios['liquid_asset_ratio'] = self.ratios['liquid_asset_ratio'].clip(0, 1)
        self.ratios['equity_to_asset'] = self.ratios['equity_to_asset'].clip(0, 1)

        self.ratios['loan_to_deposit'] = self.ratios['loan_to_deposit'].clip(lower=0, upper=3)

        self.ratios['nominal_asset_growth'] = self.ratios['nominal_asset_growth'].clip(-1, 2)

        self.ratios.replace([np.inf, -np.inf], np.nan, inplace=True)

    def generate_summary_statistics(self):
        """Generate summary statistics for the ratios."""
        if self.ratios is None:
            self.calculate_ratios()

        summary = pd.DataFrame(index=['Mean', 'Median', '10th percentile', '90th percentile'])

        for column in self.ratios.columns:
            stats = self.ratios[column].describe(percentiles=[0.1, 0.5, 0.9])
            summary[column] = [
                stats['mean'],
                stats['50%'],
                stats['10%'],
                stats['90%']
            ]

        return summary.round(4)