import librosa
import soundfile as sf
import numpy as np
from scipy.signal import butter, sosfilt


# ============================================================
# VOICE PRESETS
# ============================================================

PRESETS = {

    "normal": {
        "pitch": 0,
        "bass": 0,
        "treble": 0,
        "roughness": 0,
    },

    # Suara lebih berat, warm, sedikit husky
    "deep_husky": {
        "pitch": -1.2,
        "bass": 2.5,
        "treble": -1.5,
        "roughness": 0.025,
    },

    # Lebih berat lagi
    "deep": {
        "pitch": -1.8,
        "bass": 3.5,
        "treble": -2,
        "roughness": 0.035,
    },
}


# ============================================================
# LOW SHELF / BASS
# ============================================================

def apply_low_shelf(audio, sr, gain_db, cutoff=180):

    if gain_db == 0:
        return audio

    sos = butter(
        2,
        cutoff,
        btype="lowpass",
        fs=sr,
        output="sos"
    )

    low = sosfilt(sos, audio)

    gain = 10 ** (gain_db / 20)

    return audio + (gain - 1) * low


# ============================================================
# HIGH SHELF / TREBLE
# ============================================================

def apply_high_shelf(audio, sr, gain_db, cutoff=4000):

    if gain_db == 0:
        return audio

    sos = butter(
        2,
        cutoff,
        btype="highpass",
        fs=sr,
        output="sos"
    )

    high = sosfilt(sos, audio)

    gain = 10 ** (gain_db / 20)

    return audio + (gain - 1) * high


# ============================================================
# SOFT ROUGHNESS
# ============================================================

def apply_roughness(audio, amount):

    if amount <= 0:
        return audio

    # Soft saturation.
    # Memberikan sedikit tekstur/husky tanpa distorsi berat.

    drive = 1.0 + amount * 8.0

    processed = np.tanh(
        audio * drive
    )

    # Campur dengan suara asli
    mix = amount * 2.5

    mix = min(mix, 0.18)

    return (
        audio * (1.0 - mix)
        + processed * mix
    )


# ============================================================
# MAIN VOICE FILTER
# ============================================================

def apply_voice_filter(
    input_path,
    output_path,
    preset="deep_husky"
):

    if preset not in PRESETS:
        preset = "normal"

    settings = PRESETS[preset]

    print(
        f"[VOICE FILTER] Preset: {preset}"
    )

    print(
        f"[VOICE FILTER] Pitch: "
        f"{settings['pitch']}"
    )

    # ========================================================
    # LOAD
    # ========================================================

    audio, sr = librosa.load(
        input_path,
        sr=None,
        mono=True
    )

    # ========================================================
    # PITCH
    # ========================================================

    if settings["pitch"] != 0:

        audio = librosa.effects.pitch_shift(
            audio,
            sr=sr,
            n_steps=settings["pitch"]
        )

    # ========================================================
    # BASS
    # ========================================================

    audio = apply_low_shelf(
        audio,
        sr,
        settings["bass"]
    )

    # ========================================================
    # TREBLE
    # ========================================================

    audio = apply_high_shelf(
        audio,
        sr,
        settings["treble"]
    )

    # ========================================================
    # HUSKY / ROUGHNESS
    # ========================================================

    audio = apply_roughness(
        audio,
        settings["roughness"]
    )

    # ========================================================
    # NORMALIZE
    # ========================================================

    peak = np.max(
        np.abs(audio)
    )

    if peak > 0:

        audio = (
            audio / peak
        ) * 0.92

    # ========================================================
    # SAVE
    # ========================================================

    sf.write(
        output_path,
        audio,
        sr,
        subtype="PCM_16"
    )

    print(
        f"[VOICE FILTER] Saved: "
        f"{output_path}"
    )

    return output_path