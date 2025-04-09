import streamlit as st
import random
from datetime import datetime, timedelta
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
st.set_page_config(layout="centered")
st.title("💰💸FRIZO WIN🏧💰")

# Navigation (Tab Simulation)
tab = st.selectbox("Select Tab", ["Home", "Fast-Parity"])

if tab == "Home":
    st.header("🏠 Home")
    st.markdown(f"### 💰 Balance: ₹{st.session_state.balance:.2f}")
    st.write("Enjoy games like Fast-Parity and more coming soon.")

    st.write("### Recharge Your Wallet")
    recharge_amount = st.number_input("Enter amount to recharge", min_value=10, max_value=10000, step=10)
    if st.button("Recharge Now"):
        st.session_state.balance += recharge_amount
        st.success(f"₹{recharge_amount} added to your balance!")

elif tab == "Fast-Parity":
    period, countdown = get_current_ist_period()

    # --- Admin Control (Hidden Panel) ---
    with st.expander("🛠 Admin Control Panel"):
        password = st.text_input("Enter admin password", type="password")
        if password == "yoursecret123":  # <-- change this to your own password
            custom_result = st.number_input("Set next result manually (0–9)", min_value=0, max_value=9)
            apply_custom = st.checkbox("✅ Use custom result for next round")
            st.session_state.admin_control = {
                "use_custom": apply_custom,
                "custom_result": custom_result
            }
        else:
            st.warning("Enter correct password to access controls.")

    st.subheader(f"🎲 Period: {period}")
    st.markdown(f"⏳ Countdown: **{countdown} seconds**")
    st.markdown(f"### 💰 Available Balance: ₹{st.session_state.balance:.2f}")

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
    st.write("### 📜 Bet History")
    for b in reversed(st.session_state.fast_parity_bets[-5:]):
        st.write(f"Period {b['period']} - {b['choice']} | ₹{b['amount']} | Number: {b['number']}")

    # --- Auto-generate result every minute (for simulation only) ---
    if countdown == 1:
        # Use admin result if set
        if "admin_control" in st.session_state and st.session_state.admin_control.get("use_custom"):
            num = st.session_state.admin_control["custom_result"]
        else:
            num = get_random_result()

        color = determine_color(num)
        st.session_state.fast_parity_results.append({
            "period": period,
            "number": num,
            "color": color
        })

        # --- Payout simulation (simple logic) ---
        for bet in st.session_state.fast_parity_bets:
            if bet["period"] == period:
                if color == bet["choice"]:
                    multiplier = 2 if color in ["Red", "Green"] else 4.5
                    winnings = int(bet["amount"] * multiplier)
                    st.session_state.balance += winnings
                    st.toast(f"🎉 You won ₹{winnings} on {color}!")

        # Clear period bets
        st.session_state.fast_parity_bets = []
