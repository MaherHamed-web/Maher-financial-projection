import streamlit as st
import pandas as pd

# Title of the app
st.title("Interactive Financial Projection App")

# Add user inputs
starting_amount = st.number_input("Starting Amount ($)", value=30000, step=1000)
monthly_addition = st.number_input("Monthly Addition ($)", value=1000, step=100)
monthly_growth_rate = st.slider("Monthly Growth Rate (%)", min_value=0.0, max_value=10.0, value=2.0) / 100
projection_months = st.slider("Number of Months", min_value=1, max_value=300, value=200, step=10)

# Calculate the financial projection
months = list(range(1, projection_months + 1))
balances = []
current_balance = starting_amount
for month in months:
    current_balance = current_balance * (1 + monthly_growth_rate) + monthly_addition
    balances.append(current_balance)

# Display the results in a table
data = pd.DataFrame({"Month": months, "Balance ($)": [f"{int(balance):,}" for balance in balances]})
st.subheader("Projection Table")
st.write(data)

# Allow the user to download the table as a CSV file
csv = data.to_csv(index=False).encode('utf-8')
st.download_button(label="Download Projection as CSV", data=csv, file_name="financial_projection.csv", mime="text/csv")

# Display the results in a chart
st.subheader("Projection Chart")
st.line_chart(data.set_index("Month"))