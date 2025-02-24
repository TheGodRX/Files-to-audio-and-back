import cv2
import numpy as np

FPS = 30
GLITCH_DURATION = 0.1
BITS_PER_FRAME = int(FPS * GLITCH_DURATION)

def binary_to_file(binary_data, output_file):
    """Convert binary string to a file."""
    with open(output_file, 'wb') as file:
        # Split binary data into 8-bit chunks and convert to bytes
        bytes_data = [int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8)]
        file.write(bytes(bytes_data))

def binary_to_text(binary_data):
    """Convert binary string to text."""
    text = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))
    return text

def decode_glitch_video(video_file):
    """Extract binary data from glitch video."""
    cap = cv2.VideoCapture(video_file)

    if not cap.isOpened():
        print("[!] Error: Cannot open video file", video_file)
        return
    
    print("[*] Decoding glitch video...")

    binary_data = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Analyze every "bit frame"
        if frame_count % BITS_PER_FRAME == 0:
            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Calculate the average pixel intensity
            avg_intensity = np.mean(gray_frame)

            # Determine the bit based on the average intensity
            if avg_intensity > 127:
                binary_data.append('1')
            else:
                binary_data.append('0')

    cap.release()

    binary_str = ''.join(binary_data)
    return binary_str

def display_decoded_content(binary_data):
    """Display the decoded content as text or a preview of the file."""
    try:
        # Attempt to decode as text first
        decoded_text = binary_to_text(binary_data)
        print("\n[*] Decoded Text Preview:")
        print("------------------------")
        print(decoded_text[:500])  # Display first 500 characters to avoid overwhelming the console
        print("------------------------")
        print("[*] Note: If the above text looks correct, you can save it as a text file.")
        print("[*] If it looks like gibberish, it might be a binary file (e.g., an image or zip).")
    except:
        print("\n[*] The decoded content appears to be a binary file (not plain text).")
        print("[*] You can save it as a file and open it with the appropriate program.")

if __name__ == '__main__':
    video_file = input("Enter the path to the glitch video (e.g., glitch_output.mp4): ")

    try:
        print(f"Decoding {video_file}...")
        binary_data = decode_glitch_video(video_file)

        # Display the decoded content for preview
        display_decoded_content(binary_data)

        # Ask the user what to do next
        choice = input("\nDo you want to save the decoded content as a file or display it as text? (Enter 'file' or 'text'): ").strip().lower()

        if choice == 'file':
            output_file = input("Enter the file name to save the decoded content (e.g., decoded_file.txt): ")
            binary_to_file(binary_data, output_file)
            print(f"Decoded content saved as: {output_file}")
        elif choice == 'text':
            decoded_text = binary_to_text(binary_data)
            print("\n[*] Full Decoded Text:")
            print("---------------------")
            print(decoded_text)
            print("---------------------")
        else:
            print("Invalid choice. Please enter 'file' or 'text'.")
    except Exception as e:
        print(f"Error: {e}")
