from fastapi.testclient import TestClient
from cloudPlatform.api import app

client = TestClient(app)


def test_query_text():
    response = client.post("/query", data={"query": "Hello, how are you?"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_query_empty_text():
    response = client.post("/query", data={"query": ""})
    assert response.status_code == 400

def test_query_no_data():
    response = client.post("/query", data={})
    assert response.status_code == 400


def test_query_invalid_data():
    response = client.post("/query", json={"query": "random query goes here"})
    assert response.status_code == 400


def test_query_audio():
    audio_file_path = "../test-audio-query.mp3"
    with open(audio_file_path, "rb") as audio_file:
        response = client.post(
            "/query",
            files={"audioFile": ("file.mp3", audio_file, "audio/mpeg")}
        )
    assert response.status_code == 200
    assert "response" in response.json()


def test_text_to_speech():
    response = client.post("/text-to-speech", data={"textInput": "Hello, how are you?"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"


def test_text_to_speech_empty_text():
    response = client.post("/text-to-speech", data={"textInput": ""})
    assert response.status_code == 400
    
def test_text_to_speech_no_data():
    response = client.post("/text-to-speech", data={})
    assert response.status_code == 422


def test_text_to_speech_invalid_data():
    response = client.post("/text-to-speech", json={"textInput": "random text goes here"})
    assert response.status_code == 422
