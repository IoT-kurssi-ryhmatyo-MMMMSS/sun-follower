from machine import ADC, Pin, PWM
from utime import sleep
from math import exp

sleep(0.1)  # Wait for USB to become ready

led = Pin("LED", Pin.OUT)  # Create LED pin object

led.on()  # Turn LED on
led.off()  # Turn LED off

adc0 = ADC(0)  # GP26 = ADC0
adc1 = ADC(1)  # GP27 = ADC1

# Servo setup
servo = PWM(Pin(16))  # GP16
servo.freq(50)

print("Hello, Pi Pico W!")

VREF = 3.3  # Reference voltage
FULL = 65535  # 16-bit ADC


def set_angle(angle):
    angle = max(0, min(180, angle))
    pulse = 250 + (angle / 180) * (2700 - 250)
    servo.duty_u16(int(pulse * 65535 / 20000))


def read_adc(adc: ADC) -> int:
    # 0..65535 where 65535 ~ VREF
    return adc.read_u16()


# Start in middle position
angle = 90
set_angle(angle)

while True:
    raw0 = read_adc(adc0)
    raw1 = read_adc(adc1)

    voltage0 = raw0 * VREF / FULL
    voltage1 = raw1 * VREF / FULL

    lux0 = 3.7181 * exp(1.7869 * voltage0) * 0.95  # Calibration factor 0.95
    lux1 = 3.7181 * exp(1.7869 * voltage1) * 0.95  # Calibration factor 0.95

    # Convert to percentage (0-100%)
    p0 = raw0 * 100 / FULL
    p1 = raw1 * 100 / FULL

    diff = lux0 - lux1
    if diff > 3:
        angle += 5
    elif diff < -3:
        angle -= 5

    angle = max(0, min(180, angle))
    set_angle(angle)

    print(f"{voltage1:.3f}, {lux1:.0f} | {voltage0:.3f}, {lux0:.0f}")

    sleep(0.5)
