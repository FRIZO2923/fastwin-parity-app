import streamlit as st
import random
from datetime import datetime
import pytz

# --- Session Setup ---
if "page" not in st.session_state:
    st.session_state.page = "home"

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

# --- Page Navigation ---
if st.session_state.page == "home":
    st.set_page_config(layout="centered")
    st.title("🎮 Welcome to Frizo Games")
    st.markdown(f"💰 **Current Balance**: ₹{st.session_state.balance:.2f}")
    st.markdown("---")
    st.subheader("🎲 Choose a Game")

    if st.button("🚀 Play Fast Parity"):
        st.session_state.page = "fast_parity"

elif st.session_state.page == "fast_parity":
    st.title("🚀 Fast-Parity Game")
    period, countdown = get_current_ist_period()

    st.markdown(f"### 🎲 Period: {period}")
    st.markdown(f"⏳ Countdown: **{countdown} seconds**")
    st.markdown(f"💰 Available Balance: ₹{st.session_state.balance:.2f}")

    st.markdown("---")
    st.write("### Place Your Bet")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🟢 Join Green"):
            st.session_state.bet_choice = "Green"
    with col2:
        if st.button("🟣 Join Violet"):
            st.session_state.bet_choice = "Violet"
    with col3:
        if st.button("🔴 Join Red"):
            st.session_state.bet_choice = "Red"

    if "bet_choice" in st.session_state:
        st.markdown(f"#### Selected: {st.session_state.bet_choice}")
        amount = st.selectbox("Select Contract Money", [10, 100, 1000])
        number = st.number_input("Select a Number (0–9)", min_value=0, max_value=9, step=1)
        if st.button("✅ Confirm Bet"):
            if st.session_state.balance >= amount:
                st.session_state.balance -= amount
                st.session_state.fast_parity_bets.append({
                    "period": period,
                    "choice": st.session_state.bet_choice,
                    "amount": amount,
                    "number": number
                })
                st.success(f"Bet confirmed on {st.session_state.bet_choice} with ₹{amount} and number {number}!")
            else:
                st.error("Insufficient balance!")

    st.markdown("---")
    st.write("### 🎯 Latest Result")
    if len(st.session_state.fast_parity_results) > 0:
        last = st.session_state.fast_parity_results[-1]
        st.info(f"Result for Period {last['period']}: Number = {last['number']} | Color = {last['color']}")

    st.markdown("---")
    st.write("### 📜 Bet History")
    for b in reversed(st.session_state.fast_parity_bets[-5:]):
        st.write(f"Period {b['period']} - {b['choice']} | ₹{b['amount']} | Number: {b['number']}")

    # Auto-generate result (mock)
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

    st.markdown("---")
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"

