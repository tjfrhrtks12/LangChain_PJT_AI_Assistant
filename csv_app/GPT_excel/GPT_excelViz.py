# 🗂 구성 요약
# 📋 미리보기  	업로드한 엑셀 테이블 확인
# 📊 막대그래프	제품별 총 판매수량
# 🥧 파이차트 	지역별 판매 비중
# 🔥 히트맵	    제품 vs 부서별 판매현황


import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

# ✅ 한글 폰트 설정
if platform.system() == "Windows":
    plt.rcParams["font.family"] = "Malgun Gothic"  # 윈도우용
else:
    plt.rcParams["font.family"] = "AppleGothic"  # 맥용
plt.rcParams["axes.unicode_minus"] = False

# ✅ Streamlit 페이지 설정
st.set_page_config(page_title="📊 더존비즈온 Q4 GPT 데이터 분석", page_icon="🎯")
st.title("🎯 제품별 판매수량 시각화 분석")
st.markdown("엑셀 파일 업로드 후 분석 그래프를 확인하세요! 📈")

# ✅ 파일 업로드
uploaded_file = st.file_uploader("📁 엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("🧾 업로드된 데이터 미리보기")
    st.dataframe(df)

    # ✅ 1. 제품별 판매수량 막대그래프
    st.subheader("📦 제품별 판매수량 막대그래프")
    plt.figure(figsize=(10, 5))
    sns.barplot(data=df, x="제품명", y="판매수량", errorbar="sd")
    plt.xlabel("제품명")
    plt.ylabel("판매수량")
    plt.title("제품별 판매수량")
    st.pyplot(plt.gcf())
    plt.clf()

    # ✅ 2. 지역별 판매 비율 원형그래프
    st.subheader("📍 지역별 판매 비율 (원형그래프)")
    region_counts = df["지역"].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(region_counts, labels=region_counts.index, autopct="%1.1f%%", startangle=140)
    plt.axis("equal")
    plt.title("지역별 판매 비율")
    st.pyplot(plt.gcf())
    plt.clf()

    # ✅ 3. 부서별 제품 판매 히트맵
    st.subheader("👥 부서별 제품 판매 히트맵")
    pivot_table = df.pivot_table(index="담당부서", columns="제품명", values="판매수량", aggfunc="sum", fill_value=0)
    plt.figure(figsize=(10, 5))
    sns.heatmap(pivot_table, annot=True, cmap="YlGnBu", fmt="d")
    plt.title("부서별 제품 판매 히트맵")
    st.pyplot(plt.gcf())
    plt.clf()



# 실행 명령어 : streamlit run csv_app/GPT_excelViz.py
