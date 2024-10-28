from dotenv import load_dotenv

load_dotenv()

from gcp import google_cloud_text_to_speech, speech_to_text
from chatgpt import query_gpt


def main():
    prompt = "What is the capital of the United States?"
    response = query_gpt(prompt)
    
    google_cloud_text_to_speech(response, "output.mp3")
    text = speech_to_text("output.mp3")
    
    print(text)


if __name__ == "__main__":
    main()
