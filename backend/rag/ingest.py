"""
RAG Ingestion Pipeline - Compatible with Python 3.12
Uses TF-IDF based search - no ChromaDB or HuggingFace needed.
"""

import json
import pickle
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

DATA_DIR = Path(__file__).parent.parent.parent / "data"
INDEX_DIR = Path(__file__).parent.parent.parent / "search_index"


def load_json(filename: str) -> list:
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


def scholarships_to_docs(data: list) -> list:
    docs = []
    for item in data:
        content = f"""SCHOLARSHIP: {item['name']}
Provider: {item['provider']}
Eligibility: {item['eligibility']}
Amount: {item['amount']}
Applicable Grades: {', '.join(item['grades'])}
Stream: {', '.join(item['stream'])}
Location: {item['location']}
Description: {item['description']}
Apply at: {item['apply_url']}"""
        docs.append({"content": content, "type": "scholarship", "name": item["name"]})
    return docs


def vocational_to_docs(data: list) -> list:
    docs = []
    for item in data:
        content = f"""VOCATIONAL PATHWAY: {item['name']}
Provider: {item['provider']}
Duration: {item['duration']}
Eligibility: {item['eligibility']}
After Grade: {', '.join(item['after_grade'])}
Job Roles: {', '.join(item['job_roles'])}
Average Salary: {item['avg_salary']}
Further Education Options: {', '.join(item['further_education'])}
Description: {item['description']}"""
        docs.append({"content": content, "type": "vocational", "name": item["name"]})
    return docs


def schemes_to_docs(data: list) -> list:
    docs = []
    for item in data:
        content = f"""GOVERNMENT SCHEME: {item['name']}
Full Name: {item.get('full_name', item['name'])}
Provider: {item['provider']}
Eligibility: {item['eligibility']}
Benefit: {item['benefit']}
Applicable Grades: {', '.join(item['grades'])}
Description: {item['description']}
Apply at: {item['apply_url']}"""
        docs.append({"content": content, "type": "scheme", "name": item["name"]})
    return docs


def streams_to_docs(data: list) -> list:
    docs = []
    for item in data:
        content = f"""ACADEMIC STREAM: {item['name']}
After Grade: {item['after_grade']}
Subjects: {', '.join(item['subjects'])}
Career Paths: {', '.join(item['career_paths'])}
Entrance Exams: {', '.join(item['entrance_exams'])}
Job Roles: {', '.join(item['job_roles'])}
Best For: {item['best_for']}
Difficulty Level: {item['difficulty']}"""
        docs.append({"content": content, "type": "stream", "name": item["name"]})
    return docs


def ingest_all():
    print("📚 Loading data files...")
    scholarships = load_json("scholarships.json")
    vocational = load_json("vocational_pathways.json")
    schemes = load_json("govt_schemes.json")
    streams = load_json("academic_streams.json")

    print("📝 Converting to documents...")
    all_docs = (
        scholarships_to_docs(scholarships) +
        vocational_to_docs(vocational) +
        schemes_to_docs(schemes) +
        streams_to_docs(streams)
    )
    print(f"✅ Created {len(all_docs)} documents")

    print("🔍 Building TF-IDF search index...")
    texts = [doc["content"] for doc in all_docs]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(texts)

    print("💾 Saving search index...")
    INDEX_DIR.mkdir(exist_ok=True)
    with open(INDEX_DIR / "vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    with open(INDEX_DIR / "tfidf_matrix.pkl", "wb") as f:
        pickle.dump(tfidf_matrix, f)
    with open(INDEX_DIR / "documents.json", "w", encoding="utf-8") as f:
        json.dump(all_docs, f, ensure_ascii=False, indent=2)

    print(f"✅ Search index saved at {INDEX_DIR}")
    print(f"📊 Total documents indexed: {len(all_docs)}")
    return all_docs


def search_docs(query: str, top_k: int = 4) -> list:
    """Search for relevant documents using TF-IDF cosine similarity."""
    with open(INDEX_DIR / "vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    with open(INDEX_DIR / "tfidf_matrix.pkl", "rb") as f:
        tfidf_matrix = pickle.load(f)
    with open(INDEX_DIR / "documents.json", "r", encoding="utf-8") as f:
        documents = json.load(f)

    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = np.argsort(scores)[::-1][:top_k]
    results = [documents[idx] for idx in top_indices if scores[idx] > 0]
    return results


if __name__ == "__main__":
    ingest_all()
    print("✅ Ingestion complete!")
