import streamlit as st
import pandas as pd

# Ρυθμίσεις Σελίδας
st.set_page_config(page_title="Golden Girl Pro", layout="wide", page_icon="👑")

# --- CUSTOM CSS ΓΙΑ LUXURY ΕΜΦΑΝΙΣΗ & ΕΚΤΥΠΩΣΗ ---
st.markdown("""
    <style>
    @media print {
        .no-print { display: none !important; }
        .print-only { display: block !important; }
    }
    .stButton>button { 
        width: 100%; height: 60px; font-size: 18px; 
        background-color: #d4af37; color: black; font-weight: bold; border-radius: 10px;
    }
    .status-box {
        padding: 20px; border-radius: 10px; background-color: #262730; border: 1px solid #d4af37;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 Golden Girl Management System")

# --- SIDEBAR: ΡΥΘΜΙΣΕΙΣ ΚΑΤΑΛΟΓΟΥ ---
with st.sidebar:
    st.header("🛠️ Διαχείριση Καταλόγου")
    
    # Ρύθμιση Ποσοστού & Private
    st.session_state.comm_rate = st.slider("Ποσοστό Σαμπάνιας %", 0, 100, 25) / 100
    st.session_state.priv_price = st.number_input("Τιμή Private Show (€)", value=15.0)

    st.divider()
    
    # Διαχείριση Ποτών
    st.subheader("Προσθήκη/Αλλαγή Ποτών")
    if 'menu' not in st.session_state:
        st.session_state.menu = {"Moet": 450.0, "Dom Perignon": 800.0}
    
    with st.form("add_drink"):
        new_name = st.text_input("Όνομα Ποτού")
        new_price = st.number_input("Τιμή (€)", min_value=0.0)
        if st.form_submit_button("Προσθήκη στον Κατάλογο"):
            if new_name:
                st.session_state.menu[new_name] = new_price
                st.rerun()

    if st.button("🗑️ Καθαρισμός Καταλόγου"):
        st.session_state.menu = {}
        st.rerun()

# --- ΚΥΡΙΟ ΜΕΡΟΣ: ΚΑΤΑΓΡΑΦΗ ---
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = []

st.subheader("📝 Νέα Καταχώρηση")
c1, c2 = st.columns([1, 2])

with c1:
    girl_name = st.text_input("ΟΝΟΜΑ ΚΟΠΕΛΑΣ", placeholder="π.χ. Natasa").upper()

with c2:
    st.write("Επίλεξε Υπηρεσία/Ποτό:")
    col_p, col_m = st.columns([1, 2])
    
    with col_p:
        if st.button(f"💃 PRIVATE ({st.session_state.priv_price}€)"):
            if girl_name:
                st.session_state.sales_data.append({
                    "Κοπέλα": girl_name, "Είδος": "Private Show", 
                    "Τιμή": st.session_state.priv_price, "Προμήθεια": st.session_state.priv_price
                })
                st.toast(f"Καταχωρήθηκε Show για {girl_name}")
            else: st.error("Βάλε όνομα!")

    with col_m:
        # Δημιουργία κουμπιών για κάθε ποτό στον κατάλογο
        cols = st.columns(2)
        for i, (name, price) in enumerate(st.session_state.menu.items()):
            if cols[i % 2].button(f"🍾 {name} ({price}€)"):
                if girl_name:
                    st.session_state.sales_data.append({
                        "Κοπέλα": girl_name, "Είδος": name, 
                        "Τιμή": price, "Προμήθεια": price * st.session_state.comm_rate
                    })
                    st.toast(f"Καταχωρήθηκε {name} για {girl_name}")
                else: st.error("Βάλε όνομα!")

# --- ΑΠΟΤΕΛΕΣΜΑΤΑ & ΚΑΡΤΕΛΕΣ ---
if st.session_state.sales_data:
    df = pd.DataFrame(st.session_state.sales_data)
    
    st.divider()
    st.subheader("📊 Αναφορά Ημέρας (Καρτέλες Κοριτσιών)")
    
    # Επιλογή Καρτέλας
    all_girls = sorted(list(df["Κοπέλα"].unique()))
    selected_girl = st.selectbox("Επίλεξε Κοπέλα για να δεις την καρτέλα της (ή 'ΟΛΕΣ'):", ["ΟΛΕΣ"] + all_girls)
    
    if selected_girl == "ΟΛΕΣ":
        view_df = df
    else:
        view_df = df[df["Κοπέλα"] == selected_girl]

    st.table(view_df)

    # ΣΥΝΟΛΑ
    total_revenue = view_df["Τιμή"].sum()
    total_payout = view_df["Προμήθεια"].sum()

    st.markdown(f"""
    <div class="status-box">
        <h3>ΣΥΝΟΛΑ {selected_girl}</h3>
        <p>Συνολικός Τζίρος: <b>{total_revenue:,.2f} €</b></p>
        <p>Πληρωτέα Προμήθεια: <b>{total_payout:,.2f} €</b></p>
        <p>Καθαρά για το Μαγαζί: <b>{(total_revenue - total_payout):,.2f} €</b></p>
    </div>
    """, unsafe_allow_html=True)

    # --- ΕΚΤΥΠΩΣΗ ---
    st.write("")
    if st.button("🖨️ Εκτύπωση Ημέρας / Αποθήκευση PDF"):
        st.info("💡 Πάτα Ctrl+P (ή Command+P σε Mac) για να εκτυπώσεις την οθόνη.")
        
    if st.button("❌ Κλείσιμο Ταμείου (Reset)"):
        st.session_state.sales_data = []
        st.rerun()
else:
    st.info("Δεν υπάρχουν ακόμα καταχωρήσεις για σήμερα.")