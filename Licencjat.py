import pandas as pd
import spacy as sp
from Flatten import flatten
from Tweet import Tweet
from Token import Token
import LoadCSV
import Helpers
nlp = sp.load("pl_core_news_sm")
option = input()
print("wybierz czy chcesz 1- wczytać nowe dane 2- wczytać już zserializowane dane")
if option == 1:
    Tweets_czas_decyzji = LoadCSV.LoadCzasDecyzji()
    NAWL_BE = LoadCSV.LoadNAWL_BE()
    Tweets = Helpers.SerializeDfTweetsToObjectsAndAssigneNawlValues(Tweets_czas_decyzji, NAWL_BE, nlp)
    df = pd.DataFrame([x.as_dict() for x in Tweets])
    df.to_csv("C:\\Users\\48500\\Desktop\\Licencjat\\czasdecyzji_TVP_TVN\\Tweety.csv", sep=";")
elif option == 2: 
    Tweets = LoadCSV.LoadTweets()







stop = input()