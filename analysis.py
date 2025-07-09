import spacy
from textblob import TextBlob

nlp = spacy.load("en_core_web_sm")

def get_sentiment(text):
    doc = nlp(text)
    blob = TextBlob(text)
    print(blob)
    # TextBlob returns polarity (-1 to 1, -1 is very negative, 1 is very positive)
    # and subjectivity (0 to 1, 0 is very objective, 1 is very subjective)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

# Example usage:
texts = {
    "Source A": "Robots are revolutionizing industries and improving lives.",
    "Source B": "Automation will lead to mass unemployment and societal unrest.",
    "Source C": "While robots offer benefits, concerns about job displacement are valid."
}

for source, text in texts.items():
    polarity, subjectivity = get_sentiment(text)
    print(f"{source}: Polarity={polarity:.2f}, Subjectivity={subjectivity:.2f}")