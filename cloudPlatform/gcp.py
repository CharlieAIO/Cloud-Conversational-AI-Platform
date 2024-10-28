from google.cloud import texttospeech, speech

client = texttospeech.TextToSpeechClient()


def google_cloud_text_to_speech(text, output_file):
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            sample_rate_hertz=16000
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
    except Exception:
        raise Exception("Failed to synthesize speech")

    try:
        with open(output_file, "wb") as out:
            out.write(response.audio_content)

        print(f'Audio content written to file "{output_file}"')
        return True
    except Exception:
        raise Exception("Failed to save output file")


def speech_to_text(audio_file_path: str) -> speech.RecognizeResponse:
    client = speech.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    audio = speech.RecognitionAudio(content=content)

    response = client.recognize(config=config, audio=audio)

    return response.results[0].alternatives[0].transcript