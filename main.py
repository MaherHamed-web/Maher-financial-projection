import streamlit as st
import pandas as pd

# Language selection
language = st.radio("Select Language / اختر اللغة", ["English", "العربية"])

# Define text for English and Arabic
text = {
    "English": {
        "title": "Interactive Financial Projection App",
        "subtitle": "Developed by Abdulaziz Alerwi",
        "toggle_comparison": "Enable Comparison Between Scenarios",
        "scenario_1": "Scenario 1",
        "scenario_2": "Scenario 2",
        "starting_amount": "Starting Amount ($)",
        "contribution_type": "Contribution Frequency",
        "monthly_contribution": "Monthly",
        "yearly_contribution": "Yearly",
        "contribution_amount": "Contribution Amount ($)",
        "monthly_addition": "Monthly Addition ($)",
        "yearly_addition": "Yearly Addition ($)",
        "monthly_growth_rate": "Monthly Growth Rate (%)",
        "projection_months": "Number of Months",
        "inflation_rate": "Annual Inflation Rate (%)",
        "savings_goal": "Savings Goal ($)",
        "final_balance": "Final Balance ($):",
        "total_contributions": "Total Contributions ($):",
        "total_growth": "Total Growth ($):",
        "goal_achieved": "You can achieve your savings goal by month:",
        "goal_not_achieved": "You cannot achieve your savings goal with the current inputs.",
        "break_even": "Growth surpasses contributions at month:",
        "projection_table": "Projection Table",
        "final_balance_chart": "Final Balance Distribution",
        "chart_title": "Projection Chart",
        "comparison_chart": "Comparison Chart",
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
        "subtitle": "تم التطوير بواسطة عبدالعزيز العروي",
        "toggle_comparison": "تمكين المقارنة بين السيناريوهات",
        "scenario_1": "السيناريو 1",
        "scenario_2": "السيناريو 2",
        "starting_amount": "المبلغ الابتدائي (ريال)",
        "contribution_type": "نوع المساهمة",
        "monthly_contribution": "شهري",
        "yearly_contribution": "سنوي",
        "contribution_amount": "قيمة المساهمة (ريال)",
        "monthly_addition": "المساهمة الشهرية (ريال)",
        "yearly_addition": "المساهمة السنوية (ريال)",
        "monthly_growth_rate": "نسبة النمو الشهرية (%)",
        "projection_months": "عدد الأشهر",
        "inflation_rate": "معدل التضخم السنوي (%)",
        "savings_goal": "الهدف الادخاري (ريال)",
        "final_balance": "الرصيد النهائي (ريال):",
        "total_contributions": "إجمالي المساهمات (ريال):",
        "total_growth": "إجمالي النمو (ريال):",
        "goal_achieved": "يمكنك تحقيق هدفك الادخاري في الشهر:",
        "goal_not_achieved": "لن تتمكن من تحقيق هدفك الادخاري بناءً على المدخلات الحالية.",
        "break_even": "النمو يتجاوز المساهمات في الشهر:",
        "projection_table": "الجدول التوقعي",
        "final_balance_chart": "توزيع الرصيد النهائي",
        "chart_title": "الرسم البياني للتوقعات",
        "comparison_chart": "مخطط المقارنة",
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

# Contribution frequency selection
contribution_type = st.radio(t["contribution_type"], [t["monthly_contribution"], t["yearly_contribution"]])

# Define the contribution input based on the selected frequency
if contribution_type == t["monthly_contribution"]:
    contribution_frequency = 12  # Monthly contributions
    contribution_label = t["monthly_addition"]
else:
    contribution_frequency = 1  # Yearly contributions
    contribution_label = t["yearly_addition"]

# Toggle for comparison
enable_comparison = st.checkbox(t["toggle_comparison"])

# Comparison Mode
if enable_comparison:
    # Inputs for Scenario 1
    st.header(t["scenario_1"])
    starting_amount_1 = st.number_input(f"{t['starting_amount']} ({t['scenario_1']})", value=30000, step=1000, key="s1_start")
    contribution_amount_1 = st.number_input(f"{contribution_label} ({t['scenario_1']})", value=1000, step=100, key="s1_add")
    monthly_growth_rate_1 = st.number_input(f"{t['monthly_growth_rate']} ({t['scenario_1']})", value=2.0, step=0.1, key="s1_growth") / 100
    projection_months_1 = st.number_input(f"{t['projection_months']} ({t['scenario_1']})", value=200, step=1, key="s1_months")

    # Inputs for Scenario 2
    st.header(t["scenario_2"])
    starting_amount_2 = st.number_input(f"{t['starting_amount']} ({t['scenario_2']})", value=30000, step=1000, key="s2_start")
    contribution_amount_2 = st.number_input(f"{contribution_label} ({t['scenario_2']})", value=1500, step=100, key="s2_add")
    monthly_growth_rate_2 = st.number_input(f"{t['monthly_growth_rate']} ({t['scenario_2']})", value=3.0, step=0.1, key="s2_growth") / 100
    projection_months_2 = st.number_input(f"{t['projection_months']} ({t['scenario_2']})", value=200, step=1, key="s2_months")

    # Adjust contribution frequency for Scenario 1
    adjusted_contribution_1 = contribution_amount_1 / contribution_frequency
    adjusted_contribution_2 = contribution_amount_2 / contribution_frequency

    # Projection calculations for both scenarios
    months_1 = list(range(1, int(projection_months_1) + 1))
    balances_1 = [starting_amount_1]
    for month in months_1[1:]:
        balances_1.append(balances_1[-1] * (1 + monthly_growth_rate_1) + adjusted_contribution_1)

    months_2 = list(range(1, int(projection_months_2) + 1))
    balances_2 = [starting_amount_2]
    for month in months_2[1:]:
        balances_2.append(balances_2[-1] * (1 + monthly_growth_rate_2) + adjusted_contribution_2)

    # Combine results into a DataFrame
    comparison_df = pd.DataFrame({
        t["month"]: months_1 if len(months_1) > len(months_2) else months_2,
        t["balance_scenario_1"]: balances_1 + [None] * (len(months_2) - len(balances_1)),
        t["balance_scenario_2"]: balances_2 + [None] * (len(months_1) - len(balances_2)),
    })

    # Display comparison table and chart
    st.subheader(t["projection_table"])
    st.write(comparison_df)
    st.subheader(t["comparison_chart"])
    st.line_chart(comparison_df.set_index(t["month"]))

    # Allow CSV download
    csv = comparison_df.to_csv(index=False).encode('utf-8')
    st.download_button(label=t["download_csv"], data=csv, file_name="comparison_table.csv", mime="text/csv")
else:
    # Inputs for Single Scenario
    starting_amount = st.number_input(t["starting_amount"], value=30000, step=1000)
    contribution_amount = st.number_input(contribution_label, value=1000, step=100)
    monthly_growth_rate = st.number_input(t["monthly_growth_rate"], value=2.0, step=0.1, min_value=0.0, max_value=10.0) / 100
    projection_months = st.number_input(t["projection_months"], value=200, step=1, min_value=1, max_value=300)

    # Adjust contribution frequency
    adjusted_contribution = contribution_amount / contribution_frequency

    # Projection calculation
    months = list(range(1, int(projection_months) + 1))
    balances = [starting_amount]
    for month in months[1:]:
        balances.append(balances[-1] * (1 + monthly_growth_rate) + adjusted_contribution)

    # Summary statistics
    total_contributions = adjusted_contribution * projection_months
    total_growth = balances[-1] - (starting_amount + total_contributions)
    break_even_month = next((i for i, b in enumerate(balances) if b >= total_contributions), None)

    # Display summary statistics
    st.subheader(t["projection_table"])
    st.write(f"**{t['final_balance']}** {balances[-1]:,.2f}")
    st.write(f"**{t['total_contributions']}** {total_contributions:,.2f}")
    st.write(f"**{t['total_growth']}** {total_growth:,.2f}")
    if break_even_month:
        st.write(f"**{t['break_even']}** {break_even_month}")
