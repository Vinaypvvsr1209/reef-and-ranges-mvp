import streamlit as st
import pandas as pd

st.set_page_config(page_title="Reef & Ranges Tours - AI MVP", layout="wide")

# Core logic separated for testing
def check_availability(booked, capacity, requested):
    if requested <= 0:
        return False, "Invalid guest count."
    if (booked + requested) > capacity:
        return False, f"Double-booking prevented! Only {capacity - booked} seats left."
    return True, "Seats available! Booking confirmed."

def ai_faq_assistant(query):
    q = query.lower()
    if "pickup" in q or "time" in q:
        return "Hotel pickups in Cairns CBD run between 7:00 AM and 8:30 AM depending on your tour. Please wait outside 10 mins prior."
    elif "bring" in q or "pack" in q:
        return "Please bring reef-safe sunscreen, a towel, swimwear, a hat, a reusable water bottle, and a light rain jacket for rainforest tours."
    elif "weather" in q or "cancel" in q or "rain" in q:
        return "Safety first! If marine winds exceed 25 knots or severe weather occurs, we offer a 100% refund or free reschedule. (High-risk weather overrides are escalated to a human manager)."
    else:
        return "Confidence Low: I have flagged this enquiry for a human reservation agent to reply within 2 hours."

# Load synthetic data
@st.cache_data
def load_data():
    return pd.read_csv("tours_data.csv")

if "df" not in st.session_state:
    st.session_state.df = load_data()

st.title("🐠 Reef & Ranges Tours — AI Booking & FAQ Portal")
st.caption("Cairns, Queensland | Synthetic Prototype MVP")

# Sidebar Sign-in / Access Control (Required by Part 2)
st.sidebar.header("🔒 Staff Access Control")
role = st.sidebar.radio("Select Portal Mode:", ["Customer View (Public)", "Staff Admin (Sign-In)"])

is_authenticated = False
if role == "Staff Admin (Sign-In)":
    pwd = st.sidebar.text_input("Enter Staff Passcode:", type="password", help="Demo passcode: cairns2026")
    if pwd == "cairns2026":
        is_authenticated = True
        st.sidebar.success("Authenticated: Operations Manager")
    elif pwd:
        st.sidebar.error("Invalid passcode. Try: cairns2026")
    else:
        st.sidebar.info("Demo Passcode: `cairns2026`")

# Customer View
if role == "Customer View (Public)":
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💬 Instant AI Customer FAQ Assistant")
        st.write("Ask about pickup times, what to bring, or weather cancellations:")
        user_q = st.text_input("Your question:", placeholder="e.g., What should I bring for the reef tour?")
        if user_q:
            response = ai_faq_assistant(user_q)
            if "Confidence Low" in response:
                st.warning(response)
            else:
                st.info(response)

    with col2:
        st.subheader("📅 Live Tour Availability & Enquiry")
        df = st.session_state.df
        open_tours = df[df["status"] == "Open"]["tour_name"].tolist()
        selected_tour = st.selectbox("Select Tour:", open_tours)
        guests = st.number_input("Number of Guests:", min_value=1, max_value=15, value=2)
        customer_name = st.text_input("Your Full Name (Synthetic):")
        
        if st.button("Check & Hold Seats"):
            row = df[df["tour_name"] == selected_tour].iloc[0]
            ok, msg = check_availability(row["booked_seats"], row["max_capacity"], guests)
            if ok:
                st.session_state.df.loc[df["tour_name"] == selected_tour, "booked_seats"] += guests
                st.success(f"{msg} Reference generated for {customer_name or 'Guest'}.")
            else:
                st.error(msg)

# Staff View (Protected Data)
elif role == "Staff Admin (Sign-In)" and is_authenticated:
    st.subheader("📊 Live Manifest & Double-Booking Guard")
    st.dataframe(st.session_state.df, use_container_width=True)
    st.info("Human-in-the-loop: Weather Hold tours require manual manager approval before invoicing.")
