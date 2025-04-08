import streamlit as st
import random
from datetime import datetime
import pytz

# --- Session Setup ---
if "balance" not in st.session_state:
    st.session_state.balance = 100

if "fast_parity_bets" not in st.session_state:
    st.session_state.fast_parity_bets = []

if "fast_parity_results" not in st.session_state:
    st.session_state.fast_parity_results = []

# --- Utility Functions ---
def get_current_ist_period():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)
    return now.strftime("%Y%m%d%H%M"), 60 - now.second

def get_random_result():
    return random.randint(0, 9)

def determine_color(num):
    if num == 0 or num == 5:
        return "Violet"
    elif num % 2 == 0:
        return "Green"
    else:
        return "Red"

# --- Layout Setup ---
st.set_page_config(layout="wide", page_title="Fast-Parity Game")
st.markdown("""
    <style>
    .main {
        background-color: #f4f4f4;
    }
    .bet-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        display: flex;
        justify-content: space-around;
        padding: 1rem 0;
        border-top: 1px solid #ccc;
    }
    .bottom-nav button {
        background: none;
        border: none;
        font-size: 18px;
        font-weight: bold;
        color: #444;
    }
    </style>
""", unsafe_allow_html=True)

# --- Tab Navigation ---
tab = st.sidebar.radio("Navigation", ["Home", "Fast-Parity", "Wallet"])

# --- Home Page ---
if tab == "Home":
    st.title("🎮 Welcome to Fastwin India")
    st.markdown("#### 💰 Balance: ₹{:.2f}".format(st.session_state.balance))
    st.markdown("---")
    st.markdown("### Choose Your Game")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Fast Parity"):
            st.session_state.page = "Fast-Parity"
    with col2:
        st.button("🔒 Coming Soon")

# --- Fast-Parity Game ---
elif tab == "Fast-Parity":
    period, countdown = get_current_ist_period()

    st.markdown("""
        <div class="bet-card">
    """, unsafe_allow_html=True)

    st.subheader(f"🎲 Period: {period}")
    st.markdown(f"⏳ Countdown: **{countdown} seconds**")
    st.markdown(f"### 💰 Available Balance: ₹{st.session_state.balance:.2f}")

    st.markdown("---")
    st.write("### 🔻 Place Your Bet")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🟢 Green", use_container_width=True):
            st.session_state.bet_choice = "Green"
    with col2:
        if st.button("🟣 Violet", use_container_width=True):
            st.session_state.bet_choice = "Violet"
    with col3:
        if st.button("🔴 Red", use_container_width=True):
            st.session_state.bet_choice = "Red"

    if "bet_choice" in st.session_state:
        st.success(f"Selected: {st.session_state.bet_choice}")
        amount = st.selectbox("💵 Select Contract Money", [10, 100, 1000])
        number = st.number_input("🔢 Select a Number (0–9)", min_value=0, max_value=9, step=1)
        if st.button("✅ Confirm Bet", use_container_width=True):
            if st.session_state.balance >= amount:
                st.session_state.balance -= amount
                st.session_state.fast_parity_bets.append({
                    "period": period,
                    "choice": st.session_state.bet_choice,
                    "amount": amount,
                    "number": number
                })
                st.success(f"Bet placed: ₹{amount} on {st.session_state.bet_choice} (Number {number})")
            else:
                st.error("Insufficient balance!")

    st.markdown("---")
    st.write("### 🎯 Latest Result")
    if len(st.session_state.fast_parity_results) > 0:
        last = st.session_state.fast_parity_results[-1]
        st.success(f"Period {last['period']}: Number = {last['number']} | Color = {last['color']}")
    else:
        st.info("Waiting for next result...")

    st.markdown("---")
    st.write("### 📜 Bet History")
    for b in reversed(st.session_state.fast_parity_bets[-5:]):
        st.markdown(f"🧾 Period {b['period']} — {b['choice']} | ₹{b['amount']} | Number: {b['number']}")

    # --- Auto-generate result every minute ---
    if countdown == 1:
        num = get_random_result()
        color = determine_color(num)
        st.session_state.fast_parity_results.append({
            "period": period,
            "number": num,
            "color": color
        })

        for bet in st.session_state.fast_parity_bets:
            if bet["period"] == period:
                if color == bet["choice"]:
                    multiplier = 2 if color in ["Red", "Green"] else 4.5
                    winnings = int(bet["amount"] * multiplier)
                    st.session_state.balance += winnings
                    st.toast(f"🎉 You won ₹{winnings} on {color}!")

        st.session_state.fast_parity_bets = []

    st.markdown("""</div>""", unsafe_allow_html=True)

# --- Wallet Page ---
elif tab == "Wallet":
    st.header("👛 Wallet")
    st.markdown(f"### 💰 Current Balance: ₹{st.session_state.balance:.2f}")
    recharge_amount = st.number_input("Enter amount to recharge", min_value=10, max_value=10000, step=10)
    if st.button("Recharge Now"):
        st.session_state.balance += recharge_amount
        st.success(f"₹{recharge_amount} added to your balance!")

# --- Bottom Navigation ---
st.markdown("""
    <div class="bottom-nav">
        <form action="/?tab=Home" method="get"><button>🏠 Home</button></form>
        <form action="/?tab=Fast-Parity" method="get"><button>🎯 Fast-Parity</button></form>
        <form action="/?tab=Wallet" method="get"><button>👛 Wallet</button></form>
    </div>
""", unsafe_allow_html=True)
