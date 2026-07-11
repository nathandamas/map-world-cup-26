"""
FIFA World Cup 2026 Interactive Journey Map
Streamlit Web Application
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Setup
st.set_page_config(page_title="FIFA World Cup 26 Map", layout="wide")

# Logo and Title
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("https://raw.githubusercontent.com/nathandamas/map-world-cup-26/main/tournaments_fifa-world-cup-2026--white_700x700.football-logos.cc.png", width=100)
with col_title:
    st.title("FIFA World Cup 26™ | WE ARE 26")

# 2. Data Mappings
stages = ["1. Group Stage<br>27-06-2026", "2. Round of 32<br>03-07-2026", "3. Round of 16<br>07-07-2026", "4. Quarter-finals<br>11-07-2026", "5. Semi-finals<br>15-07-2026", "6. Final<br>19-07-2026"]

teams_elimination = {
    "SAU": 0, "QAT": 0, "KOR": 0, "CUW": 0, "HTI": 0, "IRN": 0, "IRQ": 0, "JOR": 0, "NZL": 0, "PAN": 0, "CZE": 0, "TUN": 0, "URY": 0, "UZB": 0, "SRB": 0, "ITA": 0,
    "ZAF": 1, "DEU": 1, "DZA": 1, "AUS": 1, "AUT": 1, "BIH": 1, "CPV": 1, "CIV": 1, "HRV": 1, "ECU": 1, "GHA": 1, "NLD": 1, "JPN": 1, "COD": 1, "SEN": 1, "SWE": 1,
    "BRA": 2, "CAN": 2, "COL": 2, "EGY": 2, "USA": 2, "MEX": 2, "PRY": 2, "PRT": 2, "MAR": 3, "BEL": 3,
    "FRA": 99, "ESP": 99, "NOR": 99, "GBR": 99, "ARG": 99, "CHE": 99
}

country_names = {
    "SAU": "Saudi Arabia", "QAT": "Qatar", "KOR": "South Korea", "CUW": "Curacao", "HTI": "Haiti", "IRN": "Iran", "IRQ": "Iraq", "JOR": "Jordan", "NZL": "New Zealand", "PAN": "Panama", "CZE": "Czechia", "TUN": "Tunisia", "URY": "Uruguay", "UZB": "Uzbekistan", "SRB": "Serbia", "ITA": "Italy", "ZAF": "South Africa", "DEU": "Germany", "DZA": "Algeria", "AUS": "Australia", "AUT": "Austria", "BIH": "Bosnia and Herzegovina", "CPV": "Cape Verde", "CIV": "Ivory Coast", "HRV": "Croatia", "ECU": "Ecuador", "GHA": "Ghana", "NLD": "Netherlands", "JPN": "Japan", "COD": "DR Congo", "SEN": "Senegal", "SWE": "Sweden", "BRA": "Brazil", "CAN": "Canada", "COL": "Colombia", "EGY": "Egypt", "USA": "United States", "MEX": "Mexico", "PRY": "Paraguay", "PRT": "Portugal", "MAR": "Morocco", "BEL": "Belgium", "FRA": "France", "ESP": "Spain", "NOR": "Norway", "GBR": "England", "ARG": "Argentina", "CHE": "Switzerland"
}

flags = {
    "SAU": "🇸🇦", "QAT": "🇶🇦", "KOR": "🇰🇷", "CUW": "🇨🇼", "HTI": "🇭🇹", "IRN": "🇮🇷", "IRQ": "🇮🇶", "JOR": "🇯🇴", "NZL": "🇳🇿", "PAN": "🇵🇦", "CZE": "🇨🇿", "TUN": "🇹🇳", "URY": "🇺🇾", "UZB": "🇺🇿", "SRB": "🇷🇸", "ITA": "🇮🇹", "ZAF": "🇿🇦", "DEU": "🇩🇪", "DZA": "🇩🇿", "AUS": "🇦🇺", "AUT": "🇦🇹", "BIH": "🇧🇦", "CPV": "🇨🇻", "CIV": "🇨🇮", "HRV": "🇭🇷", "ECU": "🇪🇨", "GHA": "🇬🇭", "NLD": "🇳🇱", "JPN": "🇯🇵", "COD": "🇨🇩", "SEN": "🇸🇳", "SWE": "🇸🇪", "BRA": "🇧🇷", "CAN": "🇨🇦", "COL": "🇨🇴", "EGY": "🇪🇬", "USA": "🇺🇸", "MEX": "🇲🇽", "PRY": "🇵🇾", "PRT": "🇵🇹", "MAR": "🇲🇦", "BEL": "🇧🇪", "FRA": "🇫🇷", "ESP": "🇪🇸", "NOR": "🇳🇴", "GBR": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "ARG": "🇦🇷", "CHE": "🇨🇭"
}

match_details = {
    "MAR": {"match": "FRA 2 x 0 MAR", "date": "09-07-2026"}, "BEL": {"match": "ESP 2 x 1 BEL", "date": "10-07-2026"},
    "BRA": {"match": "NOR 2 x 1 BRA", "date": "05-07-2026"}, "CAN": {"match": "MAR 3 x 0 CAN", "date": "04-07-2026"},
    "COL": {"match": "CHE 0 (4) x (3) 0 COL", "date": "07-07-2026"}, "EGY": {"match": "ARG 3 x 2 EGY", "date": "07-07-2026"},
    "USA": {"match": "BEL 4 x 1 USA", "date": "06-07-2026"}, "MEX": {"match": "GBR 3 x 2 MEX", "date": "05-07-2026"},
    "PRY": {"match": "FRA 1 x 0 PRY", "date": "04-07-2026"}, "PRT": {"match": "ESP 1 x 0 PRT", "date": "06-07-2026"},
    "DZA": {"match": "CHE 2 x 0 DZA", "date": "02-07-2026"}, "AUS": {"match": "EGY 1 (4) x (2) 1 AUS", "date": "03-07-2026"},
    "CPV": {"match": "ARG 3 x 2 CPV", "date": "03-07-2026"}, "GHA": {"match": "COL 1 x 0 GHA", "date": "03-07-2026"}
}

# 3. Data Construction
data = []
for i, stage in enumerate(stages):
    for code, elim_index in teams_elimination.items():
        status = "Eliminated" if i > elim_index else "Active"
        match_info = match_details.get(code, {}).get("match", "-") if status == "Eliminated" else "-"
        match_date = match_details.get(code, {}).get("date", "-") if status == "Eliminated" else "-"
        data.append({"Country_Code": code, "Country": country_names.get(code, code), "Stage": stage, "Status": status, "Match": match_info, "Date": match_date})
    data.append({"Country_Code": "YYY", "Country": "Not Qualified", "Stage": stage, "Status": "Not Qualified", "Match": "-", "Date": "-"})

df = pd.DataFrame(data)

# 4. Map Generation
fig = px.choropleth(
    df, locations="Country_Code", color="Status", hover_name="Country",
    animation_frame="Stage",
    color_discrete_map={"Active": "#00FF4D", "Eliminated": "#1A1A1A", "Not Qualified": "#525252"},
    projection="natural earth"
)

fig.update_layout(
    paper_bgcolor="#000000", plot_bgcolor="#000000", font_color="#FFFFFF",
    margin={"r":0,"t":0,"l":0,"b":0},
    geo=dict(showland=True, landcolor="#525252", showocean=True, oceancolor="#0B132B", showlakes=True, lakecolor="#0B132B")
)

# Display Map
st.plotly_chart(fig, use_container_width=True)

# 5. Sidebar Logic (Active Teams)
st.sidebar.title("Active Teams")
# Simplesmente exibimos a lista de times ativos filtrando pelo dataframe
# No Streamlit, você pode adicionar um slider para filtrar o mapa ou apenas mostrar a lista fixa
st.sidebar.markdown("Teams remaining in the tournament.")
