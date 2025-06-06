import os
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta, MO
from Directory import jnt_data


# def datetime_conversion(subject, format = "%Y-%m-%d %H:%M:%S"):
def convert_to_datetime(df, cols=None):
    """simple conversion function to change columns or entire dataframe to desired datatype using '.astype'

    Base code from: https://stackoverflow.com/questions/66189787/python-convert-multiple-columns-to-datetime-using-for-loop

    Modified function to support iteration of multiple columns in for loop
    """
    # Future improvement: currently facing SettingWithCopyWarning; not affecting function but if remove
    # https://stackoverflow.com/questions/45037907/python-astypestr-gives-settingwithcopywarning-and-requests-i-use-loc
    if not cols:
        # if no columns are specified, use all
        cols = df.columns
        df[cols] = df[cols].astype('datetime64[ns]')

        return df

    elif type(cols) is list:
        for col in cols:
            df[col] = df[col].astype('datetime64[ns]')

        return df

    elif cols and type(cols) is not list:
        print("Please use list for cols variable")


def convert_number_to_int_to_str(df, cols=None):
    """simple conversion function to change columns or entire dataframe to desired datatype using '.astype'

    Base code from: https://stackoverflow.com/questions/66189787/python-convert-multiple-columns-to-datetime-using-for-loop

    Modified function to support iteration of multiple columns in for loop
    """
    if not cols:
        # if no columns are specified, use all
        cols = df.columns
        df[cols] = df[cols].astype('Int64').astype('str')

        return df

    elif type(cols) is list:
        for col in cols:
            df[col] = df[col].astype('Int64').astype('str')

        return df

    elif cols and type(cols) is not list:
        print("Please use list for cols variable")


def date_mode(df, column, NA=True):

    mode_of_date = df[column].dt.date.mode(dropna=NA)

    return mode_of_date[0]


def date_max(df, column):

    max_of_date = max(df[column])

    return max_of_date


def csv_out(df_in, file_name, path, index=False, date_format='%Y-%d-%m'):
    """"output function for dataframe to got to excel output file"""
    # Create folder path if not exist
    if not os.path.exists(path):
        os.makedirs(path)

    # Test if file_name provided endswith the correct extension
    if not file_name.endswith('.csv'):
        file_name = file_name+'.csv'

    # Future implementation, auto amend false extension
    # else:
    #     file_name = file_name+'.csv'

    output_path = os.path.join(path, file_name)
    df_in.to_csv(output_path, index=index, date_format=date_format)


def col_unique_list(df, column_name):
    """" Simple function to convert a given column to a list of values"""
    unique_list = df[column_name].unique()

    return unique_list


def intersection_return(list_1, list_2):
    """" Simple function to return intersection values of two list and return as list"""
    # reference: https://stackoverflow.com/questions/2864842/common-elements-comparison-between-2-lists

    intersect_list = list(set(list_1).intersection(list_2))
    for il in intersect_list:
        print(il)

    return intersect_list


def df_merge(df_1, df_2, how='0'):
    # Simplified version without output function, simple merging of df only
    """"Append function with datatype selector, use this function to merge two dataframe of same columns"""

    out_df = df_1.merge(df_2, how="inner")

    return out_df


def date_range_list(time_1, time_2, time_format="%Y-%m-%d"):
    """Convert range of dates to list of user defined time format

    Output for list for users or function to iterate on"""
    # Ref: https://stackoverflow.com/questions/34898525/generate-list-of-months-between-interval
    # future implementation: convert to datetime format incase

    range_list = pd.date_range(time_1, time_2, freq="MS").strftime(time_format).to_list()

    return range_list


def date_diff(in_date, dif_day=0, dif_month=0, in_date_format="%Y-%m-%d", subtraction=True):
    # Check if in_date is in dt.date format
    # https://stackoverflow.com/questions/16151402/python-how-can-i-check-whether-an-object-is-of-type-datetime-date

    test_in_date = isinstance(in_date, dt.date)

    if test_in_date:
        pass
    else:
        in_date = in_date.strftime(in_date_format)

    # Deduct by desired date
    if subtraction:
        out_date = in_date - relativedelta(days=dif_day, months=dif_month)
    else:
        out_date = in_date + relativedelta(days=dif_day, months=dif_month)

    return out_date

    # Drop duplicates from
    # Option 1. Drop duplicate
    # Simplest method of dropping duplicate, default method unless this method somehow didn't drop all desired entries
    # https://saturncloud.io/blog/how-to-drop-duplicated-index-in-a-pandas-dataframe-a-complete-guide/#:~:text=Pandas%20provides%20the%20drop_duplicates(),names%20to%20the%20subset%20parameter.

    # Option 2. filter
    # Back up method in case Drop duplicate fails


# def df_merge(df, in_path, in_type='0'):
#     """"Append function with datatype selector, use this function to merge two dataframe of same columns"""
#     # Dictionaries reference:
#     # https://stackoverflow.com/questions/75512990/how-to-return-values-in-a-python-dictionary
#     extension_dict = {'0': '.xlsx',
#                       '1': '.csv',
#                       '2': '.xls'}
#
#     extension = extension_dict[in_type]
#
#     # Determine which read to use based on user selection
#     if extension in ('.xlsx','.xls'):
#         read_df = pd.read_excel(in_path) # Read as Excel file
#
#     elif extension == '.csv':
#         read_df = pd.read_csv(in_path) # Read as csv file
#
#     print(read_df.dtypes)
#
#     out_df = read_df.merge(df, how="inner")
#
#     if extension in ('.xlsx','.xls'):
#         out_df.to_excel(in_path) # Read as Excel file
#
#     elif extension == '.csv':
#         out_df.to_csv(in_path) # Read as csv file
#
#     # Drop duplicates from
#     # Option 1. Drop duplicate
#     # Simplest method of dropping duplicate, default method unless this method somehow didn't drop all desired entries
#     # https://saturncloud.io/blog/how-to-drop-duplicated-index-in-a-pandas-dataframe-a-complete-guide/#:~:text=Pandas%20provides%20the%20drop_duplicates(),names%20to%20the%20subset%20parameter.
#
#     # Option 2. filter
#     # Back up method in case Drop duplicate fails

