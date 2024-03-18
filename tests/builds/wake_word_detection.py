import os
import speech_recognition as sr
import whisper

class WhisperASR:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    curr_dir = script_dir.replace('\\', '/')
    tiny_model_path = os.path.expanduser(f'{script_dir}/models/tiny.en.pt')

    def __init__(self):
        self.model = whisper.load_model(self.tiny_model_path)
        self.mic = sr.Microphone()
        self.recognizer = sr.Recognizer()

        self.wake_word = "okay whisper"

    def transcribe_to_text(self, audio):
        result = self.model.transcribe(audio, fp16=False)
        text = result['text']
        return text

    def recognize_speech(self):
        with self.mic as source:
            while True:
                print("listening for wake word")
                try:
                    self.recognizer.adjust_for_ambient_noise(source)

                    audio = self.recognizer.listen(source, timeout=5)

                    with open('speech.wav', 'wb') as f:
                        f.write(audio.get_wav_data())
                        
                    
                    text = self.transcribe_to_text('speech.wav')
                    text = text.split()
                    text = ' '.join(text)
                    text = text.lower()

                    if self.wake_word in text:
                        print("State your demands.")
                        try:
                            self.recognizer.adjust_for_ambient_noise(source)

                            audio = self.recognizer.listen(source, timeout=5)

                            with open('speech.wav', 'wb') as f:
                                f.write(audio.get_wav_data())
                                
                            
                            text = self.transcribe_to_text('speech.wav')
                            text = text.split()
                            text = ' '.join(text)
                            text = text.lower()

                            print(text)

                        except sr.UnknownValueError:
                            continue
                        except sr.RequestError as e:
                            continue
                        except sr.WaitTimeoutError:
                            continue

                except sr.UnknownValueError:
                    continue
                except sr.RequestError as e:
                    continue
                except sr.WaitTimeoutError:
                    continue

    def listen_command(self, text):
        if 'show' in text and 'text' in text:
            print(f'text is: {text}')

asr = WhisperASR()
asr.recognize_speech()