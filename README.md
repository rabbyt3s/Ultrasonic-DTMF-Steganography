# Ultrasonic DTMF Steganography

This project demonstrates how to **embed short text messages** into a standard WAV file by repurposing **DTMF (Dual-Tone Multi-Frequency)** at **ultrasonic** frequencies (around 16–20 kHz). The hidden signals are mostly inaudible to humans but can be recovered by applying a band-pass filter and an FFT-based frequency detection pipeline.

## Features

1. **Frequency Matrix**  
   A set of \(\sim\)16–20 kHz “low” and “high” frequencies are mapped to A–Z, 0–9, etc. Characters are encoded as sine tone pairs in these ultrasonic bands.

2. **Time Dispersion**  
   Each character’s ultrasonic tone is placed at different positions in the audio, reducing the chance of overlapping signals and making the injection less noticeable.

3. **Amplitudes and Fading**  
   Sine waves undergo a fade-in/out to avoid clicks, and are scaled to keep amplitude below clipping levels.

4. **Band-Pass + FFT Decoding**  
   Decoding uses a band-pass filter around 15–21 kHz, splits audio into time blocks, then performs an FFT and peak detection to identify each pair of ultrasonic frequencies and rebuild the message.

## Repository Structure

```
ultrasonic-dtmf/
├── src/
│   ├── encode.py
│   ├── decode.py
│   ├── utils.py        # Optional helper functions
│   └── compare_audio.py
├── graphs/             # Generated waveforms, spectrograms, diff signals, etc.
├── examples/           # Example WAV files
├── README.md           # This file
├── LICENSE             # Your chosen license
└── requirements.txt    # Python dependencies
```

### Scripts Overview

- **encode.py**  
  Injects ultrasonic tones for each character into an existing WAV.  
  - *Key parameters:*  
    - `--ultrasonic_amp`: amplitude scaling for ultrasonic tones  
    - `--char_dur`: duration of each character’s tone  
    - `--sample_rate`: default 44100 Hz to keep 20 kHz within Nyquist

- **decode.py**  
  Reads the potentially ultrasonic-encoded WAV file, applies a band-pass filter, and uses block-wise FFT to locate DTMF-like pairs.  
  - *Key parameters:*  
    - `--sample_rate`: must match the WAV’s sample rate (e.g. 44100)  
    - `--chunk_duration`: size of each block in seconds for FFT detection

- **compare_audio.py** (Optional)  
  Generates waveforms, spectrograms, and difference plots to visualize whether the ultrasonic injection is visible or not.

## Installation

1. **Clone** this repository or download the zip:
   ```bash
   git clone https://github.com/rabbyt3s/ultrasonic-dtmf.git
   ```
2. **Install Dependencies**:
   ```bash
   cd ultrasonic-dtmf
   pip install -r requirements.txt
   ```
   Make sure you have Python 3.7+ and packages like `numpy`, `scipy`, `soundfile`, `matplotlib`.

## Usage

### 1. Encoding a Message

```bash
python src/encode.py "HELLO ULTRA" examples/original.wav \
    --output examples/encoded.wav \
    --ultrasonic_amp 0.1 \
    --char_dur 0.15 \
    --sample_rate 44100
```

- **`"HELLO ULTRA"`**: The message to embed.  
- **`examples/original.wav`**: Your input WAV.  
- **`--output examples/encoded.wav`**: The final file with ultrasonic injection.  
- **`--ultrasonic_amp`**: If set too low, the injection may be undetectable (or lost). If set too high, it might become audible or cause clipping.

### 2. Decoding

```bash
python src/decode.py examples/encoded.wav --sample_rate 44100
```

This will filter around ~15–21 kHz and perform block-wise FFT to detect pairs of frequencies, printing the recovered message to the terminal.

### 3. Visualizing the Differences (Optional)

```bash
python src/compare_audio.py
# Then enter:
# Original file: examples/original.wav
# Encoded file:  examples/encoded.wav
```

The script outputs images in `graphs/` showing:
- **wave_original.png**  
- **wave_encoded.png**  
- **wave_diff.png**  
- **spectrogram_comparison.png**

These confirm if ultrasonic tones are visible or remain subtle.

## Tips and Limitations

- **Hardware Roll-Off**: Many consumer speakers and microphones attenuate or distort signals above ~18 kHz. Success varies by device.  
- **Compression**: Formats like MP3 typically remove high frequencies, destroying hidden data. Use uncompressed WAV for best results.  
- **Amplitude Balancing**: Ultrasonic signals must be high enough for decoding but not so high that they become audible or damage the audio.  
- **Data Capacity**: Each character consumes a chunk of time; this method is best for short messages.

## License

Choose a license that suits your project (MIT, Apache-2.0, etc.). See `LICENSE` for details.

## Author

**Yassine TAMANI**  
GitHub: [rabbyt3s](https://github.com/rabbyt3s)  

For questions, feedback, or collaboration requests, feel free to open an issue or submit a pull request.

---

**Enjoy exploring ultrasonic DTMF steganography!** If you find this useful or have ideas for improvement, please reach out.
