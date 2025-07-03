import streamlit as st
from app.ml_model import recommend_champions, get_mock_champion_data
import matplotlib.pyplot as plt
from collections import Counter
from app.api import get_champion_list, get_champion_details, get_personal_champion_stats

st.title('Draft Unlocked')
champions = get_champion_list()

#=== Summoner stats ===
st.header("🎯 Personal Champion Performance")
game_name = st.text_input("Enter your Riot Game Name (e.g. Doublelift)", "")
tag_line = st.text_input("Enter your Riot Tag Line (e.g. NA1)", "")

if game_name and tag_line:
    with st.spinner("Fetching match history..."):
        stats = get_personal_champion_stats(game_name, tag_line, count=20)

    if stats:
        st.subheader("Your Top Champions (20 games)")
        data = []
        for champ, record in stats.items():
            games = record["games"]
            wins = record["wins"]
            win_rate = f"{(wins / games) * 100:.1f}%"
            data.append((champ, games, wins, win_rate))

        data.sort(key=lambda x: (x[1], float(x[3].strip('%'))), reverse=True) # sort by games played > winrate

        st.table(
            {
                "Champion": [row[0] for row in data],
                "Games": [row[1] for row in data],
                "Win Rate": [row[3] for row in data],
            }
        )
    else:
        st.warning("No match data found or invalid Riot ID.")

#==== Champ Details ====
st.header("Champion Detail Viewer")

champion_names = [champ["name"] for champ in get_champion_list()]
selected_champ = st.selectbox("Select a Champion", champion_names)

if selected_champ:
    # Use champion ID (e.g., "Ahri") instead of name for API call
    champion_id = next(c["id"] for c in get_champion_list() if c["name"] == selected_champ)
    details = get_champion_details(champion_id)

    if details:
        st.subheader(details["name"])
        st.image(f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion_id}_0.jpg")

        # Passive
        passive = details["passive"]
        st.markdown(f"**Passive: {passive['name']}**")
        st.caption(passive["description"])

        # Spells (Q, W, E, R)
        spell_keys = ["Q", "W", "E", "R"]
        for key, spell in zip(spell_keys, details["spells"]):
            st.markdown(f"**{key}: {spell['name']}**")
            st.caption(spell["description"])

        # Tips
        if details["allytips"]:
            st.markdown("**Ally Tips:**")
            for tip in details["allytips"]:
                st.markdown(f"- {tip}")

        if details["enemytips"]:
            st.markdown("**Enemy Tips:**")
            for tip in details["enemytips"]:
                st.markdown(f"- {tip}")

        # Link to the official champion page
        st.markdown(f"[Official Champion Page](https://www.leagueoflegends.com/en-us/champions/{champion_id.lower()})")
    else:
        st.error("Failed to load champion details.")


# === Role Distribution Visualization ===
role_counts = Counter(role for champ in champions for role in champ["roles"])
if role_counts:
    roles, counts = zip(*role_counts.items())
    fig, ax = plt.subplots()
    ax.bar(roles, counts, color='skyblue')
    ax.set_title("Champion Role Distribution")
    st.pyplot(fig)

# === Champ Recommendation Section ===
st.header("Champion Recommender")
mock_df = get_mock_champion_data()
champ_names = mock_df["name"].tolist()
selected_champ = st.selectbox("Choose Your Main Champion", champ_names)

if selected_champ:
    recs = recommend_champions(selected_champ)
    st.subheader(f"If you like {selected_champ}, try these:")
    for champ in recs:
        st.markdown(f"- {champ}")

