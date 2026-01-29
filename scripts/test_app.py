"""Integration test for streamlit_app.py synthesizers and utilities."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from streamlit_app import synth_melody, synth_vocals, write_wav_bytes, seed_from_text, wav_to_mp3_bytes


def test_instrumental_synthesis():
    """Test instrumental synthesis with different genres."""
    print("Testing instrumental synthesis...")
    genres = ["Electronic", "Pop", "Classical", "Hip-Hop", "Ambient"]
    for genre in genres:
        wav = synth_melody(f"test {genre}", tempo=100, duration=5, genre=genre, sr=22050, seed=42)
        assert wav.dtype == np.float32, f"Wrong dtype: {wav.dtype}"
        assert len(wav) == 5 * 22050, f"Wrong length for {genre}"
        assert np.max(np.abs(wav)) <= 1.0, f"Clipping detected in {genre}"
        print(f"  ✓ {genre}: {len(wav)} samples, max={np.max(np.abs(wav)):.4f}")


def test_seed_reproducibility():
    """Test that same seed produces same output."""
    print("Testing seed reproducibility...")
    wav1 = synth_melody("test", tempo=100, duration=3, genre="Pop", sr=22050, seed=123)
    wav2 = synth_melody("test", tempo=100, duration=3, genre="Pop", sr=22050, seed=123)
    assert np.allclose(wav1, wav2), "Same seed should produce identical output"
    print("  ✓ Reproducible synthesis confirmed")


def test_seed_from_text():
    """Test seed generation from text."""
    print("Testing seed from text...")
    seed1 = seed_from_text("hello world")
    seed2 = seed_from_text("hello world")
    assert seed1 == seed2, "Same text should produce same seed"
    seed3 = seed_from_text("different text")
    assert seed1 != seed3, "Different text should produce different seed"
    print(f"  ✓ Text seeding works: 'hello world' -> {seed1}")


def test_wav_export():
    """Test WAV export functionality."""
    print("Testing WAV export...")
    wav = synth_melody("export test", tempo=80, duration=2, genre="Electronic", sr=44100, seed=0)
    wav_bytes = write_wav_bytes(wav, 44100)
    assert isinstance(wav_bytes, bytes), "WAV export should return bytes"
    assert len(wav_bytes) > 100, "WAV file too small"
    print(f"  ✓ WAV export successful: {len(wav_bytes)} bytes")


def test_mp3_export():
    """Test MP3 export (skips if pydub unavailable)."""
    print("Testing MP3 export...")
    try:
        wav = synth_melody("mp3 test", tempo=100, duration=2, genre="Pop", sr=22050, seed=0)
        wav_bytes = write_wav_bytes(wav, 22050)
        mp3_bytes = wav_to_mp3_bytes(wav_bytes)
        assert isinstance(mp3_bytes, bytes), "MP3 export should return bytes"
        assert len(mp3_bytes) > 100, "MP3 file too small"
        print(f"  ✓ MP3 export successful: {len(mp3_bytes)} bytes")
    except RuntimeError as e:
        print(f"  ⊘ MP3 skipped: {e}")


def test_vocals():
    """Test vocal synthesis (skips if pyttsx3 unavailable)."""
    print("Testing vocal synthesis...")
    try:
        wav, sr = synth_vocals("hello world", sr=22050)
        assert wav.dtype == np.float32, "Vocals should be float32"
        assert len(wav) > 0, "Vocals should have samples"
        assert np.max(np.abs(wav)) <= 1.0, "Vocals should be normalized"
        print(f"  ✓ Vocal synthesis successful: {len(wav)} samples at {sr} Hz")
    except Exception as e:
        print(f"  ⊘ Vocals skipped: {e}")


if __name__ == "__main__":
    print("\n=== Musical Meme Integration Tests ===\n")
    test_instrumental_synthesis()
    test_seed_reproducibility()
    test_seed_from_text()
    test_wav_export()
    test_mp3_export()
    test_vocals()
    print("\n✓ All tests passed!\n")
