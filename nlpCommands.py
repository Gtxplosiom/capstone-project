import spacy

nlp = spacy.load('en_core_web_lg')

w1 = "press"
w2 = "click"

w1 = nlp.vocab[w1]
w2 = nlp.vocab[w2]

similar = w1.similarity(w2)
print(similar)
