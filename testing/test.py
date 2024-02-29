def whisper():
    ## whisper
    import speech_recognition as sr
    import whisper
    import tempfile
    import os

    tiny_model = whisper.load_model('models/tiny.en.pt')
    base_model = whisper.load_model('models/base.en.pt')

    def continuous_listen():
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            print("Adjusting for ambient noise. Please wait...")
            recognizer.adjust_for_ambient_noise(source, duration=5)
            print("Listening...")

        try:
            while True:
                with microphone as source:
                    try:
                        audio = recognizer.listen(source, timeout=None)
                        # Save the audio to a temporary file
                        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
                            temp_audio_path = temp_audio.name
                            temp_audio.write(audio.get_wav_data())

                        # Transcribe using Whisper
                        result = base_model.transcribe(temp_audio_path)
                        prompt_text = result['text']

                        print(f"You said: {prompt_text}")

                        if "Open" in prompt_text and "new" in prompt_text and "tab" in prompt_text:
                            print("Opened a new tab")
                        elif "Close" in prompt_text and "tab" in prompt_text:
                            print("Closed the tab")


                        # Remove the temporary audio file
                        os.remove(temp_audio_path)
                        
                    except sr.UnknownValueError:
                        print("Could not understand audio.")
                    except sr.RequestError as e:
                        print(f"Error with the API request; {e}")

        except KeyboardInterrupt:
            print("Stopping the continuous listening.")


    continuous_listen()

def fasterWhisper():
    from faster_whisper import WhisperModel
    import speech_recognition as sr
    import tempfile
    import os

    model = WhisperModel('tiny.en', compute_type="int8")

    def continuous_listen():
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            print("Adjusting for ambient noise. Please wait...")
            recognizer.adjust_for_ambient_noise(source, duration=5)
            print("Listening...")

        try:
            while True:
                with microphone as source:
                    try:
                        audio = recognizer.listen(source, timeout=None)
                        # Save the audio to a temporary file
                        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
                            temp_audio_path = temp_audio.name
                            temp_audio.write(audio.get_wav_data())

                        # Transcribe using Whisper
                        segments, _ = model.transcribe(temp_audio)
                        text = ''.join(segment.text for segment in segments)
                        print(f"You said: {text}")

                        # Remove the temporary audio file
                        os.remove(temp_audio_path)
                        
                    except sr.UnknownValueError:
                        print("Could not understand audio.")
                    except sr.RequestError as e:
                        print(f"Error with the API request; {e}")

        except KeyboardInterrupt:
            print("Stopping the continuous listening.")


    continuous_listen()

whisper()
