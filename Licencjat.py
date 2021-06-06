import pandas as pd
import spacy as sp
from Flatten import flatten
from Tweet import Tweet
from Token import Token
import LoadCSV
import Helpers
nlp = sp.load("pl_core_news_sm")
print("wybierz czy chcesz 1- wczytać nowe dane 2- wczytać już zserializowane dane")
option = '2'
nawl_vals_sum=[]
#
if option == '1':
    Tweets_czas_decyzji = LoadCSV.LoadCzasDecyzji()
    NAWL_BE = LoadCSV.LoadNAWL_BE()
    Tweets = Helpers.SerializeDfTweetsToObjectsAndAssigneNawlValues(Tweets_czas_decyzji, NAWL_BE, nlp)
    df = pd.DataFrame([x.as_dict() for x in Tweets])
    df.to_csv("E:\\Lic\\Tweety.csv", sep=";", encoding="utf-8", index=False)
elif option == '2': 
    dfTweets = LoadCSV.LoadTweets()
    Tweets = Helpers.SerializeDfTweetsToTweets(dfTweets)
    Tweets.sort(key=lambda l: l.dataCzas)
    Tweets = Helpers.group_by_time(Tweets, 10)
    print(Tweets)
    
    for group in Tweets:
        print(len(group))
        list=[]
        iter=0
        happ=0
        ang=0
        sad=0
        fear=0
        disg=0
        for tweet in group:
            if len(tweet.tokeny)>0:
                for token in tweet.tokeny:
                    happ+=float(token.happ.replace(",", "."))
                    ang+=float(token.ang.replace(",", "."))
                    sad+=float(token.sad.replace(",", "."))
                    fear+=float(token.fear.replace(",", "."))
                    disg+=float(token.disg.replace(",", "."))
                    iter+=1
        if iter>0:
            nawl_vals_sum.append([round(happ/iter,2),round(ang/iter,2),round(sad/iter,2),round(fear/iter,2),round(disg/iter,2)])
stop = input()