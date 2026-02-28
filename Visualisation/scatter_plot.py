import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sqlalchemy import create_engine

engine = create_engine("postgresql://analyst:password123@localhost:5432/bank_analytics")

df = pd.read_sql('SELECT * FROM transactions', engine)

nb_par_type = (
    df[df["amount"] > 2000]
      .groupby("transaction_type")["transaction_id"]
      .count()
      .reset_index(name="nb_transactions")
)

# Scatter plot : montant vs solde après transaction
plt.figure(figsize=(8, 5))
plt.scatter(
    df["amount"],          # axe X
    df["balance_after"],   # axe Y
    alpha=0.5              # transparence pour mieux voir les points
)

plt.title("Montant vs solde après transaction")
plt.xlabel("Montant de la transaction")
plt.ylabel("Solde après transaction")
plt.tight_layout()
plt.show()