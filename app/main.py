from flask import Flask, request, jsonify
from app.transcribe import load_model, transcribe_video
import os

app = Flask(__name__)
model = load_model("base")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if 'video' not in request.files:
        return jsonify({"error": "No video files provided"}), 400

    video_files = request.files.getlist('video')
    transcriptions = {}

    for video_file in video_files:
        if video_file.filename == '':
            return jsonify({"error": "One of the selected files is empty"}), 400

        try:
            transcription = transcribe_video(model, video_file)
            transcriptions[video_file.filename] = transcription
        except Exception as e:
            print(f"Error during transcription of {video_file.filename}: {e}")
            return jsonify({"error": f"Transcription failed for {video_file.filename}: {str(e)}"}), 500

    return jsonify({"transcriptions": transcriptions})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)