# AI Music Generator — Musical Meme

An interactive Streamlit app that generates music and vocals using algorithmic synthesis. Create instrumental tracks from text prompts, convert lyrics into sung vocals, explore random melodies, and download results as `.wav` or `.mp3`.

## Features

- **Instrumental Generation**: Create synthesized melodies with customizable tempo, genre, and duration using harmonic synthesis with attack/sustain/release envelopes and light reverb.
- **Lyrics to Vocals**: Convert text lyrics into sung vocals using local TTS with pitch modulation.
- **Random Mode**: Explore procedurally generated random compositions.
- **Genre Presets**: Electronic, Pop, Classical, Hip-Hop, Ambient with different base frequencies and note patterns.
- **Preview Playback**: Fast cached preview generation with configurable length for quick iteration.
- **Download Options**: Export as WAV directly, or MP3 (with ffmpeg).
- **Seed Control**: Use text prompts or numeric seeds for reproducible results.
- **Adjustable Parameters**: Tempo (60–160 BPM), duration (5–60 sec), sample rate (22.05–44.1 kHz).

## Quick Start

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run

```bash
streamlit run streamlit_app.py
```

Then open your browser to `http://localhost:8501`.

## Optional Dependencies

For MP3 export, install `ffmpeg` on your system:

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows (with choco)
choco install ffmpeg
```

For vocal synthesis, ensure `espeak` or `espeak-ng` is installed (TTS backend):

```bash
# Ubuntu/Debian
sudo apt-get install espeak-ng

# macOS
brew install espeak
```

## Architecture

- **Synthesis Engine** (`synth_melody`): Generates harmonic melodies with percussive beat using numpy and scipy.
- **Vocal Processing** (`synth_vocals`): TTS + pitch modulation for sung effect.
- **File I/O** (`write_wav_bytes`, `wav_to_mp3_bytes`): Temporary file handling for audio formats.
- **Streamlit UI**: Two-column layout with sidebar controls and preview/generation buttons.
- **Caching**: Preview generation cached for fast re-playback.

## Testing

Run the integration test suite:

```bash
python3 scripts/test_app.py
```

Generates a sample instrumental:

```bash
python3 scripts/test_generate.py
```

## Notes

- The generator is algorithmic and intended as a demo/prototype, not production-grade AI audio.
- Vocals rely on system TTS quality (pyttsx3 backend).
- Seed-based reproducibility ensures consistent output for the same parameters.
- Large durations (>30 sec) may take several seconds to generate.
