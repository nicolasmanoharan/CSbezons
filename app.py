import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Gestion du Stock Médical d'un Centre de Secours")

# Initialisation du stock médical
if 'stock' not in st.session_state:
    st.session_state.stock = pd.DataFrame(columns=["article", 'Quantité', 'Description'])

# Fonction pour ajouter un article
def ajouter_article(nom, quantite, description):
    new_data = pd.DataFrame({"article": [nom], 'Quantité': [quantite], 'Description': [description]})
    st.session_state.stock = pd.concat([st.session_state.stock, new_data], ignore_index=True)

# Fonction pour mettre à jour un article
def mettre_a_jour_article(index, nom, quantite, description):
    st.session_state.stock.at[index, "article"] = nom
    st.session_state.stock.at[index, 'Quantité'] = quantite
    st.session_state.stock.at[index, 'Description'] = description

# Fonction pour supprimer un article
def supprimer_article(index):
    st.session_state.stock = st.session_state.stock.drop(index).reset_index(drop=True)

# Interface pour ajouter un article
st.subheader("Ajouter un nouvel article")
with st.form(key='add_article_form'):
    nom = st.text_input("article")
    quantite = st.number_input("Quantité", min_value=0, step=1)
    description = st.text_area("Description")
    submit_button = st.form_submit_button(label='Ajouter')

    if submit_button:
        ajouter_article(nom, quantite, description)
        st.success("Article ajouté avec succès")

# Interface pour afficher et gérer le stock actuel
st.subheader("Stock Actuel")
if not st.session_state.stock.empty:
    for i, row in st.session_state.stock.iterrows():
        with st.expander(f"{row['article']} (Quantité: {row['Quantité']})"):
            updated_nom = st.text_input("article", value=row["article"], key=f"nom_{i}")
            updated_quantite = st.number_input("Quantité", value=row['Quantité'], min_value=0, step=1, key=f"quantite_{i}")
            updated_description = st.text_area("Description", value=row['Description'], key=f"description_{i}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Mettre à jour", key=f"update_{i}"):
                    mettre_a_jour_article(i, updated_nom, updated_quantite, updated_description)
                    st.success("Article mis à jour avec succès")
            with col2:
                if st.button("Supprimer", key=f"delete_{i}"):
                    supprimer_article(i)
                    st.warning("Article supprimé avec succès")
else:
    st.info("Le stock est vide. Ajoutez des articles pour commencer.")

# Interface pour afficher les statistiques du stock
st.subheader("Statistiques du Stock")
if not st.session_state.stock.empty:
    total_articles = st.session_state.stock.shape[0]
    total_quantite = st.session_state.stock['Quantité'].sum()

    st.write(f"Nombre total d'articles: {total_articles}")
    st.write(f"Quantité totale d'articles: {total_quantite}")
else:
    st.write("Aucune donnée disponible.")
