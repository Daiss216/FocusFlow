# Simple extractive summarizer - no LLM needed
import re
from collections import Counter


def _sentences(text):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in parts if len(s.split()) > 3]


def summarize(text, num_sentences=3):
    # Score sentences by word frequency, return the top ones in order.
    sentences = _sentences(text)
    if len(sentences) <= num_sentences:
        return text
    freq = Counter(w.lower() for w in re.findall(r"\b\w+\b", text))
    scores = {}
    for s in sentences:
        words = re.findall(r"\b\w+\b", s)
        scores[s] = sum(freq[w.lower()] for w in words) / len(words)
    top = sorted(scores, key=scores.get, reverse=True)[:num_sentences]
    return " ".join(s for s in sentences if s in top)


def keywords(text, top_n=5):
    # Most frequent meaningful words (quick 'key topics' list).
    freq = Counter(w.lower() for w in re.findall(r"\b\w+\b", text))
    stop = {"the", "and", "that", "this", "with", "for", "you", "are", "was"}
    return [w for w, _ in freq.most_common(top_n * 3) if w not in stop][:top_n]