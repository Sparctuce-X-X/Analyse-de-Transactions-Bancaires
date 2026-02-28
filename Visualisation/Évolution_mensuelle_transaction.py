import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sqlalchemy import create_engine

engine = create_engine("postgresql://analyst:password123@localhost:5432/bank_analytics")

df = pd.read_sql('SELECT * FROM transactions', engine)


df['transaction_date'] = pd.to_datetime(df["transaction_date"])
df['year'] = df["transaction_date"].dt.year
df['month'] = df["transaction_date"].dt.month
df['day_of_week'] = df["transaction_date"].dt.day_of_week
df['hour'] = df["transaction_date"].dt.hour



df['is_large_amount'] = np.where(df["amount"] > 3000 , True , False)



transactions_par_année_et_mois = (
    df.groupby(["year" , "month"])["transaction_id"]
    .count()
    .reset_index(name="nb_transactions")
)



transactions_par_année_et_mois["date"] = pd.to_datetime(
    transactions_par_année_et_mois["year"].astype(str) + "-" +
    transactions_par_année_et_mois["month"].astype(str) + "-01"
)

plt.figure(figsize=(12, 6))
plt.plot(
    transactions_par_année_et_mois["date"],
    transactions_par_année_et_mois["nb_transactions"]
)

plt.title("Évolution du nombre de transactions par mois")
plt.xlabel("Date")
plt.ylabel("Nombre de transactions")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()  