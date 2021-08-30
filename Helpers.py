from Tweet import Tweet
from Token import Token
from Flatten import flatten
import spacy as sp
import ast
import datetime
import dateutil.parser
#przetwarza df Tweetów w obiekty z wypełnionymi tokenami z wartościami NAWL_BE
def SerializeDfTweetsToObjectsAndAssigneNawlValues(df, NAWL_BE, nlp):
    Tweets=[]
    NAWL_BE_list= NAWL_BE.values.tolist()
    for row in df:
        tweet= Tweet(row[0], row[1], row[2], row[3], 0)
    
        tekst = nlp(tweet.tekstTweeta)
        tokeny=[]
        for token in tekst:
            tokeny.append(token.lemma_)
        tokeny_flat= flatten(tokeny)
        NAWL_BE_generator = flatten(NAWL_BE['slowo'])
        temp= set(tokeny).intersection(NAWL_BE_generator)
        if len(temp)==0:
            tweet.slowaEmotywne= 0
        tweet.slowaEmotywne=len(temp)
        tweet.tokeny = []
        
        for elem in enumerate(temp):
            NAWL_BE_element = next((x for x in NAWL_BE_list if x[0] == elem[1]), None)
            if NAWL_BE_element != None:
                tweet.tokeny.append(Token(NAWL_BE_element[0],
                              NAWL_BE_element[1], 
                              NAWL_BE_element[2],
                              NAWL_BE_element[3],
                              NAWL_BE_element[4],
                              NAWL_BE_element[5]))
        Tweets.append(tweet)
    return Tweets

#zserializuj df Tweetów na [Tweet]
def SerializeDfTweetsToTweets(df):
    Tweets=[]
    for row in df:
        tweet= Tweet(row[0], row[1], row[2], row[3], row[4])
        tokeny=[]
        dfTokens = ast.literal_eval(row[5])
        if dfTokens != []:
            for token in dfTokens:
                #token = ast.literal_eval(token)
                tweet.tokeny.append(Token(token['token'], 
                              token['happ'],
                              token['ang'],
                              token['sad'],
                              token['fear'],
                              token['disg']))
            
        Tweets.append(tweet)
    return Tweets

#podziel listę na podlisty na podstawie delty czasu
def group_by_time(objects, time):
    minutes = datetime.timedelta(minutes=time)
    objects = iter(objects)
    obj = next(objects)
    last = dateutil.parser.parse(str(obj.dataCzas))
    group = [obj]
    for obj in objects:
        time = dateutil.parser.parse(str(obj.dataCzas))
        if time > last + minutes:
            yield group
            group = []
            last = time
        group.append(obj)
        
    else:
        yield group