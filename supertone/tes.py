from supertonic import TTS

tts = TTS(auto_download=True)
style = tts.get_voice_style("F1")

wav, duration = tts.synthesize(
    text="Aku punya suara anime/VTuber atau suara seseorang, lalu AI Companion berbicara dengan suara itu.",
    lang="id",
    voice_style=style,
)

tts.save_audio(wav, "hasil.wav")

print("Selesai! Audio disimpan sebagai hasil.wav")