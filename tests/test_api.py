from fastapi.testclient import TestClient
from cloudPlatform.api import app

client = TestClient(app)

def test_query_text():
    response = client.post("/query", data={"query": "Hello, how are you?"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_query_audio():
    audio_file_path = "../output.mp3"
    with open(audio_file_path, "rb") as audio_file:
        response = client.post(
            "/query",
            files={"audioFile": ("file.mp3", audio_file, "audio/mpeg")}
        )
    assert response.status_code == 200
    assert "transcript" in response.json()



def test_query_no_data():
    response = client.post("/query", data={})
    assert response.status_code == 400
