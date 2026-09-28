from database import get_faqs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class HRChatbot:
    def __init__(self, threshold=0.18):
        self.threshold = threshold
        self.reload()

    def reload(self):
        self.faqs = get_faqs()
        self.questions = [item["question"] for item in self.faqs]
        if self.questions:
            self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            self.matrix = self.vectorizer.fit_transform(self.questions)
        else:
            self.vectorizer = None
            self.matrix = None

    def answer(self, question):
        if not self.questions:
            return {"answer": "The HR knowledge base is currently empty. Please contact HR.", "confidence": 0}

        query_vector = self.vectorizer.transform([question])
        scores = cosine_similarity(query_vector, self.matrix)[0]
        index = scores.argmax()
        score = float(scores[index])

        if score < self.threshold:
            return {
                "answer": "I'm sorry, I couldn't find the answer in the HR knowledge base. Please contact the HR team for assistance.",
                "confidence": round(score, 3)
            }

        return {
            "answer": self.faqs[index]["answer"],
            "category": self.faqs[index]["category"],
            "confidence": round(score, 3)
        }
