import pandas as pd
from datetime import datetime, timedelta

def process_anomalies_dataset(csv_filepath):
    df = pd.read_csv(csv_filepath)
    df['ValidationMessages'] = ''
    for index, row in df.iterrows():
        messages = []
        if abs(row['AmortizedCost_USDEquivalent'] - row['MarketValue_USDEquivalent']) / max(row['AmortizedCost_USDEquivalent'], row['MarketValue_USDEquivalent']) > 0.2:
            messages.append('AmortizedCost_USDEquivalent and MarketValue_USDEquivalent deviate by more than 20%')
        if row['AccountingIntent'] not in ['HTM', 'AFS', 'EQ']:
            messages.append('Invalid AccountingIntent')
        if row['TypeOfHedge'] not in [1, 2, 3]:
            messages.append('Invalid TypeOfHedge')
        if not 0 <= row['HedgePercentage'] <= 1:
            messages.append('HedgePercentage out of range')
        if not 0 <= row['HedgeInterestRate'] <= 1:
            messages.append('HedgeInterestRate out of range')
        try:
            hedge_horizon = datetime.strptime(row['HedgeHorizon'], '%Y-%m-%d')
            if hedge_horizon < datetime.now():
                messages.append('HedgeHorizon is in the past')
            if hedge_horizon < datetime.now() - timedelta(days=3652):
                messages.append('HedgeHorizon older than 10 years')

        except ValueError:
            messages.append('Invalid HedgeHorizon format')

        if row['HedgingInstrumentAtFairValue'] <= 0:
            messages.append('HedgingInstrumentAtFairValue is not positive')
        if row['EffectivePortionOfCumulativeGainsAndLosses'] > 0.5 * row['HedgingInstrumentAtFairValue']:
            messages.append('EffectivePortionOfCumulativeGainsAndLosses exceeds 50% of HedgingInstrumentAtFairValue')
        if row['Sidedness'] not in [1, 2]:
            messages.append('Invalid Sidedness')
        
        df.loc[index, 'ValidationMessages'] = '; '.join(messages)
    return df
