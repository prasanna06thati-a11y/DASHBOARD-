import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="IPL AI Dashboard",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 IPL AI Dashboard (2008 - 2022)")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("IPL_Matches_2008_2022.csv")
    df.columns = df.columns.str.lower()
    return df

df = load_data()

st.success("Dataset Loaded Successfully ✅")

# ----------------------------
# DATASET OVERVIEW
# ----------------------------
st.header("📊 Dataset Overview")

st.dataframe(df.head())

col1, col2 = st.columns(2)

with col1:
    st.write("Rows:", df.shape[0])

with col2:
    st.write("Columns:", df.shape[1])

# ----------------------------
# MISSING VALUES
# ----------------------------
st.header("🧹 Missing Values Analysis")

missing = df.isnull().sum()
st.dataframe(missing[missing > 0])

# ----------------------------
# KPI SECTION
# ----------------------------
st.header("📌 Key Metrics")

total_matches = len(df)

total_teams = pd.concat([
    df["team1"],
    df["team2"]
]).nunique()

total_cities = df["city"].nunique()

total_venues = df["venue"].nunique()

k1, k2, k3, k4 = st.columns(4)

k1.metric("Matches", total_matches)
k2.metric("Teams", total_teams)
k3.metric("Cities", total_cities)
k4.metric("Venues", total_venues)

# ----------------------------
# SIDEBAR FILTER
# ----------------------------
st.sidebar.header("🔍 Filters")

season_list = sorted(df["season"].unique())

selected_season = st.sidebar.selectbox(
    "Select Season",
    season_list
)

filtered_df = df[df["season"] == selected_season]

st.header(f"🏆 Season {selected_season}")

st.dataframe(filtered_df)

# ----------------------------
# VISUALIZATION 1
# ----------------------------
st.header("📈 Matches Per Season")

matches_per_season = (
    df.groupby("season")
      .size()
      .reset_index(name="matches")
)

fig1 = px.bar(
    matches_per_season,
    x="season",
    y="matches",
    title="IPL Matches Per Season"
)

st.plotly_chart(fig1, use_container_width=True)

# ----------------------------
# VISUALIZATION 2
# ----------------------------
st.header("🪙 Toss Decisions")

fig2 = px.pie(
    df,
    names="tossdecision",
    title="Bat vs Field Decision"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------
# VISUALIZATION 3
# ----------------------------
st.header("🏆 Top Winning Teams")

winner_df = (
    df["winningteam"]
    .value_counts()
    .reset_index()
)

winner_df.columns = ["Team", "Wins"]

fig3 = px.bar(
    winner_df.head(10),
    x="Team",
    y="Wins",
    title="Top 10 Winning Teams"
)

st.plotly_chart(fig3, use_container_width=True)

# ----------------------------
# VISUALIZATION 4
# ----------------------------
st.header("🌍 Matches By City")

city_df = (
    df["city"]
    .value_counts()
    .reset_index()
)

city_df.columns = ["City", "Matches"]

fig4 = px.bar(
    city_df.head(10),
    x="City",
    y="Matches",
    title="Top Cities Hosting IPL Matches"
)

st.plotly_chart(fig4, use_container_width=True)

# ----------------------------
# VISUALIZATION 5
# ----------------------------
st.header("⭐ Player of the Match Leaders")

pom_df = (
    df["player_of_match"]
    .value_counts()
    .reset_index()
)

pom_df.columns = ["Player", "Awards"]

fig5 = px.bar(
    pom_df.head(10),
    x="Player",
    y="Awards",
    title="Most Player of the Match Awards"
)

st.plotly_chart(fig5, use_container_width=True)

# ----------------------------
# INSIGHTS
# ----------------------------
st.header("💡 Key Insights")

top_team = df["winningteam"].value_counts().idxmax()
top_player = df["player_of_match"].value_counts().idxmax()
top_city = df["city"].value_counts().idxmax()

st.info(f"""
🏆 Most Successful Team: **{top_team}**

⭐ Most Player of the Match Awards: **{top_player}**

🌍 City Hosting Most Matches: **{top_city}**

📈 Dataset covers IPL seasons from **2008 to 2022**
""")

# ----------------------------
# CONCLUSION
# ----------------------------
st.header("📋 Conclusion")

st.write("""
This dashboard analyzes IPL matches from 2008–2022.

Key findings:

- Multiple seasons of IPL data analyzed.
- Winning trends identified.
- Toss decisions explored.
- Top teams and players highlighted.
- Match distribution across cities visualized.

The dashboard provides a quick overview of IPL performance trends and team success over time.
""")