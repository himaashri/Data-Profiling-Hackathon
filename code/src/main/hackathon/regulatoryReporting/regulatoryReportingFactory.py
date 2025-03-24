import sys

from src.main.hackathon.common.utils.configLoader import ConfigLoader
from src.main.hackathon.models.anomalyDetectionModels.modelTraining import ModelTraining
from src.main.hackathon.models.llm import get_gemini_response
from src.main.hackathon.models.validations.anomalyVerification import VerifyAnomalies

class RegulatoryReportingFactory:
    def __init__(self):
        self.config = ConfigLoader('config/config.yml')
        self.prompt = self.config.get_config('data','prompt')
        self.validation_code = self.config.get_config('data','validation_code')
        pass

    def generateReport(self):
        print('Started generating report')
        self.read_prompt_file()
        print('validation code generated')
        modelTrainer = ModelTraining(self.config)
        modelTrainer.process()
        anomalyVerification = VerifyAnomalies(self.config)
        anomalyVerification.verify()
        print('Report generated successfully')

    def read_prompt_file(self):
        try:
            with open(self.prompt, 'r') as file:
                self.prompt_text = file.read()
            generated_code=get_gemini_response(self.prompt_text)
            generated_code = generated_code.splitlines()[1:-1]
            generated_code = "\n".join(generated_code)
            with open(self.validation_code, 'w') as file:
                file.write(generated_code)
                   
        except FileNotFoundError:
            print("prompt.txt file not found")
