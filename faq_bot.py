import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
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

        # Build TF-IDF vectorizer on questions
        # Using unigrams + bigrams for better matching
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english"
        )
        self.question_vectors = self.vectorizer.fit_transform(self.questions)

    def answer(self, user_query: str, threshold: float = 0.2) -> str:
        """
        Return the answer of the most similar FAQ question using TF-IDF.
        If similarity is too low, reply that the bot is not sure.
        """
        user_query = user_query.strip()
        if not user_query:
            return "Please type a question related to jerseys, orders, sizes, delivery or customization."

        # Vectorize query
        query_vec = self.vectorizer.transform([user_query])

        # Compute cosine similarity with all FAQ questions
        scores = cosine_similarity(query_vec, self.question_vectors)[0]
        best_index = int(np.argmax(scores))
        best_score = float(scores[best_index])

        if best_score < threshold:
            return (
                "I am not fully sure about that.\n"
                "Please try asking about sizes, customization, bulk orders, delivery, payment or returns."
            )

        matched_answer = self.answers[best_index]
        return matched_answer
