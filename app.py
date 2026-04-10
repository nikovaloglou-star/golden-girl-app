import streamlit as st
import pandas as pd

# Seitenkonfiguration
st.set_page_config(page_title="Golden Girl Pro", layout="wide", page_icon="👑")

# --- CSS ΓΙΑ ΜΕΓΙΣΤΗ ΟΡΑΤΟΤΗΤΑ ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    p, span, label, .stMarkdown { color: #ffffff !important; font-weight: 500; }
    h1, h2, h3 { color: #d4af37 !important; text-align: center; }
    .stButton>button { 
        width: 100%; height: 75px; font-size: 22px !important; 
        background-color: #d4af37 !important; color: #000000 !important; 
        font-weight: bold !important; border-radius: 15px; border: 2px solid #ffffff !important;
    }
    .stTable, table { color: #ffffff !important; background-color: #1a1a1a !important; border: 1px solid #d4af37 !important; }
    th { color: #d4af37 !important; background-color: #333333 !important; }
    td { color: #ffffff !important; border-bottom: 1px solid #444 !important; }
    input { background-color: #222222 !important; color: #ffffff !important; border: 2px solid #d4af37 !important; }
    .girl-box {
        padding: 25px; border-radius: 20px; background-color: #111111; 
        border: 3px solid #d4af37; color: #ffffff !important; margin-top: 20px; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 GOLDEN GIRL MANAGEMENT")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🛠️ EINSTELLUNGEN")
    comm_rate = st.slider("Champagner Provision %", 0, 100, 25) / 100
    priv_price = st.number_input("Privat Show Preis (€)", value=15.0)
    if 'menu' not in st.session_state:
        st.session_state.menu = {"Moet": 450.0, "Dom Perignon": 800.0}
    with st.form("add_drink"):
        n_name = st.text_input("Neues Getränk")
        n_price = st.number_input("Preis (€)", min_value=0.0)
        if st.form_submit_button("HINZUFÜGEN"):
            if n_name: 
                st.session_state.menu[n_name] = n_price
                st.rerun()

# --- DATA ---
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = []

df_main = pd.DataFrame(st.session_state.sales_data)

# --- INPUT ---
st.subheader("📝 NEUE BUCHUNG")
girl_name = st.text_input("NAME DES MÄDCHENS", placeholder="NATASA").upper()

col1, col2 = st.columns([1, 2])
with col1:
    if st.button(f"💃 PRIVAT SHOW\n{priv_price}€"):
        if girl_name:
            st.session_state.sales_data.append({"Mädchen": girl_name, "Typ": "Privat", "Leistung": "Privat Show", "Preis": priv_price, "Provision": priv_price})
            st.rerun()
        else: st.error("NAME FEHLT!")

with col2:
    cols = st.columns(2)
    for i, (name, price) in enumerate(st.session_state.menu.items()):
        if cols[i % 2].button(f"🍾 {name}\n{price}€"):
            if girl_name:
                st.session_state.sales_data.append({"Mädchen": girl_name, "Typ": "Champagner", "Leistung": name, "Preis": price, "Provision": price * comm_rate})
                st.rerun()
            else: st.error("NAME FEHLT!")

# --- REPORT ---
if not df_main.empty:
    st.divider()
    st.header("📊 EINZELABRECHNUNG")
    all_girls = sorted(df_main["Mädchen"].unique())
    selected_girl = st.selectbox("WÄHLE EIN MÄDCHEN:", all_girls)
    
    if selected_girl:
        g_df = df_main[df_main["Mädchen"] == selected_girl]
        priv_sum = g_df[g_df["Typ"] == "Privat"]["Provision"].sum()
        champ_sum = g_df[g_df["Typ"] == "Champagner"]["Provision"].sum()
        total_p = priv_sum + champ_sum
        
        # ΠΡΟΣΟΧΗ: Εδώ έκλεινε λάθος το f-string πριν
        st.markdown(f"""
        <div class="girl-box">
            <h2 style='color: #d4af37 !important;'>Konto: {selected_girl}</h2>
            <p style='font-size: 22px;'>💃 Privat Shows: {priv_sum:.2f} €</p>
            <p style='font-size: 22px;'>🍾 Champagner: {champ_sum:.2f} €</p>
            <hr style='border: 1px solid #d4af37;'>
            <h2 style='color: #ffffff !important;'>GESAMT: <span style='color: #00ff00 !important;'>{total_p:.2f} €</span></h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.table(g_df[["Leistung", "Preis", "Provision"]])

    with st.expander("📂 TOTAL CLUB REPORT"):
        st.table(df_main)
        st.metric("TOTAL UMSATZ", f"{df_main['Preis'].sum():.2f} €")
        
    if st.button("❌ KASSE SCHLIESSEN"):
        st.session_state.sales_data = []
        st.rerun()