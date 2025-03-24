class VerifyAnomalies:
    def __init__(self, config):
        self.anomalies = config.get_config('model','anomalies_path')

        