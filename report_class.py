import csv

class ReportClass():
    def __init__(self, param):
        self.param = param

    def create_report_file(file_name, headers, data):
        try:
            with open(file_name, 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=';',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(headers)
                for element in iter(data):
                    spamwriter.writerow(data.get(element))
            return file_name
        except Exception as ex:
            pass
            print("Error during generating report")
             
