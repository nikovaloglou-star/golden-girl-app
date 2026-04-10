import streamlit as st
import pandas as pd

# Seitenkonfiguration (Ρυθμίσεις Σελίδας)
st.set_page_config(page_title="Golden Girl Pro", layout="wide", page_icon="👑")

# --- CSS ΓΙΑ ΜΕΓΙΣΤΗ ΟΡΑΤΟΤΗΤΑ (Λευκά γράμματα & Χρυσά Κουμπιά) ---
st.markdown("""
    <style>
    /* Φόντο ολόκληρης της εφαρμογής */
    .stApp {
        background-color: #000000 !important;
    }
    
    /* Γενικά κείμενα, παράγραφοι και ετικέτες */
    p, span, label, .stMarkdown {
        color: #ffffff !important;
        font-weight: 500;
    }

    /* Επικεφαλίδες (Χρυσό χρώμα) */
    h1, h2, h3 {
        color: #d4af37 !important;
        text-align: center;
    }

    /* ΚΟΥΜΠΙΑ: Χρυσό φόντο με ΜΑΥΡΑ έντονα γράμματα */
    .stButton>button { 
        width: 100%; 
        height: 75px; 
        font-size: 22px !important; 
        background-color: #d4af37 !important; 
        color: #000000 !important; 
        font-weight: bold !important; 
        border-radius: 15px; 
        border: 2px solid #ffffff !important;
        box-shadow: 0px 4px 10px rgba(212, 175, 55, 0.3);
    }
    
    /* ΠΙΝΑΚΕΣ: Εξαναγκασμός λευκών γραμμάτων και σκούρου φόντου */
    .stTable, table {
        color: #ffffff !important;
        background-color: #1a1a1a !important;
        border: 1px solid #d4af37 !important;
    }
    
    th {
        color: #d4af37 !important;
        background-color: #333333 !important;
        font-size: 18px !important;
    }

    td {
        color: #ffffff !important;
        font-size: 17px !important;
        border-bottom: 1px solid #444 !important;
    }

    /* Πλαίσια εισαγωγής κειμένου (Input Boxes) */
    input {
        background-color: #222222 !important;
        color: #ffffff !important;
        border: 2px solid #d4af37 !important;
        font-size: 18px !important;
    }

    /* Το πλαίσιο της ατομικής καρτέλας (Girl Box) */
    .girl-box {
        padding: 25px; 
        border-radius: 20px; 
        background-color: #111111; 
        border: 3px solid #d4af37; 
        color: #ffffff !important; 
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 GOLDEN GIRL MANAGEMENT")

# --- SIDEBAR: ΡΥΘΜΙΣΕΙΣ ΚΑΤΑΛΟΓΟΥ ---
with st.sidebar:
    st.header("🛠️ EINSTELLUNGEN")
    comm_rate = st.slider("Champagner Provision %", 0, 100, 25) / 100
    priv_price = st.number_input("Privat Show Preis (€)", value=15.0)
    
    st.divider()
    if 'menu' not in st.session_state:
        st.session_state.menu = {"Moet": 450.0, "Dom Perignon": 800.0}
    
    # Προσθήκη νέου ποτού
    with st.form("add_drink"):
        n_name = st.text_input("Neues Getränk (Όνομα)")
        n_price = st.number_input("Preis (€)", min_value=0.0)
        if st.form_submit_button("HINZUFÜGEN (ΠΡΟΣΘΗΚΗ)"):
            if n_name: 
                st.session_state.menu[n_name] = n_price
                st.rerun()

# --- ΑΠΟΘΗΚΕΥΣΗ ΔΕΔΟΜΕΝΩΝ ---
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = []

df_main = pd.DataFrame(st.session_state.sales_data)

# --- ΕΝΟΤΗΤΑ ΚΑΤΑΧΩΡΗΣΗΣ (INPUT) ---
st.subheader("📝 NEUE BUCHUNG")
girl_name = st.text_input("NAME DES MÄDCHENS (ΟΝΟΜΑ ΚΟΠΕΛΑΣ)", placeholder="π.χ. NATASA").upper()

col1, col2 = st.columns([1, 2])

with col1:
    # Κουμπί για Private Show (Fix τιμή)
    if st.button(f"💃 PRIVAT SHOW\n{priv_price}€"):
        if girl_name:
            st.session_state.sales_data.append({
                "Mädchen": girl_name, "Typ": "Privat", 
                "Leistung": "Privat Show", "Preis": priv_price, "Provision": priv_price
            })
            st.rerun()
        else: st.error("Bitte Namen eingeben!")

with col2:
    # Δυναμικά κουμπιά για σαμπάνιες
    cols = st.columns(2)
    for i, (name, price) in enumerate(st.session_state.menu.items()):
        if cols[i % 2].button(f"🍾 {name}\n{price}€"):
            if girl_name:
                st.session_state.sales_data.append({
                    "Mädchen": girl_name, "Typ": "Champagner", 
                    "Leistung": name, "Preis": price, "Provision": price * comm_rate
                })
                st.rerun()
            else: st.error("Bitte Namen eingeben!")

# --- ΕΝΟΤΗΤΑ ΕΚΚΑΘΑΡΙΣΗΣ (REPORTS) ---
if not df_main.empty:
    st.divider()
    st.header("📊 EINZELABRECHNUNG (ΚΑΡΤΕΛΑ ΚΟΠΕΛΑΣ)")
    
    all_girls = sorted(df_main["Mädchen"].unique())
    selected_girl = st.selectbox("WÄHLE EIN MÄDCHEN (ΔΙΑΛΕΞΕ ΚΟΠΕΛΑ):", all_girls)
    
    if selected_girl:
        g_df = df_main[df_main["Mädchen"] == selected_girl]
        
        # Υπολογισμοί για την καρτέλα
        priv_sum = g_df[g_df["Typ"] == "Privat"]["Provision"].sum()
        champ_sum = g_df[g_df["Typ"] == "Champagner"]["Provision"].sum()
        total_payout = priv_sum + champ_sum
        
        # Εμφάνιση της "Χρυσής Καρτέλας"
        st.markdown(f"""
        <div class="girl-box">
            <h2 style='color: #d4af37 !important; margin-bottom: 10px;'>Konto: {selected_girl}</h2>
            <p style='font-size: 22px; margin: 5px