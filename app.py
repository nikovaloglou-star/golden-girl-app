import streamlit as st

# Ρυθμίσεις Σελίδας
st.set_page_config(page_title="AURELIAN PV-Normen", layout="centered", page_icon="☀️")

# --- CSS ΓΙΑ ΕΠΑΓΓΕΛΜΑΤΙΚΗ ΕΜΦΑΝΙΣΗ ---
st.markdown("""
    <style>
    .stApp { background-color: #0A0F1E; }
    h1, h2, h3 { color: #D4A017 !important; text-align: center; }
    p, label { color: #F1F5F9 !important; font-size: 18px !important; }
    .result-box {
        padding: 20px; border-radius: 15px; background-color: #1A2236;
        border: 2px solid #06B6D4; color: #ffffff; margin-top: 20px;
    }
    .stButton>button {
        background-color: #D4A017 !important; color: #000000 !important;
        font-weight: bold; height: 60px; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("☀️ AURELIAN PV-NORMEN")
st.subheader("Τεχνικός Υπολογιστής Φωτοβολταϊκών")

# --- ΔΕΔΟΜΕΝΟ ΑΝΑ ΠΕΡΙΟΧΗ (Βάσει του αρχείου σου) ---
regions = {
    "Region A (Nord/Küste)": {"sk": 1.10, "windzone": 3},
    "Region B (Mitteldeutschland)": {"sk": 0.85, "windzone": 2},
    "Region C (Süddeutschland/Bayern)": {"sk": 1.30, "windzone": 2},
    "Region D (Hochgebirge)": {"sk": 2.50, "windzone": 4}
}

# --- ΕΙΣΑΓΩΓΗ ΣΤΟΙΧΕΙΩΝ ---
with st.container():
    region = st.selectbox("Wähle Region (Περιοχή):", list(regions.keys()))
    hoehe = st.number_input("Gebäudehöhe (Ύψος κτιρίου σε m):", min_value=0, value=10)
    neigung = st.slider("Dachneigung (Κλίση στέγης σε °):", 0, 70, 30)
    schienen = st.radio("Anzahl Schienen (Ράγες ανά πάνελ):", ["1", "2", "3"], index=1)
    hakentyp = st.selectbox("Hakentyp (Τύπος Άγκιστρου):", ["Standard", "Dünn (Λεπτό)", "Heavy Duty"])

# --- ΛΟΓΙΚΗ ΥΠΟΛΟΓΙΣΜΟΥ (Από το αρχείο AURELIAN) ---
def calculate_pv():
    data = regions[region]
    # Βασικές τιμές
    base_abstand = 142 if schienen == "2" else 100
    base_rand = 120
    
    # Διορθώσεις βάσει ύψους και κλίσης
    factor = 1.0
    if hoehe > 15: factor *= 0.85
    if neigung >= 45: factor *= 0.90
    if "Dünn" in hakentyp: factor *= 1.05
    
    abstand = int(base_abstand * factor)
    rand = int(base_rand * factor)
    
    # Επίπεδο Δυσκολίας
    difficulty = "NORMAL"
    if data["sk"] > 1.2 or data["windzone"] >= 3:
        difficulty = "HOCH (ΥΨΗΛΟ ΦΟΡΤΙΟ)"
    
    return abstand, rand, difficulty, data["sk"], data["windzone"]

# --- ΕΜΦΑΝΙΣΗ ΑΠΟΤΕΛΕΣΜΑΤΩΝ ---
if st.button("BERECHNEN (ΥΠΟΛΟΓΙΣΜΟΣ)"):
    abstand, rand, diff, sk, wz = calculate_pv()
    
    st.markdown(f"""
    <div class="result-box">
        <h3>📊 ΑΠΟΤΕΛΕΣΜΑΤΑ (RESULTS)</h3>
        <p>📏 <b>Schienenabstand:</b> {abstand} cm</p>
        <p>↔️ <b>Randabstand:</b> {rand} cm</p>
        <p>❄️ <b>Schneelast (sk):</b> {sk} kN/m²</p>
        <p>💨 <b>Windzone:</b> {wz}</p>
        <hr>
        <h3 style='color: #06B6D4;'>STATUS: {diff}</h3>
    </div>
    """, unsafe_allow_html=True)

st.info("💡 Αυτό το εργαλείο βασίζεται στις προδιαγραφές του προγράμματος AURELIAN για τη Γερμανία.")