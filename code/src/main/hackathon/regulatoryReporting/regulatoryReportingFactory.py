import sys

class RegulatoryReportingFactory:
    def __init__(self):
        pass

    def generateReport(self):
        print('Started generating report')

    def read_prompt_file(self):
        try:
            with open('code/src/main/hackathon/common/prompt.txt', 'r') as file:
                self.prompt_text = file.read()
        except FileNotFoundError:
            print("prompt.txt file not found")
