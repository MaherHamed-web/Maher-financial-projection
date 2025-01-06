import streamlit as st
import pandas as pd

# Language selection
language = st.radio("Select Language / اختر اللغة", ["English", "العربية"])

# Define text for English and Arabic
text = {
    "English": {
        "title": "Interactive Financial Projection App",
        "subtitle": "Developed by Abdulaziz Alerwi",
        "scenario_1": "Scenario 1",
        "scenario_2": "Scenario 2",
        "starting_amount": "Starting Amount ($)",
        "monthly_addition": "Monthly Addition ($)",
        "monthly_growth_rate": "Monthly Growth Rate (%)",
        "projection_months": "Number of Months",
        "projection_table": "Projection Table",
        "chart_title": "Projection Comparison Chart",
        "download_csv": "Download Comparison Table as CSV",
        "month": "Month",
        "balance_scenario_1": "Balance (Scenario 1)",
        "balance_scenario_2": "Balance (Scenario 2)",
    },
    "العربية": {
        "title": "تطبيق التوقعات المالية التفاعلية",
        "subtitle": "تم التطوير بواسطة عبدالعزيز العروي",
        "scenario_1": "السيناريو 1",
        "scenario_2": "السيناريو 2",
        "starting_amount": "المبلغ الابتدائي (ريال)",
        "monthly_addition": "المبلغ المضاف شهرياً (ريال)",
        "monthly_growth_rate": "نسبة النمو الشهرية (%)",
        "projection_months": "عدد الأشهر",
        "projection_table": "الجدول التوقعي",
        "chart_title": "مخطط مقارنة التوقعات",
        "download_csv": "تحميل جدول المقارنة بصيغة CSV",
        "month": "الشهر",
        "balance_scenario_1": "الرصيد (السيناريو 1)",
        "balance_scenario_2": "الرصيد (السيناريو 2)",
    }
}

# Use the selected language for all text
t = text[language]

# Add a title and subtitle
st.title(t["title"])
st.subheader(t["subtitle"])

# Inputs for Scenario 1
st.header(t["scenario_1"])
starting_amount_1 = st.number_input(f"{t['starting_amount']} ({t['scenario_1']})", value=30000, step=1000, key="s1_start")
monthly_addition_1 = st.number_input(f"{t['monthly_addition']} ({t['scenario_1']})", value=1000, step=100, key="s1_add")
monthly_growth_rate_1 = st.number_input(f"{t['monthly_growth_rate']} ({t['scenario_1']})", value=2.0, step=0.1, min_value=0.0, max_value=10.0, key="s1_growth") / 100
projection_months_1 = st.number_input(f"{t['projection_months']} ({t['scenario_1']})", value=200, step=1, min_value=1, max_value=300, key="s1_months")

# Inputs for Scenario 2
st.header(t["scenario_2"])
starting_amount_2 = st.number_input(f"{t['starting_amount']} ({t['scenario_2']})", value=30000, step=1000, key="s2_start")
monthly_addition_2 = st.number_input(f"{t['monthly_addition']} ({t['scenario_2']})", value=1500, step=100, key="s2_add")
monthly_growth_rate_2 = st.number_input(f"{t['monthly_growth_rate']} ({t['scenario_2']})", value=3.0, step=0.1, min_value=0.0, max_value=10.0, key="s2_growth") / 100
projection_months_2 = st.number_input(f"{t['projection_months']} ({t['scenario_2']})", value=200, step=1, min_value=1, max_value=300, key="s2_months")

# Calculate projections for Scenario 1
months_1 = list(range(1, int(projection_months_1) + 1))
balances_1 = []
current_balance_1 = starting_amount_1
for month in months_1:
    current_balance_1 = current_balance_1 * (1 + monthly_growth_rate_1) + monthly_addition_1
    balances_1.append(current_balance_1)

# Calculate projections for Scenario 2
months_2 = list(range(1, int(projection_months_2) + 1))
balances_2 = []
current_balance_2 = starting_amount_2
for month in months_2:
    current_balance_2 = current_balance_2 * (1 + monthly_growth_rate_2) + monthly_addition_2
    balances_2.append(current_balance_2)

# Combine both scenarios into one DataFrame for comparison
max_months = max(len(months_1), len(months_2))
comparison_data = pd.DataFrame({
    t["month"]: list(range(1, max_months + 1)),
    t["balance_scenario_1"]: balances_1 + [None] * (max_months - len(balances_1)),
    t["balance_scenario_2"]: balances_2 + [None] * (max_months - len(balances_2)),
})

# Display the comparison table
st.subheader(t["projection_table"])
st.write(comparison_data)

# Display the comparison chart
st.subheader(t["chart_title"])
st.line_chart(comparison_data.set_index(t["month"]))

# Allow the user to download the comparison table as a CSV file
csv = comparison_data.to_csv(index=False).encode('utf-8')
st.download_button(label=t["download_csv"], data=csv, file_name="comparison_projection.csv", mime="text/csv")
