import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sqlalchemy import create_engine

engine = create_engine("postgresql://analyst:password123@localhost:5432/bank_analytics")

df = pd.read_sql('SELECT * FROM transactions', engine)

transactions_par_type = (
    df.groupby(["transaction_type"])["transaction_id"]
    .count()
    .reset_index(name="nb_transactions")
)

transactions_par_type = transactions_par_type.sort_values("nb_transactions", ascending=False)

plt.figure(figsize=(8, 5))
plt.plot(
    transactions_par_type["transaction_type"],
    transactions_par_type["nb_transactions"]
)

plt.title("Évolution du nombre de transactions par type")
plt.xlabel("Types")
plt.ylabel("Nombre de transactions")
plt.tight_layout()

plt.show()  

