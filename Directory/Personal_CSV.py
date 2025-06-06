import csv


def csv_read(in_file):
    """Open file and reader the csv file with csv reader"""
    with open(in_file) as in_file:
        return csv.reader(in_file, delimiter="")


# def write_csv(input):
