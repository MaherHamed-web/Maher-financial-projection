import streamlit as st
import pandas as pd

# Add a title to the app
st.title("تطبيق التوقعات المالية التفاعلية")
st.subheader("تم التطوير بواسطةعبدالعزيزالعروي ")

# Add user inputs (all as input fields)
starting_amount = st.number_input("المبلغ الابتدائي (ريال)", value=30000, step=1000)
monthly_addition = st.number_input("المبلغ المضاف شهرياً (ريال)", value=1000, step=100)
monthly_growth_rate = st.number_input("نسبة النمو الشهرية (%)", value=2.0, step=0.1, min_value=0.0, max_value=10.0) / 100
projection_months = st.number_input("عدد الأشهر", value=200, step=1, min_value=1, max_value=300)

# Calculate the financial projection
months = list(range(1, int(projection_months) + 1))
balances = []
current_balance = starting_amount
for month in months:
    current_balance = current_balance * (1 + monthly_growth_rate) + monthly_addition
    balances.append(current_balance)

# Display the results in a table
data = pd.DataFrame({"الشهر": months, "الرصيد (ريال)": [int(balance) for balance in balances]})
st.subheader("الجدول التوقعي")
st.write(data)

# Display the results in a chart (using Streamlit's built-in charting)
st.subheader("الرسم البياني للتوقعات")
st.line_chart(data.set_index("الشهر"))

# Allow the user to download the table as a CSV file
csv = data.to_csv(index=False).encode('utf-8')
st.download_button(label="تحميل الجدول بصيغة CSV", data=csv, file_name="التوقعات_المالية.csv", mime="text/csv")
