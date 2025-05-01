import streamlit as st
import matplotlib.pyplot as plt

# Simulated system state
class WaterTankSystem:
    def __init__(self):
        self.water_level = st.session_state.get("water_level", 50)
        self.pump_on = st.session_state.get("pump_on", False)
        self.low_sensor = 30
        self.high_sensor = 80

    def update(self):
        if self.pump_on:
            self.water_level += 1
        else:
            self.water_level -= 1
        self.water_level = max(0, min(100, self.water_level))
        st.session_state.water_level = self.water_level

    def logic(self):
        # Simulated PLC logic
        if self.water_level <= self.low_sensor:
            self.pump_on = True
        elif self.water_level >= self.high_sensor:
            self.pump_on = False
        st.session_state.pump_on = self.pump_on

# Initialize
st.set_page_config(page_title="Virtual PLC Water Tank Lab", layout="centered")
st.title("🚰 PLC-SCADA Water Tank Virtual Lab")

tank = WaterTankSystem()

# Manual mode toggle
manual = st.checkbox("Manual Mode", value=False)

if manual:
    pump_state = st.radio("Pump Control", ["ON", "OFF"], index=0 if tank.pump_on else 1)
    tank.pump_on = (pump_state == "ON")
    st.session_state.pump_on = tank.pump_on
else:
    tank.logic()

# Run a scan cycle
if st.button("Run Scan Cycle"):
    tank.update()
st.rerun()

# Display water level
st.markdown(f"### Current Water Level: {tank.water_level:.0f}%")
st.progress(tank.water_level / 100)

fig, ax = plt.subplots()
ax.barh(["Tank"], [tank.water_level], color="blue")
ax.set_xlim(0, 100)
ax.set_title("Water Level")
st.pyplot(fig)
