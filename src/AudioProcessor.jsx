import React, { useState } from "react";

function AudioProcessor() {
  const [file, setFile] = useState(null);
  const [instruction, setInstruction] = useState("");
  const [downloadUrl, setDownloadUrl] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !instruction) return;

    const formData = new FormData();
    formData.append("instruction", instruction);
    formData.append("file", file);

    const response = await fetch("http://localhost:8000/process-audio", {
      method: "POST",
      body: formData,
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    setDownloadUrl(url);
  };

  return (
    <div>
      <h2>🎧 音声加工アプリ</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" accept=".wav" onChange={(e) => setFile(e.target.files[0])} />
        <input type="text" placeholder="指示（例: 重低音を強く）" value={instruction} onChange={(e) => setInstruction(e.target.value)} />
        <button type="submit">送信</button>
      </form>
      {downloadUrl && (
        <a href={downloadUrl} download="processed.wav">
          🔽 加工済み音声をダウンロード
        </a>
      )}
    </div>
  );
}

export default AudioProcessor;
