import pygame
import cv2
import numpy as np

# Set up glitch display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 30
GLITCH_DURATION = 0.1  # Time per glitch frame (in seconds)
BITS_PER_FRAME = int(FPS * GLITCH_DURATION)

def file_to_binary(filename):
    """Convert file to binary string."""
    with open(filename, 'rb') as file:
        file_data = file.read()
        return ''.join(format(byte, '08b') for byte in file_data)

def text_to_binary(text):
    """Convert text to binary representation."""
    return ''.join(format(ord(c), '08b') for c in text)

def glitch_to_video(binary_data, output_file):
    """Display a glitch effect and record it to a video."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Set up video writer (MP4 format with H.264 codec)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_file, fourcc, FPS, (SCREEN_WIDTH, SCREEN_HEIGHT))

    print("[*] Transmitting glitch data...")

    for bit in binary_data:
        for _ in range(BITS_PER_FRAME):
            # Clear the screen
            screen.fill((0, 0, 0))

            # Generate structured pattern based on the bit value
            if bit == '1':
                color = (255, 255, 255)  # White for '1'
            else:
                color = (0, 0, 0)  # Black for '0'

            # Draw a rectangle covering the entire screen
            pygame.draw.rect(screen, color, pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

            pygame.display.flip()

            # Capture frame and save to video
            frame = pygame.surfarray.array3d(screen)
            frame = np.rot90(frame)  # Rotate for correct orientation
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            video.write(frame)

            # Exit if the user closes the window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    video.release()
                    pygame.quit()
                    return

    print(f"[*] Data transmission complete! Saved as {output_file}")
    video.release()
    pygame.quit()

if __name__ == '__main__':
    choice = input("Do you want to encode a file or text? (Enter 'file' or 'text'): ").strip().lower()

    if choice == 'file':
        file_name = input("Enter the file name to encode (e.g., example.txt): ")
        try:
            print(f"Encoding {file_name} to glitch video...")
            binary_data = file_to_binary(file_name)
        except FileNotFoundError:
            print(f"Error: The file {file_name} was not found.")
            exit(1)
    elif choice == 'text':
        text = input("Enter the text you want to encode: ")
        print(f"Encoding text: {text}")
        binary_data = text_to_binary(text)
    else:
        print("Invalid choice. Please enter 'file' or 'text'.")
        exit(1)

    # Prompt for the output video file name
    output_file = input("Enter the name for the output video file (e.g., glitch_output.mp4): ")

    # Convert binary data to glitch video
    glitch_to_video(binary_data, output_file)
