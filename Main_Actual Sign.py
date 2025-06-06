# Please for the love of god complete just one project please stop abandoning project halfway and
# please test project feasibility before committing you stupid cun

import os
import sys
from os.path import isfile
from Directory import File_Manager
from Directory.jnt_data import ActualSignedData
from Directory import Personal_Pandas as PersonalPandas
from Directory import Data_Process_Personal as dpp
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# 0. File Path
path = os.path.dirname(__file__)
Input_path = os.path.join(path, "Input")
Input_path_as = os.path.join(Input_path, "Actual Sign")
Output_path = os.path.join(path, "Output")
Output_path_as = os.path.join(Output_path, "Actual Signed")
Postal_Code_path = os.path.join(Output_path_as, "Postal Code")

actual_signed_files = File_Manager.get_file_paths(Input_path_as)

# Iterate through all file paths / file and read all files
for csv_actual_signed in actual_signed_files:
    # 1. csv read (conversion if required)
    df_in = pd.read_csv(csv_actual_signed, date_format='%Y-%m-%d')

    # 2. data processing
    # 2.a date time processing
    PersonalPandas.convert_to_datetime(df_in, ["末端机构发件时间"])
    # pre process conversion
    df_in = ActualSignedData.ActualSignedPreprocess(df_in)

    # Improvement - iterate loop for processing multiple date of data
    # List out date and then filter out each date of dataframe and then iterate over
    # date_list = df_in["末端机构发件时间"].unique()
    # for i_date in date_list:

    # 2.b Output date
    date_mode = PersonalPandas.date_mode(df_in, "末端机构发件时间")
    # print(date_mode)

    # 2.c Timeliness
    ######
    # t0 #
    # Output year
    year_out_t0 = datetime.strftime(date_mode, "%Y")
    # Output year month
    date_year_month_t0 = datetime.strftime(date_mode, "%Y%m")
    # Output month day
    date_month_day_t0 = datetime.strftime(date_mode, "%m%d")

    ######
    # t3 #
    # Output date
    date_mode_t3 = date_mode + timedelta(days=3)
    # print(date_mode_t3)
    # Output year
    year_out_t3 = datetime.strftime(date_mode_t3, "%Y")
    # Output year month
    date_year_month_t3 = datetime.strftime(date_mode_t3, "%Y%m")
    # Output month day
    date_month_day_t3 = datetime.strftime(date_mode_t3, "%m%d")

    ######
    # t5 #
    # Output date
    date_mode_t5 = date_mode + timedelta(days=5)
    # print(date_mode_t5)
    # Output year
    year_out_t5 = datetime.strftime(date_mode_t5, "%Y")
    # Output year month
    date_year_month_t5 = datetime.strftime(date_mode_t5, "%Y%m")
    # Output month day
    date_month_day_t5 = datetime.strftime(date_mode_t5, "%m%d")

    # 3. File path management
    # 3.1 Postal
    # T0
    postal_path_t0 = os.path.join(Postal_Code_path, 'T0', str(year_out_t0))
    # T3
    postal_path_t3 = os.path.join(Postal_Code_path, 'T3', str(year_out_t3))
    # T5
    postal_path_t5 = os.path.join(Postal_Code_path, 'T5', str(year_out_t5))

    # 3.2 Timeliness

    # 4. data conversion
    # what type of data to convert to for analysis reason
    # Invoke function
    # 4.1 Postal
    df_postal_t0 = ActualSignedData.t_postal(df_in, date_mode)
    # T3 & T5 -- condition gate for t3 & t5:
    date_dif = datetime.now().date() - date_mode  # get date dif for calculating timeliness
    date_dif = int(date_dif.days)  # convert time to days count and convert to integer

    test_path_t0 = os.path.join(postal_path_t0, str(date_year_month_t0) + '.csv')
    # output new df to csv file
    ActualSignedData.postal_data_out_csv(df_postal_t0, postal_path_t0, date_year_month_t0,
                                         date_mode)

    # T3 & T5 output condition gate; only output T3 & T5 if date diff is equal and between 3 or 5 and equal or more
    # than 5 respectively
    if 5 > date_dif >= 3:
        # T3
        df_postal_t3 = ActualSignedData.t_postal(df_in, date_mode_t3, t_time='3')
        # test T3 path
        test_path_t3 = os.path.join(postal_path_t3, str(date_year_month_t3) + '.csv')
        # output T3 to csv
        ActualSignedData.postal_data_out_csv(df_postal_t3, postal_path_t3, date_year_month_t3,
                                             date_mode_t3, '3')

    elif date_dif >= 5:
        # T3
        df_postal_t3 = ActualSignedData.t_postal(df_in, date_mode_t3, t_time='3')
        # test T3 path
        test_path_t3 = os.path.join(postal_path_t3, str(date_year_month_t3) + '.csv')
        # output T3 to csv
        ActualSignedData.postal_data_out_csv(df_postal_t3, postal_path_t3, date_year_month_t3,
                                             date_mode_t3, '3')

        # T5
        df_postal_t5 = ActualSignedData.t_postal(df_in, date_mode_t5, t_time='5')
        # test T5 path
        test_path_t5 = os.path.join(postal_path_t5, str(date_year_month_t5) + '.csv')
        # output T5 to csv
        ActualSignedData.postal_data_out_csv(df_postal_t5, postal_path_t5, date_year_month_t5,
                                             date_mode_t5, '5')

    else:
        pass

    print('Completed')
    # 4b. Postal

    # Test path 2 (after new file)

    # Option 2. SQLite3

    # 6. data append to monthly data
    # Using processed data, append the data to the monthly excel file for aggregated data
    # Only necessary if adapting Excel for part 5

    # 7. Future implementation

    # 1. Plot output - automatically insert picture of graph directly into Excel
    # 2. Google Drive API - share file to cloud storage and between computer (PyDrive2)
    # 3. Ethnicolr - manpower composition by ethnicity
    # 4. Holidays - holidays module, manpower breakdown for arranging
    # 5. Interactive report - streamlit, stream sync
