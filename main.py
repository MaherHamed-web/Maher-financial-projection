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
        "savings_goal": "Savings Goal ($)",
        "goal_reached_in": "You can reach your goal in",
        "goal_unreachable": "The goal is not reachable with the current inputs.",
        "goal_months": "months.",
        "final_balance": "Final Balance ($):",
        "total_contributions": "Total Contributions ($):",
        "total_growth": "Total Growth ($):",
        "break_even": "Growth surpasses contributions at month:",
        "projection_table": "Projection Table",
        "chart_title": "Projection Chart",
        "download_csv": "Download Table as CSV",
        "month": "Month",
        "balance": "Balance ($)",
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
        "savings_goal": "الهدف الادخاري (ريال)",
        "goal_reached_in": "يمكنك تحقيق الهدف في",
        "goal_unreachable": "لا يمكن تحقيق الهدف مع المدخلات الحالية.",
        "goal_months": "أشهر.",
        "final_balance": "الرصيد النهائي (ريال):",
        "total_contributions": "إجمالي المساهمات (ريال):",
        "total_growth": "إجمالي النمو (ريال):",
        "break_even": "النمو يتجاوز المساهمات في الشهر:",
        "projection_table": "الجدول التوقعي",
        "chart_title": "الرسم البياني للتوقعات",
        "download_csv": "تحميل الجدول بصيغة CSV",
        "month": "الشهر",
        "balance": "الرصيد (ريال)",
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
if not enable_comparison:
    # Inputs for Single Scenario
    starting_amount = st.number_input(t["starting_amount"], value=30000, step=1000)
    contribution_amount = st.number_input(contribution_label, value=1000, step=100)
    monthly_growth_rate = st.number_input(t["monthly_growth_rate"], value=2.0, step=0.1, min_value=0.0, max_value=10.0) / 100
    projection_months = st.number_input(t["projection_months"], value=200, step=1, min_value=1, max_value=300)

    # Savings Goal
    savings_goal = st.number_input(t["savings_goal"], value=100000, step=1000)

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

    # Goal achievement calculation
    goal_month = next((i for i, b in enumerate(balances) if b >= savings_goal), None)

    # Display summary statistics
    st.subheader(t["projection_table"])
    st.write(f"**{t['final_balance']}** {balances[-1]:,.2f}")
    st.write(f"**{t['total_contributions']}** {total_contributions:,.2f}")
    st.write(f"**{t['total_growth']}** {total_growth:,.2f}")
    if break_even_month:
        st.write(f"**{t['break_even']}** {break_even_month}")
    if goal_month is not None:
        st.write(f"**{t['goal_reached_in']} {goal_month} {t['goal_months']}**")
    else:
        st.write(f"**{t['goal_unreachable']}**")

    # Chart for balances
    st.subheader(t["chart_title"])
    df = pd.DataFrame({t["month"]: months, t["balance"]: balances})
    st.line_chart(df.set_index(t["month"]))

    # Allow CSV download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label=t["download_csv"], data=csv, file_name="projection_table.csv", mime="text/csv")
