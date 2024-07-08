from cartesia import Cartesia
import pyaudio
import os

client = Cartesia(api_key=os.environ.get("YOUR_API_KEY"))
voice_name = "Barbershop Man"
voice_id = "VOICE_ID"
voice = client.voices.get(id=voice_id)

transcript = "hello i am simplify AI"

# You can check out our models at [docs.cartesia.ai](https://docs.cartesia.ai/getting-started/available-models).
model_id = "sonic-english"

# You can find the supported `output_format`s in our [API Reference](https://docs.cartesia.ai/api-reference/endpoints/stream-speech-server-sent-events).
output_format = {
    "container": "raw",
    "encoding": "pcm_f32le",
    "sample_rate": 44100,
}

p = pyaudio.PyAudio()
rate = 44100

stream = None

# Generate and stream audio
for output in client.tts.sse(
    model_id=model_id,
    transcript=transcript,
    voice_embedding=voice["embedding"],
    stream=True,
    output_format=output_format,
):
    buffer = output["audio"]

    if not stream:
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=rate, output=True)

    # Write the audio data to the stream
    stream.write(buffer)

stream.stop_stream()
stream.close()
p.terminate()