import spacy
from textblob import TextBlob

nlp = spacy.load("en_core_web_sm")

war_terms = ["war", "military", "weapon", "weapons", "drone", "combat", "battle",
             "conflict", "defense", "attack", "security", "armament", "soldier", "army",
             "navy", "air force", "cyberwarfare", "aggression", "invasion"]

def analyze_war_mentions(text, war_terms):
    doc = nlp(text)
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

# Example usage:
texts_war = {
    "Newspaper A": "The new robotics firm is developing advanced drones for military applications.",
    "Newspaper B": "Robots are increasingly used in security and surveillance operations.",
    "Newspaper C": "Concerns were raised about the ethical implications of autonomous weapons.",
    "Source D": "While robots offer benefits, concerns about job displacement are valid.",
    "Source A": "Robots are revolutionizing industries and improving lives.",
}

for source, text in texts_war.items():
    print(f"\n--- {source} ---")
    war_data = analyze_war_mentions(text, war_terms)
    if war_data:
        for mention in war_data:
            print(f"  Term: '{mention['term']}'")
            print(f"  Sentence: '{mention['sentence']}'")
            print(f"  Context: {'; '.join(mention['context'])}")
    else:
        print("  No direct war-related mentions found.")

