import spacy
from transformers import pipeline


sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def get_sentiment_transformers(text):
    """
    Analyzes the sentiment of a given text using a pre-trained Hugging Face model.

    Returns:
        A tuple (polarity, label). Polarity is -1 for NEGATIVE, 0 for NEUTRAL (if applicable),
        and 1 for POSITIVE. Label is the raw sentiment label from the model.
        Note: Some models only output POSITIVE/NEGATIVE, so a truly 'neutral' might
        be classified as one or the other with low confidence.
    """
    result = sentiment_pipeline(text)
    # The result is typically a list of dictionaries, e.g., [{'label': 'POSITIVE', 'score': 0.999}]
    sentiment_label = result[0]['label']
    sentiment_score = result[0]['score']

    polarity = 0 # Default to neutral if we introduce it
    if sentiment_label == 'POSITIVE':
        polarity = sentiment_score
    elif sentiment_label == 'NEGATIVE':
        polarity = -sentiment_score # Represent negative sentiment with a negative score

    # Note: Subjectivity is not directly provided by these models.
    # If you need subjectivity, you might combine this with TextBlob's subjectivity
    # or look into other methods (e.g., lexical approaches).
    return polarity, sentiment_label # Returning label instead of subjectivity as it's not applicable here

# Example usage with your texts:
texts = {
    "Source A": "Robots are revolutionizing industries and improving lives.",
    "Source B": "Automation will lead to mass unemployment and societal unrest.",
    "Source C": "While robots offer benefits, concerns about job displacement are valid.",
    "Source D": "While robots offer benefits, concerns about job displacement are valid.",
    "Source E": "Robots are revolutionizing industries and improving lives.",
}

print("--- Sentiment Analysis with Hugging Face Transformers ---")
for source, text in texts.items():
    polarity_score, sentiment_label = get_sentiment_transformers(text)
    print(f"{source}: Sentiment Label='{sentiment_label}', Polarity Score={polarity_score:.4f}")
