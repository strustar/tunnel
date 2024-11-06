import streamlit as st

class In:
    pass

def sidebar():
    with st.sidebar:
        st.markdown('#### **✴️ :orange[제원]**')
        col = st.columns(3)
        with col[0]:
            In.lane_count = st.number_input('✨ :green[차로수]', min_value=1, max_value=5, value=2, step=1)
        with col[1]:
            In.lane_width = st.number_input('✨ :green[차로폭 [m]]', value=3.5, step=0.1, format='%0.1f')
        with col[2]:
            In.edge = st.number_input('✨ :green[측대 [m]]', value=0.25, step=0.005, format='%0.3f')

        col = st.columns(2)
        with col[0]:
            In.shoulder_left = st.number_input('✨ :green[좌측 길어깨 폭 [m]]', value=1.0, step=0.1, format='%0.1f')
        with col[1]:
            In.shoulder_right = st.number_input('✨ :green[우측 길어깨 폭 [m]]', value=2.5, step=0.1, format='%0.1f')

        st.markdown('---')
        st.markdown('#### **✴️ :orange[시설한계]**')
        col = st.columns(2)
        with col[0]:
            In.tunnel_height = st.number_input('✨ :green[높이 [m]]', value=4.8, step=0.1, format='%0.1f')
        with col[1]:
            In.tunnel_space = st.number_input('✨ :green[여유공간 [mm]]', value=50., step=0.1, format='%0.1f')

        st.markdown('#### **✴️ :orange[헌치 치수]**')
        col = st.columns(2)
        with col[0]:
            In.hunch_width = st.number_input('✨ :green[폭 [m]]', value=1.0, step=0.1, format='%0.1f')
        with col[1]:
            In.hunch_height = st.number_input('✨ :green[높이 [m]]', value=0.8, step=0.1, format='%0.1f')

        st.markdown('#### **✴️ :orange[차선 도색 및 편경사]**')
        col = st.columns(3)
        with col[0]:
            In.lane_marking_width = st.number_input('✨ :green[도색 폭 [mm]]', value=150.0, step=10.0, format='%0.1f')        
        with col[1]:
            In.lane_marking_height = st.number_input('✨ :green[도색 높이 [mm]]', value=50.0, step=5.0, format='%0.1f')        
        with col[2]:
            In.superelevation = st.number_input('✨ :green[편경사 [%]]', value=2.0, step=1.0, format='%0.1f')        

        st.markdown('#### **✴️ :orange[제트팬]**')
        col = st.columns(2)
        with col[0]:
            In.top_clearance = st.number_input('✨ :green[상단여유 [mm]]', value=200.0, step=10.0, format='%0.1f')
        with col[1]:
            In.jet_fan = st.selectbox('✨ :green[제트팬 규격 [mm] : 일반형]', ('⭕ 𝜙1030 (JF-1000)', '⭕ 𝜙1280 (JF-1250)', '⭕ 𝜙1530 (JF-1500)'), index = 1)

        st.markdown('#### **✴️ :orange[단면 결정]**')
        col = st.columns(2)
        with col[0]:
            In.center_height = st.number_input('✨ :green[중심 높이 [m]]', value=0.2, step=0.1, format='%0.1f')
        with col[1]:
            In.tunnel_radius = st.number_input('✨ :green[터널 반경 [m]]', value=6.8, step=0.1, format='%0.1f')

        st.markdown('#### **✴️ :orange[터널 연장]**')
        In.tunnel_length = st.radio('✨ :green[터널 연장 [m]]', ('1,000m 미만', '1,000~3,000m', '3,000m 이상'), index=1, horizontal=True, label_visibility='collapsed')
        txt = '기계환기, 기계환기 공동구 (표준)'
        if '미만' in In.tunnel_length:
            txt = '자연환기, 자연환기 공동구'
        if '이상' in In.tunnel_length:
            txt = '기계환기, 기계환기 공동구 (방재시설물 고려하여 확대)'
        st.markdown(f'###### **:blue[*{txt}]**')

        # temp = re.findall(r'\d+\.?\d*', jet_fan);    temp = [float(num) for num in temp];
        return In