import os
import tempfile
import whisper

# Load model globally to avoid reloading it on every call. Using "base" for speed.
_whisper_model = None

def transcribe_audio(uploaded_file):
    """
    Saves the uploaded file to a temporary location, transcribes it using Whisper,
    and returns the transcription text.
    """
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model("base")

    # Create a temporary file to save the uploaded audio
    suffix = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    try:
        # Transcribe the audio
        result = _whisper_model.transcribe(tmp_file_path)
        transcript = result["text"]
    except Exception as e:
        raise Exception(f"Error transcribing audio: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)

    return transcript

def generate_audio_notes(transcript, llm):
    """
    Generates structured notes from the audio transcript using Gemini.
    """
    prompt = f"""
    You are an expert educational assistant. Please generate structured study notes from the following lecture transcript.
    Include a summary, key takeaways, and a structured outline.

    Transcript:
    {transcript}
    """
    response = llm.invoke(prompt)
    return response.content
