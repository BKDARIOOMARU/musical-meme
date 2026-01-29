import os
import tempfile
import hashlib
from io import BytesIO

import numpy as np
import scipy.signal
import soundfile as sf
import streamlit as st

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

try:
    from pydub import AudioSegment
except Exception:
    AudioSegment = None


def seed_from_text(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % (2 ** 31)


def synth_melody(prompt, tempo, duration, genre, sr=22050, seed=0):
    """Generate instrumental melody using algorithmic synthesis."""
    rng = np.random.RandomState(seed)
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)

    # Choose scale and base freq by genre
    base = {
        "Electronic": 55.0,
        "Pop": 65.0,
        "Classical": 55.0,
        "Hip-Hop": 50.0,
        "Ambient": 32.0,
    }.get(genre, 55.0)

    # Simple pentatonic-like scale intervals
    intervals = np.array([0, 2, 4, 7, 9])

    # melody notes over time
    beats = int(np.ceil(duration * (tempo / 60.0)))
    notes = rng.choice(intervals, size=beats) + rng.randint(0, 3, size=beats) * 12
    note_times = np.linspace(0, duration, beats, endpoint=False)

    wav = np.zeros_like(t)
    for n, start in zip(notes, note_times):
        freq = base * (2 ** (n / 12.0))
        idx0 = int(start * sr)
        idx1 = min(len(t), idx0 + int(sr * (60.0 / tempo)))
        if idx1 <= idx0:
            continue
        dur_samples = idx1 - idx0
        
        # Smooth envelope (attack, sustain, release)
        attack_len = max(1, int(0.05 * sr))
        release_len = max(1, int(0.1 * sr))
        if dur_samples <= attack_len + release_len:
            env = np.linspace(0, 1, dur_samples // 2).tolist() + np.linspace(1, 0, dur_samples - dur_samples // 2).tolist()
            env = np.array(env)
        else:
            attack = np.linspace(0, 1, attack_len)
            sustain = np.ones(dur_samples - attack_len - release_len)
            release = np.linspace(1, 0, release_len)
            env = np.concatenate([attack, sustain, release])
        
        # Add harmonics for richer sound
        wave = 0.8 * np.sin(2 * np.pi * freq * t[idx0:idx1])
        wave += 0.3 * np.sin(2 * np.pi * freq * 2 * t[idx0:idx1])  # 2nd harmonic
        wave += 0.15 * np.sin(2 * np.pi * freq * 3 * t[idx0:idx1]) # 3rd harmonic
        wave *= env
        wav[idx0:idx1] += wave

    # Add a simple percussive beat with more character
    beat_period = int(sr * (60.0 / tempo))
    for i in range(0, len(t), beat_period):
        length = min(800, len(t) - i)
        # Kick-like sound: low-frequency decay
        click = 0.6 * np.sin(2 * np.pi * 60 * t[i:i+length]) * np.exp(-np.linspace(0, 3, length))
        click += 0.3 * rng.randn(length) * np.exp(-np.linspace(0, 5, length))
        wav[i:i+length] += click

    # Apply simple reverb (add delayed copies)
    for delay in [int(0.05*sr), int(0.1*sr)]:
        if delay < len(wav):
            wav[delay:] += 0.3 * wav[:-delay]
    
    # Gentle lowpass to smooth
    b, a = scipy.signal.butter(4, 8000 / (sr / 2))
    try:
        wav = scipy.signal.filtfilt(b, a, wav)
    except Exception:
        pass

    # Normalize
    wav = wav / (np.max(np.abs(wav)) + 1e-9)
    return wav.astype(np.float32)


def synth_vocals(lyrics: str, sr=22050):
    """Convert lyrics to sung vocals using TTS."""
    if pyttsx3 is None:
        raise RuntimeError("pyttsx3 is not installed; vocals unavailable")

    engine = pyttsx3.init()
    # Save to temporary WAV
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    engine.save_to_file(lyrics, path)
    engine.runAndWait()

    data, sr_read = sf.read(path, dtype="float32")
    os.remove(path)

    # If stereo, mix to mono
    if data.ndim > 1:
        data = np.mean(data, axis=1)

    # Apply a simple pitch modulation to approximate singing
    t = np.arange(len(data)) / sr_read
    lfo = 1.0 + 0.02 * np.sin(2 * np.pi * 5.0 * t)
    data_mod = scipy.signal.resample(data * lfo, int(len(data) * (sr / sr_read)))
    data_mod = data_mod / (np.max(np.abs(data_mod)) + 1e-9)
    return data_mod.astype(np.float32), sr


def write_wav_bytes(wav, sr):
    """Write WAV array to bytes."""
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    sf.write(path, wav, sr)
    with open(path, "rb") as f:
        b = f.read()
    os.remove(path)
    return b


def wav_to_mp3_bytes(wav_bytes):
    """Convert WAV bytes to MP3 bytes."""
    if AudioSegment is None:
        raise RuntimeError("pydub/ffmpeg not available for MP3 export")
    audio = AudioSegment.from_file(BytesIO(wav_bytes), format="wav")
    out = BytesIO()
    audio.export(out, format="mp3")
    return out.getvalue()


st.set_page_config(page_title="AI Music Generator", layout="wide")

st.title("AI Music Generator — Musical Meme")
st.write("Generate instrumentals and sung vocals from prompts and lyrics.")

with st.sidebar:
    st.header("Generation Options")
    mode = st.selectbox("Mode", ["Instrumental", "Lyrics to Vocals", "Random"])
    genre = st.selectbox("Genre", ["Electronic", "Pop", "Classical", "Hip-Hop", "Ambient"])
    tempo = st.slider("Tempo (BPM)", 60, 160, 100)
    duration = st.slider("Duration (seconds)", 5, 60, 15)
    sr = st.selectbox("Sample rate", [22050, 32000, 44100], index=0)
    seed_text = st.text_input("Seed text (optional)")
    seed = seed_from_text(seed_text) if seed_text.strip() else st.number_input("Seed", value=0, step=1)

st.markdown("---")

if mode == "Instrumental":
    prompt = st.text_input("Prompt (describe mood, instruments, motifs)")
elif mode == "Lyrics to Vocals":
    lyrics = st.text_area("Enter lyrics to convert to sung vocals")
else:
    prompt = "random"
    lyrics = "La la la"

preview_len = st.sidebar.slider("Preview length (seconds)", 3, 10, 5)

col1, col2 = st.columns(2)

@st.cache_data(show_spinner=False)
def generate_preview_bytes(mode, prompt_arg, lyrics_arg, tempo, genre, sr, seed, preview_len):
    """Cache-friendly preview generation."""
    try:
        if mode == "Lyrics to Vocals":
            s, sr_out = synth_vocals(lyrics_arg or "", sr=sr)
            max_samples = int(preview_len * sr_out)
            s = s[:max_samples]
            return write_wav_bytes(s, sr_out)
        else:
            s = synth_melody(prompt_arg or "", tempo, preview_len, genre, sr=sr, seed=seed)
            return write_wav_bytes(s, sr)
    except Exception as e:
        return None

with col1:
    if st.button("Generate"):
        try:
            if mode == "Instrumental":
                s = synth_melody(prompt or "", tempo, duration, genre, sr=sr, seed=seed)
                wav_bytes = write_wav_bytes(s, sr)
                st.audio(wav_bytes)
                st.download_button("Download WAV", data=wav_bytes, file_name="instrumental.wav", mime="audio/wav")
                try:
                    mp3_bytes = wav_to_mp3_bytes(wav_bytes)
                    st.download_button("Download MP3", data=mp3_bytes, file_name="instrumental.mp3", mime="audio/mpeg")
                except Exception:
                    st.info("MP3 export unavailable (requires pydub + ffmpeg)")

            elif mode == "Lyrics to Vocals":
                if not lyrics.strip():
                    st.error("Please provide lyrics.")
                else:
                    s, sr_out = synth_vocals(lyrics, sr=sr)
                    wav_bytes = write_wav_bytes(s, sr_out)
                    st.audio(wav_bytes)
                    st.download_button("Download WAV", data=wav_bytes, file_name="vocals.wav", mime="audio/wav")
            else:
                s = synth_melody(prompt, tempo, duration, genre, sr=sr, seed=seed)
                wav_bytes = write_wav_bytes(s, sr)
                st.audio(wav_bytes)
                st.download_button("Download WAV", data=wav_bytes, file_name="random.wav", mime="audio/wav")

        except Exception as e:
            st.exception(e)

    # Fast preview controls
    if st.button("Play Preview"):
        with st.spinner("Generating preview..."):
            preview = generate_preview_bytes(
                mode, 
                prompt if mode != "Lyrics to Vocals" else None, 
                lyrics if mode == "Lyrics to Vocals" else None, 
                tempo, genre, sr, seed, preview_len
            )
            if preview is None:
                st.error("Preview generation failed (TTS or dependencies may be missing).")
            else:
                st.audio(preview)
                st.download_button("Download Preview WAV", data=preview, file_name="preview.wav", mime="audio/wav")

with col2:
    st.header("Tips & Notes")
    st.markdown("- Instrumental generation is a simple algorithmic synthesizer with harmonics and light reverb.")
    st.markdown("- Vocals use local TTS (pyttsx3) and pitch modulation to approximate singing.")
    st.markdown("- For MP3 export, install `pydub` and have `ffmpeg` available on PATH.")
    st.markdown("- Adjust `Seed` or `Seed text` for repeatable results.")
    st.markdown("- Preview length is configurable in the sidebar for quick iterations.")
