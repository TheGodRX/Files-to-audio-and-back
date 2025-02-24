import wave
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import os

# Constants for frequencies
FREQ_HIGH = 528  # Hz for binary '1'
FREQ_LOW = 432   # Hz for binary '0'
SAMPLE_RATE = 44100  # Standard sample rate
DURATION = 0.1  # Duration of each tone (100 ms)
TOLERANCE = 50  # Frequency detection tolerance

def plot_waveform(samples, filename):
    """Plot the waveform of the WAV file."""
    try:
        time = np.linspace(0, len(samples) / SAMPLE_RATE, num=len(samples))
        plt.figure(figsize=(12, 4))
        plt.plot(time, samples)
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.title(f"Waveform of {filename}")
        plt.close()  # Close the plot to prevent memory issues
    except Exception as e:
        print(f"Error plotting waveform: {e}")

def bandpass_filter(signal_data, lowcut, highcut, fs, order=5):
    """Apply a bandpass filter to isolate frequencies."""
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = signal.butter(order, [low, high], btype='band')
    return signal.filtfilt(b, a, signal_data)

def moving_average_filter(signal_data, window_size=5):
    """Smooth signal using a moving average filter."""
    return np.convolve(signal_data, np.ones(window_size) / window_size, mode='same')

def normalize_audio(samples):
    """Normalize the audio signal to full range."""
    max_val = np.max(np.abs(samples))
    if max_val == 0:
        return samples
    return np.int16(samples / max_val * 32767)

def decode_audio_to_binary(filename):
    """Decode the audio tones to binary data using adaptive frequency detection."""
    with wave.open(filename, 'r') as wav_file:
        frames = wav_file.readframes(wav_file.getnframes())
        samples = np.frombuffer(frames, dtype=np.int16)
    
    # Normalize and filter the audio signal
    samples = normalize_audio(samples)
    samples = bandpass_filter(samples, 400, 1100, SAMPLE_RATE)
    samples = moving_average_filter(samples, window_size=5)

    binary_data = []
    num_samples_per_bit = int(SAMPLE_RATE * DURATION)

    # Process audio in chunks
    for i in range(0, len(samples), num_samples_per_bit):
        chunk = samples[i:i+num_samples_per_bit]

        # Apply FFT to detect dominant frequency
        freqs = np.fft.fftfreq(len(chunk), d=1/SAMPLE_RATE)
        fft_result = np.fft.fft(chunk)
        magnitudes = np.abs(fft_result)

        # Find dominant frequency in the chunk
        peak_index = np.argmax(magnitudes)
        peak_freq = abs(freqs[peak_index])

        # Adaptive frequency detection with tolerance
        if FREQ_HIGH - TOLERANCE <= peak_freq <= FREQ_HIGH + TOLERANCE:
            binary_data.append('1')
        elif FREQ_LOW - TOLERANCE <= peak_freq <= FREQ_LOW + TOLERANCE:
            binary_data.append('0')
        else:
            # If the frequency is not within tolerance, assume the last known value
            binary_data.append(binary_data[-1] if binary_data else '0')

    return ''.join(binary_data)

def binary_to_text(binary):
    """Convert binary string to readable text."""
    text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8) if len(binary[i:i+8]) == 8)
    return text

def suggest_file_type(decoded_text):
    """Suggest a file type based on the content."""
    try:
        decoded_text.encode('utf-8')
        
        # Check for HTML/XML-like content (requires more concrete tags)
        if '<html>' in decoded_text.lower() or '<!doctype html>' in decoded_text.lower() or '<body>' in decoded_text.lower():
            return "HTML/XML File (.html or .xml)"
        
        # Check for JSON structure
        elif decoded_text.startswith('{') or decoded_text.startswith('['):
            return "JSON File (.json)"
        
        # Check for ZIP files (PK header signature)
        elif decoded_text.startswith('PK'):
            return "ZIP File (.zip)"
        
        # Check for Python files (Python keyword detection)
        elif 'def ' in decoded_text or 'import ' in decoded_text:
            return "Python File (.py)"
        
        # Check for Bash script (Bash shebang and commands)
        elif decoded_text.startswith('#!/bin/bash'):
            return "Bash Script File (.sh)"
        
        # Check for Ruby files (Ruby keyword detection)
        elif 'def ' in decoded_text or 'class ' in decoded_text:
            return "Ruby File (.rb)"
        
        else:
            return "Text File (.txt)"
    
    except:
        return "Binary File (Unknown Type)"

def save_decoded_text_to_file(decoded_text, file_type):
    """Prompt user for a file name and save the decoded text."""
    save_file_name = input(f"Enter the file name to save the decoded content ({file_type}): ")
    with open(save_file_name, 'w') as file:
        file.write(decoded_text)
    print(f"Decoded content saved as: {save_file_name}")

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
        
        # Suggest file type based on decoded content
        file_type = suggest_file_type(decoded_text)
        print(f"[*] Suggested File Type: {file_type}")
        
        # Ask user whether to save as text or binary
        choice = input("\nDo you want to save the decoded content as a file or display it as text? (Enter 'file' or 'text'): ").strip().lower()

        if choice == 'file':
            save_decoded_text_to_file(decoded_text, file_type)
        elif choice == 'text':
            print("\n[*] Full Decoded Text:")
            print("---------------------")
            print(decoded_text)
            print("---------------------")
        else:
            print("Invalid choice. Please enter 'file' or 'text'.")
    except Exception as e:
        print(f"Error decoding content: {e}")
        print("[*] The decoded content appears to be a binary file (not plain text).")
        print("[*] You can save it as a file and open it with the appropriate program.")

if __name__ == '__main__':
    file_name = input("Enter the WAV file to decode (e.g., encoded_file.wav): ")

    try:
        print(f"Decoding {file_name}...")
        binary_data = decode_audio_to_binary(file_name)
        print("Decoded binary data:", binary_data)

        display_decoded_content(binary_data)

    except FileNotFoundError:
        print(f"File '{file_name}' not found. Please check the file path and try again.")
