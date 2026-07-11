import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração de Página
st.set_page_config(page_title="FIFA World Cup 26 Map", layout="wide")

# 2. Dados
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

flags = {
    "SAU": "🇸🇦", "QAT": "🇶🇦", "KOR": "🇰🇷", "CUW": "🇨🇼", "HTI": "🇭🇹", "IRN": "🇮🇷", "IRQ": "🇮🇶", "JOR": "🇯🇴", "NZL": "🇳🇿", "PAN": "🇵🇦", "CZE": "🇨🇿", "TUN": "🇹🇳", "URY": "🇺🇾", "UZB": "🇺🇿", "SRB": "🇷🇸", "ITA": "🇮🇹", "ZAF": "🇿🇦", "DEU": "🇩🇪", "DZA": "🇩🇿", "AUS": "🇦🇺", "AUT": "🇦🇹", "BIH": "🇧🇦", "CPV": "🇨🇻", "CIV": "🇨🇮", "HRV": "🇭🇷", "ECU": "🇪🇨", "GHA": "🇬🇭", "NLD": "🇳🇱", "JPN": "🇯🇵", "COD": "🇨🇩", "SEN": "🇸🇳", "SWE": "🇸🇪", "BRA": "🇧🇷", "CAN": "🇨🇦", "COL": "🇨🇴", "EGY": "🇪🇬", "USA": "🇺🇸", "MEX": "🇲🇽", "PRY": "🇵🇾", "PRT": "🇵🇹", "MAR": "🇲🇦", "BEL": "🇧🇪", "FRA": "🇫🇷", "ESP": "🇪🇸", "NOR": "🇳🇴", "GBR": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "ARG": "🇦🇷", "CHE": "🇨🇭"
}

# 3. Sidebar (Lista de Times)
st.sidebar.title("FIFA World Cup 26™")
stage_idx = st.sidebar.slider("Select Stage:", 0, 5, 0, format="%s")
current_stage_name = stages[stage_idx]

st.sidebar.markdown(f"### Active Teams ({current_stage_name})")
active_list = []
sorted_codes = sorted(teams_elimination.keys(), key=lambda k: country_names[k])
for code in sorted_codes:
    if stage_idx <= teams_elimination[code]:
        active_list.append(f"{flags.get(code, '')} {country_names[code]}")

for team in active_list:
    st.sidebar.write(team)

# 4. Processamento do DataFrame para o Mapa
data = []
for code, elim_index in teams_elimination.items():
    # Define o status baseado no slider atual
    status = "Eliminated" if stage_idx > elim_index else "Active"
    data.append({"Country_Code": code, "Country": country_names.get(code, code), "Status": status})

# Adiciona dummies para forçar a legenda
data.extend([
    {"Country_Code": "AAA", "Country": "Active", "Status": "Active"},
    {"Country_Code": "BBB", "Country": "Eliminated", "Status": "Eliminated"},
    {"Country_Code": "CCC", "Country": "Not Qualified", "Status": "Not Qualified"}
])
df = pd.DataFrame(data)

# 5. Criar Mapa
fig = px.choropleth(
    df, locations="Country_Code", color="Status", hover_name="Country",
    color_discrete_map={"Active": "#00FF4D", "Eliminated": "#1A1A1A", "Not Qualified": "#525252"},
    category_orders={"Status": ["Active", "Eliminated", "Not Qualified"]},
    projection="natural earth"
)

fig.update_layout(
    paper_bgcolor="#000000", plot_bgcolor="#000000", font_color="#FFFFFF",
    margin={"r":0,"t":0,"l":0,"b":0},
    geo=dict(
        showland=True, landcolor="#525252", 
        showocean=True, oceancolor="#0B132B", 
        showlakes=True, lakecolor="#0B132B",
        bgcolor="#000000"
    )
)

# Renderizar
st.title(f"FIFA World Cup 26™ | {current_stage_name}")
st.plotly_chart(fig, use_container_width=True)

# CSS para Bandeiras
st.markdown("""
<style>
    div[data-testid="stSidebar"] { background-color: #111; }
    text { font-family: "Arial", "Segoe UI Emoji", sans-serif !important; }
</style>
""", unsafe_allow_html=True)
