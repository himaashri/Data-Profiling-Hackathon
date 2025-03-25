import pandas as pd
from datetime import datetime

def process_anomalies_dataset(csv_filepath):
    """
    Processes an anomalies dataset, applying validation rules and adding validation messages.

    Args:
        csv_filepath (str): The path to the CSV file containing the anomalies dataset.

    Returns:
        pandas.DataFrame: The processed DataFrame with added validation messages.  Returns None if there's an error reading the file.
    """

    try:
        df = pd.read_csv(csv_filepath)
    except FileNotFoundError:
        return None

    df['ValidationMessages'] = ''

    for index, row in df.iterrows():
        messages = []

        # IdentifierType validation
        if row['IdentifierType'] not in ["CUSIP", "ISIN", "SEDOL", "Internal"]:
            messages.append(f"IdentifierType '{row['IdentifierType']}' is invalid.")

        # AmortizedCost_USDEquivalent validation
        try:
            amortized_cost = int(row['AmortizedCost_USDEquivalent'])
            if amortized_cost != round(amortized_cost):
                messages.append("AmortizedCost_USDEquivalent is not a whole number.")
        except (ValueError, TypeError):
            messages.append("AmortizedCost_USDEquivalent is missing or invalid.")

        # MarketValue_USDEquivalent validation
        try:
            market_value = int(row['MarketValue_USDEquivalent'])
            if market_value != round(market_value):
                messages.append("MarketValue_USDEquivalent is not a whole number.")
        except (ValueError, TypeError):
            messages.append("MarketValue_USDEquivalent is missing or invalid.")


        # AccountingIntent validation
        if row['AccountingIntent'] not in ["AFS", "HTM", "EQ"]:
            messages.append(f"AccountingIntent '{row['AccountingIntent']}' is invalid.")

        # TypeOfHedge validation
        try:
            type_of_hedge = int(row['TypeOfHedge'])
            if type_of_hedge not in [1, 2]:
                messages.append(f"TypeOfHedge '{row['TypeOfHedge']}' is invalid.")
        except (ValueError, TypeError):
            messages.append("TypeOfHedge is missing or invalid.")

        # HedgedRisk validation
        try:
            hedged_risk = int(row['HedgedRisk'])
            if hedged_risk not in [1, 2, 3, 4]:
                messages.append(f"HedgedRisk '{row['HedgedRisk']}' is invalid.")
        except (ValueError, TypeError):
            messages.append("HedgedRisk is missing or invalid.")

        # HedgeInterestRate validation
        try:
            hedge_interest_rate = int(row['HedgeInterestRate'])
            if hedge_interest_rate not in [1, 2, 3, 4, 5]:
                messages.append(f"HedgeInterestRate '{row['HedgeInterestRate']}' is invalid.")
        except (ValueError, TypeError):
            messages.append("HedgeInterestRate is missing or invalid.")

        # HedgePercentage validation
        try:
            hedge_percentage = float(row['HedgePercentage'])
            if hedge_percentage > 1 or hedge_percentage < 0:
                messages.append(f"HedgePercentage '{row['HedgePercentage']}' is out of range (0-1).")

        except (ValueError, TypeError):
            messages.append("HedgePercentage is missing or invalid.")

        # HedgeHorizon validation
        try:
            datetime.strptime(row['HedgeHorizon'], '%Y-%m-%d')
        except (ValueError, TypeError):
            messages.append("HedgeHorizon is missing or has an invalid date format (yyyy-mm-dd).")

        # HedgedCashFlow validation
        try:
            hedged_cash_flow = int(row['HedgedCashFlow'])
            if hedged_cash_flow not in [1,2]:
              messages.append(f"HedgedCashFlow '{row['HedgedCashFlow']}' is invalid.")
        except (ValueError, TypeError):
            messages.append("HedgedCashFlow is missing or invalid.")


        # Sidedness validation
        try:
            sidedness = int(row['Sidedness'])
            if sidedness not in [1, 2]:
                messages.append(f"Sidedness '{row['Sidedness']}' is invalid.")
        except (ValueError, TypeError):
            messages.append("Sidedness is missing or invalid.")

        # HedgingInstrumentAtFairValue validation
        try:
            hedging_instrument = int(row['HedgingInstrumentAtFairValue'])
            if hedging_instrument != round(hedging_instrument):
                messages.append("HedgingInstrumentAtFairValue is not a whole number.")
        except (ValueError, TypeError):
            messages.append("HedgingInstrumentAtFairValue is missing or invalid.")


        # EffectivePortionOfCumulativeGainsAndLosses validation
        try:
            effective_portion = int(row['EffectivePortionOfCumulativeGainsAndLosses'])
            if effective_portion != round(effective_portion):
                messages.append("EffectivePortionOfCumulativeGainsAndLosses is not a whole number.")
        except (ValueError, TypeError):
            messages.append("EffectivePortionOfCumulativeGainsAndLosses is missing or invalid.")

        # ASU2017-12HedgeDesignations validation
        try:
            asu_designation = int(row['ASU2017-12HedgeDesignations'])
            if asu_designation not in [1, 2, 3]:
                messages.append(f"ASU2017-12HedgeDesignations '{row['ASU2017-12HedgeDesignations']}' is invalid.")
        except (ValueError, TypeError):
            messages.append("ASU2017-12HedgeDesignations is missing or invalid.")

        df.loc[index, 'ValidationMessages'] = '; '.join(messages) if messages else 'No validation errors.'

    return df