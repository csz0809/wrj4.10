import streamlit as st
import folium
import numpy as np
import pandas as pd
from streamlit_folium import st_folium
from folium.plugins import Draw

st.set_page_config(page_title="无人机监控", layout="wide")
st.title("无人机实时监控平台")

# 1. 心跳图
st.subheader("📡 心跳状态监控")
t = np.linspace(0, 50, 100)
heart = np.sin(t * 0.8) * 0.5 + 0.5
noise = np.random.randn(100) * 0.05
signal = heart + noise

df = pd.DataFrame({
    "时间": t,
    "心跳信号": signal
})
st.line_chart(df, x="时间", y="心跳信号", use_container_width=True)

# 2. 地图 + 障碍物绘制
st.subheader("🗺️ 电子围栏与障碍物")

m = folium.Map(
    location=[30.5928, 114.3055],
    zoom_start=13,
    tiles="openstreetmap"
)

# 只开启多边形绘制
draw = Draw(
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

data = st_folium(m, width=1200, height=600)

# 3. 识别绘制的障碍物
if data and data.get("last_active_drawing"):
    st.success("已识别新绘制的障碍物区域")
    st.json(data["last_active_drawing"]["geometry"])

st.caption("在地图上绘制多边形即可标记障碍物")
