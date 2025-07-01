from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def get_mock_champion_data():
    """
    Returns a mock dataset of champions and their roles.
    This would later be replaced with real stat-based feature vectors.
    """
    return pd.DataFrame([
        {"name": "Aatrox", "roles": ["Fighter", "Tank"]},
        {"name": "Ahri", "roles": ["Mage", "Assassin"]},
        {"name": "Alistar", "roles": ["Tank", "Support"]},
        {"name": "Annie", "roles": ["Mage"]},
        {"name": "Ashe", "roles": ["Marksman", "Support"]},
        {"name": "Amumu", "roles": ["Tank", "Mage"]},
        {"name": "Master Yi", "roles": ["Assassin", "Fighter"]},
        {"name": "Soraka", "roles": ["Support", "Mage"]},
        {"name": "Garen", "roles": ["Fighter", "Tank"]},
        {"name": "Lux", "roles": ["Mage", "Support"]}
    ])

def recommend_champions(champ_name, top_n=3):
    """
    Recommend similar champions based on shared roles using cosine similarity.
    """
    df = get_mock_champion_data()
    mlb = MultiLabelBinarizer()
    role_matrix = mlb.fit_transform(df["roles"])
    similarity_matrix = cosine_similarity(role_matrix)

    idx = df[df["name"] == champ_name].index[0]
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    recommendations = [df.iloc[i]["name"] for i, score in sim_scores[1:top_n+1]]
    return recommendations
