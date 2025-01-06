import streamlit as st
import pandas as pd

# Add a title to the app
st.title("تطبيق التوقعات المالية التفاعلية")
st.subheader("تم التطوير بواسطة عبدالعزيز العروي ")

# Add user inputs
starting_amount = st.number_input("المبلغ الابتدائي (ريال)", value=30000, step=1000)
monthly_addition = st.number_input("المبلغ المضاف شهرياً (ريال)", value=1000, step=100)
monthly_growth_rate = st.number_input("نسبة النمو الشهرية (%)", value=2.0, step=0.1, min_value=0.0, max_value=10.0) / 100
projection_months = st.number_input("عدد الأشهر", value=200, step=1, min_value=1, max_value=300)

# Optional: Inflation rate
inflation_rate = st.number_input("معدل التضخم السنوي (%)", value=2.0, step=0.1, min_value=0.0) / 100

# Optional: Savings goal
savings_goal = st.number_input("الهدف الادخاري (ريال)", value=500000, step=1000)

# Calculate the financial projection
months = list(range(1, int(projection_months) + 1))
balances = []
current_balance = starting_amount
for month in months:
    current_balance = current_balance * (1 + monthly_growth_rate) + monthly_addition
    balances.append(current_balance)

# Inflation-adjusted balances
inflation_adjusted_balances = [
    balance / ((1 + inflation_rate) ** (month / 12)) for month, balance in enumerate(balances, start=1)
]

# Determine if the savings goal is met and when
goal_month = None
if balances[-1] >= savings_goal:
    for month, balance in enumerate(balances, start=1):
        if balance >= savings_goal:
            goal_month = month
            break

# Display summary metrics
total_contributions = monthly_addition * projection_months
total_growth = balances[-1] - (starting_amount + total_contributions)

st.subheader("الإحصائيات")
st.write(f"**الرصيد النهائي (ريال):** {int(balances[-1]):,}")
st.write(f"**إجمالي المساهمات (ريال):** {int(total_contributions):,}")
st.write(f"**إجمالي النمو (ريال):** {int(total_growth):,}")
if goal_month:
    st.write(f"**يمكنك تحقيق هدفك الادخاري في الشهر {goal_month}.**")
else:
    st.write("**لن تتمكن من تحقيق هدفك الادخاري بناءً على المدخلات الحالية.**")

# Display the results in a table
data = pd.DataFrame({
    "الشهر": months,
    "الرصيد (ريال)": [int(balance) for balance in balances],
    "الرصيد بعد التضخم (ريال)": [int(balance) for balance in inflation_adjusted_balances]
})
st.subheader("الجدول التوقعي")
st.write(data)

# Visualize contributions vs. growth
contribution_vs_growth = pd.DataFrame({
    "المصدر": ["المساهمات", "النمو"],
    "القيمة (ريال)": [total_contributions, total_growth]
})
st.subheader("توزيع الرصيد النهائي")
st.bar_chart(contribution_vs_growth.set_index("المصدر"))

# Display the results in a chart
st.subheader("الرسم البياني للتوقعات")
st.line_chart(data.set_index("الشهر")[["الرصيد (ريال)", "الرصيد بعد التضخم (ريال)"]])

# Allow the user to download the table as a CSV file
csv = data.to_csv(index=False).encode('utf-8')
st.download_button(label="تحميل الجدول بصيغة CSV", data=csv, file_name="التوقعات_المالية.csv", mime="text/csv")
