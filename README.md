

# Ultrasonic DTMF Steganography

A simple proof-of-concept demonstrating how to **hide short text messages** within a WAV file by moving DTMF tones into the **20.5–26 kHz** ultrasonic range. Humans typically cannot hear those frequencies, but a filter and FFT-based decoder can extract them.

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
- **Ultrasonic-DTMF-Steganography.pdf**: A detailed document/paper about the project.  
- **encode.py**: Script to embed ultrasonic messages into a WAV file.  
- **decode.py**: Script to detect and decode those ultrasonic messages.  
- **utils.py**: Helper functions (filtering, plotting, etc.).

## Quick Start

### 1. Encoding an Ultrasonic Message

```bash
python encode.py "HELLO ULTRASONIC" path/to/original.wav
```

- **`"HELLO ULTRASONIC"`**: The message text to embed.
- **`path/to/original.wav`**: The input WAV file (should be **96 kHz** for best results).

By default:
- **`--ultrasonic_amp`** (amplitude) is set to **0.1**,  
- **`--char_dur`** (duration per character) is **0.15 seconds**,  
- **`--sample_rate`** is **96000 Hz**.

If you want to override them, you can specify, for example:

```bash
python encode.py "HELLO" path/to/original.wav \
    --output path/to/encoded.wav \
    --ultrasonic_amp 0.2 \
    --char_dur 0.12 \
    --sample_rate 96000
```

Otherwise, **default values** will be used.

### 2. Decoding

```bash
python decode.py path/to/encoded.wav
```

You can also override certain parameters like `--sample_rate`, but they default to **96000 Hz** if omitted.

### 3. Reviewing Results

1. **Check the console** output for the recovered text.  
2. **(Optional)** Inspect the audio in an editor (like Audacity) to see if there’s additional energy around **20.5–26 kHz**.  
3. **(Optional)** Generate wave or spectrogram plots using the `compare_audio.py` script to visualize the differences.

## Notes and Limitations

- **Hardware Limitations**: Many standard speakers and microphones roll off beyond ~20 kHz.  
- **File Format**: Uncompressed WAV is recommended. MP3/AAC compression can strip out high frequencies.  
- **Data Capacity**: Each character is mapped to a pair of ultrasonic frequencies. Large messages may become more audible if amplitude is raised.  
- **Amplitude Tuning**: If `--ultrasonic_amp` is too high, the signal could become faintly audible or distort the original. If too low, decoding might fail.

## More Details

See **Ultrasonic-DTMF-Steganography.pdf** for a technical overview, including how the scripts work, the frequencies used, and best practices for successful encoding/decoding.

## Usage Examples

### Encoding with Default Parameters

```bash
python encode.py "SECRET" original.wav
```

This command embeds the message "SECRET" into `original.wav` and outputs `encoded_phrase_ultrasonic.wav` with default settings.

### Encoding with Custom Parameters

```bash
python encode.py "CONFIDENTIAL" original.wav \
    --output confidential_encoded.wav \
    --ultrasonic_amp 0.05 \
    --char_dur 0.2 \
    --sample_rate 96000
```

This command embeds the message "CONFIDENTIAL" into `original.wav`, outputs to `confidential_encoded.wav`, sets the ultrasonic amplitude to **0.05**, character duration to **0.2 seconds**, and ensures the sample rate is **96 kHz**.

### Decoding a Message

```bash
python decode.py encoded_phrase_ultrasonic.wav
```

This command decodes the hidden message from `encoded_phrase_ultrasonic.wav` and prints the recovered text to the console.

### Comparing Original and Encoded Audio

To visually inspect the encoding, you can use the `compare_audio.py` script:

```bash
python compare_audio.py original.wav encoded_phrase_ultrasonic.wav --output graphs
```

This generates the following in the `graphs` directory:
- **wave_original.png**: Original audio waveform.
- **wave_encoded.png**: Encoded audio waveform containing ultrasonic signals.
- **spectrogram_comparison.png**: Comparative spectrograms showing ultrasonic bands injected around **20.5–26 kHz**.
- **difference_spectrum.png**: Difference spectrum (if enabled).
- **analysis_stats.txt**: Statistical analysis including SNR and amplitude ratios.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, feel free to reach out via GitHub Issues or contact me directly through my [GitHub profile](https://github.com/rabbyt3s).
