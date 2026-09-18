# Record microphone audio to a WAV file.
import sounddevice as sd
import soundfile as sf


def record_mic(seconds, out_path, samplerate=16000):
    # Record from the default mic for `seconds` and save as WAV.
    print("Recording for %ds... speak now!" % seconds)
    audio = sd.rec(int(seconds * samplerate), samplerate=samplerate,
                   channels=1, dtype="float32")
    sd.wait()
    sf.write(out_path, audio, samplerate)
    print("Saved to %s" % out_path)
    return out_path