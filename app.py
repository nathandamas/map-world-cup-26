import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- Page Configuration ---
st.set_page_config(page_title="FIFA World Cup 26 Map", layout="wide")

# --- Initializing State ---
if 'stage_index' not in st.session_state:
    st.session_state.stage_index = 0
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False

# --- Constants & Data Configuration ---
STAGES = [
    "Group Stage", "Round of 32", "Round of 16", 
    "Quarter-finals", "Semi-finals", "Final"
]
DATES = [
    "27-06-2026", "03-07-2026", "07-07-2026", 
    "11-07-2026", "15-07-2026", "19-07-2026"
]

# Defines the stage index when each team is eliminated
TEAMS_ELIMINATION = {
    # 0 = Group Stage
    "SAU": 0, "QAT": 0, "KOR": 0, "CUW": 0, "HTI": 0, "IRN": 0, "IRQ": 0, "JOR": 0, 
    "NZL": 0, "PAN": 0, "CZE": 0, "TUN": 0, "URY": 0, "UZB": 0, "SRB": 0, "ITA": 0,
    # 1 = Round of 32
    "ZAF": 1, "DEU": 1, "DZA": 1, "AUS": 1, "AUT": 1, "BIH": 1, "CPV": 1, "CIV": 1, 
    "HRV": 1, "ECU": 1, "GHA": 1, "NLD": 1, "JPN": 1, "COD": 1, "SEN": 1, "SWE": 1,
    # 2 = Round of 16
    "BRA": 2, "CAN": 2, "COL": 2, "EGY": 2, "USA": 2, "MEX": 2, "PRY": 2, "PRT": 2, 
    # 3 = Quarter-finals
    "MAR": 3, "BEL": 3, "CHE": 3, "NOR": 3,
    # 4 = Semi-finals
    "FRA": 4, "GBR": 4, 
    # 99 = Active (Final)
    "ARG": 99, "ESP": 99
}

COUNTRY_NAMES = {
    "SAU": "Saudi Arabia", "QAT": "Qatar", "KOR": "South Korea", "CUW": "Curacao", 
    "HTI": "Haiti", "IRN": "Iran", "IRQ": "Iraq", "JOR": "Jordan", "NZL": "New Zealand", 
    "PAN": "Panama", "CZE": "Czechia", "TUN": "Tunisia", "URY": "Uruguay", 
    "UZB": "Uzbekistan", "SRB": "Serbia", "ITA": "Italy", "ZAF": "South Africa", 
    "DEU": "Germany", "DZA": "Algeria", "AUS": "Australia", "AUT": "Austria", 
    "BIH": "Bosnia and Herzegovina", "CPV": "Cape Verde", "CIV": "Ivory Coast", 
    "HRV": "Croatia", "ECU": "Ecuador", "GHA": "Ghana", "NLD": "Netherlands", 
    "JPN": "Japan", "COD": "DR Congo", "SEN": "Senegal", "SWE": "Sweden", 
    "BRA": "Brazil", "CAN": "Canada", "COL": "Colombia", "EGY": "Egypt", 
    "USA": "United States", "MEX": "Mexico", "PRY": "Paraguay", "PRT": "Portugal", 
    "MAR": "Morocco", "BEL": "Belgium", "FRA": "France", "ESP": "Spain", 
    "NOR": "Norway", "GBR": "England", "ARG": "Argentina", "CHE": "Switzerland"
}

ISO_MAP = {
    "SAU": "sa", "QAT": "qa", "KOR": "kr", "CUW": "cw", "HTI": "ht", "IRN": "ir", 
    "IRQ": "iq", "JOR": "jo", "NZL": "nz", "PAN": "pa", "CZE": "cz", "TUN": "tn", 
    "URY": "uy", "UZB": "uz", "SRB": "rs", "ITA": "it", "ZAF": "za", "DEU": "de", 
    "DZA": "dz", "AUS": "au", "AUT": "at", "BIH": "ba", "CPV": "cv", "CIV": "ci", 
    "HRV": "hr", "ECU": "ec", "GHA": "gh", "NLD": "nl", "JPN": "jp", "COD": "cd", 
    "SEN": "sn", "SWE": "se", "BRA": "br", "CAN": "ca", "COL": "co", "EGY": "eg", 
    "USA": "us", "MEX": "mx", "PRY": "py", "PRT": "pt", "MAR": "ma", "BEL": "be", 
    "FRA": "fr", "ESP": "es", "NOR": "no", "GBR": "gb", "ARG": "ar", "CHE": "ch"
}

MATCH_DETAILS = {
    # Round of 32 Matches
    "DZA": {"match": "CHE 2 x 0 DZA", "date": "02-07-2026"}, 
    "AUS": {"match": "EGY 4 (p) x (p) 2 AUS", "date": "03-07-2026"},
    "CPV": {"match": "ARG 3 x 2 CPV", "date": "03-07-2026"}, 
    "GHA": {"match": "COL 1 x 0 GHA", "date": "03-07-2026"},
    
    # Round of 16 Matches
    "PRY": {"match": "FRA 1 x 0 PRY", "date": "04-07-2026"},
    "CAN": {"match": "MAR 3 x 0 CAN", "date": "04-07-2026"},
    "MEX": {"match": "GBR 3 x 2 MEX", "date": "05-07-2026"},
    "BRA": {"match": "NOR 2 x 0 BRA", "date": "05-07-2026"},
    "USA": {"match": "BEL 4 x 1 USA", "date": "06-07-2026"}, 
    "PRT": {"match": "ESP 2 x 1 PRT", "date": "06-07-2026"},
    "COL": {"match": "CHE 1 x 0 COL", "date": "07-07-2026"}, 
    "EGY": {"match": "ARG 2 x 1 EGY", "date": "07-07-2026"},
    
    # Quarter-final Matches
    "MAR": {"match": "FRA 2 x 0 MAR", "date": "10-07-2026"}, 
    "BEL": {"match": "ESP 2 x 0 BEL", "date": "10-07-2026"},
    "CHE": {"match": "ARG 2 x 0 CHE", "date": "11-07-2026"},
    "NOR": {"match": "GBR 2 x 0 NOR", "date": "11-07-2026"},
    
    # Semi-final Matches
    "FRA": {"match": "ESP 2 x 0 FRA", "date": "14-07-2026"},
    "GBR": {"match": "ARG 2 x 1 GBR", "date": "15-07-2026"}
}

# --- Sidebar UI ---
st.sidebar.title("FIFA World Cup 26™")

# Player Button
if st.sidebar.button("▶ Play Animation"):
    st.session_state.is_playing = True
    st.session_state.stage_index = 0  # Restarts animation

# Slider
st.session_state.stage_index = st.sidebar.select_slider(
    "Select Stage:", 
    options=range(len(STAGES)), 
    value=st.session_state.stage_index, 
    format_func=lambda x: STAGES[x]
)

stage_index = st.session_state.stage_index
st.sidebar.markdown(f"**Date:** {DATES[stage_index]}")
st.sidebar.markdown("---")
st.sidebar.subheader("Active Teams")

# Display active teams with flags
for country_code in sorted(TEAMS_ELIMINATION.keys(), key=lambda k: COUNTRY_NAMES[k]):
    if stage_index <= TEAMS_ELIMINATION[country_code]:
        iso_code = ISO_MAP.get(country_code, "xx")
        st.sidebar.markdown(
            f"![Flag](https://flagcdn.com/w20/{iso_code}.png) {COUNTRY_NAMES[country_code]}"
        )

# --- Header & Map Placeholder ---
col1, col2 = st.columns([1, 8])
with col1:
    st.image(
        "https://raw.githubusercontent.com/nathandamas/map-world-cup-26/main/tournaments_fifa-world-cup-2026--white_700x700.football-logos.cc.png", 
        width=80
    )
with col2:
    st.title(f"FIFA World Cup 26™ | {STAGES[stage_index]}")

map_placeholder = st.empty()

# --- Data Preparation ---
map_data = [
    {"Country_Code": "AAA", "Country": "Active", "Status": "Active", "Match": "-", "Date": "-"},
    {"Country_Code": "BBB", "Country": "Eliminated", "Status": "Eliminated", "Match": "-", "Date": "-"},
    {"Country_Code": "CCC", "Country": "Not Qualified", "Status": "Not Qualified", "Match": "-", "Date": "-"}
]

for country_code, elimination_index in TEAMS_ELIMINATION.items():
    status = "Eliminated" if stage_index > elimination_index else "Active"
    
    match_info = MATCH_DETAILS.get(country_code, {}).get("match", "Eliminated by Points") \
        if status == "Eliminated" else "-"
    match_date = MATCH_DETAILS.get(country_code, {}).get("date", "-") \
        if status == "Eliminated" else "-"
    
    map_data.append({
        "Country_Code": country_code, 
        "Country": COUNTRY_NAMES.get(country_code, country_code), 
        "Status": status, 
        "Match": match_info, 
        "Date": match_date
    })

df = pd.DataFrame(map_data)

# --- Map Visualization ---
fig = px.choropleth(
    df, 
    locations="Country_Code", 
    color="Status", 
    hover_name="Country",
    color_discrete_map={
        "Active": "#00FF4D", 
        "Eliminated": "#404040", 
        "Not Qualified": "#525252"
    },
    category_orders={"Status": ["Active", "Eliminated", "Not Qualified"]},
    hover_data={"Status": True, "Match": True, "Date": True, "Country_Code": False},
    projection="natural earth"
)

# Customize hover tooltip and country borders
fig.update_traces(
    marker_line_color="#000000",
    marker_line_width=0.7,
    hovertemplate="<b>%{hovertext}</b><br>"
                  "Status: %{customdata[0]}<br>"
                  "Match: %{customdata[1]}<br>"
                  "Date: %{customdata[2]}<extra></extra>"
)

# Apply layout styling
fig.update_layout(
    paper_bgcolor="#000000", 
    plot_bgcolor="#000000", 
    font_color="#FFFFFF",
    margin={"r": 0, "t": 20, "l": 0, "b": 0},
    legend=dict(
        x=0.08, y=0.5, 
        bgcolor="rgba(0,0,0,0.6)", 
        bordercolor="#FFFFFF", 
        borderwidth=1.5
    ),
    geo=dict(
        showland=True, 
        landcolor="#525252", 
        showocean=True, 
        oceancolor="#0B132B", 
        showlakes=True, 
        lakecolor="#0B132B", 
        bgcolor="#000000", 
        showcountries=True,
        countrycolor="#000000",
        showcoastlines=True,
        coastlinecolor="#000000"
    )
)

map_placeholder.plotly_chart(fig, use_container_width=True)

# --- Animation Logic ---
# Needs to run after drawing the map to ensure visual update
if st.session_state.is_playing:
    if st.session_state.stage_index < len(STAGES) - 1:
        time.sleep(1.0)
        st.session_state.stage_index += 1
        st.rerun()
    else:
        st.session_state.is_playing = False
        st.rerun()
