# src/utils.py
import numpy as np
from scipy.signal import butter, filtfilt

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    if highcut >= nyq:
        raise ValueError(
            f"Highcut={highcut} Hz >= Nyquist={nyq} Hz; lower your frequencies or increase the sample_rate."
        )
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def plot_signal(signal, sr, title, output_path, duration=None):
    """
    Generates and saves a plot of the audio signal.
    Optionally limits the displayed duration.
    """
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 4))
    if duration:
        samples = int(sr * duration)
        times = np.arange(samples) / sr
        plt.plot(times, signal[:samples])
    else:
        times = np.arange(len(signal)) / sr
        plt.plot(times, signal)
    plt.title(title)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_fft(signal, sr, title, output_path, low_freq=20000, high_freq=27000):
    """
    Generates and saves a plot of the filtered signal's Fourier transform.
    Adjusted for ultrasonic frequencies (20-27 kHz)
    """
    import matplotlib.pyplot as plt
    from scipy.signal import butter, filtfilt

    b, a = butter_bandpass(low_freq, high_freq, sr, order=5)
    filtered = filtfilt(b, a, signal)
    window = np.hanning(len(filtered))
    windowed = filtered * window
    fft_result = np.abs(np.fft.fft(windowed))
    freqs = np.fft.fftfreq(len(windowed), 1 / sr)
    
    pos_mask = freqs > 0
    freqs = freqs[pos_mask]
    fft_result = fft_result[pos_mask]
    
    plt.figure(figsize=(12, 6))
    plt.plot(freqs, fft_result)
    plt.title(title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.xlim(19000, 28000)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def generate_capacity_graph(max_duration, char_duration, gap_duration, output_path):
    """
    Generates a graph showing the estimated message storage capacity based on audio duration
    
    Args:
        max_duration (float): Maximum duration to analyze in seconds
        char_duration (float): Character duration in seconds
        gap_duration (float): Duration of silence between characters in seconds
        output_path (str): Path to save the graph
    """
    durations = np.arange(0, max_duration + 1, 30)  # Points every 30 seconds
    char_capacity = durations / (char_duration + gap_duration)
    
    plt.figure(figsize=(12, 6))
    plt.plot(durations / 60, char_capacity, 'b-', linewidth=2)
    plt.title("Storage Capacity Estimation")
    plt.xlabel("Audio Duration (minutes)")
    plt.ylabel("Number of Characters")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print("[GRAPH] capacity_estimation.png generated.")
