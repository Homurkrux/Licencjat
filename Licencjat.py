import pandas as pd
import spacy as sp
from Flatten import flatten
from Tweet import Tweet
from Token import Token
import LoadCSV
import Helpers
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="darkgrid")

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
    TVN = [tweet for tweet in Tweets if tweet.debata  == 'TVN']
    TVP = [tweet for tweet in Tweets if tweet.debata  == 'TVP']
    TVN = Helpers.group_by_time(TVN, 10)
    TVP = Helpers.group_by_time(TVP, 10)
    
    
    for group in TVP:
        print(len(group))
        list=[]
        iter=0
        happ=0
        ang=0
        sad=0
        fear=0
        disg=0
        time=''
        for tweet in group:
            if iter == 0:
                time = tweet.dataCzas
            if len(tweet.tokeny)>0:
                for token in tweet.tokeny:
                    happ+=float(token.happ.replace(",", "."))
                    ang+=float(token.ang.replace(",", "."))
                    sad+=float(token.sad.replace(",", "."))
                    fear+=float(token.fear.replace(",", "."))
                    disg+=float(token.disg.replace(",", "."))
                    iter+=1
        if iter>0:
            nawl_vals_sum.append([time, round(happ/iter,2),round(ang/iter,2),round(sad/iter,2),round(fear/iter,2),round(disg/iter,2)])
    nawl_vals_sum_df = pd.DataFrame.from_records(nawl_vals_sum, columns=['Time', 'Happines', 'Anger', 'Sadnes', 'Fear', 'Disapointment' ])
    nawl_vals_sum_df = nawl_vals_sum_df.melt('Time', var_name="emotions", value_name='Nawl_Values')
    sns.relplot(x="Time", y="Nawl_Values", hue="emotions", kind="line", data=nawl_vals_sum_df);
    plt.show()
stop = input()