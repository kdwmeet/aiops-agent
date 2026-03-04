import streamlit as st
import pandas as pd
from app.analyzer import analyze_log_content

st.set_page_config(page_title="AIOps Log Analyzer", layout="wide")

st.title("서버 장애 예측 및 로그 분석기")
st.caption("복잡한 서버 로그 파일을 업로드하면 AI가 장애 원인을 분석하고 해결책을 제안합니다.")
st.divider()

# --- 사이드바: 로그 업로드 ---
with st.sidebar:
    st.header("로그 파일 입력")
    uploaded_file = st.file_uploader("서버 로그 (.log, .txt)", type=["log", "txt"])

    analzyze_btn = st.button("로그 분석 시작", type="primary")

# --- 메인: 분석 결과 ---
if analzyze_btn and uploaded_file:
    # 파일 읽기 (바이트 -> 문자열 디코딩)
    try:
        log_content = uploaded_file.read().decode("utf-8")
    except:
        st.error("파일을 읽을 수 없습니다. UTF-8 인코딩인지 확인해주세요.")
        st.stop()

    # 로그 미리보기
    with st.expander("원본 로그 파일 미리보기 (마지막 20줄)"):
        st.code("\n".join(log_content.splitlines()[-20:]))

    with st.spinner("SRE AI가 로그 패턴을 분석하고 있습니다..."):
        result = analyze_log_content(log_content)

        if "error" in result:
            st.error("분석 중 오류가 발생했습니다.")
            st.write(result["raw"])
        else:
            # 상태 대시보드
            status = result.get("status", "Healthy")
            color = "red" if status == "Critical" else "orange" if status == "Warning" else "green"

            st.markdown(f"### 진단 결과: :{color}[{status}]")
            st.info(f"**요약:** {result.get('summary')}")

            st.divider()

            col1, col2 = st.columns(2)

            # 감지된 패턴
            with col1:
                st.subheader("감지된 이상 징후")
                patterns = result.get("detected_patterns", [])
                if patterns:
                    for p in patterns:
                        st.warning(f"- {p}")

                else:
                    st.success("특이 사항 없음")
            
            # 원인 및 해결책
            with col2:
                st.subheader("원인 분석 및 해결책")
                st.markdown(f"**Root Cause:**\n{result.get('root_cause')}")
                st.markdown(f"**Action Item:**")
                st.code(result.get('recommendation'), language="bash")