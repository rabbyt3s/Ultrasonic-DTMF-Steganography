![image](https://github.com/user-attachments/assets/c7576b5f-9b7d-4cbc-97df-f88899df0eae)


# Ultrasonic DTMF Steganography

A simple proof-of-concept demonstrating how to **hide short text messages** within a WAV file by moving DTMF tones into the **16–20 kHz** ultrasonic range. Humans typically cannot hear those frequencies, but a filter and FFT-based decoder can extract them.

## Repository Structure

```
rabbyt3s/
├── README.md                        <-- This file
├── Ultrasonic-DTMF-Steganography.pdf
├── decode.py
├── encode.py
└── utils.py
```

- **README.md**: Instructions and project overview.  
- **Ultrasonic-DTMF-Steganography.pdf**: A more detailed document/paper about the project.  
- **encode.py**: Script to embed ultrasonic messages into a WAV file.  
- **decode.py**: Script to detect and decode those ultrasonic messages.  
- **utils.py**: Optional helper functions (filtering, plotting, etc.).

## Quick Start

### 1. Encoding an Ultrasonic Message

```bash
python encode.py "HELLO ULTRASONIC" path/to/original.wav
```

- **`"HELLO ULTRASONIC"`**: The message text to embed.
- **`path/to/original.wav`**: The input WAV file (should be 44.1 kHz for best results).

By default:
- **`--ultrasonic_amp`** (amplitude) is set to 0.1,  
- **`--char_dur`** (duration per character) is 0.15 seconds,  
- **`--sample_rate`** is 44100 Hz.

If you want to override them, you can specify, for example:
```bash
python encode.py "HELLO" path/to/original.wav \
    --output path/to/encoded.wav \
    --ultrasonic_amp 0.2 \
    --char_dur 0.12 \
    --sample_rate 44100
```

Otherwise, **default values** will be used.

### 2. Decoding

```bash
python decode.py path/to/encoded.wav
```

Again, you can override certain parameters like `--sample_rate`, but they default to 44100 if omitted.

### 3. Reviewing Results

1. **Check the console** output for the recovered text.  
2. **(Optional)** Inspect the audio in an editor (like Audacity) to see if there’s additional energy around 16–20 kHz.  
3. **(Optional)** Generate wave or spectrogram plots if you have separate visualization scripts.

## Notes and Limitations

- **Hardware Limitations**: Many standard speakers and mics roll off beyond ~18 kHz.  
- **File Format**: Uncompressed WAV recommended. MP3/AAC compression can strip out high frequencies.  
- **Data Capacity**: Each character is mapped to a pair of ultrasonic frequencies. Large messages may become more audible if amplitude is raised.  
- **Amplitude Tuning**: If `--ultrasonic_amp` is too high, the signal could become faintly audible or distort the original. If too low, decoding might fail.

## More Details

See **Ultrasonic-DTMF-Steganography.pdf** for a technical overview, including how the scripts work, the frequencies used, and best practices for successful encoding/decoding.

## Author

**Yassine TAMANI**  
GitHub: [rabbyt3s](https://github.com/rabbyt3s)

Feel free to submit pull requests or open issues for suggestions/improvements. Enjoy experimenting with **Ultrasonic DTMF Steganography**!
