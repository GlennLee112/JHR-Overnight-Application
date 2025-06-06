import pandas as pd
import Directory.Personal_Pandas as PersonalPandas
import Directory.File_Manager as PersonalFM
import numpy as np
import datetime as dt
# from datetime import datetime
import os

# Compilation of list from raw data to be used for function to choose columns from

actual_sign_column_list_T0 = ["AWB",
                              "DP No. | Delivery",
                              "Delivery Dispatcher",
                              "Destination Postcode",
                              "末端机构发件时间",
                              "Arrival Time",
                              "Delivery Signature",
                              "On-Time Signed",
                              "T+3 On-Time",
                              "T+5 On-Time",
                              "COD Amount",
                              "COD"]

Col_to_conv_time_T0 = ["末端机构发件时间",
                       "Arrival Time",
                       "Delivery Signature"]

Merge_on_col_list_postal = ['DP No. | Delivery',
                            'Destination Postcode']

Overnight_Details_Header = ['Scanning DP No. | Last', 'Data Date',
                            'AWB_T1_COD', 'AWB_T1_NCOD',
                            'AWB_T2_COD', 'AWB_T2_NCOD',
                            'AWB_T3_COD', 'AWB_T3_NCOD',
                            'AWB_T4_COD', 'AWB_T4_NCOD',
                            'AWB_>=T5_COD', 'AWB_>=T5_NCOD',
                            'AWB_T1_Y_Return_Parcel',
                            'AWB_T2_Y_Return_Parcel',
                            'AWB_T3_Y_Return_Parcel',
                            'AWB_T4_Y_Return_Parcel',
                            'AWB_>=T5_Y_Return_Parcel']

Delivery_Summary_Header = ['DP No. | Delivery',
                           'Dispatcher ID',
                           'Volume | Delivery',
                           'Volume | Delivery Signature']

Arrival_Summary_Header = ['Operating Station No.',
                          '应到总票数',
                          'Qty | Arrived']


class ActualSignedData:
    @staticmethod
    def ActualSignedPreprocess(df_input):
        # COD Amount fill blank and convert to float
        df_input["COD Amount"].fillna(0, inplace=True)
        df_input["COD Amount"] = df_input["COD Amount"].astype('int')
        # COD np.where
        df_input["COD"] = np.where(df_input["COD Amount"] > 0, "COD", "NCOD")

        return df_input

    @staticmethod
    def t_postal(df_input, date_mode_to_use, t_time='0'):
        """Return postal code breakdown dataframe of actual signed data given

        This will return postal code dataframe for further processing"""

        time_dict = {'0': 'T0',
                     '3': 'T+3',
                     '5': 'T+5',
                     '7': 'T+7', }

        time_to_app = time_dict[t_time]
        # print(time_to_app)

        if t_time != '0':
            t_col_to_use = f'{time_to_app} On-Time'
        else:
            t_col_to_use = 'On-Time Signed'

        # print(t_col_to_use)

        # assign required column to dataframe
        df_actual_signed = df_input[actual_sign_column_list_T0]
        # Replace '-' of On-Time Signed to 'N'
        df_actual_signed[t_col_to_use] = df_actual_signed[t_col_to_use].replace("-", "N")
        # Convert column to date time, column to convert datetime already set in above
        PersonalPandas.convert_to_datetime(df_actual_signed, Col_to_conv_time_T0)
        # Get mode from the datetime
        date_mode = PersonalPandas.date_mode(df_actual_signed, '末端机构发件时间')
        # Add column to indicate date_mode
        df_actual_signed['Date'] = date_mode_to_use
        # Convert postal code to string
        PersonalPandas.convert_number_to_int_to_str(df_actual_signed, ['Destination Postcode'])
        # pivot and return data
        df_output = pd.pivot_table(df_actual_signed,
                                   values=['AWB'],
                                   index=['DP No. | Delivery', 'Destination Postcode', 'Date'],
                                   columns=['COD', t_col_to_use],
                                   aggfunc="count").fillna(0).astype(int).reset_index()

        # Merge multiindex to single index for ease of reading
        # https://stackoverflow.com/questions/47637153/pandas-combining-header-rows-of-a-multiindex-dataframe
        # Shorten with list comprehension with Deepseek assistance
        e_list = [f'{i}' if j == '' else f'{i}_{j}_{k}' for i, j, k in df_output.columns]

        # assign list to output df columns
        df_output.columns = e_list

        # Rename date columns to
        df_output.rename(columns={'Date': f'{time_to_app}_Date'}, inplace=True)

        print(df_output.dtypes)

        return df_output

    @staticmethod
    def postal_data_out_csv(df_in, out_path, file_name, time_mode, timeliness='0'):
        """Output postal data to path provided in CSV format

        Function include auto merging with existing CSV data (if present) or directly create new CSV file

        In addition, auto select of columns to use based on timeliness type

        Parameters
        ----------
        df_in = New Pandas dataframe input
        out_path = Path to CSV output into
        file_name = The string to be used to rename file as
        test_path = Existing data file path; also serve as read path
        time_mode = datetime value to be compared and filter out in new data
        """

        # Timeliness Select
        time_dict = {'0': 'T0',
                     '3': 'T+3',
                     '5': 'T+5'}

        timeliness = time_dict[timeliness]
        # print(time_to_app)

        t_col_to_use = f'{timeliness}_Date'

        # Test if path is present; refer to personal_file_manager for more information
        test_path = os.path.join(out_path, file_name + '.csv')
        file_path_test = PersonalFM.test_path(test_path)
        print("Postal Data Out")
        if file_path_test:
            print(
                'File exists, proceed to concat new data to aggregated data')  # for debugging; enable or disable as required
            # load old file
            df_to_merge = pd.read_csv(test_path, date_format='%Y-%m-%d')
            # filling NA value as int; avoid
            df_to_merge["Destination Postcode"] = df_to_merge['Destination Postcode'].fillna(0).astype(str)
            # Convert to date
            # df_to_merge["T0_Date"] = pd.to_datetime(df_to_merge["T0_Date"].str.strip('"'), format='%Y-%m-%d')
            # Final Option; directly remove aggregated data that has the same date as data to be merged
            # Filter entries that has the same date as new T0 data
            # Convert data_mode again to same format just in case
            date_mode = time_mode.strftime('%Y-%m-%d')
            # filter out
            df_to_merge = df_to_merge[df_to_merge[t_col_to_use] != date_mode]
            # df_to_merge.info() # print out dataframe info; enable or disable as required
            # Concat new T0 data with aggregated data
            df_out = pd.concat([df_in, df_to_merge])
            # invoke csv out once all processing is completed
            PersonalPandas.csv_out(df_out, str(file_name), out_path)

        # If file doesn't exist, call excel_out for straight export (excel auto create file; file creation not needed)
        else:
            print("File doesn't exists; outputting new file")  # for debugging; enable or disable as required
            # Straight csv out
            PersonalPandas.csv_out(df_in, str(file_name), out_path)

    @staticmethod
    def t0_data(df_input):
        print("Other")

    @staticmethod
    def t3_data(df_input):
        print("Other")

    @staticmethod
    def postal_overall(df_input):
        #https://stackoverflow.com/questions/68373291/add-new-row-as-header-in-multiindexed-dataframe
        print("Other")


class Overnight:
    @staticmethod
    def Overnight_Preprocess(df_in):
        df_in = df_in.copy(deep=False)
        # Remove empty entry
        df_in = df_in[df_in['Arrival Time'].notnull()]
        # overnight_df['Arrival Time'] = pd.to_datetime(overnight_df['Arrival Time'], "coerce").dt.date
        # overnight_df['Scanning Time | Last'] = pd.to_datetime(overnight_df['Scanning Time | Last'], "coerce").dt.date
        df_in[['Arrival Time', 'Scanning Time | Last']] = (df_in[['Arrival Time', 'Scanning Time | Last']]
                                                           .apply(pd.to_datetime, errors='coerce'))

        # Filter out 'JHR0' DP
        df_in = df_in[(~df_in['Scanning DP No. | Last'].str.contains("JHR0", regex=True) == True)]
        # Filter out column where last scan dp is the same as pick up dp; disabled for now
        # df_in = df_in[(df_in['Scanning DP No. | Last']) != (df_in['DP No. | Pick Up'])]
        # print(overnight_df.dtypes)
        # Replace COD from chinese text to english
        df_in["COD"] = np.where(df_in["COD"] == '是', 'COD', 'NCOD')
        # Assign full text to return parcel (Y/N to Y_Return_Parcel, N_Return_Parcel)
        df_in["Return Parcel"] = np.where(df_in["Return Parcel"] == 'Y', 'Y_Return_Parcel', 'N_Return_Parcel')

        print("Overnight_Preprocess: Done")
        return df_in

    @staticmethod
    def Overnight_Summary(df_in, date_mode_to_use):
        """Summary calculation of overall Overnight volume in AWB count

        Parameter:
        1. df - input df as basis for calculation and transformation
        2. date_mode_to_use - use for new Data Date column for output dataframe in string format; for ease of comparison;
                                output data must be converted back to datetime format when imported for other purpose

        Filtering condition:
        1. Filter out - no arrival scan
        2. Filter out - DP with 'JHR0' string
        3. Filter out - arrival within latest date (parcel that just arrived and doesn't count as overnight
        """
        overnight_sum_df = df_in.copy(deep=False)
        # Set up df
        # 1. Datetime conversion; convert to datetime and then date
        # overnight_df[['Arrival Time', 'Scanning Time | Last']] = (overnight_df[['Arrival Time', 'Scanning Time | Last']]
        #                                                           .apply(pd.to_datetime, errors='coerce'))
        overnight_sum_df['Scanning Time | Last'] = overnight_sum_df['Scanning Time | Last'].dt.date
        overnight_sum_df['Arrival Time'] = overnight_sum_df['Arrival Time'].dt.date

        # 2. Data cleaning - replace NA date time with blank for ease of filtering
        # overnight_df['Arrival Time'] = overnight_df['Arrival Time'].fillna('')
        # overnight_df = overnight_df[(overnight_df['Arrival Time'] != "")]
        # overnight_df = overnight_df[overnight_df['Arrival Time'].notnull()]
        # print(overnight_sum_df['Arrival Time'])

        # 3. Data filtering and processing
        # Todays date, get max date
        # max_date_test = max(overnight_df['Arrival Time']).replace(hour=0, minute=0, second=0)
        # print(overnight_df['Arrival Time'])
        # max_date = PersonalPandas.date_diff(max(overnight_df['Arrival Time']), dif_day=1)
        max_date = max(overnight_sum_df['Arrival Time'])

        print(f'Overnight sum processing - max date is: {max_date}')
        # max_date = max_date.strftime('%Y-%m-%d')
        # Filter by condition
        # Filter out arrival of today & DP starting with 'JHR0'
        # overnight_sum_df = overnight_sum_df[(~overnight_sum_df['Scanning DP No. | Last'].str.contains("JHR0",
        #                                                                                               regex=True) == True) &  # Unnecessary DP; note the tilde (~) operator for logic inversion
        #                                     (overnight_sum_df['Arrival Time'] < max_date)] # Today Arrival removal

        overnight_sum_df = overnight_sum_df[(overnight_sum_df['Arrival Time'] < max_date)]  # Today Arrival removal

        # Assign data date

        # 3.1 New
        # Grouping and summarizing data into a short summarized table
        # overnight_df = overnight_df.groupby('Scanning DP No. | Last').size().reset_index()
        # overnight_df.reset_index(inplace=True, drop=True)
        # overnight_df.columns.values[1] = 'Overnight Volume'
        # overnight_df['Data Date'] = max_date

        df_output = pd.pivot_table(overnight_sum_df,
                                   values=['AWB'],
                                   index=['Scanning DP No. | Last'],
                                   aggfunc="count").fillna(0).astype(int).reset_index()

        # df_output = overnight_df

        df_output['Data Date'] = date_mode_to_use

        return df_output

    # @staticmethod
    # def overnight_csv_get(df, date_filter, column):

    @staticmethod
    def Overnight_Timeliness(df_in, date_mode_to_use):
        overnight_timeliness_df = df_in.copy(deep=False)
        # # 1. Datetime conversion; convert to datetime and then date
        overnight_timeliness_df['Scanning Time | Last'] = overnight_timeliness_df['Scanning Time | Last'].dt.date
        overnight_timeliness_df['Arrival Time'] = overnight_timeliness_df['Arrival Time'].dt.date

        # 2. Get the data date
        # Obtain the max date of arrival time data
        max_date = max(overnight_timeliness_df['Arrival Time'])
        # print(f'Overnight time processing max date is: {max_date}')
        # print(overnight_timeliness_df['Arrival Time'])
        # max_date = max_date_test - pd.Timedelta(1, unit="d")
        # max_date = max_date.strftime('%Y-%m-%d')

        # 3. Filtering
        # 3.1 Arrival Date filtering
        # empty date
        # date before max
        overnight_timeliness_df = overnight_timeliness_df[(overnight_timeliness_df['Arrival Time'] < max_date)]
        # # 3.2 JHR0 DP filtering
        # overnight_timeliness_df = overnight_timeliness_df[(~overnight_timeliness_df['Scanning DP No. | Last'].str.
        #                                                    contains("JHR0", regex=True) == True)]
        # 4. Calculation
        # 4.1 timeliness
        # print(overnight_timeliness_df.dtypes)
        # https://stackoverflow.com/questions/37840812/pandas-subtracting-two-date-columns-and-the-result-being-an-integer
        overnight_timeliness_df['Timeliness'] = (max_date - overnight_timeliness_df['Arrival Time']).fillna(0)
        overnight_timeliness_df['Timeliness'] = overnight_timeliness_df['Timeliness'].dt.days

        # print(overnight_timeliness_df['Timeliness'])
        # type(overnight_timeliness_df['Timeliness'])
        # print((overnight_timeliness_df["Timeliness"]))
        # print(overnight_timeliness_df.dtypes)

        # 5. Pivot
        # 5.0 Timeliness assign
        # assign timeliness, by assigning the timeliness into 'group'
        # Ref: https://stackoverflow.com/questions/39109045/numpy-where-with-multiple-conditions
        # Ref: https://stackoverflow.com/questions/79509402/python-environment-error-typeerror-choicelist-and-default-value-do-not-have-a
        pivot_condition = [overnight_timeliness_df['Timeliness'] >= 5,
                           overnight_timeliness_df["Timeliness"] == 4,
                           overnight_timeliness_df["Timeliness"] == 3,
                           overnight_timeliness_df["Timeliness"] == 2,
                           overnight_timeliness_df["Timeliness"] == 1]

        pivot_choices = ['>=T5', 'T4', 'T3', 'T2', 'T1']
        overnight_timeliness_df["T_category"] = np.select(pivot_condition, pivot_choices, default="Other")

        # 5.1 COD Pivot
        # Filter out '0' before pivoting
        overnight_timeliness_df = overnight_timeliness_df[(overnight_timeliness_df['T_category'] != 'Other')]

        df_output = pd.pivot_table(overnight_timeliness_df,
                                   values=['AWB'],
                                   index=['Scanning DP No. | Last'],
                                   columns=['T_category'],
                                   aggfunc="count").fillna(0).astype(int).reset_index()

        # 6. Formatting column and multi-header reduction
        # https://stackoverflow.com/questions/47637153/pandas-combining-header-rows-of-a-multiindex-dataframe
        # print(max_date)
        df_output['Data Date'] = date_mode_to_use
        overnight_timeliness_df_list = [f'{i}' if j == '' else f'{j}' for i, j in df_output.columns]

        df_output.columns = overnight_timeliness_df_list

        df_output = df_output[['Scanning DP No. | Last', 'Data Date', 'T1', 'T2', 'T3', 'T4', '>=T5']]

        return df_output

    @staticmethod
    def Overnight_Details(df_in, date_mode_to_use):
        # print(overnight_timeliness_df.dtypes)
        overnight_timeliness_df_in = df_in.copy(deep=False)
        # # 1. Datetime conversion; convert to datetime and then date
        overnight_timeliness_df_in['Scanning Time | Last'] = overnight_timeliness_df_in['Scanning Time | Last'].dt.date
        overnight_timeliness_df_in['Arrival Time'] = overnight_timeliness_df_in['Arrival Time'].dt.date

        # 2. Get the data date
        # Obtain the max date of arrival time data
        max_date = max(overnight_timeliness_df_in['Arrival Time'])
        # print(f'Overnight time processing max date is: {max_date}')
        # print(overnight_timeliness_df['Arrival Time'])
        # max_date = max_date_test - pd.Timedelta(1, unit="d")
        # max_date = max_date.strftime('%Y-%m-%d')

        # 3. Filtering
        # 3.1 Arrival Date filtering
        # empty date
        # date before max
        overnight_timeliness_df_in = overnight_timeliness_df_in[(overnight_timeliness_df_in['Arrival Time'] < max_date)]
        # # 3.2 JHR0 DP filtering
        # overnight_timeliness_df = overnight_timeliness_df[(~overnight_timeliness_df['Scanning DP No. | Last'].str.
        #                                                    contains("JHR0", regex=True) == True)]
        # 4. Calculation
        # 4.1 timeliness
        # print(overnight_timeliness_df.dtypes)
        # https://stackoverflow.com/questions/37840812/pandas-subtracting-two-date-columns-and-the-result-being-an-integer
        overnight_timeliness_df_in['Timeliness'] = (max_date - overnight_timeliness_df_in['Arrival Time']).fillna(0)
        overnight_timeliness_df_in['Timeliness'] = overnight_timeliness_df_in['Timeliness'].dt.days

        # print(overnight_timeliness_df['Timeliness'])
        # type(overnight_timeliness_df['Timeliness'])
        # print((overnight_timeliness_df["Timeliness"]))
        # print(overnight_timeliness_df.dtypes)

        # 5. Pivot
        # 5.0 Timeliness assign
        # assign timeliness, by assigning the timeliness into 'group'
        # Ref: https://stackoverflow.com/questions/39109045/numpy-where-with-multiple-conditions
        # Ref: https://stackoverflow.com/questions/79509402/python-environment-error-typeerror-choicelist-and-default-value-do-not-have-a
        pivot_condition = [overnight_timeliness_df_in['Timeliness'] >= 5,
                           overnight_timeliness_df_in["Timeliness"] == 4,
                           overnight_timeliness_df_in["Timeliness"] == 3,
                           overnight_timeliness_df_in["Timeliness"] == 2,
                           overnight_timeliness_df_in["Timeliness"] == 1]

        pivot_choices = ['>=T5', 'T4', 'T3', 'T2', 'T1']
        overnight_timeliness_df_in["T_category"] = np.select(pivot_condition, pivot_choices, default="Other")

        # 5.1 COD Pivot
        # Assign copy of original dataframe
        df_merge_cod = overnight_timeliness_df_in.copy()
        # Mandatory filter - T_category = Other
        df_merge_cod = df_merge_cod[(overnight_timeliness_df_in['T_category'] != 'Other')]
        # Pivot by COD
        df_merge_cod = pd.pivot_table(df_merge_cod, values=['AWB'], index=['Scanning DP No. | Last'],
                                      columns=['T_category', 'COD'], aggfunc="count").fillna(0).astype(
            int).reset_index()

        # 5.2 Return
        # Assign copy of original dataframe
        df_merge_return = overnight_timeliness_df_in.copy()
        # Mandatory filter - T_category = Other
        df_merge_return = df_merge_return[(overnight_timeliness_df_in['T_category'] != 'Other')]
        df_merge_return = df_merge_return[(overnight_timeliness_df_in['Return Parcel'] == 'Y_Return_Parcel')]
        #
        df_merge_return = pd.pivot_table(df_merge_return, values=['AWB'], index=['Scanning DP No. | Last'],
                                         columns=['T_category', 'Return Parcel'],
                                         aggfunc="count").fillna(0).astype(int).reset_index()

        # 6. Formatting column and multi-header reduction
        # https://stackoverflow.com/questions/47637153/pandas-combining-header-rows-of-a-multiindex-dataframe
        # print(max_date)
        # 6.1 COD
        df_merge_cod['Data Date'] = date_mode_to_use
        overnight_timeliness_df_list_cod = [f'{i}' if j == '' else f'{i}_{j}_{k}' for i, j, k in df_merge_cod.columns]

        df_merge_cod.columns = overnight_timeliness_df_list_cod

        # 6.2 Return

        df_merge_return['Data Date'] = date_mode_to_use
        overnight_timeliness_df_list_return = [f'{i}' if j == '' else f'{i}_{j}_{k}' for i, j, k in
                                               df_merge_return.columns]

        df_merge_return.columns = overnight_timeliness_df_list_return

        # 7. Merge
        # Merge separated dataframe from previous step (step 6)
        # https://stackoverflow.com/questions/44327999/how-to-merge-multiple-dataframes
        df_final = pd.merge(df_merge_cod, df_merge_return, how="outer", on=["Scanning DP No. | Last", "Data Date"])

        # 8. Rearrange header - import from outside
        df_final = df_final[Overnight_Details_Header]

        return df_final

    @staticmethod
    def Overnight_Overall(df_in, date_mode_to_use):
        overnight_overall_df_in = df_in.copy(deep=False)
        # # 1. Datetime conversion; convert to datetime and then date
        overnight_overall_df_in['Scanning Time | Last'] = overnight_overall_df_in['Scanning Time | Last'].dt.date
        overnight_overall_df_in['Arrival Time'] = overnight_overall_df_in['Arrival Time'].dt.date

        # 2. Get the data date
        # Obtain the max date of arrival time data
        max_date = max(overnight_overall_df_in['Arrival Time'])

        # 3. Filtering
        # 3.1 Arrival Date filtering
        # date before max
        overnight_overall_df_in = overnight_overall_df_in[(overnight_overall_df_in['Arrival Time'] < max_date)]

        # 4. Calculation
        # 4.1 timeliness
        # print(overnight_timeliness_df.dtypes)
        # https://stackoverflow.com/questions/37840812/pandas-subtracting-two-date-columns-and-the-result-being-an-integer
        overnight_overall_df_in['Timeliness'] = (max_date - overnight_overall_df_in['Arrival Time']).fillna(0)
        overnight_overall_df_in['Timeliness'] = overnight_overall_df_in['Timeliness'].dt.days

        # 5. Pivot
        # 5.0 Timeliness
        # assign timeliness, by assigning the timeliness into 'group'
        # Ref: https://stackoverflow.com/questions/39109045/numpy-where-with-multiple-conditions
        # Ref: https://stackoverflow.com/questions/79509402/python-environment-error-typeerror-choicelist-and-default-value-do-not-have-a
        pivot_condition = [overnight_overall_df_in['Timeliness'] >= 5,
                           overnight_overall_df_in["Timeliness"] == 4,
                           overnight_overall_df_in["Timeliness"] == 3,
                           overnight_overall_df_in["Timeliness"] == 2,
                           overnight_overall_df_in["Timeliness"] == 1]

        pivot_choices = ['>=T5', 'T4', 'T3', 'T2', 'T1']
        overnight_overall_df_in["T_category"] = np.select(pivot_condition, pivot_choices, default="Other")

        # 5.1 Melt
        # Assign copy of original dataframe
        df_final = overnight_overall_df_in.copy()
        # Mandatory filter - T_category = Other
        df_final = df_final[(overnight_overall_df_in['T_category'] != 'Other')]
        # Pivot by required column as index
        df_final = pd.pivot_table(df_final, values=['AWB'],
                                  index=['Scanning DP No. | Last', "Return Parcel", 'T_category',
                                         "COD"],
                                  aggfunc="count").fillna(0).astype(int).reset_index()
        # Insert Data Date column
        df_final["Data Date"] = date_mode_to_use

        return df_final

    @staticmethod
    def Overnight_AWB(df_in, date_mode_to_use):
        overnight_awb_df_in = df_in.copy(deep=False)
        # # 1. Datetime conversion; convert to datetime and then date
        overnight_awb_df_in['Scanning Time | Last'] = overnight_awb_df_in['Scanning Time | Last'].dt.date
        overnight_awb_df_in['Arrival Time'] = overnight_awb_df_in['Arrival Time'].dt.date

        # 2. Get the data date
        # Obtain the max date of arrival time data
        max_date = max(overnight_awb_df_in['Arrival Time'])

        # 3. Filtering
        # 3.1 Arrival Date filtering
        # date before max
        overnight_awb_df_in = overnight_awb_df_in[(overnight_awb_df_in['Arrival Time'] < max_date)]

        # 4. Calculation
        # 4.1 timeliness
        # print(overnight_timeliness_df.dtypes)
        # https://stackoverflow.com/questions/37840812/pandas-subtracting-two-date-columns-and-the-result-being-an-integer
        overnight_awb_df_in['Timeliness'] = (max_date - overnight_awb_df_in['Arrival Time']).fillna(0)
        overnight_awb_df_in['Timeliness'] = overnight_awb_df_in['Timeliness'].dt.days

        # 5. Pivot
        # 5.0 Timeliness
        # assign timeliness, by assigning the timeliness into 'group'
        # Ref: https://stackoverflow.com/questions/39109045/numpy-where-with-multiple-conditions
        # Ref: https://stackoverflow.com/questions/79509402/
        pivot_condition = [overnight_awb_df_in['Timeliness'] >= 5,
                           overnight_awb_df_in["Timeliness"] == 4,
                           overnight_awb_df_in["Timeliness"] == 3,
                           overnight_awb_df_in["Timeliness"] == 2,
                           overnight_awb_df_in["Timeliness"] == 1]

        pivot_choices = ['T5 & Above', 'T4', 'T3', 'T2', 'T1']
        overnight_awb_df_in["T_category"] = np.select(pivot_condition, pivot_choices, default="Other")

        overnight_awb_df_in = overnight_awb_df_in[(overnight_awb_df_in['T_category'] != 'Other')]

        overnight_awb_df_in["Data Date"] = date_mode_to_use

        overnight_awb_df_in = overnight_awb_df_in[['AWB', 'DP No. | Pick Up', 'Arrival Time', 'Scanning Type | Last',
                                                   'Scanning DP No. | Last', 'Scanning Time | Last', 'COD',
                                                   'Return Parcel',
                                                   'T_category', 'Data Date']]

        return overnight_awb_df_in

    @staticmethod
    def Overnight_data_out_csv(df_in, out_path, file_name, time_mode, inplace=True):
        """Output overnight data to path provided in CSV format

        Function include auto merging with existing CSV data (if present) or directly create new CSV file

        Due to no column selection required, process is simplified compare to postal data out csv function

        Parameters
        ----------
        df_in = New Pandas dataframe input
        out_path = Path to CSV output into
        file_name = The string to be used to rename file as
        test_path = Existing data file path; also serve as read path
        time_mode = datetime value to be compared and filter out in new data
        """

        # Test if path is present; refer to personal_file_manager for more information
        test_path = os.path.join(out_path, file_name + '.csv')
        file_path_test = PersonalFM.test_path(test_path)
        print("Data Out")

        if file_path_test:
            print('File exists, proceed to concat new data to aggregated data')  # enable / disable for debugging
            # load old file
            df_to_merge = pd.read_csv(str(test_path), date_format='%Y-%m-%d')  # date_format='%Y-%m-%d'
            # Convert to date
            # Final Option; directly remove aggregated data that has the same date as data to be merged
            # Filter entries that has the same date as new T0 data
            # Convert data_mode again to same format just in case
            # time_mode = time_mode.strftime('%Y-%m-%d')
            print(f'csv out date_mode is {time_mode}')
            # df_to_merge['Data Date'] = df_to_merge['Data Date'].strftime('%Y-%m-%d')
            # filter out
            df_to_merge = df_to_merge[df_to_merge['Data Date'] != time_mode]
            print(f'{time_mode} in df_to_merge: {df_to_merge.isin([time_mode])}')
            # df_to_merge.info() # print out dataframe info; enable or disable as required
            # Concat new T0 data with aggregated data and sort
            df_out = pd.concat([df_in, df_to_merge])
            df_out.sort_values(by=['Data Date'], ascending=False, inplace=inplace)
            df_out.drop_duplicates(keep="last", inplace=inplace)
            # invoke csv out once all processing is completed
            PersonalPandas.csv_out(df_out, str(file_name), out_path)

        # If file doesn't exist, call excel_out for straight export (excel auto create file; file creation not needed)
        else:
            print("File doesn't exists; outputting new file")  # for debugging; enable or disable as required
            # Straight csv out
            PersonalPandas.csv_out(df_in, str(file_name), out_path)


class DeliveryMonitoring:
    @staticmethod
    def delivery_mon_process(df_input):
        # get first 10 characters of date column
        df_input['Date'] = df_input['Date'].str[0:10]
        # Lambda for column to datetime
        df_input['Date'] = df_input['Date'].apply(lambda x: pd.to_datetime(x))
        # Reassign
        df_final = df_input  # [Delivery_Mon_Header]
        # Test dtypes; enable or disable as required
        print(df_final.dtypes)

        return df_final

    @staticmethod
    def Delivery_Summary(df_in, date_mode):
        """Transform Delivery summary data to required path format"""
        # Copy dataframe
        delivery_sum_df_in = df_in.copy(deep=False)
        # Header selection
        delivery_sum_df_in = delivery_sum_df_in[Delivery_Summary_Header]
        # New 'Data Date' column set up
        delivery_sum_df_in["Data Date"] = date_mode
        # # Filter
        # delivery_sum_df_in = delivery_sum_df_in.dropna()

        return delivery_sum_df_in


class ArrivalMonitoring:
    @staticmethod
    def arrival_mon_process(df_input):
        # get first 10 characters of date column
        df_input['Date'] = df_input['Date'].str[0:10]
        # Lambda for column to datetime
        df_input['Date'] = df_input['Date'].apply(lambda x: pd.to_datetime(x))
        # Reassign
        df_final = df_input  # [Delivery_Mon_Header]
        # Test dtypes; enable or disable as required
        print(df_final.dtypes)

        return df_final

    @staticmethod
    def Arrival_Summary(df_in, date_mode):
        # Copy dataframe
        arrival_sum_df_in = df_in.copy(deep=False)
        # Header selection
        arrival_sum_df_in = arrival_sum_df_in[Arrival_Summary_Header]
        # New 'Data Date' column set up
        arrival_sum_df_in["Data Date"] = date_mode

        return arrival_sum_df_in


def data_out_csv(df_in, out_path, file_name, time_mode):
    """Output overnight data to path provided in CSV format

    Function include auto merging with existing CSV data (if present) or directly create new CSV file

    Due to no column selection required, process is simplified compare to postal data out csv function

    Parameters
    ----------
    df_in = New Pandas dataframe input
    out_path = Path to CSV output into
    file_name = The string to be used to rename file as
    test_path = Existing data file path; also serve as read path
    time_mode = datetime value to be compared and filter out in new data
    """

    # Test if path is present; refer to personal_file_manager for more information
    test_path = os.path.join(out_path, file_name + '.csv')
    file_path_test = PersonalFM.test_path(test_path)
    print("Data Out")

    if file_path_test:
        print('File exists, proceed to concat new data to aggregated data')  # enable / disable for debugging
        # load old file
        df_to_merge = pd.read_csv(str(test_path))  # date_format='%Y-%m-%d'
        # Convert to date
        # Final Option; directly remove aggregated data that has the same date as data to be merged
        # Filter entries that has the same date as new T0 data
        # Convert data_mode again to same format just in case
        # time_mode = time_mode.strftime('%Y-%m-%d')
        print(f'csv out date_mode is {time_mode}')
        # df_to_merge['Data Date'] = df_to_merge['Data Date'].strftime('%Y-%m-%d')
        # filter out
        df_to_merge = df_to_merge[df_to_merge['Data Date'] != time_mode]
        # df_to_merge.info() # print out dataframe info; enable or disable as required
        # Concat new T0 data with aggregated data and sort
        df_out = pd.concat([df_in, df_to_merge])
        df_out.sort_values(by=['Data Date'], ascending=False)
        # invoke csv out once all processing is completed
        PersonalPandas.csv_out(df_out, str(file_name), out_path)

    # If file doesn't exist, call excel_out for straight export (excel auto create file; file creation not needed)
    else:
        print("File doesn't exists; outputting new file")  # for debugging; enable or disable as required
        # Straight csv out
        PersonalPandas.csv_out(df_in, str(file_name), out_path)
