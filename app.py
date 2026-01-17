from fastapi import FastAPI, UploadFile, File
import shutil
import os
import librosa
import numpy as np
from transformers import pipeline
import cv2
import moviepy.editor as mp
import whisper

app = FastAPI(title="PulsePoint AI", description="AI-powered video processing platform")

# Ensure temp directory exists
os.makedirs("temp", exist_ok=True)

# Load models
whisper_model = whisper.load_model("base")
sentiment_analyzer = pipeline("sentiment-analysis")
hook_generator = pipeline("text2text-generation", model="t5-small")

@app.post("/process_video")
async def process_video(file: UploadFile = File(...)):
    # Save uploaded file
    file_path = f"temp/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 1. Extract audio
    video = mp.VideoFileClip(file_path)
    audio_path = f"temp/{os.path.splitext(file.filename)[0]}_audio.wav"
    video.audio.write_audiofile(audio_path)
    
    # 2. Analyze audio for emotional peaks
    y, sr = librosa.load(audio_path)
    rms = librosa.feature.rms(y=y)[0]
    peaks = librosa.util.peak_pick(rms, pre_max=10, post_max=10, pre_avg=10, post_avg=10, delta=0.1, wait=10)
    peaks_times = librosa.frames_to_time(peaks, sr=sr)
    
    # 3. Transcribe audio
    transcription = whisper_model.transcribe(audio_path)["text"]
    
    # 4. Sentiment analysis
    sentiment = sentiment_analyzer(transcription)[0]
    
    # 5. Generate hook
    hook = hook_generator(f"Create a catchy, engaging hook headline for this content: {transcription[:200]}", max_length=50)[0]['generated_text']
    
    # 5. Face detection and cropping (simplified)
    cap = cv2.VideoCapture(file_path)
    ret, frame = cap.read()
    cropped_path = None
    if ret:
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        if faces:
            x, y, w, h = faces[0]
            # Crop around face, but for vertical, adjust
            height, width = frame.shape[:2]
            # Simple crop to vertical aspect
            new_width = int(height * 9 / 16)
            center_x = x + w // 2
            left = max(0, center_x - new_width // 2)
            right = min(width, center_x + new_width // 2)
            cropped = frame[:, left:right]
            cropped_path = f"temp/{os.path.splitext(file.filename)[0]}_cropped.jpg"
            cv2.imwrite(cropped_path, cropped)
    
    # Clean up
    os.remove(file_path)
    os.remove(audio_path)
    
    return {
        "message": "Video processed",
        "peaks": peaks.tolist(),
        "peaks_times": peaks_times.tolist(),
        "transcription": transcription,
        "sentiment": sentiment,
        "hook": hook,
        "cropped_image": cropped_path
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)