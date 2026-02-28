import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sqlalchemy import create_engine

engine = create_engine("postgresql://analyst:password123@localhost:5432/bank_analytics")

df = pd.read_sql('SELECT * FROM transactions', engine)

plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df,
    x="transaction_type",   # catégories en X
    y="amount"              # montants en Y
)

plt.title("Distribution des montants par type de transaction")
plt.xlabel("Type de transaction")
plt.ylabel("Montant")
plt.xticks(rotation=30)
plt.tight_layout()

plt.show()


