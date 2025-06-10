import spacy
from textblob import TextBlob

nlp = spacy.load("en_core_web_sm")


text = """
I absolutely love this new phone! The camera quality is amazing, though the battery life could be better. 
The customer service was terrible when I had an issue, but overall I'm quite satisfied with my purchase.
"""

doc = nlp(text)

# sentiment analysis
blob = TextBlob(text)

print("Text:", text)
print("\nSentiment Analysis Results:")
print("-" * 50)
print(f"Polarity: {blob.sentiment.polarity:.2f} (Range: -1 to 1)")
print(f"Subjectivity: {blob.sentiment.subjectivity:.2f} (Range: 0 to 1)")

if blob.sentiment.polarity > 0.5:
    sentiment = "Strongly Positive"
elif blob.sentiment.polarity > 0.1:
    sentiment = "Positive"
elif blob.sentiment.polarity < -0.5:
    sentiment = "Strongly Negative"
elif blob.sentiment.polarity < -0.1:
    sentiment = "Negative"
else:
    sentiment = "Neutral"

print(f"\nOverall Sentiment: {sentiment}")

print("\nSentence-level Analysis:")
print("-" * 50)
for sent in doc.sents:
    sent_blob = TextBlob(sent.text)
    print(f"\nSentence: {sent.text}")
    print(f"Polarity: {sent_blob.sentiment.polarity:.2f}")
    print(f"Subjectivity: {sent_blob.sentiment.subjectivity:.2f}")