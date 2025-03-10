import whisper
import os
import tempfile
import subprocess

def load_model(model_name="base"):
    return whisper.load_model(model_name)

def transcribe_video(model, video_file):
    temp_video_path = None
    temp_audio_path = None

    try:
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video:
            video_file.save(temp_video.name)
            temp_video_path = temp_video.name

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio_path = temp_audio.name

        try:
            subprocess.run([
                "ffmpeg",
                "-y",
                "-i", temp_video_path,
                "-vn",
                "-acodec", "pcm_s16le",
                "-ac", "1",
                "-ar", "16000",
                temp_audio_path
            ], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"FFmpeg error: {e.stderr.decode()}")
            raise

        result = model.transcribe(temp_audio_path)
        return result["text"]

    except Exception as e:
        print(f"Error during transcription: {e}")
        raise

    finally:

        if temp_video_path and os.path.exists(temp_video_path):
            os.remove(temp_video_path)
            print(f"Temporary video file deleted: {temp_video_path}")
        if temp_audio_path and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            print(f"Temporary audio file deleted: {temp_audio_path}")