import sys
from report_class import ReportClass

def main():
    tokens = sys.argv[1:3]
    
    rowHead = list(["Header1", "Header2", "Header3"])    
    dictData = dict(pr1=["data10", "data20", "data30"], pr2=["data11", "data21", "data31"])            

    ReportClass.create_report_file('test.csv', rowHead, dictData)    


if __name__ == "__main__":
    main()
