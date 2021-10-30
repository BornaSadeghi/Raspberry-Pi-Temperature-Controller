#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from gpiozero import DigitalOutputDevice, CPUTemperature
from time import sleep, time
try:
    from matplotlib import pyplot as plt, style
    headless = False
except Exception:
    print("matplotlib failed to import, running in headless mode")
    headless = True

import argparse
parser = argparse.ArgumentParser(description='Process fan controller options')
parser.add_argument('--threshold', dest='threshold', type=float, help="Fan activation temperature threshold")
parser.add_argument('--headless', dest='headless', action='store_true', help="Enable headless mode")
parser.set_defaults(headless=False, threshold=68)
args = parser.parse_args()

if args.headless:
    headless = True

def activate_fan():
    if fan.value == 0:
        print("Fan is on")
        fan.on()
    sleep(FAN_ON_DELAY)

def deactivate_fan():
    if fan.value == 1:
        print("Fan is off")
        fan.off()
    sleep(FAN_OFF_DELAY)

def update_data():
    global lowest_temperature, highest_temperature
    cputemp = cpu.temperature
    x_data.append(time()-start_time)
    y_data.append(cputemp)

    if len(x_data) > MAX_ENTRIES:
        del x_data[0]
        del y_data[0]

    lowest_temperature = min(cputemp, lowest_temperature)
    highest_temperature = max(cputemp, highest_temperature)
    print("Time: {} s, CPU Temperature: {} °C".format(x_data[-1], cputemp))

def update_chart():
    ax.clear()
    plt.tight_layout()
    plt.title("CPU Temperature (°C) over Time (s)")
    plt.ylabel("CPU Temperature (°C)")
    plt.xlabel("Time (s)")

    plt.ylim(lowest_temperature-Y_PADDING, highest_temperature+Y_PADDING)
    ax.plot(x_data, y_data, 'o-r')
    figure.canvas.draw()
    plt.pause(0.01)

def init_chart():
    style.use("fivethirtyeight")
    figure = plt.figure()
    ax = figure.add_subplot(1,1,1)

    plt.title("CPU Temperature (°C) over Time (s)")
    plt.ylabel("CPU Temperature (°C)")
    plt.xlabel("Time (s)")
    plt.tight_layout()
    plt.ion()
    plt.show()

fan = DigitalOutputDevice(17)
cpu = CPUTemperature()

fan_on = False

# Temperature at which the fan is turned on
TEMPERATURE_THRESHOLD = args.threshold
# Time between temperature checks when fan is off
FAN_OFF_DELAY = 20
# Time between temperature checks when fan is on
FAN_ON_DELAY = 5

# Plot temperature over time
x_data = []
y_data = []
start_time = time()
lowest_temperature = 1000
highest_temperature = 0

# How much higher/lower the y-axis should show compared to max/min value
Y_PADDING = 5
MAX_ENTRIES = 10

if not headless:
    init_chart()

while True:
    try:
        update_data()
        if not headless:
            update_chart()

        activate_fan() if cpu.temperature > TEMPERATURE_THRESHOLD else deactivate_fan()
    except KeyboardInterrupt:
        break
