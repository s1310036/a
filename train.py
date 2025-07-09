# train.py
from transformers import BertJapaneseTokenizer, BertModel
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import torch
import joblib
# main.py
from classifier import BertVectorizer
# （残りは同じ）

# BERTベクトル変換器
class BertVectorizer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese')
        self.model = BertModel.from_pretrained('cl-tohoku/bert-base-japanese')
        self.model.eval()

    def transform(self, X):
        vectors = []
        for text in X:
            tokens = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
            with torch.no_grad():
                output = self.model(**tokens)
            cls_vec = output.last_hidden_state[:, 0, :].squeeze().numpy()
            vectors.append(cls_vec)
        return vectors

    def fit(self, X, y=None):
        return self

# 学習データ
train_texts = [
    "重低音をもっと響かせて", "低音を強調して",
    "高音を少し下げて", "シャリシャリするから抑えて",
    "エコーかけて", "残響を追加して"
]
train_labels = ["low_boost", "low_boost", "high_cut", "high_cut", "reverb", "reverb"]

# パイプライン作成
pipe = Pipeline([
    ("vectorizer", BertVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])

# 学習と保存
pipe.fit(train_texts, train_labels)
joblib.dump(pipe, "bert_audio_classifier.pkl")
print("✅ モデルの学習と保存が完了しました")