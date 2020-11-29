from gpiozero import DigitalOutputDevice, CPUTemperature
from matplotlib import pyplot as plt, style
from matplotlib.animation import FuncAnimation
from time import sleep, time

fan = DigitalOutputDevice(17)
cpu = CPUTemperature()

fan_on = False

TEMPERATURE_THRESHOLD = 68
# Waiting time before turning fan off when temperature is low enough
FAN_OFF_DELAY = 10
# Time between temperature checks
UPDATE_DELAY = 5

assert(FAN_OFF_DELAY >= UPDATE_DELAY)

# Plot temperature over time
x_data = [0]
y_data = [cpu.temperature]

def fan_on():
    if fan.value == 0:
        print("Fan is on")
    fan.on()

def fan_off():
    sleep(FAN_OFF_DELAY - UPDATE_DELAY)
    if fan.value == 1:
        print("Fan is off")
    fan.off()

style.use("fivethirtyeight")
figure = plt.figure()
ax1 = figure.add_subplot(1,1,1)

# How much higher/lower the y-axis should show compared to max/min value
Y_PADDING = 5

start_time = time()
lowest_temperature = 1000
highest_temperature = 0

plt.title("CPU Temperature (°C) over Time (s)")
plt.ylabel("CPU Temperature (°C)")
plt.xlabel("Time (s)")
plt.tight_layout()

def update(i):
    global lowest_temperature, highest_temperature
    x_data.append(time()-start_time)
    y_data.append(cpu.temperature)
    print("Time: {} s, CPU Temperature: {} °C".format(x_data[-1], cpu.temperature))
    
    lowest_temperature = min(cpu.temperature, lowest_temperature)
    highest_temperature = max(cpu.temperature, highest_temperature)
    
    plt.ylim(lowest_temperature-Y_PADDING, highest_temperature+Y_PADDING)
    ax1.plot(x_data, y_data, 'r')
    
    fan_on() if cpu.temperature > TEMPERATURE_THRESHOLD else fan_off()

anim = FuncAnimation(figure, update, interval=UPDATE_DELAY*1000)
plt.show()

