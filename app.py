import streamlit as st
import time
import random

# ================= CONFIG =================
st.set_page_config(page_title="Traffic Control", layout="wide")

# ================= CSS =================
st.markdown("""
<style>
body { background-color: #f4f6f9; }

.header {
    background: white;
    padding: 25px;
    border-bottom: 2px solid #ddd;
    font-size: 36px;
    font-weight: bold;
    text-align: center;
}

.kpi {
    background: white;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    border: 1px solid #ddd;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #e0e0e0;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
}

.active { border: 2px solid green; }

.green { color: green; font-weight: bold; }
.yellow { color: orange; font-weight: bold; }
.red { color: red; font-weight: bold; }

.center {
    background: white;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    border: 2px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown('<div class="header">🚦 Smart Traffic Control System</div>', unsafe_allow_html=True)

# ================= INITIAL DATA =================
if "roads" not in st.session_state:
    st.session_state.roads = {"Road A": 40, "Road B": 60, "Road C": 30, "Road D": 50}
if "current_road" not in st.session_state:
    st.session_state.current_road = max(st.session_state.roads, key=st.session_state.roads.get)
if "timer" not in st.session_state:
    st.session_state.timer = 0
if "phase" not in st.session_state:
    st.session_state.phase = "green"

roads = st.session_state.roads
arrival_rate = {"Road A": 2, "Road B": 3, "Road C": 1, "Road D": 2}
departure_rate = 8
max_capacity = 120
green_time = 15
yellow_time = 2

placeholder = st.empty()

# ================= UPDATE FUNCTION =================
def update_traffic():
    current_road = st.session_state.current_road
    total_vehicles = sum(roads.values())

    # Update queues based on phase
    if st.session_state.phase == "green":
        roads[current_road] = max(0, roads[current_road] - departure_rate)
        for r in roads:
            if r != current_road:
                roads[r] = min(max_capacity, roads[r] + random.randint(0, arrival_rate[r]))
        st.session_state.timer += 1
        if st.session_state.timer >= green_time:
            st.session_state.phase = "yellow"
            st.session_state.timer = 0
    elif st.session_state.phase == "yellow":
        st.session_state.timer += 1
        if st.session_state.timer >= yellow_time:
            st.session_state.phase = "green"
            st.session_state.timer = 0
            # Switch road
            st.session_state.current_road = max(roads, key=roads.get)

    # Render UI
    with placeholder.container():
        k1, k2, k3 = st.columns(3)
        k1.markdown(f'<div class="kpi">🚗 Total Vehicles<br><b>{total_vehicles}</b></div>', unsafe_allow_html=True)
        k2.markdown(f'<div class="kpi">🚦 {"Active Road" if st.session_state.phase=="green" else "Switching From"}<br><b>{current_road}</b></div>', unsafe_allow_html=True)
        k3.markdown(f'<div class="kpi">⏳ Timer<br><b>{green_time - st.session_state.timer if st.session_state.phase=="green" else yellow_time - st.session_state.timer}s</b></div>', unsafe_allow_html=True)

        st.markdown("---")
        cols = st.columns(4)
        for i, (name, value) in enumerate(roads.items()):
            if name == current_road:
                status = "🟢 GREEN" if st.session_state.phase=="green" else "🟡 YELLOW"
                color = "green" if st.session_state.phase=="green" else "yellow"
                active = "active"
            else:
                status = "🔴 RED"
                color = "red"
                active = ""
            cols[i].markdown(f"""
                <div class="card {active}">
                    <h4>{name}</h4>
                    <p>Queue: {value}</p>
                    <p class="{color}">{status}</p>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.markdown(f"""
                <div class="center">
                    <h2>{'🟢 GREEN SIGNAL' if st.session_state.phase=='green' else '🟡 YELLOW SIGNAL'}</h2>
                    <h1>{current_road}</h1>
                    <p>Time Remaining: {green_time - st.session_state.timer if st.session_state.phase=='green' else yellow_time - st.session_state.timer} sec</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("---")
        st.subheader("📊 Traffic Analytics")
        st.bar_chart(roads)

# ================= AUTO-REFRESH =================
while True:
    update_traffic()
    time.sleep(1)
    st.experimental_rerun()  # Forces Streamlit to refresh every second