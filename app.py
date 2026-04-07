import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
from datetime import datetime
import time

# 全局状态
if "A" not in st.session_state:
    st.session_state.A = (32.232200, 118.749000)
if "B" not in st.session_state:
    st.session_state.B = (32.234300, 118.749000)
if "A_set" not in st.session_state:
    st.session_state.A_set = False
if "B_set" not in st.session_state:
    st.session_state.B_set = False
if "height" not in st.session_state:
    st.session_state.height = 46
if "coord_system" not in st.session_state:
    st.session_state.coord_system = "GCJ-02"
if "heartbeat_data" not in st.session_state:
    st.session_state.heartbeat_data = []
if "polygon_memory" not in st.session_state:
    st.session_state.polygon_memory = []
if "is_drawing" not in st.session_state:
    st.session_state.is_drawing = False
if "temp_points" not in st.session_state:
    st.session_state.temp_points = []

# 深色主题
st.set_page_config(layout="wide", page_title="航线规划")
st.markdown("""
    <style>
    .stApp { background-color: #1e1e2e; color: #fff; }
    .css-1d391kg { background-color: #2d2d3f; }
    .css-1vq4p5l { background-color: #2d2d3f; }
    </style>
""", unsafe_allow_html=True)

# 左侧导航栏
with st.sidebar:
    st.title("导航")
    selected = option_menu(
        "功能页面",
        ["航线规划", "飞行监控"],
        icons=["map", "activity"],
        menu_icon="cast",
        default_index=0,
    )
    st.divider()
    st.subheader("坐标系")
    coord = st.radio("", ["GCJ-02(高德/百度)", "WGS-84"], index=0)
    st.session_state.coord_system = coord
    st.divider()
    st.subheader("系统状态")
    if st.session_state.A_set:
        st.success("A点已设")
    else:
        st.button("A点未设", type="primary", disabled=True)
    if st.session_state.B_set:
        st.success("B点已设")
    else:
        st.button("B点未设", type="primary", disabled=True)

# 主页面
if selected == "航线规划":
    st.title("航线规划（3D地图）")
    st.subheader("坐标信息")

    col_map, col_ctrl = st.columns([3, 1])

    with col_ctrl:
        st.subheader("控制面板")
        a_lat = st.number_input("起点A纬度", value=st.session_state.A[0], format="%.6f")
        a_lon = st.number_input("起点A经度", value=st.session_state.A[1], format="%.6f")
        b_lat = st.number_input("终点B纬度", value=st.session_state.B[0], format="%.6f")
        b_lon = st.number_input("终点B经度", value=st.session_state.B[1], format="%.6f")
        height = st.slider("飞行高度(m)", 0, 200, value=st.session_state.height)
        st.session_state.height = height

        if st.button("设置A点"):
            st.session_state.A = (a_lat, a_lon)
            st.session_state.A_set = True
        if st.button("设置B点"):
            st.session_state.B = (b_lat, b_lon)
            st.session_state.B_set = True

        st.divider()
        st.subheader("障碍物设置")
        if st.button("开始圈选障碍物"):
            st.session_state.is_drawing = True
            st.session_state.temp_points = []
            st.info("点击地图圈点 → 右键结束")
        if st.button("清除障碍物"):
            st.session_state.polygon_memory = []
            st.session_state.temp_points = []
            st.warning("已清除")

        st.divider()
        st.subheader("心跳状态")
        now = datetime.now().strftime("%H:%M:%S")
        st.metric("当前时间", now)
        st.success("心跳正常")
        st.session_state.heartbeat_data.append(time.time())
        if len(st.session_state.heartbeat_data) > 20:
            st.session_state.heartbeat_data.pop(0)

    with col_map:
        center_lat = (st.session_state.A[0] + st.session_state.B[0]) / 2
        center_lon = (st.session_state.A[1] + st.session_state.B[1]) / 2
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=18,
            tiles="Cartodb dark_matter"  # 深色地图，和截图一致
        )

        # A/B点标记
        if st.session_state.A_set:
            folium.CircleMarker(st.session_state.A, radius=15, color="red", fill=True, popup="A点").add_to(m)
        if st.session_state.B_set:
            folium.CircleMarker(st.session_state.B, radius=15, color="green", fill=True, popup="B点").add_to(m)
        if st.session_state.A_set and st.session_state.B_set:
            folium.PolyLine([st.session_state.A, st.session_state.B], color="blue", weight=3).add_to(m)

        # 障碍物
        for poly in st.session_state.polygon_memory:
            folium.Polygon(locations=poly, color="red", fill=True, fill_opacity=0.5).add_to(m)
        if st.session_state.temp_points:
            folium.PolyLine(locations=st.session_state.temp_points, color="red").add_to(m)

        output = st_folium(m, width=1000, height=600)

        # 圈选逻辑
        if st.session_state.is_drawing and output.get("last_clicked"):
            lat = output["last_clicked"]["lat"]
            lon = output["last_clicked"]["lng"]
            st.session_state.temp_points.append([lat, lon])
        if output.get("last_object_clicked") is None and len(st.session_state.temp_points) >= 3:
            st.session_state.polygon_memory.append(st.session_state.temp_points)
            st.session_state.is_drawing = False
            st.session_state.temp_points = []
            st.success("障碍物已保存")

elif selected == "飞行监控":
    st.title("飞行监控")
    st.info("监控功能待实现")
