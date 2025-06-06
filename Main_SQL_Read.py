import os
import pandas as pd
import Directory.jnt_SQL as jnt_sql
from Directory.Personal_SQL import sql_alchemy as p_sql_al
from sqlalchemy.ext.automap import automap_base

# def main():
# 0. File path
# Base
path = os.path.dirname(__file__)
# Input path
Input_path = os.path.join(path, "Input", "SQL")
# Output/Database path
database_path = os.path.join(path, "Database", "test.db")

# Engine
# engine = p_sql_al.engine_creation(database_path)
#
# # automap_base
# Base = automap_base()
# Base.prepare(engine)

# with engine.connect() as conn:
#     # df_out = pd.read_sql_table('overnight_awb', conn)
#     result = jnt_sql.overnight_awb_read('2025-05-06', database_path)

result = jnt_sql.overnight_awb_read('2025-05-08', database_path)
print(result)

# print(df_out.columns)
# print(len(df_out))
# print(df_out["Data_Date"].unique())

# result.to_csv("overnight_awb_extract.csv", index=False)
