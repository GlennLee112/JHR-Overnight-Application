# JHR-Overnight-Application
JHR Overnight Application made with **Python**, utilizing Tkinter on the front end for UI elements, with Pandas, **SQLAlchemy**, **Openpyxl**, and other utilities providing backend data processing, aggregating, storage, and data output. 'Main.py' is compiled into a UI executable with Pyinstaller.

Lightweight Application used by J&T Johor region for automated Overnight data processing and output. The main objective and outcome of the application is to streamline the data process and improve work efficiency.

Disclaimer: with compliance to J&T Express (Malaysia) Sdn. Bhd. NDA agreement, this app, and any associate code are considered 'personal invention' and fall under personal (inventor's) discretion to modify and repurpose if required.  

# Components
1. Main (Main_Tkinter.py)
   - Main application Containing the main Tkinter UI component of the application, application function by calling in a subroutine to execute functions as required
2. Overnight subroutine (Main_Overnight.py)
   - Subroutine for processing raw Overnight data, utilizing Pandas for transforming raw data into separate final output; AWB list is uploaded to the database within the 'Database' folder utilizing SQLAlchemy ORM, summarized data is appended automatically by year and month to the 'Output' Folder in csv format (for reading speed and ease of accessbility)
3. Delivery and Arrival subroutine (Main_Delivery.py & Main_Arrival.py)
   - Simple subroutine to aggregate Delivery and Arrival data to the respective folder

# Objectives
- Improve data cleaning and processing time and minimize errors from the process, improving data quality and accuracy

# Result
- Reduction of error rate to 0% (data integrity tested by comparing past data to assess data accuracy)
- Greatly reduced processing time and final output data size (estimated 15 minutes for the entire data workflow; reduced file size from approximately 50 MB range to 7 MB range by replacing the previous file with heavy reliance on Excel calculation to trim down the file).
- Enabled aggregated data viewing.
- Allowed future implementation of different data output types from data processing.

# Impact
- Allowed detailed overview of monthly overnight trends, vastly improving data insight into the region's overnight status (data used in conjunction with Power BI).
- Reduced file size vastly improved frontline personnel's accessibility to overnight data, which was previously a main grievance of frontline personnel regarding overnight data.
