import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class FAQBot:
    def __init__(self, faq_path: str):
        # Load FAQ Excel
        self.faq_df = pd.read_excel(faq_path)

        # Basic validation
        if "question" not in self.faq_df.columns or "answer" not in self.faq_df.columns:
            raise ValueError("Excel must have 'question' and 'answer' columns")

        # Drop rows with missing data
        self.faq_df = self.faq_df.dropna(subset=["question", "answer"])

        # Extract lists
        self.questions = self.faq_df["question"].astype(str).tolist()
        self.answers = self.faq_df["answer"].astype(str).tolist()

        # Embedding model
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Precompute embeddings
        self.question_embeddings = self.model.encode(
            self.questions,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

    def answer(self, user_query: str, threshold: float = 0.55) -> str:
        """
        Return only the matched answer.
        If similarity is too low, reply with a fallback message.
        """
        user_query = user_query.strip()
        if not user_query:
            return "Please type a question related to jerseys, orders, sizes, delivery or customization."

        # Embed user question
        query_emb = self.model.encode(
            [user_query],
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        # Similarity scores
        scores = cosine_similarity(query_emb, self.question_embeddings)[0]
        best_index = int(np.argmax(scores))
        best_score = float(scores[best_index])

        # Low confidence fallback
        if best_score < threshold:
            return "I am not sure about that. Try asking about sizes, customization, bulk orders, delivery, payment or returns."

        # Return only the answer
        matched_answer = self.answers[best_index]
        return matched_answer
