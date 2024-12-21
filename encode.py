# src/encode.py
import numpy as np
import soundfile as sf
from scipy.signal import find_peaks, butter, filtfilt
import argparse
import os
from utils import butter_bandpass, plot_signal, plot_fft
import scipy.signal

# Global Parameters and Matrices
FREQS_LOW =  [20500, 21000, 21500, 22000, 22500, 23000, 23500]
FREQS_HIGH = [24000, 24500, 25000, 25500, 26000]

EXTENDED_MATRIX = [
    ['A', 'B', 'C', 'D', 'E'],
    ['F', 'G', 'H', 'I', 'J'],
    ['K', 'L', 'M', 'N', 'O'],
    ['P', 'Q', 'R', 'S', 'T'],
    ['U', 'V', 'W', 'X', 'Y'],
    ['Z', '0', '1', '2', '3'],
    ['4', '5', '6', '7', '8']
]

def find_frequencies(char):
    for i, row in enumerate(EXTENDED_MATRIX):
        if char in row:
            return FREQS_LOW[i], FREQS_HIGH[row.index(char)]
    return None

def generate_tone(char, duration=0.2, sample_rate=96000):
    pair = find_frequencies(char)
    if not pair:
        return np.zeros(int(sample_rate * duration))
    
    freq_low, freq_high = pair
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sig_low = np.sin(2 * np.pi * freq_low * t)
    sig_high = np.sin(2 * np.pi * freq_high * t)
    signal = 0.5 * sig_low + 0.5 * sig_high
    
    # Fade in/out to avoid clicks
    fade_len = int(sample_rate * 0.01)
    if fade_len > 0 and len(signal) > 2 * fade_len:
        fade_in = np.linspace(0, 1, fade_len)
        fade_out = fade_in[::-1]
        signal[:fade_len] *= fade_in
        signal[-fade_len:] *= fade_out
    
    # Amplitude normalization
    max_amp = np.max(np.abs(signal)) + 1e-9
    signal /= max_amp
    return signal

def encode_phrase(phrase, input_wav, output_wav="encoded_phrase_ultrasonic.wav", 
                 char_dur=0.15, gap_dur=0.08, sample_rate=96000, ultrasonic_amp=0.15):
    # Read the original audio file
    audio_data, file_sr = sf.read(input_wav)
    
    # Resample if needed
    if file_sr != sample_rate:
        print(f"[INFO] Resampling input from {file_sr} Hz to {sample_rate} Hz")
        samples = len(audio_data)
        new_samples = int(samples * (sample_rate / file_sr))
        audio_data = scipy.signal.resample(audio_data, new_samples)
    
    audio_length = len(audio_data)
    
    # Generate signals for each character
    char_signals = []
    for char in phrase.upper():
        if char.isspace():
            continue
        tone = generate_tone(char, duration=char_dur, sample_rate=sample_rate)
        char_signals.append(tone)
    
    # Calculate dispersion positions
    segment_length = audio_length // (len(char_signals) + 1)
    mixed = audio_data.copy()
    
    # Disperse characters in the audio
    for i, signal in enumerate(char_signals):
        start_pos = (i + 1) * segment_length - len(signal) // 2
        if len(mixed.shape) > 1:  # If stereo
            signal_stereo = np.column_stack((signal, signal))
            mixed[start_pos:start_pos + len(signal)] += ultrasonic_amp * signal_stereo
        else:  # If mono
            mixed[start_pos:start_pos + len(signal)] += ultrasonic_amp * signal
    
    # Final normalization
    max_abs = np.max(np.abs(mixed))
    if max_abs > 1.0:
        mixed /= max_abs
        
    sf.write(output_wav, mixed.astype(np.float32), sample_rate)
    print(f"[ENCODE] Message encoded in '{output_wav}' at {sample_rate} Hz")

def main():
    parser = argparse.ArgumentParser(description='Encode an ultrasonic message in a WAV file')
    parser.add_argument('message', help='Message to encode')
    parser.add_argument('input_wav', help='Original WAV file')
    parser.add_argument('--output', '-o', default="encoded_phrase_ultrasonic.wav", help='Encoded WAV file')
    parser.add_argument('--char_dur', '-c', type=float, default=0.15, help='Duration per character (seconds)')
    parser.add_argument('--gap_dur', '-g', type=float, default=0.3, help='Duration of silence between characters (seconds)')
    parser.add_argument('--sample_rate', '-s', type=int, default=96000, help='Sample rate (Hz)')
    parser.add_argument('--ultrasonic_amp', '-a', type=float, default=0.1, help='Ultrasonic signal amplitude')
    args = parser.parse_args()
    
    encode_phrase(
        phrase=args.message,
        input_wav=args.input_wav,
        output_wav=args.output,
        char_dur=args.char_dur,
        gap_dur=args.gap_dur,
        sample_rate=args.sample_rate,
        ultrasonic_amp=args.ultrasonic_amp
    )

if __name__ == "__main__":
    main()
