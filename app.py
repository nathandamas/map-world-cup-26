import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FIFA World Cup 26 Map", layout="wide")

# 1. Configurações e Mapeamentos
stages = ["1. Group Stage<br>27-06-2026", "2. Round of 32<br>03-07-2026", "3. Round of 16<br>07-07-2026", "4. Quarter-finals<br>11-07-2026", "5. Semi-finals<br>15-07-2026", "6. Final<br>19-07-2026"]

iso_map = {
    "SAU": "sa", "QAT": "qa", "KOR": "kr", "CUW": "cw", "HTI": "ht", "IRN": "ir", "IRQ": "iq", "JOR": "jo", "NZL": "nz", "PAN": "pa", "CZE": "cz", "TUN": "tn", "URY": "uy", "UZB": "uz", "SRB": "rs", "ITA": "it", "ZAF": "za", "DEU": "de", "DZA": "dz", "AUS": "au", "AUT": "at", "BIH": "ba", "CPV": "cv", "CIV": "ci", "HRV": "hr", "ECU": "ec", "GHA": "gh", "NLD": "nl", "JPN": "jp", "COD": "cd", "SEN": "sn", "SWE": "se", "BRA": "br", "CAN": "ca", "COL": "co", "EGY": "eg", "USA": "us", "MEX": "mx", "PRY": "py", "PRT": "pt", "MAR": "ma", "BEL": "be", "FRA": "fr", "ESP": "es", "NOR": "no", "GBR": "gb", "ARG": "ar", "CHE": "ch"
}

teams_elimination = {
    "SAU": 0, "QAT": 0, "KOR": 0, "CUW": 0, "HTI": 0, "IRN": 0, "IRQ": 0, "JOR": 0, "NZL": 0, "PAN": 0, "CZE": 0, "TUN": 0, "URY": 0, "UZB": 0, "SRB": 0, "ITA": 0,
    "ZAF": 1, "DEU": 1, "DZA": 1, "AUS": 1, "AUT": 1, "BIH": 1, "CPV": 1, "CIV": 1, "HRV": 1, "ECU": 1, "GHA": 1, "NLD": 1, "JPN": 1, "COD": 1, "SEN": 1, "SWE": 1,
    "BRA": 2, "CAN": 2, "COL": 2, "EGY": 2, "USA": 2, "MEX": 2, "PRY": 2, "PRT": 2, "MAR": 3, "BEL": 3,
    "FRA": 99, "ESP": 99, "NOR": 99, "GBR": 99, "ARG": 99, "CHE": 99
}

country_names = {
    "SAU": "Saudi Arabia", "QAT": "Qatar", "KOR": "South Korea", "CUW": "Curacao", "HTI": "Haiti", "IRN": "Iran", "IRQ": "Iraq", "JOR": "Jordan", "NZL": "New Zealand", "PAN": "Panama", "CZE": "Czechia", "TUN": "Tunisia", "URY": "Uruguay", "UZB": "Uzbekistan", "SRB": "Serbia", "ITA": "Italy", "ZAF": "South Africa", "DEU": "Germany", "DZA": "Algeria", "AUS": "Australia", "AUT": "Austria", "BIH": "Bosnia and Herzegovina", "CPV": "Cape Verde", "CIV": "Ivory Coast", "HRV": "Croatia", "ECU": "Ecuador", "GHA": "Ghana", "NLD": "Netherlands", "JPN": "Japan", "COD": "DR Congo", "SEN": "Senegal", "SWE": "Sweden", "BRA": "Brazil", "CAN": "Canada", "COL": "Colombia", "EGY": "Egypt", "USA": "United States", "MEX": "Mexico", "PRY": "Paraguay", "PRT": "Portugal", "MAR": "Morocco", "BEL": "Belgium", "FRA": "France", "ESP": "Spain", "NOR": "Norway", "GBR": "England", "ARG": "Argentina", "CHE": "Switzerland"
}

# 2. Dados com "Dummy Points" para forçar a legenda a ficar fixa
data = []
for stage in stages:
    # Adicionamos os 3 pontos "invisíveis" em cada estágio para forçar a legenda
    data.extend([
        {"Country_Code": "AAA", "Country": "Active", "Status": "Active", "Stage": stage},
        {"Country_Code": "BBB", "Country": "Eliminated", "Status": "Eliminated", "Stage": stage},
        {"Country_Code": "CCC", "Country": "Not Qualified", "Status": "Not Qualified", "Stage": stage}
    ])
    for code, elim_index in teams_elimination.items():
        status = "Eliminated" if stages.index(stage) > elim_index else "Active"
        data.append({"Country_Code": code, "Country": country_names.get(code, code), "Status": status, "Stage": stage})

df = pd.DataFrame(data)

# 3. Mapa com Animação Nativa
fig = px.choropleth(
    df, locations="Country_Code", color="Status", hover_name="Country",
    animation_frame="Stage",
    color_discrete_map={"Active": "#00FF4D", "Eliminated": "#1A1A1A", "Not Qualified": "#525252"},
    category_orders={"Status": ["Active", "Eliminated", "Not Qualified"]},
    projection="natural earth"
)

# 4. Ajustes de Layout (A "Mágica" para legenda e slider)
fig.update_layout(
    paper_bgcolor="#000000", plot_bgcolor="#000000", font_color="#FFFFFF",
    margin={"r":0,"t":50,"l":0,"b":0},
    # Posição da legenda: x=0.05 (mais à esquerda), y=0.5 (centro vertical)
    legend=dict(x=0.02, y=0.5, bgcolor="rgba(0,0,0,0.5)", bordercolor="#333", borderwidth=1),
    geo=dict(
        showland=True, landcolor="#525252", 
        showocean=True, oceancolor="#0B132B", 
        showlakes=True, lakecolor="#0B132B", bgcolor="#000000"
    )
)

# 5. Interface Streamlit
col1, col2 = st.columns([1, 8])
with col1:
    st.image("https://raw.githubusercontent.com/nathandamas/map-world-cup-26/main/tournaments_fifa-world-cup-2026--white_700x700.football-logos.cc.png", width=80)
with col2:
    st.title("FIFA World Cup 26™ | WE ARE 26")

# Renderiza o gráfico
st.plotly_chart(fig, use_container_width=True)

# Lista de times na Sidebar (opcional, mas bom para contexto)
st.sidebar.title("Active Teams")
st.sidebar.markdown("Use the map slider below to filter by stage.")
