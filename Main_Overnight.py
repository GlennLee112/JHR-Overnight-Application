import os
import sys
from os.path import isfile
from Directory import File_Manager
from Directory import jnt_data
from Directory.jnt_data import Overnight
from Directory import Personal_Pandas as PersonalPandas
from Directory import jnt_SQL as jnt_sql
import pandas as pd
from datetime import datetime, timedelta
import pandas.io.common
from pathlib import Path
import sys


def main():
    # 1. File Path and variables

    def get_base_path():
        # Ref:
        # https://stackoverflow.com/questions/404744/determining-application-path-in-a-python-exe-generated-by-pyinstaller
        # https://stackoverflow.com/questions/66734987/absolute-path-of-exe-file-not-working-properly-in-python
        """Base path function condition gate to determine if file is running as script of as executable"""
        if getattr(sys, 'frozen', False):
            path_return = os.path.dirname(sys.executable)
        elif __file__:
            path_return = os.path.dirname(__file__)

        return path_return

    # Base
    path = get_base_path()
    # Input
    input_path = os.path.join(path, "Input")
    input_path_overnight = os.path.join(input_path, "Overnight")
    # Output
    output_path = os.path.join(path, "Output")
    output_path_overnight = os.path.join(output_path, "Overnight")
    # File list
    overnight_files = File_Manager.get_file_paths(input_path_overnight)
    # SQL Path
    database_path = os.path.join(path, "Database", "test.db")

    # Empty list hold
    # For sql batch writing purpose
    base_df_awb = []
    # For sql date filtering purpose
    date_list = []

    for csv_overnight in overnight_files:
        # 1. csv read
        # handle empty error
        try:
            df_in = pd.read_csv(csv_overnight, date_format='%Y-%m-%d')
        except pd.errors.EmptyDataError:
            print(csv_overnight, " is empty")
            continue

        # 2. Processing
        # Process data for overnight summary use
        overnight_sum_df = Overnight.Overnight_Preprocess(df_in)
        # # Process data for overnight timeliness use
        # overnight_timeliness_df = overnight_sum_df.copy()
        # # Process data for overnight details use
        # overnight_details_df = overnight_timeliness_df.copy()
        # # Process data for overnight overall use
        # overnight_overall_df = overnight_details_df.copy()

        # 3. Date Mode
        # 3.1 Overnight Summary
        # 3.1.1 Overnight Summary - Mode
        overnight_date_max = PersonalPandas.date_max(overnight_sum_df, 'Arrival Time')
        # Append
        date_list.append(overnight_date_max)
        # 3.1.2 Overnight Summary - year
        overnight_date_year = datetime.strftime(overnight_date_max, "%Y")
        # 3.1.3 Overnight Summary - year month
        overnight_date_year_month = datetime.strftime(overnight_date_max, "%Y%m")
        # 3.1.4 Overnight Summary - full
        overnight_date_full = overnight_date_max.strftime('%Y-%m-%d')
        # 3.1.4 Overnight Summary - full (CSV)
        overnight_date_full_csv = overnight_date_max.strftime('%d-%m-%Y')

        # print(Overnight_date_max)
        # print(overnight_sum_df.dtypes)
        # 4. Dataframe creation
        # 4.1 Overnight Summary

        overnight_summary_df = Overnight.Overnight_Summary(overnight_sum_df, overnight_date_full)
        # print(overnight_sum_df.dtypes)
        # 4.2 Overnight Timeliness

        # Recall dataframe, due to some unidentified issue, it is required to call in original dataframe again
        # Overnight Timeliness function execute
        overnight_timeliness_df = Overnight.Overnight_Timeliness(overnight_sum_df,
                                                                 overnight_date_full)

        # 4.3 Overnight Details
        # df_in_o_d = pd.read_csv(csv_overnight, date_format='%Y-%m-%d')
        # overnight_details_df = Overnight.Overnight_Preprocess(df_in_o_d)
        overnight_details_df = Overnight.Overnight_Details(overnight_sum_df,
                                                           overnight_date_full)

        # 4.4 Overnight Overall
        overnight_overall_df = Overnight.Overnight_Overall(overnight_sum_df,
                                                           overnight_date_full)

        # 4.5 Overnight AWB - SQL
        overnight_awb_sql = Overnight.Overnight_AWB(overnight_sum_df,
                                                    overnight_date_max) # use datetime for datetime upload

        # 4.5

        # Future plan
        # Output overnight overall to sqlite database
        # 4.5 Overnight Overall_db transformation
        # 4.5.1 Create ANM list for connection between (cancelled; reduce database dependencies)
        # e.g.:

        # 5. Output data
        # 5.0 Path creation
        Overnight_summary_path = os.path.join(output_path_overnight, 'Summary', overnight_date_year)
        Overnight_timeliness_path = os.path.join(output_path_overnight, 'Timeliness', overnight_date_year)
        Overnight_details_path = os.path.join(output_path_overnight, 'Details', overnight_date_year)
        Overnight_overall_path = os.path.join(output_path_overnight, 'Overall', overnight_date_year)
        # # 5.1 Overnight Summary output
        Overnight.Overnight_data_out_csv(overnight_summary_df, Overnight_summary_path,
                                         overnight_date_year_month, overnight_date_full)
        # 5.2 Overnight Timeliness output
        Overnight.Overnight_data_out_csv(overnight_timeliness_df, Overnight_timeliness_path,
                                         overnight_date_year_month, overnight_date_full)
        # 5.3 Overnight Details output
        Overnight.Overnight_data_out_csv(overnight_details_df, Overnight_details_path,
                                         overnight_date_year_month, overnight_date_full)
        # 5.4 Overnight Overall output
        Overnight.Overnight_data_out_csv(overnight_overall_df, Overnight_overall_path,
                                         overnight_date_year_month, overnight_date_full_csv)

        # 6. SQL dataframe append
        # Combine of dataframe to sql database
        # filter of df by Data date before concatenating
        if isinstance(base_df_awb, pd.Series):
            base_df_awb = base_df_awb[(base_df_awb["Data Date"] != overnight_date_full)]
        # Append
        base_df_awb.append(overnight_awb_sql)

    # 7. SQL update
    # Once appending is completed, concat df to one list
    final_df = pd.concat(base_df_awb).reset_index(drop=True)
    # final_df.to_csv("test_output_2.csv")

    # Rename columns to one compliant with sql data base
    final_df.rename(columns={'Scanning DP No. | Last': 'Scanning_DP_Last',
                             'AWB': 'AWB',
                             'Data Date': 'Data_Date',
                             'Scanning Type | Last': 'Scanning_Type_Last',
                             'Arrival Time': 'Arrival_Time',
                             'Scanning Time | Last': 'Scanning_Time_Last',
                             'Return Parcel': 'Return_Parcel',
                             'DP No. | Pick Up': 'Pick_Up_DP'
                             },
                    inplace=True)

    print(final_df.columns)

    # Change Data_Date to date only string format
    final_df['Data_Date'] = final_df['Data_Date'].dt.strftime('%Y-%m-%d')

    # 3. data update
    jnt_sql.overnight_awb_update(final_df, database_path, date=date_list)


if __name__ == "__main__":
    main()
