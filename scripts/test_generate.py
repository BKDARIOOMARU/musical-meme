"""Generate a sample instrumental WAV using the app's synth algorithm (standalone).

Run: python3 scripts/test_generate.py
"""
import os
import numpy as np
import scipy.signal
import soundfile as sf


def synth_melody(prompt, tempo, duration, genre, sr=22050, seed=0):
    rng = np.random.RandomState(seed)
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)

    base = {
        "Electronic": 55.0,
        "Pop": 65.0,
        "Classical": 55.0,
        "Hip-Hop": 50.0,
        "Ambient": 32.0,
    }.get(genre, 55.0)

    intervals = np.array([0, 2, 4, 7, 9])

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
        env = np.linspace(0, 1, idx1 - idx0)
        wave = 0.8 * np.sin(2 * np.pi * freq * t[idx0:idx1]) * env
        wav[idx0:idx1] += wave

    beat_period = int(sr * (60.0 / tempo))
    for i in range(0, len(t), beat_period):
        length = min(400, len(t) - i)
        click = rng.randn(length) * np.exp(-np.linspace(0, 5, length))
        wav[i:i+length] += 0.5 * click

    # lowpass
    b, a = scipy.signal.butter(4, 8000 / (sr / 2))
    try:
        wav = scipy.signal.filtfilt(b, a, wav)
    except Exception:
        pass

    wav = wav / (np.max(np.abs(wav)) + 1e-9)
    return wav.astype(np.float32)


if __name__ == "__main__":
    out_dir = os.path.join(os.getcwd(), "samples")
    os.makedirs(out_dir, exist_ok=True)

    wav = synth_melody(prompt="bright synth arpeggio", tempo=110, duration=10, genre="Electronic", sr=22050, seed=42)
    out_path = os.path.join(out_dir, "sample_instrumental.wav")
    sf.write(out_path, wav, 22050)
    print("Wrote:", out_path)
    print("Max amplitude:", float(np.max(np.abs(wav))))
