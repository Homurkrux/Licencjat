from Tweet import Tweet
from Token import Token
from Flatten import flatten
import spacy as sp


def SerializeDfTweetsToObjectsAndAssigneNawlValues(df, NAWL_BE, nlp):
    Tweets=[]
    for row in df:
        tweet= Tweet(row[0], row[1], row[2], row[3])
    
        tekst = nlp(tweet.tekstTweeta)
        tokeny=[]
        for token in tekst:
            tokeny.append(token.lemma_)
        tokeny= flatten(tokeny)
        NAWL_BE_generator = flatten(NAWL_BE)
        temp= set(tokeny).intersection(NAWL_BE_generator)
        for elem in enumerate(temp):
            NAWL_BE_element = next((x for x in NAWL_BE if x[0] == elem[1]), None)
            tweet.tokeny = []
            if NAWL_BE_element != None:
                tweet.tokeny.append(Token(NAWL_BE_element[0],
                              NAWL_BE_element[1], 
                              NAWL_BE_element[2],
                              NAWL_BE_element[3],
                              NAWL_BE_element[4],
                              NAWL_BE_element[5]))
        Tweets.append(tweet)
    return Tweets



