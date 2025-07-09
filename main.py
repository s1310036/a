from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from classifier import BertVectorizer

from pydub import AudioSegment
import tempfile
import joblib
import os

# ffmpeg のパス（必要に応じて環境に合わせて変更）
AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"

app = FastAPI()

# React など別オリジンからのリクエストを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドの URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === 分類エンドポイント ===
@app.post("/classify")
async def classify(instruction: str = Form(...)):
    # モデルファイルへのパスを絶対指定しておくと安心
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "bert_audio_classifier.pkl")
    model = joblib.load(MODEL_PATH)
    prediction = model.predict([instruction])[0]
    return JSONResponse(content={"分類結果": prediction})

# === 音声加工エンドポイント ===
@app.post("/process-audio")
async def process_audio(
    instruction: str = Form(...),
    file: UploadFile = File(...)
):
    # アップロードされたファイルを一時保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_in:
        temp_in.write(await file.read())
        in_path = temp_in.name

    # 読み込み＆加工
    audio = AudioSegment.from_file(in_path, format="wav")
    if "重低音" in instruction and "強く" in instruction:
        audio = audio.low_pass_filter(100)

    # 加工後を一時出力
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_out:
        audio.export(temp_out.name, format="wav", bitrate="192k")
        out_path = temp_out.name

    return FileResponse(
        out_path,
        media_type="audio/wav",
        filename="processed.wav"
    )
