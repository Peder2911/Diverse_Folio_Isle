
def bodiesToSentences(bodies):
    sentences = []

    for body in bodies:
        sents = body.split('\n')
        sents = [sent.strip() for sent in sents if sent != '']
        sentences += sents

    return(sentences)
