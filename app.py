import streamlit as st
import pandas as pd

# Ρυθμίσεις Σελίδας
st.set_page_config(page_title="Golden Girl Pro", layout="wide", page_icon="👑")

# CSS για την εμφάνιση των κουμπιών και των πλαισίων
st.markdown("""
    <style>
    .stButton>button { 
        width: 100%; height: 60px; font-size: 18px; 
        background-color: #d4af37; color: black; font-weight: bold; border-radius: 10px;
    }
    .girl-stats {
        padding: 15px; border-radius: 10px; background-color: #1e1e1e; border-left: 5px solid #d4af37; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 Golden Girl Management")

# --- ΠΛΑΪΝΟ ΜΕΝΟΥ (SIDEBAR): ΡΥΘΜΙΣΕΙΣ ---
with st.sidebar:
    st.header("🛠️ Einstellungen") # Ρυθμίσεις
    comm_rate = st.slider("Champagner Provision %", 0, 100, 25) / 100 # Ποσοστό
    priv_price = st.number_input("Preis Private Show (€)", value=15.0) # Τιμή Show
    
    st.divider()
    if 'menu' not in st.session_state:
        st.session_state.menu = {"Moet": 450.0, "Dom Perignon": 800.0}
    
    # Φόρμα για προσθήκη ποτών
    with st.form("add_drink"):
        n_name = st.text_input("Neues Getränk") # Όνομα νέου ποτού
        n_price = st.number_input("Preis (€)", min_value=0.0) # Τιμή
        if st.form_submit_button("Hinzufügen"): # Προσθήκη
            if n_name: 
                st.session_state.menu[n_name] = n_price
                st.rerun()

# --- ΜΝΗΜΗ ΔΕΔΟΜΕΝΩΝ ---
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = []

df_main = pd.DataFrame(st.session_state.sales_data)

# --- ΠΕΡΙΟΧΗ ΚΑΤΑΧΩΡΗΣΗΣ ---
st.subheader("📝 Buchung eingeben") # Εισαγωγή Καταχώρησης
girl_name = st.text_input("NAME DES MÄDCHENS", placeholder="z.B. NATASA").upper()

# --- LIVE ΕΛΕΓΧΟΣ ΓΙΑ ΤΗΝ ΚΟΠΕΛΑ ---
if girl_name and not df_main.empty:
    girl_filter = df_main[df_main["Mädchen"] == girl_name]
    if not girl_filter.empty:
        with st.container():
            st.markdown(f'<div class="girl-stats"><b>Aktueller Stand für {girl_name}:</b></div>', unsafe_allow_html=True)
            st.dataframe(girl_filter[["Leistung", "Preis", "Provision"]], use_container_width=True)
            st.info(f"Gesamt bisher für {girl_name}: {girl_filter['Provision'].sum():.2f} €")

# --- ΚΟΥΜΠΙΑ ΓΙΑ ΤΑ ΠΟΣΑ ---
col1, col2 = st.columns([1, 2])

with col1:
    if st.button(f"💃 PRIVATE SHOW\n({priv_price}€ FIX)"):
        if girl_name:
            st.session_state.sales_data.append({"Mädchen": girl_name, "Leistung": "Private Show", "Preis": priv_price, "Provision": priv_price})
            st.success(f"Show für {girl_name} gespeichert!"); st.rerun()
        else: st.error("Namen eingeben!")

with col2:
    cols = st.columns(2)
    for i, (name, price) in enumerate(st.session_state.menu.items()):
        if cols[i % 2].button(f"🍾 {name}\n({price}€)"):
            if girl_name:
                st.session_state.sales_data.append({"Mädchen": girl_name, "Leistung": name, "Preis": price, "Provision": price * comm_rate})
                st.success(f"{name} für {girl_name} gespeichert!"); st.rerun()
            else: st.error("Namen eingeben!")

# --- ΓΕΝΙΚΗ ΕΙΚΟΝΑ ΚΑΙ ΚΑΡΤΕΛΕΣ ---
if not df_main.empty:
    st.divider()
    st.subheader("📊 Tagesabrechnung") # Ημερήσια Αναφορά
    
    tabs = st.tabs(["Alle Buchungen", "Abrechnung pro Mädchen"])
    
    with tabs[0]: # Όλες οι κινήσεις
        st.table(df_main)
        
    with tabs[1]: # Καρτέλα ανά κοπέλα
        all_girls = sorted(df_main["Mädchen"].unique())
        for g in all_girls:
            g_df = df_main[df_main["Mädchen"] == g]
            with st.expander(f"Konto: {g}"): # Καρτέλα: [Όνομα]
                st.table(g_df)
                st.write(f"**Auszahlung für {g}: {g_df['Provision'].sum():.2f} €**")

    # ΣΥΝΟΛΑ ΣΤΟ ΠΛΑΙ (SIDEBAR)
    st.sidebar.markdown("---")
    st.sidebar.metric("Gesamtumsatz Club", f"{df_main['Preis'].sum():.2f} €") # Τζίρος Μαγαζιού
    st.sidebar.metric("Gesamtauszahlung Mädchen", f"{df_main['Provision'].sum():.2f} €") # Σύνολο Κοριτσιών

    if st.button("❌ Kasse schließen / Reset"): # Κλείσιμο Ταμείου
        st.session_state.sales_data = []
        st.rerun()