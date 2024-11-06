import plotly.graph_objects as go
import numpy as np
import streamlit as st
from sidebar import sidebar

st.set_page_config(page_title = "터널 단면 자동화", page_icon = "🚇", layout = "wide", initial_sidebar_state="expanded", )

# 상단 여백 줄이기 위한 CSS 스타일 추가
st.markdown("""
    <style>
        .block-container {
            padding-top: 3rem;
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        # [data-testid="stMarkdownContainer"] {
        #     margin-bottom: -20px;  # 이 값을 조정하여 간격 조절
        # }
    </style>
""", unsafe_allow_html=True)

In = sidebar()
total_width = In.lane_count * In.lane_width + In.shoulder_left + In.shoulder_right
if '1030' in In.jet_fan:
    jet_d1 = 1030
    jet_d2 = 1200
    jet_d3 = 1818    
elif '1280' in In.jet_fan:
    jet_d1 = 1280
    jet_d2 = 1450
    jet_d3 = 2218    
else:
    jet_d1 = 1530
    jet_d2 = 1750
    jet_d3 = 2668
jet_a = (jet_d3 - jet_d2)/2

col = st.columns(7)
with col[0]:
    check_center_line = st.checkbox('중심선 표시', value=True)
with col[1]:
    check_other_line = st.checkbox(':blue[기타선 표시]', value=True)
with col[2]:
    check_lane_marking = st.checkbox(':orange[차선 도색 표시]', value=True)
with col[3]:
    check_superelevation = st.checkbox('편경사 모두 표시', value=True)
with col[4]:
    check_tunnel_circle = st.checkbox('터널 점선원 표시', value=False)

family = 'sans-serif, Arial, Nanumgothic, Georgia'
def shape(fig, typ, x0,y0,x1,y1, fillcolor, color, width, **kargs):
    dash = 'solid'
    if len(kargs) > 0:  dash = kargs['LineStyle']            
    fig.add_shape(
        type=typ, x0=x0, y0=y0, x1=x1, y1=y1, fillcolor=fillcolor, opacity=1, layer='below',
        line=dict(color=color, width=width, dash=dash, ), )  # dash = solid, dot, dash, longdash, dashdot, longdashdot, '5px 10px'

def annotation(fig, x,y, color, txt, xanchor, yanchor, **kargs):
    bgcolor = None;  size = 18;  font_weight = 'bold'
    if len(kargs) > 0:  bgcolor = kargs['bgcolor'];  size = kargs['size']
    fig.add_annotation(
        x=x, y=y, text=txt, showarrow=False, bgcolor=bgcolor,
        font=dict(color=color, size=size, family=family, weight=font_weight),
        xanchor=xanchor, yanchor=yanchor, )
    
# 데이터 생성
box_x = [In.shoulder_left - In.edge, In.shoulder_left]
box_y = [0, 0]
for i in range(1, In.lane_count+1):
    box_x.append(In.shoulder_left + In.lane_width*i)
    box_y.append(0)
box_x.extend([total_width, total_width, total_width-In.hunch_width, In.shoulder_left, 0, 0])
box_y.extend([0, In.tunnel_height - In.hunch_height, In.tunnel_height, In.tunnel_height, In.tunnel_height - In.hunch_height, 0])

lane_temp = [In.shoulder_left] + [In.shoulder_left + In.lane_width * i for i in range(1, In.lane_count + 1)]
lane_x = [(value - In.lane_marking_width/2000, value + In.lane_marking_width/2000, value + In.lane_marking_width/2000, value - In.lane_marking_width/2000) for value in lane_temp]
lane_y = [(0, 0, In.lane_marking_height / 1000, In.lane_marking_height / 1000)]*len(lane_x)

def rotate_points(x, y, slope):
    x_center, y_center = total_width/2, 0  # 회전 중심점
    theta = np.arctan(slope/100)  # 회전 각도 계산 (라디안 단위)
    x_new = [];  y_new = []   # 회전된 좌표 리스트
    
    for x_val, y_val in zip(x, y):
        # 튜플 형태일 경우 각 항목별로 회전 적용
        if isinstance(x_val, tuple) and isinstance(y_val, tuple):
            x_rotated_pair = []
            y_rotated_pair = []
            for xv, yv in zip(x_val, y_val):
                x_rotated = x_center + (xv - x_center) * np.cos(theta) - (yv - y_center) * np.sin(theta)
                y_rotated = y_center + (xv - x_center) * np.sin(theta) + (yv - y_center) * np.cos(theta)
                x_rotated_pair.append(x_rotated)
                y_rotated_pair.append(y_rotated)
            x_new.append(tuple(x_rotated_pair))
            y_new.append(tuple(y_rotated_pair))
        # 일반 숫자일 경우 바로 회전 적용
        else:
            x_rotated = x_center + (x_val - x_center) * np.cos(theta) - (y_val - y_center) * np.sin(theta)
            y_rotated = y_center + (x_val - x_center) * np.sin(theta) + (y_val - y_center) * np.cos(theta)
            x_new.append(x_rotated)
            y_new.append(y_rotated)
    
    return x_new, y_new


# 그래프 생성  =================================================================================================================
fig = go.Figure()
for kk in range(2):
    sgn = 1 if kk == 0 else -1
    x0 = total_width/2 - sgn*jet_a/1000;  y0 = In.tunnel_height + In.top_clearance/1000 + jet_d3/2000*0.03;  x1 = x0 - sgn*jet_d2/1000;  y1 = y0 + jet_d2/1000  # In.jet_d3/2*0.03 : 반경의 3% 오프셋
    shape(fig, 'circle', x0,y0,x1,y1, None, "yellow", 2)

    xc = (x0 + x1)/2;  yc = (y0 + y1)/2
    x0 = xc - jet_d1/2000;  y0 = yc - jet_d1/2000;  x1 = xc + jet_d1/2000;  y1 = yc + jet_d1/2000
    shape(fig, 'circle', x0,y0,x1,y1, None, "yellow", 2)
    x0 = xc - jet_d3/2000;  y0 = yc - jet_d3/2000;  x1 = xc + jet_d3/2000;  y1 = yc + jet_d3/2000
    shape(fig, 'circle', x0,y0,x1,y1, None, "white", 2, LineStyle='dash')

y0 = -0.5*In.tunnel_height;  y1 = 2*In.tunnel_height
if check_center_line:
    x0 = In.shoulder_left
    shape(fig, 'line', x0,y0,x0,y1, None, 'magenta', 4, LineStyle='longdashdot')
    annotation(fig, x0,y1, 'magenta', '℄ 도로 중심선', 'left', 'bottom')

    x0 = total_width/2
    shape(fig, 'line', x0,y0,x0,y1, None, 'green', 4, LineStyle='longdashdot')
    annotation(fig, x0,y1, 'green', '℄ 터널 중심선', 'left', 'bottom')

if check_other_line:
    # x0 좌표 리스트 정의
    x_positions = [0,In.shoulder_left - In.edge, total_width] + [In.shoulder_left + In.lane_width * i for i in range(1, In.lane_count + 1)]
    for x0 in x_positions:
        shape(fig, 'line', x0, y0, x0, y1, None, 'blue', 3, LineStyle='longdashdot')

for kk in range(7):
    if check_superelevation:        
        slope = -3 + kk    
        lane_x_rotated, lane_y_rotated = rotate_points(lane_x, lane_y, slope)
        box_x_rotated, box_y_rotated = rotate_points(box_x, box_y, slope)
    else:
        if kk == 1:
            break
        lane_x_rotated, lane_y_rotated = rotate_points(lane_x, lane_y, In.superelevation)
        box_x_rotated, box_y_rotated = rotate_points(box_x, box_y, In.superelevation)
        
    if check_lane_marking:
        for (x0, x1, x2, x3), (y0, y1, y2, y3) in zip(lane_x_rotated, lane_y_rotated):        
            x_coords = [x0, x1, x2, x3, x0]  # 폐곡선을 위해 처음 좌표를 마지막에 추가
            y_coords = [y0, y1, y2, y3, y0]

            # Scatter로 사각형 추가
            fig.add_trace(go.Scatter(
                x=x_coords,
                y=y_coords,
                mode='lines',
                fill='toself',  # 폐곡선으로 채우기
                line=dict(color='orange', width=3, dash='solid')
            ))

    # y 값이 tunnel_height/2 이상인 인덱스 찾기
    indices = [i for i, value in enumerate(box_y_rotated) if value >= In.tunnel_height/2]
    hunch_coordinates = [(box_x_rotated[i], box_y_rotated[i]) for i in indices]  # 해당 인덱스의 x, y 좌표 추출
    for x_val, y_val in hunch_coordinates:
        x0 = x_val - In.tunnel_space / 1000
        y0 = y_val - In.tunnel_space / 1000
        x1 = x_val + In.tunnel_space / 1000
        y1 = y_val + In.tunnel_space / 1000
        shape(fig, 'circle', x0,y0,x1,y1, None, "yellow", 2)

    # 데이터 추가
    fig.add_trace(go.Scatter(
        x=box_x_rotated, y=box_y_rotated, mode='lines',
        line=dict(color='cyan', width=2),        
        # marker=dict(size=10, color='red')
        ), )

# 레이아웃 설정
fig.update_layout(
    autosize=False, height=1000, margin=dict(l=0, r=0, t=0, b=0), #hovermode='x unified',    
    dragmode='pan',  # 'zoom' 대신 'pan'으로 변경하여 드래그로 이동 가능
    showlegend=False,
    xaxis=dict(
        # range=[-0.6*total_width, -0.4*total_width],
        range=[-0.5*total_width, 1.5*total_width],
        showgrid=False,
        scaleanchor="y", scaleratio=1,
        rangeslider=dict(visible=False)
    ),
    yaxis=dict(
        # range=[-0.3*In.tunnel_height, 0.3*In.tunnel_height],
        range=[-0.5*In.tunnel_height, 2.5*In.tunnel_height],
        showgrid=False,
    ),
    modebar_add=['scrollZoom']  # 스크롤 zoom 활성화
)

# 레이아웃 설정 (제로 라인과 틱 라벨 제거)
fig.update_xaxes(showline=False, showticklabels=False, zeroline=False)
fig.update_yaxes(showline=False, showticklabels=False, zeroline=False)

# 추가 config 설정
config = {
    'scrollZoom': True,  # 스크롤 zoom 활성화
    'displayModeBar': True,  # 도구 모음 항상 표시
    'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'drawclosedpath', 'drawcircle', 'drawrect', 'eraseshape'],
    'dragmode': 'pan'  # 드래그 모드를 'pan'으로 설정
}


import numpy as np
import plotly.graph_objects as go

# 기준점 설정
x_center, y_center = total_width/2, In.center_height  # 기준점 좌표

# 직선 길이 설정
line_length = 10  # 직선의 길이

# 각도 설정 (라디안으로 변환)
angle_left = np.radians(30)    # 120도
angle_right = np.radians(150)  # -120도

# 좌측 직선 끝점 좌표 계산
x_left = x_center + line_length * np.cos(angle_left)
y_left = y_center + line_length * np.sin(angle_left)

# 우측 직선 끝점 좌표 계산
x_right = x_center + line_length * np.cos(angle_right)
y_right = y_center + line_length * np.sin(angle_right)

# # 기준점 추가
# fig.add_trace(go.Scatter(x=[x_center], y=[y_center], mode="markers", name="Center"))

# 좌측 직선 추가
fig.add_trace(go.Scatter(
    x=[x_center, x_left], y=[y_center, y_left], mode="lines",
    line=dict(color='red', width=2, dash='solid')
    ))

# 우측 직선 추가
fig.add_trace(go.Scatter(
    x=[x_center, x_right], y=[y_center, y_right], mode="lines",
    line=dict(color='red', width=2, dash='solid')
    ))
x0 = x_center - In.tunnel_radius;  y0 = y_center - In.tunnel_radius
x1 = x_center + In.tunnel_radius;  y1 = y_center + In.tunnel_radius
if check_tunnel_circle:
    shape(fig, 'circle', x0, y0, x1, y1, None, "green", 3, LineStyle='dash')


# ===========================================================================
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Streamlit 제목
# st.title("Arc Visualization Using Center, Radius, Start Angle, and End Angle")

# 중심점, 반지름, 시작 각도 및 끝 각도 설정
cx, cy = x_center, y_center     # 중심 좌표
radius = In.tunnel_radius        # 반지름
start_angle = 30*np.pi/180   # 시작 각도 (라디안으로, 0은 오른쪽 방향)
end_angle = 150*np.pi/180  # 끝 각도 (라디안으로, 90도는 위쪽 방향)

# 아크의 좌표 계산 함수
def calculate_arc(cx, cy, radius, start_angle, end_angle, num_points=100):
    angles = np.linspace(start_angle, end_angle, num_points)
    x_arc = cx + radius * np.cos(angles)
    y_arc = cy + radius * np.sin(angles)
    return x_arc, y_arc

# 중심점 표시
fig.add_trace(go.Scatter(x=[cx], y=[cy], mode="markers+text", text=["Center"], textposition="top center", name="Center"))

for i in range(2):
    # 아크 좌표 계산
    if i == 1:  radius += 0.3
    x_arc, y_arc = calculate_arc(cx, cy, radius, start_angle, end_angle)

    # 아크 표시
    fig.add_trace(go.Scatter(x=x_arc, y=y_arc, mode="lines", name="Arc",
                        line=dict(color='green', width=3, dash='solid')))


# 배수 구조물 ===========================================================================
ditch = 0.1   # 노면 Ditch (100*100 or 150*150)
sump_cover = 0.075  # 집수정 뚜껑 두께
perforated_d = 0.300  # 유공관 직경
common_cover = 0.060
walkway_w, walkway_h = 0.750, 2.000   # 검사원 통로 (터널 우측에만)

common_left_w1, common_left_w2, common_left_h = 0.400, 0.500, 0.640
common_right_w1, common_right_w2, common_right_h = 0.550, 0.650, 0.940

arc_x2, arc_y2 = [], []
for iter in range(2):
    rx, ry = 0 - (In.edge - 0.250), 0;  sgn = 1  # 기준선
    common_w1, common_w2, common_h = common_left_w1, common_left_w2, common_left_h
    if iter == 1:
        rx, ry = total_width + (In.edge - 0.250), 0;  sgn = -1        
        common_w1, common_w2, common_h = common_right_w1, common_right_w2, common_right_h

    # 기준선 위 작도
    sx, sy = rx, ry
    for i in range(1, 6):
        # 노면 Ditch (100*100 or 150*150)
        if i == 1:  ex = sx;  ey = sy + 0.075
        if i == 2:  ex = sx - sgn*0.120;  ey = sy + 0.175
        if i == 3:  ex = sx - sgn*0.030;  ey = sy + common_h + common_cover - (0.075 + 0.175);  ex3 = ex;  ey3 = ey   # 검사원 통로
        if i == 4:  ex = sx - sgn*0.150;  ey = sy;  ex4 = ex;  ey4 = ey
        if i == 5:  ex = sx - sgn*(common_w2 + 0.100 + 0.050);  ey = sy;  ex5 = ex;  ey5 = ey  # Var 연장선
            
        shape(fig, 'line', sx,sy,ex,ey, None, "green", 2)
        sx = ex;  sy = ey

    ex = ex4;  ey = ey4
    shape(fig, 'rect', ex,ey,ex-sgn*(common_w2+0.100),ey-common_cover, None, "green", 2)  # 공동구 뚜껑
    ex = ex5;  ey = ey5
    arc_x2.append(ex5);  arc_y2.append(ey5)
    shape(fig, 'circle', ex,ey-0.050,ex+sgn*0.100,ey+0.050, None, "yellow", 2)   # 반지름 50인 터널선 외곽 체크용 원

    if iter == 1:
        ex = ex3+walkway_w
        ey = ey3+walkway_h
        shape(fig, 'rect', ex3,ey3,ex,ey, None, "green", 2)  # 검사원 통로
        shape(fig, 'circle', ex-0.050,ey-0.050,ex+0.050,ey+0.050, None, "yellow", 2)  # 반지름 50인 터널선 외곽 체크용 원

    ex6 = ex4 - sgn*0.050;  ey6 = ey4 - common_cover
    sx = ex6;  sy = ey6
    for i in range(7, 10):
        if i == 7:  ex = sx;  ey = sy - common_h    
        if i == 8:  ex = sx - sgn*common_w1;  ey = sy
        if i == 9:  ex = sx + sgn*(common_w1 - common_w2);  ey = sy + common_h

        shape(fig, 'line', sx,sy,ex,ey, None, "green", 2)  # 공동구
        sx = ex;  sy = ey


    # 기준선 아래 작도
    sx, sy = rx, ry
    for i in range(1, 7):
        # 노면 Ditch (100*100 or 150*150)
        if i == 1:  ex = sx;  ey = sy - ditch
        if i == 2:  ex = sx + sgn*ditch;  ey = sy
        if i == 3:  ex = sx;  ey = sy + ditch
        if i == 4:  ex = sx + sgn*0.150;  ey = sy;  ex4 = ex;  ey4 = ey
        if i == 5:  ex = sx + sgn*0.500;  ey = sy    
        if i == 6:  ex = sx;  ey = sy - 0.500;  ex6 = ex;  ey6 = ey
        
        shape(fig, 'line', sx,sy,ex,ey, None, "yellow", 2)
        sx = ex;  sy = ey

    ex = ex4;  ey = ey4
    shape(fig, 'rect', ex,ey,ex+sgn*0.450,ey-sump_cover, None, "yellow", 2)  # 집수정 뚜껑

    ex = ex6;  ey = ey6
    shape(fig, 'rect', ex,ey,ex-sgn*0.550,ey-0.500, None, "yellow", 2)  # 집수정 외부
    shape(fig, 'line', ex,ey,ex-sgn*2.550,ey, None, "yellow", 2)  # Var 연장선

    ex7 = ex6 - sgn*0.125;  ey7 = ey6 - 0.400
    ex = ex7;  ey = ey7
    shape(fig, 'rect', ex,ey,ex-sgn*0.300,ey+(0.900-sump_cover), None, "yellow", 2)  # 집수정
    shape(fig, 'line', ex,ey,ex+sgn*0.425,ey+0.450, None, "yellow", 2)  # 맹암거 선 우측

    ex8 = ex7 - sgn*0.300;  ey8 = ey7
    shape(fig, 'line', ex8,ey8,ex8-sgn*0.125,ey8+0.400, None, "yellow", 2)  # 맹암거 선 좌측

    shape(fig, 'circle', ex8,ey8+0.050,ex8+sgn*perforated_d,ey8+perforated_d+0.050, None, "yellow", 2)  # 유공관 원



# 삼점원, 삼점 아크, 터널 그리기 ==================================================================================
import sympy as sp

for iter in range(2):    
    sgn = 1
    if iter == 1:  sgn = -1

    # 변수 정의
    x, y = sp.symbols('x y')

    # 원의 중심과 반지름
    cx, cy = total_width/2, In.center_height   # 원의 중심 (3, 4)
    r = In.tunnel_radius         # 반지름 5

    # 직선의 기울기와 y절편
    angle = 150
    if iter == 1:  angle = 30
    a = np.tan(np.radians(angle))        # 직선의 기울기
    b = -a*cx + cy         # y절편

    # 원의 방정식과 직선 방정식 설정
    circle_eq = (x - cx)**2 + (y - cy)**2 - r**2
    line_eq = y - (a * x + b)

    # 연립 방정식 풀기
    solutions = sp.solve([circle_eq, line_eq], (x, y))

    # 결과 출력
    for row in solutions:
        if row[1] > 0:
            arc_x1, arc_y1 = float(row[0]), float(row[1])        



    #  두 점 P1, P2의 수직 이등분선과 다른 직선 L1_P1-L1_P2의 교점을 계산하는 함수  =======================
    import sympy as sp

    def perpendicular_bisector_intersection(x1, y1, x2, y2, l1_x1, l1_y1, l1_x2, l1_y2):
        # 두 점의 중점 계산
        x_c = (x1 + x2) / 2
        y_c = (y1 + y2) / 2
        
        # 두 점을 연결하는 선의 기울기 계산
        if x2 != x1:
            m = (y2 - y1) / (x2 - x1)
            # 수직 이등분선의 기울기
            m_perp = -1 / m
        else:
            # 두 점이 수직으로 위치할 경우, 수직 이등분선은 수평선이 됨
            m_perp = 0
        
        # 변수 정의
        x, y = sp.symbols('x y')
        
        # 수직 이등분선의 방정식
        if m_perp != 0:
            perpendicular_eq = y - y_c - m_perp * (x - x_c)
        else:
            # 수평선일 경우 y = y_c 형태
            perpendicular_eq = y - y_c
        
        # L1 직선의 기울기와 방정식
        if l1_x2 != l1_x1:
            m_l1 = (l1_y2 - l1_y1) / (l1_x2 - l1_x1)
            c_l1 = l1_y1 - m_l1 * l1_x1
            other_line_eq = y - (m_l1 * x + c_l1)
        else:
            # L1이 수직선일 경우
            other_line_eq = x - l1_x1
        
        # 연립 방정식 풀기
        solution = sp.solve([perpendicular_eq, other_line_eq], (x, y))
        
        # 결과 확인 및 변환
        if solution:
            intersection_x = float(solution[x])
            intersection_y = float(solution[y])
            return (intersection_x, intersection_y)
        else:
            return None  # 교점이 없을 경우

    # 예시 좌표
    p1_x, p1_y = arc_x1, arc_y1
    p2_x, p2_y = arc_x2[iter], arc_y2[iter]
    l1_p1_x, l1_p1_y = cx, cy
    l1_p2_x, l1_p2_y = arc_x1, arc_y1

    # 함수 호출
    intersection = perpendicular_bisector_intersection(p1_x, p1_y, p2_x, p2_y, l1_p1_x, l1_p1_y, l1_p2_x, l1_p2_y)

    # 결과 출력
    arc_x3, arc_y3 = intersection


    import numpy as np
    import plotly.graph_objects as go

    # 중심점과 두 점의 좌표
    h, k = arc_x3, arc_y3  # 중심점 예시
    x1, y1 = arc_x1, arc_y1  # 첫 번째 점
    x2, y2 = arc_x2[iter], arc_y2[iter]  # 두 번째 점

    # 반지름 계산
    r = np.sqrt((x1 - h)**2 + (y1 - k)**2)

    # 첫 번째 점과 두 번째 점의 각도를 계산
    angle1 = np.arctan2(y1 - k, x1 - h)
    angle2 = np.arctan2(y2 - k, x2 - h)

    # 각도를 [0, 2π] 범위로 조정
    if angle1 < 0:
        angle1 += 2 * np.pi
    if angle2 < 0:
        angle2 += 2 * np.pi

    # 작은 아크를 그리기 위해 두 각도 차이를 구함
    angle_diff = abs(angle2 - angle1)

    # 짧은 아크 선택
    if angle_diff > np.pi:
        # 큰 아크를 피하기 위해 angle2를 2π 추가하여 작은 경로로 설정
        theta = np.linspace(angle2, angle1 + 2 * np.pi, 100)
    else:
        # 작은 아크는 angle1에서 angle2까지로 설정
        theta = np.linspace(angle1, angle2, 100)

    # 원의 x, y 좌표 계산 (아크)
    x_arc = h + r * np.cos(theta)
    y_arc = k + r * np.sin(theta)

    # 원 전체를 위한 각도 범위
    full_circle = np.linspace(0, 2 * np.pi, 300)

    # 원의 전체 x, y 좌표 계산
    x_full_circle = h + r * np.cos(full_circle)
    y_full_circle = k + r * np.sin(full_circle)

    # 원 전체 그리기
    if check_tunnel_circle:
        fig.add_trace(go.Scatter(
            x=x_full_circle, y=y_full_circle,
        mode='lines',
        line=dict(color='magenta', dash='dash', width=3),
        name="원 전체"
        ))

    # 아크 그리기
    fig.add_trace(go.Scatter(
        x=x_arc, y=y_arc,
        mode='lines',
        line=dict(color='magenta', width=3),
        name="아크"
    ))

    # 중심점과 두 점 표시
    fig.add_trace(go.Scatter(
        x=[h, x1, x2], y=[k, y1, y2],
        mode='markers+text',
        marker=dict(color='red', size=10),
        text=["중심", "점1", "점2"],
        textposition="top center"
    ))


# Streamlit에 그래프 표시
st.plotly_chart(fig, config=config, use_container_width=True)


