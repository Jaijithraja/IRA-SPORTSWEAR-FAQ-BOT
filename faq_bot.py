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

    def answer(self, user_query: str, threshold: float = 0.15) -> str:
        """
        Return the answer of the most similar FAQ question using TF-IDF.
        If similarity is too low, reply that the bot is not sure.
        """
        user_query = user_query.strip().lower()
        if not user_query:
            return "Please type a question related to jerseys, orders, sizes, delivery or customization."

        # Handle common size-related questions
        size_keywords = ['size', 'sizing', 'measurement', 'measurements', 'fit']
        jersey_keywords = ['jersey', 'jerseys', 'shirt', 'shirts', 'uniform', 'uniforms']

        is_size_question = any(word in user_query for word in size_keywords)
        is_jersey_question = any(word in user_query for word in jersey_keywords)

        if is_size_question and is_jersey_question:
            return (
                "Our jerseys are available in a wide range of sizes from XS to 5XL. "
                "For the most accurate fit, please refer to our size chart available on the product page. "
                "If you're between sizes, we recommend going up a size for a more comfortable fit. "
                "Would you like information about a specific size or measurement?"
            )

        # Vectorize query
        query_vec = self.vectorizer.transform([user_query])

        # Compute cosine similarity with all FAQ questions
        scores = cosine_similarity(query_vec, self.question_vectors)[0]
        best_index = int(np.argmax(scores))
        best_score = float(scores[best_index])

        if best_score < threshold:
            if is_size_question and is_jersey_question:
                return (
                    "Our jerseys are available in sizes XS to 5XL. For specific measurements, please check the size chart on the product page. "
                    "Would you like information about a particular size range or style?"
                )
            return (
                "I'm not entirely sure about that. Could you rephrase your question? "
                "I can help with information about sizes, customization, orders, delivery, and more."
            )

        matched_answer = self.answers[best_index]
        return matched_answer
