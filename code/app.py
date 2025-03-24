
from src.main.hackathon.regulatoryReporting.regulatoryReportingFactory import RegulatoryReportingFactory

def main():
    factory = RegulatoryReportingFactory()
    factory.generateReport()
    print('Hurray!! Started')

if __name__ == "__main__":
    main()