import sqlite3
import spacy
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import sys
import os

# --- CONFIGURATION ---
DB_FILE = "reddit_data.db"
OUTPUT_IMAGE_FILE = "top_100_entities.png"
# You can use a more accurate but slower model if needed, e.g., 'en_core_web_trf'
SPACY_MODEL = "en_core_web_sm" 

def load_text_from_db():
    """Connects to the SQLite DB and yields all text content for analysis."""
    if not os.path.exists(DB_FILE):
        print(f"Error: Database file '{DB_FILE}' not found.", file=sys.stderr)
        print("Please run the previous script to generate the database.", file=sys.stderr)
        sys.exit(1)
        
    print(f"Connecting to '{DB_FILE}' to load text data...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Fetch text from posts (title and selftext)
    cursor.execute("SELECT title, selftext FROM posts")
    for row in cursor.fetchall():
        yield row[0] # Yield title
        if row[1] and row[1].strip(): # Ensure selftext is not None or empty
             yield row[1] # Yield selftext

    # Fetch text from comments
    cursor.execute("SELECT body FROM comments")
    for row in cursor.fetchall():
        if row[0] and row[0].strip(): # Ensure comment body is not None or empty
            yield row[0] # Yield comment body
            
    conn.close()
    print("Finished loading data from database.")

def analyze_and_count_entities(texts, nlp):
    """Processes texts with spaCy, finds PERSON and ORG entities, and counts them."""
    entity_counts = Counter()
    
    # Process texts in batches for better performance using nlp.pipe
    batch_size = 50 
    text_count = 0
    print("Analyzing text with spaCy to find entities... (This may take a while)")
    
    for doc in nlp.pipe(texts, batch_size=batch_size):
        # Filter for PERSON and ORG entities
        valid_entities = [
            ent.text.strip().title() # Clean, strip whitespace, and convert to Title Case
            for ent in doc.ents 
            if ent.label_ in ["PERSON", "ORG"] and len(ent.text.strip()) > 2 # Filter by type and min length
        ]
        entity_counts.update(valid_entities)
        text_count += 1
        if text_count % 1000 == 0:
            print(f"  ...processed {text_count} text blocks...")
            
    print(f"Analysis complete. Found {len(entity_counts)} unique entities.")
    return entity_counts

def plot_top_entities(counter, top_n=100):
    """Creates and saves a bar chart of the top N most common entities."""
    if not counter:
        print("No entities found to plot.")
        return
        
    print(f"Generating plot for the top {top_n} entities...")
    
    # Get the top N most common entities
    top_entities = counter.most_common(top_n)
    
    # Create a pandas DataFrame for easy plotting
    df = pd.DataFrame(top_entities, columns=['Entity', 'Frequency'])
    
    # Create the plot
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 20))
    
    # Plot horizontal bar chart (better for long labels)
    ax.barh(df['Entity'], df['Frequency'], color='skyblue')
    
    # Invert y-axis to have the most frequent on top
    ax.invert_yaxis()
    
    # Add labels and title
    ax.set_xlabel('Frequency Count', fontsize=12)
    ax.set_ylabel('Entity (Person or Organization)', fontsize=12)
    ax.set_title(f'Top {top_n} Most Frequent Entities Found in Reddit Data', fontsize=16, pad=20)
    
    # Add frequency numbers on the bars
    for i, (value, name) in enumerate(zip(df['Frequency'], df['Entity'])):
        ax.text(value + 0.5, i, f" {value}", ha='left', va='center', fontsize=9)
        
    # Adjust layout and save the file
    plt.tight_layout(pad=3.0)
    plt.savefig(OUTPUT_IMAGE_FILE, dpi=300)
    
    print(f"Successfully saved chart to '{OUTPUT_IMAGE_FILE}'")

def main():
    """Main function to run the analysis and plotting pipeline."""
    # 1. Load spaCy model
    try:
        nlp = spacy.load(SPACY_MODEL)
        print(f"spaCy model '{SPACY_MODEL}' loaded successfully.")
    except OSError:
        print(f"Error: spaCy model '{SPACY_MODEL}' not found.", file=sys.stderr)
        print(f"Please run 'python -m spacy download {SPACY_MODEL}' to install it.", file=sys.stderr)
        sys.exit(1)
        
    # 2. Load text from the database
    all_texts = load_text_from_db()
    
    # 3. Analyze text to find and count entities
    entity_counter = analyze_and_count_entities(all_texts, nlp)
    
    # 4. Plot the results
    plot_top_entities(entity_counter, top_n=100)

if __name__ == "__main__":
    main()