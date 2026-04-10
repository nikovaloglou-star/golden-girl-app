import streamlit as st
import pandas as pd

# Seitenkonfiguration
st.set_page_config(page_title="Golden Girl Pro", layout="wide", page_icon="👑")

# --- ΒΕΛΤΙΩΜΕΝΟ CSS ΓΙΑ ΜΕΓΙΣΤΗ ΟΡΑΤΟΤΗΤΑ ---
st.markdown("""
    <style>
    /* Γενικό φόντο και χρώμα γραμματοσειράς */
    .main { background-color: #000000; color: #ffffff; }
    
    /* Επικεφαλίδες */
    h1, h2, h3 { color: #d4af37 !important; }
    
    /* Κουμπιά: Χρυσό φόντο με ΜΑΥΡΑ γράμματα για να ξεχωρίζουν */
    .stButton>button { 
        width: 100%; height: 70px; font-size: 20px !important; 
        background-color: #d4af37 !important; color: #000000 !important; 
        font-weight: bold !important; border-radius: 12px; border: 2px solid #ffffff;
    }
    
    /* Πλαίσια εισαγωγής κειμένου */
    .stTextInput>div>div>input {
        background-color: #333333 !important; color: #ffffff !important;
        border: 2px solid #d4af37 !important; font-size: 18px;
    }

    /* Πίνακες: Λευκά γράμματα σε σκούρο φόντο */
    .stDataFrame, .stTable {
        background-color: #1a1a1a !important; color: #ffffff !important;
        border: 1px solid #d4af37;
    }
    
    /* Στατιστικά κοπέλας */
    .girl-box {
        padding: 20px; border-radius: 15px; background-color: #1a1a1a; 
        border: 2px solid #d4af37; color: #ffffff; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 GOLDEN GIRL MANAGEMENT")

# --- SIDEBAR: ΡΥΘΜΙΣΕΙΣ ---
with st.sidebar:
    st.header("🛠️ EINSTELLUNGEN")
    comm_rate = st.slider("Champagner %", 0, 100, 25) / 100
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

# --- ΜΝΗΜΗ ΔΕΔΟΜΕΝΩΝ ---
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = []

df_main = pd.DataFrame(st.session_state.sales_data)

# --- ΕΙΣΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ ---
st.subheader("📝 NEUE BUCHUNG (ΝΕΑ ΚΑΤΑΧΩΡΗΣΗ)")
girl_name = st.text_input("NAME DES MÄDCHENS (ΟΝΟΜΑ ΚΟΠΕΛΑΣ)", placeholder="NATASA").upper()

col1, col2 = st.columns([1, 2])

with col1:
    if st.button(f"💃 PRIVAT SHOW\n{priv_price}€"):
        if girl_name:
            st.session_state.sales_data.append({
                "Mädchen": girl_name, "Typ": "Privat", 
                "Leistung": "Privat Show", "Preis": priv_price, "Provision": priv_price
            })
            st.rerun()
        else: st.error("NAME FEHLT!")

with col2:
    cols = st.columns(2)
    for i, (name, price) in enumerate(st.session_state.menu.items()):
        if cols[i % 2].button(f"🍾 {name}\n{price}€"):
            if girl_name:
                st.session_state.sales_data.append({
                    "Mädchen": girl_name, "Typ": "Champagner", 
                    "Leistung": name, "Preis": price, "Provision": price * comm_rate
                })
                st.rerun()
            else: st.error("NAME FEHLT!")

# --- ΑΤΟΜΙΚΕΣ ΚΑΡΤΕΛΕΣ & ΑΝΑΛΥΣΗ ---
if not df_main.empty:
    st.divider()
    st.header("📊 EINZELABRECHNUNG (ΑΤΟΜΙΚΗ ΚΑΡΤΕΛΑ)")
    
    all_girls = sorted(df_main["Mädchen"].unique())
    selected_girl = st.selectbox("WÄHLE EIN MÄDCHEN (ΔΙΑΛΕΞΕ ΚΟΠΕΛΑ):", all_girls)
    
    if selected_girl:
        g_df = df_main[df_main["Mädchen"] == selected_girl]
        
        # Διαχωρισμός κατανάλωσης και shows
        privat_total = g_df[g_df["Typ"] == "Privat"]["Provision"].sum()
        champagner_total = g_df[g_df["Typ"] == "Champagner"]["Provision"].sum()
        
        st.markdown(f"""
        <div class="girl-box">
            <h2 style='color: #d4af37;'>Konto: {selected_girl}</h2>
            <p style='font-size: 20px;'>💃 Privat Shows: <b>{privat_total:.2f} €</b></p>
            <p style='font-size: 20px;'>🍾 Champagner Provision: <b>{champagner_total:.2f} €</b></p>
            <hr style='border: 1px solid #d4af37;'>
            <h3 style='color: #ffffff;'>GESAMT AUSZAHLUNG: <span style='color: #00ff00;'>{privat_total + champagner_total:.2f} €</span></h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("Detaillierte Liste (Αναλυτική Λίστα):")
        st.table(g_df[["Leistung", "Preis", "Provision"]])

    # ΓΕΝΙΚΟ ΤΑΜΕΙΟ ΜΑΓΑΖΙΟΥ (Μόνο για εσένα)
    with st.expander("TOTAL CLUB REPORT (ΓΕΝΙΚΟ ΤΑΜΕΙΟ)"):
        st.write(df_main)
        st.metric("TOTAL UMSATZ (ΤΖΙΡΟΣ)", f"{df_main['Preis'].sum():.2f} €")
        st.metric("TOTAL MÄDCHEN (ΚΟΠΕΛΕΣ)", f"{df_main['Provision'].sum():.2f} €")
        
    if st.button("❌ KASSE SCHLIESSEN (RESET)"):
        st.session_state.sales_data = []
        st.rerun()