from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

categories = {
    "Story": "a narrative story with characters and events",
    "Research Paper": "an academic research study with methodology and results",
    "Technical Documentation": "instructions explaining software systems or APIs",
    "Study Notes": "educational summaries and key learning points",
    "Article": "general informational writing for readers"
}

# ✅ Precompute once
category_embeddings = {
    k: model.encode(v, convert_to_tensor=True)
    for k, v in categories.items()
}

def detect_document_type(text):
    text_sample = text[:1500]
    doc_embedding = model.encode(text_sample, convert_to_tensor=True)

    best_score = 0
    best_type = "Article"

    for category, cat_embedding in category_embeddings.items():
        score = util.cos_sim(doc_embedding, cat_embedding).item()

        if score > best_score:
            best_score = score
            best_type = category

    return best_type, round(best_score * 100, 2)