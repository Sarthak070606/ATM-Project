import streamlit as st

class Account:
    def __init__(self, accNo, pin, balance):
        self.accNo = accNo
        self.pin = pin
        self.balance = balance
        self.history = []

    def getAccNo(self):
        return self.accNo

    def getPin(self):
        return self.pin

    def getBalance(self):
        return self.balance

    def deposit(self, amount):
        self.balance += amount
        self._addHistory(f"Deposit: Rs. {amount}")
        return True

    def withdraw(self, amount):
        if amount % 100 != 0:
            return "❌ Amount must be in multiples of 100!"
        elif amount > (self.balance - 500):
            return "❌ Insufficient balance! Minimum Rs. 500 must remain."
        else:
            self.balance -= amount
            self._addHistory(f"Withdraw: Rs. {amount}")
            return "✅ Withdrawal successful! Collect your cash."

    def printBalance(self):
        return f"💰 Current Balance: Rs. {self.balance:.2f}"

    def showHistory(self):
        if not self.history:
            return ["No transactions yet."]
        return self.history

    def _addHistory(self, msg):
        if len(self.history) >= 5:
            self.history.pop(0)  # keep last 5
        self.history.append(msg)


# ===============================
# ATM Class
# ===============================
class ATM:
    def __init__(self):
        self.accounts = [
            Account(1001, 2006, 2000000.55),
            Account(1002, 2007, 50000.00),
            Account(1003, 2008, 10000.75),
            Account(1004, 2009, 100010.75),
            Account(1005, 2010, 100000.75)
            
            
        ]
        self.currentUser = None

    def login(self, accNo, pin):
        for acc in self.accounts:
            if acc.getAccNo() == accNo and acc.getPin() == pin:
                self.currentUser = acc
                return True
        return False


# ===============================
# Streamlit UI
# ===============================
st.set_page_config(page_title="ATM Machine", page_icon="🏦", layout="centered")

st.title("🏦 ATM Machine Simulator")

# Initialize ATM in session state
if "atm" not in st.session_state:
    st.session_state.atm = ATM()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

atm = st.session_state.atm

# ===============================
# LOGIN PAGE
# ===============================
if not st.session_state.logged_in:
    st.subheader("🔐 Login to your account")
    accNo = st.number_input("Enter Account Number", min_value=1000, max_value=9999, step=1)
    pin = st.text_input("Enter PIN", type="password")
    
    if pin.isdigit():
        pin = int(pin)
    else:
        pin = None



    if st.button("Login"):
        if atm.login(accNo, pin):
            st.session_state.logged_in = True
            st.success(f"✅ Login successful! Welcome, Account {accNo}")
        else:
            st.error("❌ Invalid Account Number or PIN!")

# ===============================
# ATM MENU
# ===============================
else:
    st.subheader("💳 ATM Menu")

    menu = st.radio("Choose an option", [
        "Balance Inquiry",
        "Cash Withdrawal",
        "Cash Deposition",
        "Transaction History",
        "Logout"
    ])

    user = atm.currentUser

    if menu == "Balance Inquiry":
        st.info(user.printBalance())

    elif menu == "Cash Withdrawal":
        amt = st.number_input("Enter amount to withdraw (Rs.)", min_value=100, step=100)
        if st.button("Withdraw"):
            result = user.withdraw(amt)
            if "✅" in result:
                st.success(result)
            else:
                st.error(result)

    elif menu == "Cash Deposition":
        amt = st.number_input("Enter amount to deposit (Rs.)", min_value=100, step=100)
        if st.button("Deposit"):
            user.deposit(amt)
            st.success("✅ Deposit successful!")

    elif menu == "Transaction History":
        st.write("📝 Last 5 Transactions:")
        for i, record in enumerate(user.showHistory(), 1):
            st.text(f"{i}. {record}")

    elif menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.atm.currentUser = None
        st.success("✅ Logged out successfully!")


