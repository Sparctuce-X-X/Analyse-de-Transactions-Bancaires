# Analyse de Transactions Bancaires

Projet complet d'analyse de transactions bancaires, de la donnée brute au reporting, pensé pour montrer une démarche d'analyste / data analyst de bout en bout.

## 🎯 Objectifs du projet

- Partir d'un CSV brut de transactions bancaires.
- Nettoyer et structurer les données avec pandas (clients, comptes, transactions).
- Charger ces tables dans une base PostgreSQL via SQLAlchemy.
- Réaliser des analyses SQL (volumes, distributions, anomalies).
- Explorer et visualiser les données en Python (notebooks + scripts standalone).
- Documenter clairement la démarche pour un recruteur / manager data.

## 🧰 Stack & Outils

- **Langage :** Python (pandas, NumPy)
- **Base de données :** PostgreSQL
- **Connexion BD :** SQLAlchemy
- **Visualisation :** Matplotlib, Seaborn
- **Environnement :** Jupyter Notebooks + scripts Python

## 📁 Structure du projet

```bash
.
├── README.md
├── data/
│   └── raw/
│       └── Comprehensive_Banking_Database.csv
├── notebooks/
│   ├── 01_load_and_clean.ipynb
│   └── 02_analysis.ipynb
├── sql/
│   ├── 01_create_tables.sql
│   └── 02_analysis_queries.sql
├── Visualisation/
│   ├── Distribution_montant.py
│   ├── Évolution_mensuelle_transaction.py
│   ├── Repartition_type_transactions.py
│   └── scatter_plot.py
└── test/
    ├── analyse_cog.ipynb
    ├── cog_2023.csv
    ├── IGT - Pouvoir de réchauffement global.csv
    └── test.py
```

Les dossiers `test/` contiennent des fichiers de travail annexes sans lien direct avec l'analyse bancaire principale.

## 📊 Données & Modèle

Source : `data/raw/Comprehensive_Banking_Database.csv`

À partir de ce fichier brut, le notebook `01_load_and_clean.ipynb` construit trois tables propres :

### 1. `clients`

Table de clients dédupliqués.

- Nettoyage :
  - Suppression des doublons sur l'identifiant client.
  - Renommage et homogénéisation des noms de colonnes.

### 2. `accounts`

Table de comptes bancaires.

- Construction d'un identifiant de compte `account_id` (par ex. à partir du couple client / type de compte).
- Déduplication par couple (client, type de compte).
- Renommage des colonnes pour cohérence (snake_case).

### 3. `transactions`

Table de transactions nettoyée.

- Filtrage des lignes avec `TransactionID` manquant.
- Génération de `account_id` pour rattacher chaque transaction à un compte.
- Renommage des colonnes (par ex. `TransactionID` → `transaction_id`, `Date` → `transaction_date`, etc.).
- Sélection d'un schéma clair : `transaction_id`, `account_id`, `transaction_date`, `transaction_type`, `amount`, `balance_before`, `balance_after`, ...

## 🗄️ Intégration PostgreSQL

Connexion via SQLAlchemy :

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://analyst:password123@localhost:5432/bank_analytics"
)
```

Les DataFrames nettoyés sont chargés dans PostgreSQL :

- `clients_df` → table `clients`
- `accounts_df` → table `accounts`
- `transactions_df` → table `transactions`

En pratique, le chargement se fait avec `DataFrame.to_sql` (`if_exists='replace'` pour recréer la table ou `if_exists='append'` pour ajouter des données).

Un script SQL dédié (`sql/01_create_tables.sql`) peut formaliser le schéma (PK/FK, index) pour une utilisation plus avancée.

## 🔎 Analyses SQL (`sql/02_analysis_queries.sql`)

Le fichier `02_analysis_queries.sql` contient plusieurs requêtes illustrant une analyse typique :

1. **Volume de transactions par mois**
   - Utilisation de `date_trunc('month', transaction_date)` + `COUNT(*)`.
2. **Répartition des transactions par type**
   - `GROUP BY transaction_type`.
   - Calcul du **nombre** et du **pourcentage** via une fenêtre `SUM(COUNT(*)) OVER ()`.
3. **Solde moyen par type de compte**
   - `ROUND(AVG(account_balance), 2)` pour avoir un indicateur lisible par type de compte.
4. **Détection de transactions « anormales »**
   - Filtre sur des montants élevés (`amount > 3500`).
   - Possibilité de limiter aux transactions récentes :
     `transaction_date >= CURRENT_DATE - INTERVAL '30 days'`.

Ces requêtes montrent comment combiner **filtres**, **conditions sur les dates**, **montants** et **types de transaction** dans PostgreSQL.

## 📓 Notebooks d analyse

### `01_load_and_clean.ipynb`

- Chargement du CSV brut avec pandas.
- Nettoyage / structuration en trois DataFrames : `clients_df`, `accounts_df`, `transactions_df`.
- Préparation de la connexion PostgreSQL et logique de chargement.

### `02_analysis.ipynb`

- Chargement de la table `transactions` depuis PostgreSQL avec `pd.read_sql`.
- EDA de base :
  - `head()`, `shape`, `dtypes`, `isna().sum()`, `describe()`.
- Transformation de la date :
  - `df['transaction_date'] = pd.to_datetime(df['transaction_date'])`.
  - Création de variables dérivées : `year`, `month`, `day_of_week`, `hour`.
- Feature engineering :
  - `df['is_large_amount'] = np.where(df['amount'] > 3000, True, False)`.
- Agrégations :
  - Groupement par `['year', 'month']` pour compter les transactions mensuelles.
  - Construction d'une colonne `date` (année-mois) pour les courbes temporelles.
- Visualisation :
  - Courbe d'évolution mensuelle du nombre de transactions (Matplotlib) avec légendes, axes nommés, rotation des ticks, `plt.tight_layout()`.
- Comptage des transactions de gros montants (> 2000) par `transaction_type` via `groupby`.

Un deuxième notebook `02_analysis_visualization.ipynb` est centré sur les visualisations, avec une logique similaire.

## 📈 Scripts de visualisation (`Visualisation/`)

Ces scripts montrent comment passer d'une analyse notebook à des scripts réutilisables.

### `Distribution_montant.py`

- Chargement des transactions depuis PostgreSQL.
- Utilisation de Seaborn pour un **boxplot** :
  - `sns.boxplot(data=df, x="transaction_type", y="amount")`.
- Objectif : visualiser la **distribution des montants** par type de transaction (médiane, dispersion, outliers).

### `Évolution_mensuelle_transaction.py`

- Agrégation par année / mois du nombre de transactions.
- Courbe de tendance mensuelle avec Matplotlib.

### `Repartition_type_transactions.py`

- Comptage des transactions par type.
- Visualisation sous forme de barres ou de camembert.

### `scatter_plot.py`

- Représentation en nuage de points (**scatter plot**) :
  - Axe X : `amount` (montant de la transaction).
  - Axe Y : `balance_after` (solde après transaction).
  - Ajout de transparence (`alpha=0.5`) pour mieux voir les zones denses.
- Objectif : comprendre la relation entre **montant des transactions** et **niveau de solde après opération**.

## 📦 Installation & exécution

### 1. Cloner le dépôt

```bash
git clone <URL_DU_REPO>
cd "Analyse de transactions bancaires"
```

### 2. Créer l environnement Python

Avec `venv` par exemple :

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate  # Windows
```

Installer les dépendances principales (à adapter en fonction de votre environnement) :

```bash
pip install pandas numpy sqlalchemy psycopg2-binary matplotlib seaborn jupyter
```

(Un fichier `requirements.txt` pourra être ajouté pour figer les versions.)

### 3. Lancer PostgreSQL et créer la base

- Créer une base `bank_analytics`.
- Créer un utilisateur `analyst` avec le mot de passe `password123` (ou adapter la chaîne de connexion dans les notebooks et scripts).

### 4. Exécuter les notebooks

Lancer Jupyter :

```bash
jupyter notebook
```

Puis ouvrir dans l ordre :

1. `notebooks/01_load_and_clean.ipynb` pour générer et charger les tables.
2. `notebooks/02_analysis.ipynb` (et `02_analysis_visualization.ipynb`) pour l'analyse et les graphiques.

### 5. Exécuter les scripts de visualisation

Depuis la racine du projet (après activation de l'environnement) :

```bash
python Visualisation/Distribution_montant.py
python Visualisation/Évolution_mensuelle_transaction.py
python Visualisation/Repartition_type_transactions.py
python Visualisation/scatter_plot.py
```

Chaque script se connecte à PostgreSQL, charge les transactions et affiche le graphique correspondant (et/ou enregistre un fichier PNG dans `Visualisation/`).

## 🧠 Compétences mises en avant

- **Pandas / Python**
  - Chargement et nettoyage de données tabulaires.
  - Gestion des dates, filtres et agrégations (`groupby`, `reset_index`, `size`, `count`).
  - Feature engineering simple (variables booléennes, dérivées temporelles).
- **SQL / PostgreSQL**
  - Jointures conceptuelles entre clients / comptes / transactions.
  - Agrégations, filtres complexes, fonctions de fenêtre (pourcentages).
  - Requêtes pour la détection d'anomalies.
- **Visualisation de données**
  - Graphiques temporels (séries mensuelles).
  - Boxplots par catégorie, scatter plots.
  - Utilisation combinée de Matplotlib et Seaborn.
- **Architecture analytique de bout en bout**
  - Passage d'un fichier brut à une base relationnelle structurée.
  - Séparation claire entre préparation, stockage, analyse SQL, analyse Python et visualisation.

## 🔭 Améliorations possibles

- Ajouter un fichier `requirements.txt` complet avec les versions exactes.
- Formaliser le schéma PostgreSQL (PK/FK, index) dans `sql/01_create_tables.sql`.
- Développer des analyses avancées :
  - KPIs par client (activité, solde moyen, fréquence des transactions).
  - Indicateurs de type « churn » ou détection de comportements atypiques.
- Construire un petit dashboard (Streamlit / Dash / outil BI) connecté à PostgreSQL.
- Ajouter des tests automatisés / validations autour de la logique de nettoyage et de chargement.
