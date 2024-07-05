import streamlit as st
import pandas as pd
from PIL import Image

# Charger les données à partir des fichiers CSV
personnel_df = pd.read_csv('data/personnel.csv')
medicale_df = pd.read_csv('data/medicale.csv')
stock_df = pd.read_csv('data/stock.csv')

# Interface utilisateur Streamlit
st.set_page_config(page_title="Gestion des Articles Médicaux - Centre de Secours", page_icon=":ambulance:", layout="wide")

# Charger le logo depuis le dossier images
logo = Image.open('image/images.jpeg')

# Afficher le logo dans l'interface
st.image(logo, width=200)

# Sélectionner le nom et prénom à partir du fichier personnel.csv
st.header("Sélectionner Personnel")
nom_prenom = st.selectbox("Nom Prénom", personnel_df['nom_prenom'].tolist())

# Entrer le numéro d'intervention
st.header("Numéro d'intervention")
num_intervention = st.text_input("Numéro d'intervention")

# Sélectionner un article médical à partir du fichier medicale.csv
st.header("Sélectionner Article Médical")
article = st.selectbox("Article Médical", medicale_df['article'].tolist())

# Entrer le nombre d'articles à déduire
st.header("Quantité à déduire")
quantite = st.number_input("Quantité", min_value=1, step=1)

# Bouton pour mettre à jour le stock
if st.button("Mettre à jour le stock"):
    # Vérifier si l'article est dans le stock
    if article in stock_df['article'].values:
        # Déduire la quantité de l'article
        stock_df.loc[stock_df['article'] == article, 'quantite'] -= quantite
        # S'assurer que la quantité ne soit pas négative
        stock_df.loc[stock_df['quantite'] < 0, 'quantite'] = 0
        # Sauvegarder les modifications dans le fichier stock.csv
        stock_df.to_csv('stock.csv', index=False)
        st.success(f"{quantite} de {article} déduit du stock.")
    else:
        st.error("L'article sélectionné n'est pas dans le stock.")

# Afficher le stock actuel
st.header("Stock Actuel")
st.dataframe(stock_df)
