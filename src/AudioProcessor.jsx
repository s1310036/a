import React, { useState } from "react";

function Classifier() {
  const [instruction, setInstruction] = useState("");
  const [result, setResult] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("instruction", instruction);

    const response = await fetch("http://localhost:8000/classify", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setResult(data["分類結果"]);
  };

  return (
    <div>
      <h2>指示文分類アプリ</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="指示を入力（例: 高音を少し下げて）"
          value={instruction}
          onChange={(e) => setInstruction(e.target.value)}
        />
        <button type="submit">分類</button>
      </form>
      {result && <p>分類結果: {result}</p>}
    </div>
  );
}

export default Classifier;
