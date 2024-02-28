import xlrd
from openpyxl import Workbook
from datetime import datetime

def get_list(file_path):
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_index(0)

    output_tuples = []

    for row_idx in range(1, sheet.nrows):
        row = sheet.row_values(row_idx)
        donorId = row[2]
        try:
            donorDate = xlrd.xldate_as_datetime(row[3], workbook.datemode)
        except:
            donorDate = ''

        filter_1 = row[7]
        filter_2 = row[10]
        if donorDate:
            if filter_1 == "W007":
                output_tuples.append((donorId, donorDate))

    return output_tuples

def filter_data(file_path, reference_tuples):
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_index(0)

    output_rows = []

    for reference_donor_id, reference_donor_date in reference_tuples:
        closest_rows = []
        closest_dates = []

        for row_idx in range(1, sheet.nrows):
            row = sheet.row_values(row_idx)
            donorAlias = row[3]
            donorId = row[5]
            try:
                donorDate = xlrd.xldate_as_datetime(row[7], workbook.datemode)
            except:
                donorDate = ''
            donorWeight = row[9]
            donorUcn = row[12]

            if donorDate and donorId == reference_donor_id:
                # Append to the closest dates list
                closest_dates.append((donorId, donorDate, donorWeight, donorAlias, donorUcn))

        # Sort the closest dates list based on the difference
        closest_dates.sort(key=lambda x: abs(reference_donor_date - x[1]))

        # Take the five closest dates, including those before and after if necessary
        closest_rows.extend(closest_dates[:5])

        # Extend the output_rows list
        output_rows.extend(closest_rows)

    return output_rows

if __name__ == "__main__":
    referenced_xls = 'sample1.xls'
    data_xls = 'sample2.xls'

    reference_tuples = get_list(reference_xls)
    output_rows = filter_data(data_xls, reference_tuples)

    wb = Workbook()
    ws = wb.active

    for row in output_rows:
        ws.append(row)

    wb.save("output.xlsx")