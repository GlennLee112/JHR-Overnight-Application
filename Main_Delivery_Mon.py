import Directory.File_Manager as File_Manager
from Directory.jnt_data import *
import sys


Delivery_Mon_Header = ['Date',
                       'DP No. | Delivery',
                       'Dispatcher ID',
                       'Volume | Delivery',
                       'Volume | Delivery Signature']


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
    delivery_mon_input_path = os.path.join(path, "Input", "Delivery Monitoring")
    output_path = os.path.join(path, "Output", "Delivery Monitoring")
    # Read Folder location
    delivery_mon_files = File_Manager.get_file_paths(delivery_mon_input_path)

    # 1. Read file
    for file_delivery in delivery_mon_files:
        print(file_delivery)
        # 1. read file
        try:
            # condition gate for file types
            if file_delivery.endswith(".csv"):
                print('is csv')
                df_in = pd.read_csv(file_delivery, date_format='%Y-%m-%d', low_memory=False)
            elif file_delivery.endswith(".xlsx"):
                print('is excel')
                df_in = pd.read_excel(file_delivery, date_format='%Y-%m-%d')

        except UnicodeDecodeError:
            print("Please make sure file is in csv 'UTF-8' format")
            break

        except pd.errors.EmptyDataError:
            print(file_delivery, " is empty")
            continue

        # 2. Preprocess
        delivery_mon_df = DeliveryMonitoring.delivery_mon_process(df_in)

        # date_mode = df_in['Date'].mode()
        # 3. Date
        date_use = PersonalPandas.date_max(delivery_mon_df, "Date")
        # reformat time
        delivery_date_full = date_use.strftime('%Y-%m-%d')
        delivery_date_year_month = date_use.strftime("%Y%m")
        delivery_date_year = date_use.strftime("%Y")

        print(delivery_date_full)
        print(type(delivery_date_full))

        # 4. Data transform
        # Final data to be used
        delivery_mon_sum_df = DeliveryMonitoring.Delivery_Summary(delivery_mon_df, delivery_date_full)

        # 4. Data output
        output_path_final = os.path.join(output_path, delivery_date_year)
        # Universal data_out_csv
        data_out_csv(delivery_mon_sum_df, output_path_final,
                     delivery_date_year_month, delivery_date_full)


if __name__ == "__main__":
    main()
