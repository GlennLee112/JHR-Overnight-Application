# JHR-Overnight-Application
JHR Overnight Application made with **Python**, utilizing Tkinter on the front end for UI element, with Pandas, **SQLAlchemy**, **Openpyxl** and other utilities providing backend data processing, aggregationg, storage, and data output. 'Main.py' is compiled into executable using Pyinstaller.

Lightweight Application used by J&T Johor region for (mainly) Overnight data processing and output. This is a shell app without any relevant data required for processing; demonstration of the application can be made upon request.

Disclaimer: with compliant to J&T Express (Malaysia) Sdn. Bhd. NDA aggrement, this app and any associate code are considered 'personal invention' and falls under personal (inventors) discretion to modify and repurpose if required.  

# Components
1. Main (Main_Tkinter.py)
   - Main application Containing the main Tkinter UI component of the application, application function by calling in sub 
2. Overnight subroutine (Main_Overnight.py (Pandas))
   - Subroutine for processing raw Overnight data, utilizing Pandas for transforming raw data into separate final output; AWB list is uploaded to database within 'Database' folder utilizing SQLAlchemy ORM, summarized data is appended automatically by year and month to the 'Ouput' Folder in csv. format (for reading speed and ease of accessbility)
3. Delivery and Arrival subroutine
   - Simple subroutine to aggregate Delivery and arrival data to respective folder 
