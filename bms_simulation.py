import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
import pandas as pd

# ---------- Output Folder Management ----------
counter_file = "output_counter.txt"

def get_output_number():
    if os.path.exists(counter_file):
        with open(counter_file, "r") as f:
            num = int(f.read().strip()) + 1
    else:
        num = 1
    with open(counter_file, "w") as f:
        f.write(str(num))
    return num

output_num = get_output_number()

# Timestamp with only hour:minute AM/PM
timestamp = datetime.now().strftime("%Y-%m-%d__%I-%M%p") 
folder_name = f"Output-{output_num:03d}__{timestamp}"
os.makedirs(folder_name, exist_ok=True)

# ---------- Time setup (1 hour, per second) ----------
time = np.arange(0, 3600, 1)

# Example simulated data
soc = np.linspace(100, 55, len(time))             # SOC (%)
soh = np.linspace(100, 99.97, len(time))          # SOH (%)
voltage = np.linspace(14.8, 13.0, len(time))      # Pack Voltage (V)
temperature = np.linspace(25, 29.5, len(time))    # Temperature (°C)
power = np.random.normal(20, 5, len(time))        # Power (W)
protections = np.zeros(len(time))                 # Protections (0 = normal)

# ---------- PLOTTING ----------
fig, axs = plt.subplots(3, 2, figsize=(14, 8))
fig.suptitle("EV Battery Management System (BMS) Dashboard", fontsize=16, fontweight="bold")

# SOC
axs[0, 0].plot(time, soc, color="blue", label="SOC (%)")
axs[0, 0].axhspan(80, 100, facecolor="green", alpha=0.2, label="Good (>80%)")
axs[0, 0].axhspan(20, 80, facecolor="orange", alpha=0.2, label="Medium (20–80%)")
axs[0, 0].axhspan(0, 20, facecolor="red", alpha=0.2, label="Low (<20%)")
axs[0, 0].set_title("State of Charge (SOC)")
axs[0, 0].set_xlabel("Time (s)")
axs[0, 0].set_ylabel("SOC (%)")
axs[0, 0].grid(True)
axs[0, 0].legend()

# SOH
axs[0, 1].plot(time, soh, color="darkorange", label="SOH (%)")
axs[0, 1].axhspan(90, 100, facecolor="green", alpha=0.2, label="Healthy (>90%)")
axs[0, 1].axhspan(70, 90, facecolor="orange", alpha=0.2, label="Warning (70–90%)")
axs[0, 1].axhspan(0, 70, facecolor="red", alpha=0.2, label="Poor (<70%)")
axs[0, 1].set_title("State of Health (SOH)")
axs[0, 1].set_xlabel("Time (s)")
axs[0, 1].set_ylabel("SOH (%)")
axs[0, 1].grid(True)
axs[0, 1].legend()

# Voltage
axs[1, 0].plot(time, voltage, color="blue", label="Voltage (V)")
axs[1, 0].axhspan(13.5, 15, facecolor="green", alpha=0.2, label="Nominal")
axs[1, 0].axhspan(12, 13.5, facecolor="orange", alpha=0.2, label="Low Voltage")
axs[1, 0].axhspan(0, 12, facecolor="red", alpha=0.2, label="Critical Low")
axs[1, 0].set_title("Battery Pack Voltage")
axs[1, 0].set_xlabel("Time (s)")
axs[1, 0].set_ylabel("Voltage (V)")
axs[1, 0].grid(True)
axs[1, 0].legend()

# Temperature
axs[1, 1].plot(time, temperature, color="red", label="Temp (°C)")
axs[1, 1].axhspan(0, 40, facecolor="green", alpha=0.2, label="Safe (<40°C)")
axs[1, 1].axhspan(40, 60, facecolor="orange", alpha=0.2, label="Warning (40–60°C)")
axs[1, 1].axhspan(60, 100, facecolor="red", alpha=0.2, label="Overheat (>60°C)")
axs[1, 1].set_title("Cell Temperature")
axs[1, 1].set_xlabel("Time (s)")
axs[1, 1].set_ylabel("Temperature (°C)")
axs[1, 1].grid(True)
axs[1, 1].legend()

# Power
axs[2, 0].plot(time, power, color="green", label="Power (W)")
axs[2, 0].axhspan(0, 25, facecolor="green", alpha=0.2, label="Normal Load")
axs[2, 0].axhspan(25, 35, facecolor="orange", alpha=0.2, label="High Load")
axs[2, 0].axhspan(35, 50, facecolor="red", alpha=0.2, label="Critical Load")
axs[2, 0].set_title("Power Output")
axs[2, 0].set_xlabel("Time (s)")
axs[2, 0].set_ylabel("Power (W)")
axs[2, 0].grid(True)
axs[2, 0].legend()

# Protections
axs[2, 1].plot(time, protections, label="Protections", color="purple")
axs[2, 1].set_title("Protection Flags")
axs[2, 1].set_xlabel("Time (s)")
axs[2, 1].set_ylabel("Protection Flags")
axs[2, 1].set_yticks([0])
axs[2, 1].set_yticklabels(["Normal"])
axs[2, 1].grid(True)
axs[2, 1].legend()

plt.tight_layout(rect=[0, 0, 1, 0.96])

# Save graph
output_path = os.path.join(folder_name, "bms_dashboard.png")
plt.savefig(output_path, dpi=300)

# Save data to Excel
data = {
    "Time (s)": time,
    "SOC (%)": soc,
    "SOH (%)": soh,
    "Voltage (V)": voltage,
    "Temperature (°C)": temperature,
    "Power (W)": power,
    "Protection": protections
}
df = pd.DataFrame(data)
excel_path = os.path.join(folder_name, "bms_data.xlsx")
df.to_excel(excel_path, index=False)

# Show the graph live
plt.show()

print("✅ Simulation complete!")
print(f"📊 Dashboard saved at: {output_path}")
print(f"📑 Data saved at: {excel_path}")
