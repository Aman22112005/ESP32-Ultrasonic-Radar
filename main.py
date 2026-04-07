import machine
import time

# --- 1. HARDWARE PINS ---
trig_pin = machine.Pin(13, machine.Pin.OUT)
echo_pin = machine.Pin(14, machine.Pin.IN)
buzzer = machine.Pin(26, machine.Pin.OUT)
servo_pin = machine.Pin(27)

# Servo PWM at 50Hz
servo = machine.PWM(servo_pin, freq=50)

# --- 2. FUNCTIONS ---
def get_distance():
    # Send 10us trigger pulse
    trig_pin.value(0)
    time.sleep_us(2)
    trig_pin.value(1)
    time.sleep_us(10)
    trig_pin.value(0)
    
    try:
        # Measure echo time (30ms timeout)
        duration = machine.time_pulse_us(echo_pin, 1, 30000)
        
        # Handle timeouts (empty space)
        if duration < 0:
            buzzer.value(0) 
            return 0 
            
        # Calculate distance in cm
        distance = (duration * 0.0343) / 2
        
        # Alarm logic: Beep if object is 1-20cm away
        if 0 < distance <= 20:
            buzzer.value(1)
        else:
            buzzer.value(0)
            
        return int(distance)
        
    except OSError:
        buzzer.value(0) # Safety mute on error
        return "err" 

def set_servo_angle(angle):
    # Map 0-180 degrees to PWM duty cycle limits
    min_duty = 1800 
    max_duty = 8000 
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))
    servo.duty_u16(duty)

# --- 3. STARTUP SEQUENCE ---
time.sleep(1)
set_servo_angle(90) # Center servo

# 3-Second Countdown
sec = 3
print(f"Starting the servo in {sec} sec.")   
for i in range(sec, 0, -1):
    print(i)
    time.sleep(1)

# Smoothly reset to starting angle
for i in range(90, 15, -2): 
    set_servo_angle(i)
    time.sleep_ms(50)

# --- 4. MAIN RADAR LOOP ---
while True:
    
    # Sweep Forward
    for current_angle in range(15, 166, 1):
        set_servo_angle(current_angle)
        time.sleep_ms(70) # Wait for motor & echo to clear
        
        dist = get_distance()
        print(f"{current_angle},{dist}.") # Send data to PC
        
    # Sweep Backward
    for current_angle in range(165, 14, -1):
        set_servo_angle(current_angle)
        time.sleep_ms(70) 
        
        dist = get_distance()
        print(f"{current_angle},{dist}.")
