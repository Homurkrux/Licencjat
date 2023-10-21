from Tweet import Tweet
from Token import Token
from NAWLWord import NAWLWord
from Flatten import flatten
import spacy as sp
import ast
import datetime
import dateutil.parser
#metoda przetwarzająca df Tweetów w obiekty 
#z wypełnionymi tokenami z wartościami NAWL i NAWL_BE
def SerializeDfTweetsToObjectsAndAssigneNawlValues(df, NAWL_BE, NAWL, nlp):
    Tweets=[]
    NAWL_BE_list= NAWL_BE.values.tolist()
    NAWL_list= NAWL.values.tolist()
    for row in df:
        #zainicjowanie obiektu tweeta z danymi na temat czasu opublikowania, tekstu tweeta, płci autora, 
        #identywikatora debaty do której się odnosi i ilosći słów emotywnych
        tweet= Tweet(row[0], row[1], row[2], row[3], 0) 
        #tokenizacja tekstu tweeta
        tekst = nlp(tweet.tekstTweeta)
        tokeny=[]
        for token in tekst:
            #lemantyzacja tokenów wydobytych z tekstu
            tokeny.append(token.lemma_)
        tokeny_flat= flatten(tokeny)
        NAWL_BE_generator = flatten(NAWL_BE['slowo'])
        #znalezienie intersekcji między listą tokenów a słowami w NAWL_BE
        intersekcja= set(tokeny).intersection(NAWL_BE_generator)
        if len(intersekcja)==0:
            tweet.slowaEmotywne= 0
        tweet.slowaEmotywne=len(intersekcja)
        tweet.tokeny = []
        
        for elem in enumerate(intersekcja):
            NAWL_BE_element = next((x for x in NAWL_BE_list if x[0] == elem[1]), None)
            NAWL_element = next((x for x in NAWL_list if x[0] == elem[1]), None)
            if NAWL_BE_element != None and NAWL_element != None:
                tweet.tokeny.append(Token(
                    #przypisani wartości NAWL_word z NAWL_BE
                              NAWL_BE_element[0], 
                    #przypisanie wartośći hap_M_all z NAWL_BE
                              NAWL_BE_element[1], 
                    #przypisanie wartośći ang_M_all z NAWL_BE
                              NAWL_BE_element[2], 
                    #przypisanie wartośći sad_M_all z NAWL_BE
                              NAWL_BE_element[3], 
                    #przypisanie wartośći fea_M_all z NAWL_BE
                              NAWL_BE_element[4], 
                    #przypisanie wartośći dis_M_all z NAWL_BE
                              NAWL_BE_element[5], 
                    #przypisanie wartośći val_M_all z NAWL
                              NAWL_element[1], 
                    #przypisanie wartośći aro_M_all z NAWL
                              NAWL_element[2])) 
        Tweets.append(tweet)
    return Tweets


def SerializeNAWLAndNAWL_BEIntoOneList(NAWL_BE, NAWL):
    words = []
    NAWL_BE_list= NAWL_BE.values.tolist()
    NAWL_list= NAWL.values.tolist()
    for record in NAWL_BE_list:
        NAWL_element = next((x for x in NAWL_list if x[0] == record[0]), None)
        if record != None and NAWL_element != None:
                words.append(NAWLWord(record[0],
                              record[1], 
                              record[2],
                              record[3],
                              record[4],
                              record[5],
                              NAWL_element[1],
                              NAWL_element[2]))
    return words
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
                              token['disg'],
                              token['val'],
                              token['arou']))
            
        Tweets.append(tweet)
    return Tweets

#zserializuj df Tweetów na [Tweet]
def dfNAWLToObjectsNAWLWords(df):
    words=[]
    for row in df:
        word= NAWLWord(row[0],
                              row[1], 
                              row[2],
                              row[3],
                              row[4],
                              row[5],
                              row[6],
                              row[7])
           
        words.append(word)
    return words

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