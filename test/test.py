import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

url = "https://www.insee.fr/fr/statistiques/fichier/6800675/v_commune_2023.csv"
url_backup = "https://minio.lab.sspcloud.fr/lgaliana/data/python-ENSAE/cog_2023.csv"

df = pd.read_csv('cog_2023.csv');

