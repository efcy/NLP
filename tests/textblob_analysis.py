import spacy
from textblob import TextBlob

nlp = spacy.load("en_core_web_sm")


def run_textblob(text):
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


run_textblob("Hangzhou Yushu Technology Co. is a good company.")
run_textblob("Robots are revolutionizing industries and improving lives.")
