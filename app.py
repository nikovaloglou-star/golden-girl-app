import streamlit as st
import pandas as pd

# Ρυθμίσεις εμφάνισης
st.set_page_config(page_title="Golden Girl App", page_icon="👑")

st.markdown("""
    <style>
    .stButton>button { 
        width: 100%; 
        height: 70px; 
        font-size: 20px; 
        background-color: #d4af37; 
        color: black;
        border-radius: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 Golden Girl Management")

# Ρυθμίσεις στο πλάι
st.sidebar.header("⚙️ Ρυθμίσεις")
comm_rate = st.sidebar.slider("Ποσοστό Σαμπάνιας %", 0, 100, 25) / 100
fix_show = st.sidebar.number_input("Πληρωμή Show (€)", value=15.0, max_value=30.0)

if 'menu' not in st.session_state:
    st.session_state.menu = {"Moet": 450.0, "Dom Perignon": 800.0, "Veuve Clicquot": 350.0}

if 'sales' not in st.session_state:
    st.session_state.sales = []

# Κύριο Μέρος
girl_name = st.text_input("ΟΝΟΜΑ ΚΟΠΕΛΑΣ", placeholder="Γράψε το όνομα εδώ...")

st.subheader("Καταχώρηση")
col1, col2 = st.columns(2)

with col1:
    if st.button(f"💃 PRIVATE SHOW\n({fix_show}€ FIX)"):
        if girl_name:
            st.session_state.sales.append({"Κοπέλα": girl_name, "Είδος": "Private", "Αξία": fix_show, "Πληρωμή": fix_show})
            st.success(f"Μπήκε το Show για {girl_name}")
        else:
            st.error("Βάλε όνομα!")

with col2:
    for name, price in st.session_state.menu.items():
        if st.button(f"🍾 {name}\n({price}€)"):
            if girl_name:
                st.session_state.sales.append({"Κοπέλα": girl_name, "Είδος": name, "Αξία": price, "Πληρωμή": price * comm_rate})
                st.success(f"Μπήκε η {name} για {girl_name}")
            else:
                st.error("Βάλε όνομα!")

# Πίνακας
if st.session_state.sales:
    st.divider()
    df = pd.DataFrame(st.session_state.sales)
    st.table(df)
    
    total_revenue = df["Αξία"].sum()
    total_girls = df["Πληρωμή"].sum()
    
    st.metric("Συνολικός Τζίρος", f"{total_revenue:.2f} €")
    st.metric("Πληρωτέα στα Κορίτσια", f"{total_girls:.2f} €")
    st.warning(f"Καθαρό Ταμείο Μαγαζιού: {total_revenue - total_girls:.2f} €")

    if st.button("🗑️ Reset (Νέα Μέρα)"):
        st.session_state.sales = []
        st.rerun()