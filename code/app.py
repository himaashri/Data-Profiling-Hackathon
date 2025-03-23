import sys
from hackathon.regulatoryReporting.regulatoryReportingFactory import RegulatoryReportingFactory

def main():
    factory = RegulatoryReportingFactory()
    factory.read_prompt_file()
    print('Hurray!! Started')

if __name__ == "__main__":
    main()