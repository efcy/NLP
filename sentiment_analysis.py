from transformers import pipeline
import numpy as np
import spacy
import json

nlp = spacy.load("en_core_web_sm")
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

war_terms = ["war", "military", "weapon", "weapons", "drone", "combat", "battle",
             "conflict", "defense", "attack", "security", "armament", "soldier", "army",
             "navy", "air force", "cyberwarfare", "aggression", "invasion"]


def analyze_war_mentions(doc):
    mentions = []
    for token in doc:
        if token.lower_ in war_terms:
            # Get the sentence containing the war term
            sentence = token.sent.text
            mentions.append({
                "term": token.text,
                "sentence": sentence,
                "context": [] # To store dependency context
            })

            # Explore dependency relationships for context
            for child in token.children:
                mentions[-1]["context"].append(f"{child.text} ({child.dep_})")
            if token.head != token: # If it's not the root of the sentence
                mentions[-1]["context"].append(f"{token.head.text} (head: {token.dep_})")
    return mentions


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
    sentiment_label = result[0]['label']
    sentiment_score = result[0]['score']

    polarity = 0
    if sentiment_label == 'POSITIVE':
        polarity = sentiment_score
    elif sentiment_label == 'NEGATIVE':
        polarity = -sentiment_score # Represent negative sentiment with a negative score

    return polarity, sentiment_label # Returning label instead of subjectivity as it's not applicable here
   

if __name__ == "__main__":
    with open('output.json') as f:
        data = json.load(f)

    west_sentiment = []
    west_war_count = 0
    china_war_count = 0
    china_sentiment = []
    for item in data:
        
        if item['origin'] == 'west':
            print(f"{item['title']}")
            text = item['text']
    
            doc = nlp(text)
            war_mentions = analyze_war_mentions(doc)
            west_war_count += len(war_mentions)
            sentences = [sent.text for sent in doc.sents]

            # Filter out very short or empty sentences that might cause issues
            sentences = [s.strip() for s in sentences if s.strip()]

            chunk_sentiments = []
            chunk_labels = []
            for sentence in sentences:
                polarity_score, sentiment_label = get_sentiment_transformers(sentence)

                chunk_sentiments.append(polarity_score)
                chunk_labels.append(sentiment_label)

            avg_polarity = np.mean(chunk_sentiments)
            print(avg_polarity)
            west_sentiment.append(avg_polarity)

            if avg_polarity > 0.1: # Thresholds can be adjusted
                overall_label = "POSITIVE"
            elif avg_polarity < -0.1:
                overall_label = "NEGATIVE"
            else:
                overall_label = "NEUTRAL" # Or 'MIXED' if you prefer
            
            print(f"\t{overall_label}")
        if item['origin'] == 'china':
            print(f"{item['title_translation']}")
            text = item['translation']

            doc = nlp(text)
            war_mentions = analyze_war_mentions(doc)
            china_war_count += len(war_mentions)
            sentences = [sent.text for sent in doc.sents]

            # Filter out very short or empty sentences that might cause issues
            sentences = [s.strip() for s in sentences if s.strip()]

            chunk_sentiments = []
            chunk_labels = []
            for sentence in sentences:
                polarity_score, sentiment_label = get_sentiment_transformers(sentence)
                #print(f"Sentiment Label='{sentiment_label}', Polarity Score={polarity_score:.4f}")
                chunk_sentiments.append(polarity_score)
                chunk_labels.append(sentiment_label)

            avg_polarity = np.mean(chunk_sentiments)
            china_sentiment.append(avg_polarity)
            if avg_polarity > 0.1: # Thresholds can be adjusted
                overall_label = "POSITIVE"
            elif avg_polarity < -0.1:
                overall_label = "NEGATIVE"
            else:
                overall_label = "NEUTRAL" # Or 'MIXED' if you prefer
        
            print(f"\t{overall_label}")
    
    print("west_sentiment", west_sentiment)
    print()
    print(f"West: {np.mean(west_sentiment)} - War: {west_war_count}")
    print(f"China: {np.mean(china_sentiment)}- War: {china_war_count}")