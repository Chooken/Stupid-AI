from TTS.api import TTS
import sounddevice as sd
import numpy as np

class Vocalizer:

    def __init__(self):

        ## Very Natural but can take extremely long time to process GPU is must have
        #self.tts_engine = TTS("tts_models/en/ek1/tacotron2", gpu=True)
        
        ## Pretty good, very quick to process
        self.tts_engine = TTS("tts_models/en/ljspeech/glow-tts")
                
        ## More Natural but sounds like a little girl -- 0.9 sec
        #self.tts_engine = TTS("tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=False)

        ## Less natural and quite quick -- 0.5 sec
        # self.tts_engine = TTS("tts_models/en/ljspeech/speedy-speech", progress_bar=False, gpu=False)

        self.Say("Stupid has booted.")

    def Say(self, sentence):

        ## Used for YourTSS Model
        # wav = self.tts_engine.tts(sentence, speaker=self.tts_engine.speakers[2], language="en")
        # sd.play(wav, 17000)

        ## Process TTS
        wav = self.tts_engine.tts(sentence)
        wav = np.multiply(wav, 0.1)
        sd.play(wav, 24000)