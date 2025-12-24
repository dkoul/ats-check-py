"""Keyword extraction and matching utilities."""

import re
from typing import List
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer


# Common stopwords to exclude
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "been", "be",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "can", "this", "that", "these",
    "those", "i", "you", "he", "she", "it", "we", "they", "what", "which",
    "who", "when", "where", "why", "how", "all", "each", "every", "both",
    "few", "more", "most", "other", "some", "such", "only", "own", "same",
    "so", "than", "too", "very", "just", "about", "up", "out", "if", "into",
    "through", "during", "before", "after", "above", "below", "between",
    "under", "again", "further", "then", "once", "here", "there", "also",
    "any", "our", "their", "your", "my", "me", "him", "her", "us", "them",
}


def extract_keywords(text: str, top_n: int = 50) -> List[str]:
    """
    Extract key terms from text using TF-IDF.

    Args:
        text: Input text
        top_n: Number of top keywords to return

    Returns:
        List of keywords sorted by importance
    """
    # Clean and tokenize text
    text_clean = clean_text(text)

    # Extract word frequencies
    words = text_clean.lower().split()
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]

    # Get word frequencies
    word_freq = Counter(words)

    # Extract multi-word phrases (bigrams and trigrams)
    phrases = extract_phrases(text_clean)

    # Combine single words and phrases
    all_terms = list(word_freq.keys()) + phrases

    # Use TF-IDF to score terms
    try:
        if len(all_terms) > 0:
            vectorizer = TfidfVectorizer(
                max_features=top_n,
                ngram_range=(1, 3),
                stop_words=list(STOPWORDS)
            )
            vectorizer.fit([text_clean])
            keywords = vectorizer.get_feature_names_out()
            return list(keywords)[:top_n]
    except Exception:
        pass

    # Fallback to simple frequency-based extraction
    return [word for word, _ in word_freq.most_common(top_n)]


def extract_phrases(text: str) -> List[str]:
    """
    Extract meaningful multi-word phrases.

    Args:
        text: Input text

    Returns:
        List of phrases
    """
    # Common technical/professional phrases pattern
    phrases = []

    # Extract capitalized phrases (likely to be important terms)
    capitalized_phrases = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', text)
    phrases.extend([p.lower() for p in capitalized_phrases if len(p.split()) <= 3])

    # Extract acronyms and technical terms
    acronyms = re.findall(r'\b[A-Z]{2,}\b', text)
    phrases.extend([a.lower() for a in acronyms if 2 <= len(a) <= 6])

    return list(set(phrases))


def clean_text(text: str) -> str:
    """
    Clean text for keyword extraction.

    Args:
        text: Input text

    Returns:
        Cleaned text
    """
    # Remove URLs
    text = re.sub(r'http\S+|www.\S+', '', text)

    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # Remove special characters but keep spaces and alphanumeric
    text = re.sub(r'[^a-zA-Z0-9\s\-]', ' ', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def calculate_keyword_match(resume_text: str, jd_text: str) -> int:
    """
    Calculate keyword match percentage between resume and job description.

    Args:
        resume_text: Resume text
        jd_text: Job description text

    Returns:
        Match percentage (0-100)
    """
    # Extract keywords from both texts
    resume_keywords = set(extract_keywords(resume_text, top_n=50))
    jd_keywords = set(extract_keywords(jd_text, top_n=50))

    if not jd_keywords:
        return 100  # No JD keywords to match

    # Calculate overlap
    common_keywords = resume_keywords.intersection(jd_keywords)
    match_percentage = int((len(common_keywords) / len(jd_keywords)) * 100)

    return min(100, match_percentage)
