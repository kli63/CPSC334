import socket
import pygame

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ambient Light Sensor Visualization")

def sensor_value_to_color(value):
    color_intensity = max(0, min(255, int(value / 4095 * 255)))
    return (color_intensity, color_intensity, color_intensity)

print("Creating server...")
s = socket.socket()
s.bind(('0.0.0.0', 10000))
s.listen(0)

running = True
while running:
    client, addr = s.accept()
    try:
        while True:
            content = client.recv(32).decode("utf-8").strip()
            if len(content) == 0:
                break

            try:
                sensor_value = int(content)
                print(f"Received sensor value: {sensor_value}")

                color = sensor_value_to_color(sensor_value)
                screen.fill(color)
                pygame.display.flip()

            except ValueError:
                print("Invalid sensor value received")

    except ConnectionResetError:
        print("Client disconnected")
    
    client.close()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
s.close()
