import Directory.File_Manager as File_Manager
from Directory.jnt_data import *
import sys


def main():
    # 0. Path creation

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

    path = get_base_path()
    delivery_mon_input_path = os.path.join(path, "Input", "Arrival Monitoring")
    output_path = os.path.join(path, "Output", "Arrival Monitoring")
    # Read Folder location
    arrival_mon_files = File_Manager.get_file_paths(delivery_mon_input_path)

    # 1. Read file
    for file_arrival in arrival_mon_files:
        print(file_arrival)
        # 1. read file
        try:
            # condition gate for file types
            if file_arrival.endswith(".csv"):
                print('is csv')
                df_in = pd.read_csv(file_arrival, date_format='%Y-%m-%d', low_memory=False)
            elif file_arrival.endswith(".xlsx"):
                print('is excel')
                df_in = pd.read_excel(file_arrival, date_format='%Y-%m-%d', engine="openpyxl")

        except UnicodeDecodeError:
            print("Please make sure file is in csv 'UTF-8' format")
            break

        except pd.errors.EmptyDataError:
            print(file_arrival, " is empty")

        # 2. Preprocess
        arrival_mon_df = ArrivalMonitoring.arrival_mon_process(df_in)

        # date_mode = df_in['Date'].mode()
        # 3. Date
        date_use = PersonalPandas.date_max(arrival_mon_df, "Date")
        # reformat time
        arrival_date_full = date_use.strftime('%Y-%m-%d')
        arrival_date_year = date_use.strftime('%Y')
        arrival_date_year_month = date_use.strftime("%Y%m")

        print(arrival_date_full)
        print(type(arrival_date_full))

        # 4. Data transform
        # Final data to be used
        arrival_mon_sum_df = ArrivalMonitoring.Arrival_Summary(arrival_mon_df, arrival_date_full)

        # 5. Data output
        output_path_final = os.path.join(path, "Output", "Arrival Monitoring", arrival_date_year)
        # Universal data_out_csv
        data_out_csv(arrival_mon_sum_df, output_path_final,
                     arrival_date_year_month+" Arrival Mon", arrival_date_full)


if __name__ == "__main__":
    main()
