import wave
import struct
import math

# Define frequencies for binary encoding (high and low tone for 1 and 0)
FREQ_HIGH = 528  # Hz for binary '1'
FREQ_LOW = 432    # Hz for binary '0'
SAMPLE_RATE = 44100  # Standard sample rate for audio files
DURATION = 0.1  # Duration of each tone (100 ms)

def encode_data_to_audio(data, file_name):
    """Encode binary data to a series of audio tones and write incrementally to a file."""
    with wave.open(file_name, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono channel
        wav_file.setsampwidth(2)  # 16-bit samples
        wav_file.setframerate(SAMPLE_RATE)  # Sample rate
        
        # Process each byte in the data
        for byte in data:
            for bit in range(8):  # Process each bit in the byte (from left to right)
                tone_freq = FREQ_HIGH if byte & (1 << (7 - bit)) else FREQ_LOW
                # Generate the sound for this bit
                samples = int(SAMPLE_RATE * DURATION)
                for i in range(samples):
                    sample = math.sin(2 * math.pi * tone_freq * i / SAMPLE_RATE)
                    wav_file.writeframes(struct.pack('h', int(sample * 32767)))  # Write sample to file incrementally

def file_to_binary(filename):
    """Convert file to binary string."""
    with open(filename, 'rb') as file:
        file_data = file.read()
        return ''.join(format(byte, '08b') for byte in file_data)

def text_to_binary(text):
    """Convert text to a binary string."""
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_bytes(binary):
    """Convert a binary string to a list of bytes."""
    return [int(binary[i:i+8], 2) for i in range(0, len(binary), 8)]

if __name__ == '__main__':
    choice = input("Do you want to encode a file or text? (Enter 'file' or 'text'): ").strip().lower()

    if choice == 'file':
        file_name = input("Enter the file name to encode (e.g., example_script.py): ")
        try:
            print(f"Encoding {file_name} to audio...")
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

    # Convert binary data to bytes
    byte_data = binary_to_bytes(binary_data)

    # Prompt for the output audio file name
    output_file_name = input("Enter the name for the output audio file (e.g., encoded_audio.wav): ")

    # Convert binary data (as bytes) to audio and write to the user-defined file name
    encode_data_to_audio(byte_data, output_file_name)

    print(f"Audio file saved as {output_file_name}")
