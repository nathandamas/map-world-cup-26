import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FIFA World Cup 26 Map", layout="wide")

# 1. Mapeamentos e Dados
stages = ["Group Stage", "Round of 32", "Round of 16", "Quarter-finals", "Semi-finals", "Final"]
dates = ["27-06-2026", "03-07-2026", "07-07-2026", "11-07-2026", "15-07-2026", "19-07-2026"]

teams_elimination = {
    "SAU": 0, "QAT": 0, "KOR": 0, "CUW": 0, "HTI": 0, "IRN": 0, "IRQ": 0, "JOR": 0, "NZL": 0, "PAN": 0, "CZE": 0, "TUN": 0, "URY": 0, "UZB": 0, "SRB": 0, "ITA": 0,
    "ZAF": 1, "DEU": 1, "DZA": 1, "AUS": 1, "AUT": 1, "BIH": 1, "CPV": 1, "CIV": 1, "HRV": 1, "ECU": 1, "GHA": 1, "NLD": 1, "JPN": 1, "COD": 1, "SEN": 1, "SWE": 1,
    "BRA": 2, "CAN": 2, "COL": 2, "EGY": 2, "USA": 2, "MEX": 2, "PRY": 2, "PRT": 2, "MAR": 3, "BEL": 3,
    "FRA": 99, "ESP": 99, "NOR": 99, "GBR": 99, "ARG": 99, "CHE": 99
}

country_names = {
    "SAU": "Saudi Arabia", "QAT": "Qatar", "KOR": "South Korea", "CUW": "Curacao", "HTI": "Haiti", "IRN": "Iran", "IRQ": "Iraq", "JOR": "Jordan", "NZL": "New Zealand", "PAN": "Panama", "CZE": "Czechia", "TUN": "Tunisia", "URY": "Uruguay", "UZB": "Uzbekistan", "SRB": "Serbia", "ITA": "Italy", "ZAF": "South Africa", "DEU": "Germany", "DZA": "Algeria", "AUS": "Australia", "AUT": "Austria", "BIH": "Bosnia and Herzegovina", "CPV": "Cape Verde", "CIV": "Ivory Coast", "HRV": "Croatia", "ECU": "Ecuador", "GHA": "Ghana", "NLD": "Netherlands", "JPN": "Japan", "COD": "DR Congo", "SEN": "Senegal", "SWE": "Sweden", "BRA": "Brazil", "CAN": "Canada", "COL": "Colombia", "EGY": "Egypt", "USA": "United States", "MEX": "Mexico", "PRY": "Paraguay", "PRT": "Portugal", "MAR": "Morocco", "BEL": "Belgium", "FRA": "France", "ESP": "Spain", "NOR": "Norway", "GBR": "England", "ARG": "Argentina", "CHE": "Switzerland"
}

iso_map = {"SAU": "sa", "QAT": "qa", "KOR": "kr", "CUW": "cw", "HTI": "ht", "IRN": "ir", "IRQ": "iq", "JOR": "jo", "NZL": "nz", "PAN": "pa", "CZE": "cz", "TUN": "tn", "URY": "uy", "UZB": "uz", "SRB": "rs", "ITA": "it", "ZAF": "za", "DEU": "de", "DZA": "dz", "AUS": "au", "AUT": "at", "BIH": "ba", "CPV": "cv", "CIV": "ci", "HRV": "hr", "ECU": "ec", "GHA": "gh", "NLD": "nl", "JPN": "jp", "COD": "cd", "SEN": "sn", "SWE": "se", "BRA": "br", "CAN": "ca", "COL": "co", "EGY": "eg", "USA": "us", "MEX": "mx", "PRY": "py", "PRT": "pt", "MAR": "ma", "BEL": "be", "FRA": "fr", "ESP": "es", "NOR": "no", "GBR": "gb", "ARG": "ar", "CHE": "ch"}

match_details = {
    "MAR": {"match": "FRA 2 x 0 MAR", "date": "09-07-2026"}, "BEL": {"match": "ESP 2 x 1 BEL", "date": "10-07-2026"},
    "BRA": {"match": "NOR 2 x 1 BRA", "date": "05-07-2026"}, "CAN": {"match": "MAR 3 x 0 CAN", "date": "04-07-2026"},
    "COL": {"match": "CHE 0 (4) x (3) 0 COL", "date": "07-07-2026"}, "EGY": {"match": "ARG 3 x 2 EGY", "date": "07-07-2026"},
    "USA": {"match": "BEL 4 x 1 USA", "date": "06-07-2026"}, "MEX": {"match": "GBR 3 x 2 MEX", "date": "05-07-2026"},
    "PRY": {"match": "FRA 1 x 0 PRY", "date": "04-07-2026"}, "PRT": {"match": "ESP 1 x 0 PRT", "date": "06-07-2026"},
    "DZA": {"match": "CHE 2 x 0 DZA", "date": "02-07-2026"}, "AUS": {"match": "EGY 1 (4) x (2) 1 AUS", "date": "03-07-2026"},
    "CPV": {"match": "ARG 3 x 2 CPV", "date": "03-07-2026"}, "GHA": {"match": "COL 1 x 0 GHA", "date": "03-07-2026"}
}

# 2. Sidebar e Slider
st.sidebar.title("FIFA World Cup 26™")
stage_idx = st.sidebar.select_slider("Select Stage:", options=range(len(stages)), format_func=lambda x: stages[x])

st.sidebar.markdown(f"**Date:** {dates[stage_idx]}")
st.sidebar.markdown("---")
st.sidebar.subheader(f"Active Teams")

for code in sorted(teams_elimination.keys(), key=lambda k: country_names[k]):
    if stage_idx <= teams_elimination[code]:
        iso_code = iso_map.get(code, "xx")
        st.sidebar.markdown(f"![Flag](https://flagcdn.com/w20/{iso_code}.png) {country_names[code]}")

# 3. Preparação dos dados do Mapa (Merge de resultados)
data = [
    {"Country_Code": "AAA", "Country": "Active", "Status": "Active", "Match": "-", "Date": "-"},
    {"Country_Code": "BBB", "Country": "Eliminated", "Status": "Eliminated", "Match": "-", "Date": "-"},
    {"Country_Code": "CCC", "Country": "Not Qualified", "Status": "Not Qualified", "Match": "-", "Date": "-"}
]

for code, elim_index in teams_elimination.items():
    status = "Eliminated" if stage_idx > elim_index else "Active"
    # Busca detalhes se eliminado
    match_info = match_details.get(code, {}).get("match", "Eliminated by Points") if status == "Eliminated" else "-"
    match_date = match_details.get(code, {}).get("date", "-") if status == "Eliminated" else "-"
    
    data.append({
        "Country_Code": code, "Country": country_names.get(code, code), 
        "Status": status, "Match": match_info, "Date": match_date
    })

df = pd.DataFrame(data)

# 4. Mapa
fig = px.choropleth(
    df, locations="Country_Code", color="Status", hover_name="Country",
    color_discrete_map={"Active": "#00FF4D", "Eliminated": "#404040", "Not Qualified": "#525252"},
    category_orders={"Status": ["Active", "Eliminated", "Not Qualified"]},
    hover_data={"Status": True, "Match": True, "Date": True, "Country_Code": False},
    projection="natural earth"
)

# Atualiza Tooltip para mostrar os resultados
fig.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>Status: %{customdata[0]}<br>Match: %{customdata[1]}<br>Date: %{customdata[2]}<extra></extra>"
)

fig.update_layout(
    paper_bgcolor="#000000", plot_bgcolor="#000000", font_color="#FFFFFF",
    margin={"r":0,"t":20,"l":0,"b":0},
    legend=dict(x=0.08, y=0.5, bgcolor="rgba(0,0,0,0.6)", bordercolor="#FFFFFF", borderwidth=1.5),
    geo=dict(showland=True, landcolor="#525252", showocean=True, oceancolor="#0B132B", showlakes=True, lakecolor="#0B132B", bgcolor="#000000")
)

# 5. Header
col1, col2 = st.columns([1, 8])
with col1:
    st.image("https://raw.githubusercontent.com/nathandamas/map-world-cup-26/main/tournaments_fifa-world-cup-2026--white_700x700.football-logos.cc.png", width=80)
with col2:
    st.title(f"FIFA World Cup 26™ | {stages[stage_idx]}")

st.plotly_chart(fig, use_container_width=True)
