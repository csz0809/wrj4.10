import streamlit as st
import folium
import numpy as np
import pandas as pd
from streamlit_folium import st_folium

# 页面配置
st.set_page_config(page_title="无人机监控", layout="wide")
st.title("🚁 无人机智能化应用 - 项目Demo")

# ---------------------- 1. 心跳数据可视化 ----------------------
st.subheader("📡 心跳状态监控")

# 生成模拟心跳数据
time = np.linspace(0, 30, 50)
battery = 95 - time * 0.3 + np.random.randn(50) * 0.5
altitude = 80 + np.random.randn(50) * 3
speed = 12 + np.random.randn(50) * 1.5

# 绘制心跳图表（多列展示）
col1, col2, col3 = st.columns(3)
with col1:
    st.line_chart(pd.DataFrame({"电量(%)": battery}), use_container_width=True)
with col2:
    st.line_chart(pd.DataFrame({"高度(m)": altitude}), use_container_width=True)
with col3:
    st.line_chart(pd.DataFrame({"速度(m/s)": speed}), use_container_width=True)

# ---------------------- 2. 地图 + 障碍物圈选 ----------------------
st.subheader("🗺️ 地图与障碍物管理")

# 初始化地图（OpenStreetMap 必亮，无黑屏）
m = folium.Map(
    location=[30.5928, 114.3055],  # 初始中心点（可修改）
    zoom_start=12,
    tiles="openstreetmap"  # 海外服务器最稳的瓦片
)

# 只开启多边形绘制（障碍物圈选）
draw = folium.plugins.Draw(
    draw_options={
        "polyline": False,
        "polygon": True,
        "rectangle": True,
        "circle": False,
        "marker": False
    },
    edit_options={"edit": True, "remove": True}
)
draw.add_to(m)

# 渲染地图
map_result = st_folium(m, width=1200, height=600)

# 展示绘制的障碍物信息
if map_result and map_result.get("last_active_drawing"):
    st.success("✅ 已识别障碍物区域")
    st.json(map_result["last_active_drawing"]["geometry"])
