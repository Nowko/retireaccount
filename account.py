import streamlit as st

def calculate_monthly_saving(target_amount, saving_years, annual_return):
    r = annual_return / 100 / 12  # 월 수익률
    n = saving_years * 12  # 총 저축 개월 수

    # 매달 저축할 금액 계산
    monthly_saving = target_amount * r / ((1 + r) ** n - 1)

    return round(monthly_saving)

# --- Streamlit 화면 구성 ---

st.markdown("### 📊 목표 금액 기반 저축 계산기")
st.markdown('<p style="color:gray; font-size:13px;">Made by <strong>NOWKO</strong> on Brunch</p>', unsafe_allow_html=True)
st.caption("목표 금액을 정하고, 저축 기간과 수익률을 입력하면 매달 얼마를 저축해야 하는지 계산합니다.")

# 입력값 받기
target_amount_million = st.number_input("목표 금액 (만원)", min_value=0, value=7200, step=100)
saving_years = st.number_input("저축 기간 (년)", min_value=1, value=30)
annual_return = st.number_input("연 수익률 (%)", min_value=0.0, value=2.7)

# 계산
if st.button("🧮 계산하기"):
    target_amount = target_amount_million * 10000  # 만원 → 원
    result = calculate_monthly_saving(target_amount, saving_years, annual_return)
    result_million = result / 10000
    st.subheader(f"👉 매달 저축해야 할 금액: **{result_million:,.1f}만 원**")
    st.caption("※ 복리 기준으로 매달 일정 금액을 저축할 경우, 목표 금액을 달성할 수 있습니다.")
