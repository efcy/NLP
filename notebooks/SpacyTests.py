import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell
def _():
    # run this first python -m spacy download en_core_web_sm

    import spacy

    nlp = spacy.load("en_core_web_sm")
    doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
    for token in doc:
        print(token.text, token.pos_, token.dep_)
    return (spacy,)


@app.cell
def _(spacy):
    def _():
        nlp = spacy.load("en_core_web_sm")
    
        # Process whole documents
        text = ("When Sebastian Thrun started working on self-driving cars at "
                "Google in 2007, few people outside of the company took him "
                "seriously. “I can tell you very senior CEOs of major American "
                "car companies would shake my hand and turn away because I wasn’t "
                "worth talking to,” said Thrun, in an interview with Recode earlier "
                "this week.")
        doc = nlp(text)
    
        # Analyze syntax
        print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
        print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
    
        # Find named entities, phrases and concepts
        for entity in doc.ents:
            print(entity.text, entity.label_)

    _()

    return


if __name__ == "__main__":
    app.run()
