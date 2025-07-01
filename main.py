import streamlit as st
from app.api import get_champion_list
from app.ml_model import recommend_champions, get_mock_champion_data
import matplotlib.pyplot as plt
from collections import Counter

st.title('LoL Champion Insights Dashboard')

# === Champion Filtering Section ===
champions = get_champion_list()
roles = ["All", "Fighter", "Mage", "Tank", "Assassin", "Marksman", "Support"]
selected_role = st.selectbox("Filter by Role", roles)

# Filter champions based on selected role
if champions:
    if selected_role != "All":
        champions = [champ for champ in champions if selected_role in champ["roles"]]

    st.subheader(f"Champions Matching Filter ({len(champions)})")
    for champ in champions:
        st.text(f"{champ['name']} ({', '.join(champ['roles'])})")
else:
    st.error("Could not load champion data.")

# === Role Distribution Visualization ===
role_counts = Counter(role for champ in champions for role in champ["roles"])
if role_counts:
    roles, counts = zip(*role_counts.items())
    fig, ax = plt.subplots()
    ax.bar(roles, counts, color='skyblue')
    ax.set_title("Champion Role Distribution")
    st.pyplot(fig)

# === Champion Recommendation Section ===
st.header("Champion Recommender")
mock_df = get_mock_champion_data()
champ_names = mock_df["name"].tolist()
selected_champ = st.selectbox("Choose Your Main Champion", champ_names)

if selected_champ:
    recs = recommend_champions(selected_champ)
    st.subheader(f"If you like {selected_champ}, try these:")
    for champ in recs:
        st.markdown(f"- {champ}")
