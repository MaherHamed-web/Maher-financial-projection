import streamlit as st
import pandas as pd

# Language selection
language = st.radio("Select Language / اختر اللغة", ["English", "العربية"])

# Define text for English and Arabic
text = {
    "English": {
        "title": "Interactive Financial Projection App",
        "subtitle": "Developed by Abdulaziz Alerwi )",
        "starting_amount": "Starting Amount ($)",
        "monthly_addition": "Monthly Addition ($)",
        "monthly_growth_rate": "Monthly Growth Rate (%)",
        "projection_months": "Number of Months",
        "inflation_rate": "Annual Inflation Rate (%)",
        "savings_goal": "Savings Goal ($)",
        "final_balance": "Final Balance ($):",
        "total_contributions": "Total Contributions ($):",
        "total_growth": "Total Growth ($):",
        "goal_achieved": "You can achieve your savings goal by month:",
        "goal_not_achieved": "You cannot achieve your savings goal with the current inputs.",
        "projection_table": "Projection Table",
        "final_balance_chart": "Final Balance Distribution",
        "chart_title": "Projection Chart",
        "download_csv": "Download Table as CSV",
        "month": "Month",
        "balance": "Balance ($)",
        "inflation_adjusted_balance": "Inflation-Adjusted Balance ($)",
        "source": "Source",
        "contributions": "Contributions",
        "growth": "Growth",
    },
    "العربية": {
        "title": "تطبيق التوقعات المالية التفاعلية",
        "subtitle": "تم التطوير بواسطة عبدالعزيز العروي ",
        "starting_amount": "المبلغ الابتدائي (ريال)",
        "monthly_addition": "المبلغ المضاف شهرياً (ريال)",
        "monthly_growth_rate": "نسبة النمو الشهرية (%)",
        "projection_months": "عدد الأشهر",
        "inflation_rate": "معدل التضخم السنوي (%)",
        "savings_goal": "الهدف الادخاري (ريال)",
        "final_balance": "الرصيد النهائي (ريال):",
        "total_contributions": "إجمالي المساهمات (ريال):",
        "total_growth": "إجمالي النمو (ريال):",
        "goal_achieved": "يمكنك تحقيق هدفك الادخاري في الشهر:",
        "goal_not_achieved": "لن تتمكن من تحقيق هدفك الادخاري بناءً على المدخلات الحالية.",
        "projection_table": "الجدول التوقعي",
        "final_balance_chart": "توزيع الرصيد النهائي",
        "chart_title": "الرسم البياني للتوقعات",
        "download_csv": "تحميل الجدول بصيغة CSV",
        "month": "الشهر",
        "balance": "الرصيد (ريال)",
        "inflation_adjusted_balance": "الرصيد بعد التضخم (ريال)",
        "source": "المصدر",
        "contributions": "المساهمات",
        "growth": "النمو",
    }
}

# Use the selected language for all text
t = text[language]

# Add a title and subtitle
st.title(t["title"])
st.subheader(t["subtitle"])

# Add user inputs
starting_amount = st.number_input(t["starting_amount"], value=30000, step=1000)
monthly_addition = st.number_input(t["monthly_addition"], value=1000, step=100)
monthly_growth_rate = st.number_input(t["monthly_growth_rate"], value=2.0, step=0.1, min_value=0.0, max_value=10.0) / 100
projection_months = st.number_input(t["projection_months"], value=200, step=1, min_value=1, max_value=300)
inflation_rate = st.number_input(t["inflation_rate"], value=2.0, step=0.1, min_value=0.0) / 100
savings_goal = st.number_input(t["savings_goal"], value=500000, step=1000)

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

st.subheader(t["projection_table"])
st.write(f"**{t['final_balance']}** {int(balances[-1]):,}")
st.write(f"**{t['total_contributions']}** {int(total_contributions):,}")
st.write(f"**{t['total_growth']}** {int(total_growth):,}")
if goal_month:
    st.write(f"**{t['goal_achieved']}** {goal_month}")
else:
    st.write(f"**{t['goal_not_achieved']}**")

# Display the results in a table
data = pd.DataFrame({
    t["month"]: months,
    t["balance"]: [int(balance) for balance in balances],
    t["inflation_adjusted_balance"]: [int(balance) for balance in inflation_adjusted_balances]
})
st.write(data)

# Visualize contributions vs. growth
contribution_vs_growth = pd.DataFrame({
    t["source"]: [t["contributions"], t["growth"]],
    t["balance"]: [total_contributions, total_growth]
})
st.subheader(t["final_balance_chart"])
st.bar_chart(contribution_vs_growth.set_index(t["source"]))

# Display the results in a chart
st.subheader(t["chart_title"])
st.line_chart(data.set_index(t["month"])[[t["balance"], t["inflation_adjusted_balance"]]])

# Allow the user to download the table as a CSV file
csv = data.to_csv(index=False).encode('utf-8')
st.download_button(label=t["download_csv"], data=csv, file_name="financial_projection.csv", mime="text/csv")
