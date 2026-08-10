import json
import sys
import wave
import vosk

MODEL_PATH = 'model'

vosk.SetLogLevel(-1)


def transcribe(wav_path):
    wf = wave.open(wav_path, 'rb')
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != 'NONE':
        raise ValueError('WAVはmono, 16bit, PCM形式である必要があります')

    model = vosk.Model(MODEL_PATH)
    recognizer = vosk.KaldiRecognizer(model, wf.getframerate())

    texts = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            texts.append(json.loads(recognizer.Result())['text'])

    texts.append(json.loads(recognizer.FinalResult())['text'])
    return ''.join(texts)


if __name__ == '__main__':
    print(transcribe(sys.argv[1]))
