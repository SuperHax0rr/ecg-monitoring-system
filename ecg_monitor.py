import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque

# =========================
# SERIAL PORT
# =========================
ser = serial.Serial('COM5', 9600)

# =========================
# ECG BUFFER
# =========================
BUFFER_SIZE = 250

ecg_data = deque([0] * BUFFER_SIZE, maxlen=BUFFER_SIZE)

# =========================
# GRAPH SETUP
# =========================
fig, ax = plt.subplots()

line, = ax.plot(ecg_data, lw=1.5)

ax.set_ylim(250, 700)

ax.set_title("ECG Monitor")

ax.set_xlabel("Samples")
ax.set_ylabel("Amplitude")

status_text = ax.text(
    0.02,
    0.95,
    "Status: Waiting",
    transform=ax.transAxes,
    fontsize=12,
    verticalalignment='top'
)

# =========================
# SIGNAL ANALYSIS
# =========================
def analyze_signal(data):

    data = np.array(data)

    peak_to_peak = np.max(data) - np.min(data)

    variation = np.std(data)

    # Too weak / disconnected-like
    if peak_to_peak < 8:
        return "Not Connected"

    # Excessive unstable spikes
    if variation > 45:
        return "Abnormal Signal"

    return "Connected"

# =========================
# UPDATE FUNCTION
# =========================
def update(frame):

    try:

        value = ser.readline().decode().strip()

        # =========================
        # LEADS DISCONNECTED
        # =========================
        if value == "!":

            status_text.set_text("Status: Not Connected")

            return line,

        # =========================
        # ECG VALUE
        # =========================
        ecg = int(value)

        ecg_data.append(ecg)

        # =========================
        # LIGHT SMOOTHING
        # =========================
        smooth = np.convolve(
            ecg_data,
            np.ones(3) / 3,
            mode='same'
        )

        line.set_ydata(smooth)

        # =========================
        # STATUS DETECTION
        # =========================
        status = analyze_signal(smooth)

        status_text.set_text(f"Status: {status}")

    except:
        pass

    return line,

# =========================
# ANIMATION
# =========================
ani = FuncAnimation(
    fig,
    update,
    interval=20,
    cache_frame_data=False
)

plt.show()