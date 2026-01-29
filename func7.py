import streamlit as st
import pandas as pd
import numpy as np
import time
from sklearn.metrics import mean_squared_error

# ==========================================
# 1. 화면 및 CSS 스타일 설정 (디지털 디자인)
# ==========================================
st.set_page_config(page_title="F1 Sim Score Match", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.cdnfonts.com/css/ds-digital');

.digital-dashboard {
    background-color: #000000;
    border: 4px solid #333;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.8);
    font-family: 'DS-Digital', sans-serif;
    color: white;
    width: 100%;
    margin-bottom: 20px;
}

.dashboard-title {
    font-family: sans-serif;
    color: #888;
    font-size: 14px;
    letter-spacing: 2px;
    margin-bottom: 10px;
    text-transform: uppercase;
}

.score-big {
    font-size: 120px;
    line-height: 120px;
    font-weight: bold;
}

.score-unit {
    font-size: 40px;
    color: #555;
    vertical-align: top;
    margin-left: 5px;
}

.dist-info {
    font-family: 'DS-Digital', sans-serif;
    color: #666;
    font-size: 24px;
    margin-top: 15px;
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏎️ Function 7: Similarity Score Match")

# ==========================================
# 2. 사이드바: 파일 업로드 기능 구현 (핵심 변경!)
# ==========================================
with st.sidebar:
    st.header("📂 Data Upload")
    st.write("팀원 코드로 추출한 CSV 파일을 업로드해주세요.")
    
    # [핵심] 파일 업로더 위젯 추가
    uploaded_ref = st.file_uploader("1. 기준 파일 (Reference)", type=['csv'])
    uploaded_tgt = st.file_uploader("2. 대상 파일 (Target)", type=['csv'])
    
    st.markdown("---")
    st.header("🎮 Controller")
    # 파일이 둘 다 있어야만 버튼이 활성화됨
    if uploaded_ref and uploaded_tgt:
        start_btn = st.button("▶️ Start Simulation", type="primary")
    else:
        st.info("파일 2개를 모두 업로드하면 시작 버튼이 나타납니다.")
        start_btn = False

# ==========================================
# 3. 데이터 로드 및 점수 계산 로직
# ==========================================
def process_uploaded_data(ref_file, tgt_file):
    try:
        # 업로드된 파일 객체를 바로 pandas로 읽음
        df_ref = pd.read_csv(ref_file)
        df_target = pd.read_csv(tgt_file)
        
        # 필수 컬럼 확인
        required = ['Distance', 'Speed']
        if not all(col in df_ref.columns for col in required):
            st.error(f"기준 파일에 필수 컬럼({required})이 없습니다.")
            return None
        if not all(col in df_target.columns for col in required):
            st.error(f"대상 파일에 필수 컬럼({required})이 없습니다.")
            return None
        
        # 거리 동기화
        dist_ref = df_ref['Distance'].values
        speed_ref = df_ref['Speed'].values
        dist_target = df_target['Distance'].values
        speed_target = df_target['Speed'].values
        
        max_dist = min(dist_ref.max(), dist_target.max())
        common_dist = np.arange(0, max_dist, 1)
        
        v_ref = np.interp(common_dist, dist_ref, speed_ref)
        v_target = np.interp(common_dist, dist_target, speed_target)
        
        # 점수 계산
        scores = []
        distances = []
        step = 100
        
        for i in range(step, len(common_dist), step):
            seg_ref = v_ref[i-step:i]
            seg_target = v_target[i-step:i]
            rmse = np.sqrt(mean_squared_error(seg_ref, seg_target))
            score = max(0, 100 - (rmse * 2))
            scores.append(score)
            distances.append(common_dist[i])
            
        return pd.DataFrame({'Distance': distances, 'Score': scores})

    except Exception as e:
        st.error(f"데이터 처리 중 오류 발생: {e}")
        return None

# ==========================================
# 4. 레이아웃 및 실행 로직
# ==========================================
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📋 Status")
    status_text = st.empty()
    
    if not uploaded_ref or not uploaded_tgt:
        status_text.warning("Waiting for CSV files...")
    else:
        status_text.info("Ready to analyze.")

with col2:
    dashboard_placeholder = st.empty()
    
    # 초기 대시보드 (OFF 상태)
    initial_html = """
    <div class="digital-dashboard">
        <div class="dashboard-title">Real-time Score</div>
        <div><span class="score-big" style="color: #333;">--</span><span class="score-unit">/100</span></div>
        <div class="dist-info">DIST: 0 M</div>
    </div>
    """
    dashboard_placeholder.markdown(initial_html, unsafe_allow_html=True)

# 시작 버튼 눌렀을 때 실행
if start_btn and uploaded_ref and uploaded_tgt:
    # 데이터 처리 함수 호출
    history_df = process_uploaded_data(uploaded_ref, uploaded_tgt)
    
    if history_df is not None:
        status_text.success(f"Processing... ({len(history_df)} segments)")
        progress_bar = st.progress(0)
        
        for idx, row in history_df.iterrows():
            score = row['Score']
            dist = row['Distance']
            
            # 색상 로직
            if score >= 90:
                color = "#00ff00"
                glow = "0 0 20px #00ff00, 0 0 40px #00ff00"
            elif score >= 70:
                color = "#ffffff"
                glow = "0 0 10px #ffffff"
            else:
                color = "#ff0000"
                glow = "0 0 20px #ff0000"
            
            # 대시보드 업데이트
            dashboard_html = f"""
            <div class="digital-dashboard">
                <div class="dashboard-title">Real-time Score</div>
                <div>
                    <span class="score-big" style="color: {color}; text-shadow: {glow};">
                        {int(score):02d}
                    </span>
                    <span class="score-unit">/100</span>
                </div>
                <div class="dist-info">DIST: {int(dist)} M</div>
            </div>
            """
            dashboard_placeholder.markdown(dashboard_html, unsafe_allow_html=True)
            progress_bar.progress((idx + 1) / len(history_df))
            time.sleep(0.1)
            
        status_text.success("Analysis Complete!")