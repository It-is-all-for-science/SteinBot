import whisper
from pydub import AudioSegment
import os

def ogg_to_wav(ogg_path):
    wav_path = ogg_path.replace('.ogg', '.wav')
    audio = AudioSegment.from_ogg(ogg_path)
    audio.export(wav_path, format="wav")
    return wav_path

def transcribe_voice(ogg_path):
    wav_path = ogg_to_wav(ogg_path)
    model = whisper.load_model("small")
    result = model.transcribe(wav_path)
    if os.path.exists(wav_path):
        os.remove(wav_path)
    return result['text']