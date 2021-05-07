import pandas as pd
import spacy as sp
from Flatten import flatten
from Tweet import Tweet
from Token import Token
import LoadCSV
import Helpers
nlp = sp.load("pl_core_news_sm")

Tweets_czas_decyzji = LoadCSV.LoadCzasDecyzji()
NAWL_BE = LoadCSV.LoadNAWL_BE()

Tweets = Helpers.SerializeDfTweetsToObjectsAndAssigneNawlValues(Tweets_czas_decyzji, NAWL_BE, nlp)




df = pd.DataFrame([x.as_dict() for x in Tweets])
df.to_csv("E:\\Lic\\Tweety.csv")
stop = input()