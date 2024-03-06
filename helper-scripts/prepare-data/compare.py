import kenlm  # Install this library if you haven't already

# Load your ARPA model
arpa_model_path = "path/to/your/arpa/model.arpa"
model = kenlm.LanguageModel(arpa_model_path)

# Example sentences from corpus B
corpus_b_sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Machine learning algorithms are powerful tools.",
    # ... more sentences ...
]

# Compute likelihood scores for each sentence
likelihood_scores = []
for sentence in corpus_b_sentences:
    # Tokenize and preprocess the sentence (similar to how you preprocessed corpus A)
    tokens = sentence.lower().split()  # Adjust tokenization as needed
    log_likelihood = model.score(" ".join(tokens))
    likelihood_scores.append(log_likelihood)

# Sort sentences by likelihood (higher is better)
sorted_indices = sorted(range(len(corpus_b_sentences)), key=lambda i: likelihood_scores[i], reverse=True)
top_k_sentences = [corpus_b_sentences[i] for i in sorted_indices[:10]]  # Select top-k sentences

print("Top sentences from corpus B based on ARPA model likelihood:")
for sentence in top_k_sentences:
    print(sentence)
