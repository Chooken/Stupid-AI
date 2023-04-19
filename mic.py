import speech_recognition as sr
import whisper
import queue
import threading
import torch
import numpy as np
import time

class MicTranscription():

    running = True

    def __init__(self) -> None:

        ## Init Model Type
        self.audio_model = whisper.load_model("tiny.en")

        ## Init Queues for Threading
        self.audio_queue = queue.Queue()
        self.result_queue = queue.Queue()

        ## Start the threads
        threading.Thread(target=self.record_audio).start()
        threading.Thread(target=self.transcribe_forever).start()
        
    def record_audio(self) -> None:

        #load the speech recognizer and set the initial energy threshold and pause threshold
        r = sr.Recognizer()
        r.energy_threshold = 300
        r.pause_threshold = 0.8
        r.dynamic_energy_threshold = False

        ## Grab the mic
        with sr.Microphone(sample_rate=16000) as source:
            print("Say something!")
            while True:

                ## Stop Thread when application is closed
                if not self.running:
                    break

                ## Listen to mic for input
                try:
                    audio = r.listen(source, 2)
                except:
                    continue

                ## Do stuff to audio
                torch_audio = torch.from_numpy(np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0)
                audio_data = torch_audio

                ## Put Audio data into the queue to be transcribed
                self.audio_queue.put_nowait(audio_data)


    def transcribe_forever(self) -> None:
        while True:

            ## Stop Thread when application is closed
            if not self.running:
                    break

            ## Try to Grab audio from queue otherwise waits 0.16 ms until retry
            try:
                audio_data = self.audio_queue.get(False)
            except queue.Empty:
                time.sleep(0.16)
                continue

            ## Transcribe Audio from data
            result = self.audio_model.transcribe(audio_data, fp16=False, language='english')

            ## Grab the transcribed text and put in results queue
            predicted_text = result["text"]
            self.result_queue.put_nowait(predicted_text.strip())
