# classifier.py
from transformers import BertJapaneseTokenizer, BertModel
from sklearn.base import BaseEstimator, TransformerMixin
import torch

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
