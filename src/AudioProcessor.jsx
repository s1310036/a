import React, { useState } from "react";

function AudioProcessor() {
  const [instruction, setInstruction] = useState("");
  const [file, setFile] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [classification, setClassification] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!instruction || !file) {
      alert("指示文と音声ファイルを両方入力してください。");
      return;
    }

    // === 分類エンドポイントを先に呼ぶ ===
    const formDataForClassify = new FormData();
    formDataForClassify.append("instruction", instruction);

    const classifyResponse = await fetch("http://localhost:8000/classify", {
      method: "POST",
      body: formDataForClassify,
    });

    const classifyData = await classifyResponse.json();
    setClassification(classifyData["分類結果"]);

    // === 音声加工エンドポイントを呼ぶ ===
    const formData = new FormData();
    formData.append("instruction", instruction);
    formData.append("file", file);

    const processResponse = await fetch("http://localhost:8000/process-audio", {
      method: "POST",
      body: formData,
    });

    if (processResponse.ok) {
      const blob = await processResponse.blob();
      const url = window.URL.createObjectURL(blob);
      setDownloadUrl(url);
    } else {
      alert("加工に失敗しました。");
    }
  };

  return (
    <div>
      <h2>音声加工・分類アプリ</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="指示を入力（例: 重低音を強く）"
          value={instruction}
          onChange={(e) => setInstruction(e.target.value)}
        />
        <input
          type="file"
          accept="audio/*"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit">分類して加工</button>
      </form>

      {classification && <p>分類結果: {classification}</p>}

      {downloadUrl && (
        <p>
          <a href={downloadUrl} download="processed.wav">
            加工済みファイルをダウンロード
          </a>
        </p>
      )}
    </div>
  );
}

export default AudioProcessor;
