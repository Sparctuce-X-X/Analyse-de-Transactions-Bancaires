import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://analyst:password123@localhost:5432/bank_analytics")

csv_path = "../data/raw/Comprehensive_Banking_Database.csv"

df = pd.read_csv(csv_path)

print(df.groupby("Customer ID")["TransactionID"].nunique().sort_values(ascending=False).head(10)
)