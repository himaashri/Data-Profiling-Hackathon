from src.main.hackathon.models.validations.validations import process_anomalies_dataset


class VerifyAnomalies:
    def __init__(self, config):
        self.anomalies = config.get_config('model','anomalies_path')
        self.final_anomalies = config.get_config('model','final_anomalies_path')

    def verify(self):
        df = process_anomalies_dataset(self.anomalies)
        df.to_csv(self.final_anomalies, index=False)
        print('Anomalies verified and saved to', self.final_anomalies)
        