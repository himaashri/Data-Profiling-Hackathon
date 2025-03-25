import pandas as pd

def process_anomalies_dataset(csv_filepath):
    """
    Processes an anomalies dataset based on predefined validation rules.

    Args:
        csv_filepath (str): The path to the CSV file containing the anomalies dataset.

    Returns:
        pandas.DataFrame: The processed DataFrame with added validation messages.  Returns None if the file is not found.
    """
    try:
        df = pd.read_csv(csv_filepath)
    except FileNotFoundError:
        return None

    validation_rules = {
        "IdentifierType": lambda x: x in ["CUSIP", "ISIN", "SEDOL", "Internal"],
        "AmortizedCost_USDEquivalent": lambda x: isinstance(x, (int, float)) and x == round(x),
        "MarketValue_USDEquivalent": lambda x: isinstance(x, (int, float)) and x == round(x),
        "AccountingIntent": lambda x: x in ["AFS", "HTM", "EQ"],
        "TypeOfHedge": lambda x: x in [1, 2],
        "HedgedRisk": lambda x: x in [1, 2, 3, 4],
        "HedgeInterestRate": lambda x: x in [1, 2, 3, 4, 5],
        "HedgePercentage": lambda x: isinstance(x, (int, float)) and 0 <= x <= 1,
        "HedgeHorizon": lambda x: pd.to_datetime(x, format='%Y-%m-%d', errors='coerce').notna(),
        "HedgedCashFlow": lambda x: x in [1, 2],
        "Sidedness": lambda x: x in [1, 2],
        "HedgingInstrumentAtFairValue": lambda x: isinstance(x, (int, float)) and x == round(x),
        "EffectivePortionOfCumulativeGainsAndLosses": lambda x: isinstance(x, (int, float)) and x == round(x),
        "ASU2017-12HedgeDesignations": lambda x: x in [1, 2, 3],
    }

    df['ValidationMessages'] = ''

    for index, row in df.iterrows():
        for col, rule in validation_rules.items():
            value = row[col]
            if pd.isna(value):
                df.loc[index, 'ValidationMessages'] += f"{col} is missing\n"
            elif not rule(value):
                df.loc[index, 'ValidationMessages'] += f"{col} is {value} which is invalid\n"

    return df
