import pandas as pd

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

    validation_messages = []
    for index, row in df.iterrows():
        row_messages = []
        for col, rule in validation_rules.items():
            value = row[col]
            if pd.isna(value):
                row_messages.append(f"{col} is missing")
            elif not rule(value):
                if col == "HedgeHorizon":
                    row_messages.append(f"{col} is not in yyyy-mm-dd format")
                elif col in ["AmortizedCost_USDEquivalent", "MarketValue_USDEquivalent", "HedgingInstrumentAtFairValue", "EffectivePortionOfCumulativeGainsAndLosses"]:
                    row_messages.append(f"{col} is not a rounded whole dollar amount")

                else:
                    row_messages.append(f"{col} is {value} which is not in {list(set(df[col].dropna()))}")

        validation_messages.append("; ".join(row_messages))

    df['ValidationMessages'] = validation_messages
    return df