import streamlit as st
import pandas as pd

# Seitenkonfiguration
st.set_page_config(page_title="Golden Girl Pro", layout="wide", page_icon="👑")

# --- CSS ΓΙΑ ΜΕΓΙΣΤΗ ΟΡΑΤΟΤΗΤΑ ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    p, span, label, .stMarkdown { color: #ffffff !important; font-weight: bold; }
    h1, h2, h3 { color: #d4af37 !important; text-align: center; font-family: 'Arial'; }
    
    /* ΚΟΥΜΠΙΑ */
    .stButton>button { 
        width: 100%; height: 80px; font-size: 22px !important; 
        background-color: #d4af37 !important; color: #000000 !important; 
        font-weight: bold !important; border-radius: 15px; border: 2px solid #ffffff !important;
    }
    
    /* ΠΙΝΑΚΕΣ */
    .stTable, table { color: #ffffff !important; background-color: #1a1a1a !important; border: 2px solid #d4af37 !important; width: 100%; }
    th { color: #d4af37 !important; background-color: #333333 !important; font-size: 18px !important; text-align: center !important; }
    td { color: #ffffff !important; font-size: 18px !important; text-align: center !important; border-bottom: 1px solid #444 !important; }
    
    /* INPUT BOX */
    input { background-color: #222222 !important; color: #ffffff !important; border: 2px solid #d4af37 !important; font-size: 20px !important; }
    
    /* ΚΑΡΤΕΛΑ ΚΟΠΕΛΑΣ */
    .girl-box {
        padding: 30px; border-radius: 20px; background-color: #111111; 
        border: 3px solid #d4af37; color: #ffffff !important; margin-bottom: 25px;
        box-shadow: 0px 0px 15px #d4af37;
    }
    </style>
    """, unsafe_allow_html=True)

# Συνάρτηση για μορφοποίηση ευρώ (π.χ. 450,00€)
def format_euro(amount):
    return f"{amount:,.2f}€".replace(",", "X").replace(".", ",").replace("X", ".")

st.title("👑 GOLDEN GIRL MANAGEMENT")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🛠️ EINSTELLUNGEN")
    comm_rate = st.sidebar.slider("Champagner %", 0, 100, 25) / 100
    priv_price = st.sidebar.number_input("Privat Preis (€)", value=15.0)
    
    if 'menu' not in st.session_state:
        st.session_state.menu = {"Moet": 450.0, "Dom Perignon": 800.0}
    
    with st.form("add_drink"):
        n_name = st.text_input("Neues Getränk")
        n_price = st.number_input("Preis (€)", min_value=0.0)
        if st.form_submit_button("HINZUFÜGEN"):
            if n_name: 
                st.session_state.menu[n_name] = n_price
                st.rerun()

# --- INITIALIZE DATA ---
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = []

# --- INPUT SECTION ---
st.subheader("📝 NEUE BUCHUNG (KATAXΩΡΗΣΗ)")
g_name = st.text_input("NAME DES MÄDCHENS (ΟΝΟΜΑ)", key="input_name").upper()

col1, col2 = st.columns([1, 2])

with col1:
    if st.button(f"💃 PRIVAT\n{format_euro(priv_price)}"):
        if g_name:
            st.session_state.sales_data.append({
                "Mädchen": g_name, "Typ": "Privat", 
                "Leistung": "Privat Show", "Preis": priv_price, "Auszahlung": priv_price
            })
            st.toast(f"✔ {g_name} - Privat")
        else: st.error("NAME!")

with col2:
    cols = st.columns(2)
    for i, (name, price) in enumerate(st.session_state.menu.items()):
        if cols[i % 2].button(f"🍾 {name}\n{format_euro(price)}"):
            if g_name:
                st.session_state.sales_data.append({
                    "Mädchen": g_name, "Typ": "Champagner", 
                    "Leistung": name, "Preis": price, "Auszahlung": price * comm_rate
                })
                st.toast(f"✔ {g_name} - {name}")
            else: st.error("NAME!")

# --- REPORTS ---
if st.session_state.sales_data:
    df = pd.DataFrame(st.session_state.sales_data)
    
    st.divider()
    st.header("📊 ABRECHNUNG (ΕΚΚΑΘΑΡΙΣΗ)")
    
    all_girls = sorted(df["Mädchen"].unique())
    selected_girl = st.selectbox("WÄHLE EIN MÄDCHEN (ΕΠΙΛΟΓΗ ΚΟΠΕΛΑΣ):", all_girls)
    
    if selected_girl:
        g_df = df[df["Mädchen"] == selected_girl].copy()
        
        # Υπολογισμοί
        p_show = g_df[g_df["Typ"] == "Privat"]["Auszahlung"].sum()
        p_champ = g_df[g_df["Typ"] == "Champagner"]["Auszahlung"].sum()
        total_p = p_show + p_champ
        
        # Μορφοποίηση για τον πίνακα
        display_df = g_df[["Leistung", "Preis", "Auszahlung"]].copy()
        display_df["Preis"] = display_df["Preis"].apply(format_euro)
        display_df["Auszahlung"] = display_df["Auszahlung"].apply(format_euro)

        st.markdown(f"""
        <div class="girl-box">
            <h2 style='color: #d4af37 !important;'>Mädchen: {selected_girl}</h2>
            <p style='font-size: 22px;'>💃 Privat Shows Total: {format_euro(p_show)}</p>
            <p style='font-size: 22px;'>🍾 Champagner Provision: {format_euro(p_champ)}</p>
            <hr style='border: 1px solid #d4af37;'>
            <h2 style='color: #ffffff !important;'>GESAMT AUSZAHLUNG: <span style='color: #00ff00 !important;'>{format_euro(total_p)}</span></h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.table(display_df)

    # --- TOTAL CLUB REPORT ---
    with st.expander("📂 TOTAL CLUB REPORT (ΓΕΝΙΚΟ ΤΑΜΕΙΟ)"):
        report_df = df.copy()
        report_df["Preis"] = report_df["Preis"].apply(format_euro)
        report_df["Auszahlung"] = report_df["Auszahlung"].apply(format_euro)
        st.table(report_df)
        
        total_revenue = df["Preis"].sum()
        total_girls = df["Auszahlung"].sum()
        
        st.metric("TOTAL UMSATZ (ΤΖΙΡΟΣ)", format_euro(total_revenue))
        st.metric("TOTAL MÄDCHEN (ΚΟΠΕΛΕΣ)", format_euro(total_girls))
        st.write(f"### NETTO CLUB: {format_euro(total_revenue - total_girls)}")

    if st.button("❌ KASSE SCHLIESSEN (RESET)"):
        st.session_state.sales_data = []
        st.rerun()