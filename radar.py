import pygame
import serial
import math
import sys

# --- 1. Connection Settings ---
# CHANGE THIS to your ESP32's actual port (e.g., 'COM5')
arduino_port = 'COM6' 
baud_rate = 115200 

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=0.01)
except serial.SerialException:
    print(f"Error: Could not open port {arduino_port}. Is Thonny closed?")
    sys.exit()

# --- 2. Pygame Setup ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Real-Time Ultrasonic Radar")

# Colors
DARK_GREEN = (0, 50, 0)
BRIGHT_GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Radar Geometry
CENTER = (WIDTH // 2, HEIGHT - 30) # Bottom center of screen
MAX_RADIUS = 500 # How far the radar graphic reaches in pixels
MAX_DISTANCE_CM = 200 # How far the sensor should look in real life (200cm)

font = pygame.font.SysFont('Consolas', 16)

# We use a separate surface for the sweeping beam so we can fade it out over time
radar_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# A semi-transparent black screen used to create the "fading trail" effect
fade_mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
fade_mask.fill((0, 0, 0, 8)) # The '8' controls how fast the trail fades (lower = longer trail)

current_angle = 90
distance = 0

def draw_static_grid():
    """Draws the permanent radar rings and angle lines."""
    # Draw concentric distance rings
    for r in range(100, MAX_RADIUS + 1, 100):
        pygame.draw.arc(screen, DARK_GREEN, 
                        (CENTER[0] - r, CENTER[1] - r, r * 2, r * 2), 
                        0, math.pi, 2)
        
        # Add distance labels
        cm_label = int((r / MAX_RADIUS) * MAX_DISTANCE_CM)
        text = font.render(f"{cm_label}cm", True, DARK_GREEN)
        screen.blit(text, (CENTER[0] + 5, CENTER[1] - r - 20))

    # Draw angle lines (30, 60, 90, 120, 150 degrees)
    for angle in range(30, 151, 30):
        rad = math.radians(angle)
        x = CENTER[0] + MAX_RADIUS * math.cos(rad)
        y = CENTER[1] - MAX_RADIUS * math.sin(rad)
        pygame.draw.line(screen, DARK_GREEN, CENTER, (x, y), 2)
        
        # Add angle labels
        text = font.render(f"{angle}°", True, DARK_GREEN)
        screen.blit(text, (x + 10, y - 10))

# --- 3. Main UI Loop ---
print("Pygame Radar started! Close the window to stop.")
clock = pygame.time.Clock()
running = True

while running:
    # 1. Handle window closing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Read Serial Data from ESP32
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if "." in line:
            data = line.replace(".", "").split(",")
            if len(data) == 2:
                try:
                    current_angle = int(data[0])
                    distance = int(data[1])
                except ValueError:
                    pass # Ignore glitches

    # 3. Calculate beam coordinates
    rad = math.radians(current_angle)
    beam_x = CENTER[0] + MAX_RADIUS * math.cos(rad)
    beam_y = CENTER[1] - MAX_RADIUS * math.sin(rad)

    # 4. Draw the fading effect
    radar_surface.blit(fade_mask, (0, 0))

    # --- NEW BEAM DRAWING LOGIC ---
    if 0 < distance < MAX_DISTANCE_CM:
        # Calculate exactly where the beam hits the object
        pixel_dist = (distance / MAX_DISTANCE_CM) * MAX_RADIUS
        hit_x = CENTER[0] + pixel_dist * math.cos(rad)
        hit_y = CENTER[1] - pixel_dist * math.sin(rad)
        
        # Draw a GREEN line from the center TO the object
        pygame.draw.line(radar_surface, BRIGHT_GREEN, CENTER, (hit_x, hit_y), 4)
        
        # Draw a RED line from the object out to the MAX RANGE (the blocked signal)
        pygame.draw.line(radar_surface, RED, (hit_x, hit_y), (beam_x, beam_y), 4)
        
    else:
        # No object detected: Draw the full beam solid GREEN
        pygame.draw.line(radar_surface, BRIGHT_GREEN, CENTER, (beam_x, beam_y), 4)
    # ------------------------------

    # 7. Assemble the final screen
    screen.fill(BLACK) # Clear the base screen
    screen.blit(radar_surface, (0, 0)) # Paste the sweeping/fading beams on top
    draw_static_grid() # Draw the sharp, non-fading grid on the very top

    # Add live data text
    data_text = font.render(f"ANGLE: {current_angle}° | DIST: {distance} cm", True, BRIGHT_GREEN)
    screen.blit(data_text, (20, 20))

    pygame.display.flip() # Push everything to the monitor
    clock.tick(60) # Limit to 60 Frames Per Second

# Clean up when done
ser.close()
pygame.quit()
sys.exit()