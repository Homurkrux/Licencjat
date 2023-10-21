import pandas as pd
import spacy as sp
from Flatten import flatten
from Tweet import Tweet
from Token import Token
import LoadCSV
import Helpers
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import numpy as np
import statistics
sns.set_theme(style="darkgrid")

nlp = sp.load("pl_core_news_sm")
print("wybierz czy chcesz 1- wczytać nowe dane 2- wczytać już zserializowane dane")
option = '2'
nawl_vals_sum=[]
emoWords_sum=[]
len_of_group_sum=[]
if option == '1':
    Tweets_czas_decyzji = LoadCSV.LoadCzasDecyzji()

    NAWL_BE = LoadCSV.LoadNAWL_BE()
    NAWL = LoadCSV.LoadNAWL()
    NAWLWords = Helpers.SerializeNAWLAndNAWL_BEIntoOneList(NAWL_BE, NAWL)
    dfWords = pd.DataFrame([x.as_dict() for x in NAWLWords])
    dfWords.to_csv("E:\\Lic\\NAWLWords.csv", sep=";", encoding="utf-8", index=False)
    Tweets = Helpers.SerializeDfTweetsToObjectsAndAssigneNawlValues(Tweets_czas_decyzji, NAWL_BE, NAWL, nlp)
    Tweets.sort(key=lambda l: l.dataCzas)
    df = pd.DataFrame([x.as_dict() for x in Tweets])
    df.to_csv("E:\\Lic\\Tweety.csv", sep=";", encoding="utf-8", index=False)
elif option == '2': 
    dfTweets = LoadCSV.LoadTweets()
    dfNAWLWords = LoadCSV.LoadNAWLWords()
    Tweets = Helpers.SerializeDfTweetsToTweets(dfTweets)
    NAWLWords = Helpers.dfNAWLToObjectsNAWLWords(dfNAWLWords)
    #Tweets.sort(key=lambda l: l.dataCzas)
    #TVN = [tweet for tweet in Tweets if tweet.debata  == 'TVN' ]
    #TVN= [tweet for tweet in TVN if tweet.dataCzas >= datetime.datetime.strptime('08-10-2019', "%m-%d-%Y")]
    #TVP = [tweet for tweet in Tweets if tweet.debata  == 'TVP']
    pointsTweets = dict(
        valence = [],
        arousal = [],
        happy = [],
        angry = [],
        sad = [],
        fear = [],
        disgust = []
        )
    pointsNAWL = dict(
        valence = [],
        arousal = [],
        happy = [],
        angry = [],
        sad = [],
        fear = [],
        disgust = []
        )
    pointsNAWLList=[]
    pointsTweetsList=[]
    tweetsCount=0
    tweetsWithTokens=0
    tweetWords =0
    tweetsWithoutWords =0
    tweetsWithoutTokens =0
    tweetDistinctWords =[]
    for word in NAWLWords:
        pointsNAWL["valence"].append((float(word.val.replace(",", "."))))
        pointsNAWL["arousal"].append((float(word.arou.replace(",", "."))))
        pointsNAWL["happy"].append((float(word.happ.replace(",", "."))))
        pointsNAWL["angry"].append((float(word.ang.replace(",", "."))))
        pointsNAWL["sad"].append((float(word.sad.replace(",", "."))))
        pointsNAWL["fear"].append((float(word.fear.replace(",", "."))))
        pointsNAWL["disgust"].append((float(word.disg.replace(",", "."))))

        pointsNAWLList.append((float(word.val.replace(",", ".")),float(word.arou.replace(",", "."))))
    for tweet in Tweets:
        tweetsCount+=1
        if tweet.tekstTweeta == "":
            tweetsWithoutWords+=1
        if tweet.slowaEmotywne == 0 :
            tweetsWithoutTokens+=1
        if len(tweet.tokeny) > 0 :
            tweetsWithTokens+=1
        for token in tweet.tokeny:
            tweetWords+=1
            if token.token not in tweetDistinctWords:
                tweetDistinctWords.append(token.token)
            pointsTweets["valence"].append((float(token.val.replace(",", "."))))
            pointsTweets["arousal"].append((float(token.arou.replace(",", "."))))
            pointsTweets["happy"].append((float(token.happ.replace(",", "."))))
            pointsTweets["angry"].append((float(token.ang.replace(",", "."))))
            pointsTweets["sad"].append((float(token.sad.replace(",", "."))))
            pointsTweets["fear"].append((float(token.fear.replace(",", "."))))
            pointsTweets["disgust"].append((float(token.disg.replace(",", "."))))

            pointsTweetsList.append((float(token.val.replace(",", ".")),float(token.arou.replace(",", "."))))
    print('tweetsCount:', tweetsCount)
    print('tweetsWithTokens:', tweetsWithTokens)
    print('tweetWords:', tweetWords)
    print('tweetsWithoutWords:', tweetsWithoutWords)
    print('tweetDistinctWordsCount:', len(tweetDistinctWords))
    print('tweetsWithoutTokens:', tweetsWithoutTokens)
    print('tweetDistinctWords:', sorted(tweetDistinctWords))
    #WYKRESY

    xT, yT = zip(*pointsTweetsList)
    xW, yW = zip(*pointsNAWLList)

    nawlVal, nawlAro, nawlHapp, nawlAng, nawlSad, nawlFear, nawlDisg = pointsNAWL.values()
    tweetVal, tweetAro, tweetHapp, tweetAng, tweetSad, tweetFear, tweetDisg = pointsTweets.values()

    #ROZKLAD NORMALNY

    #NAWL valence
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    hist_values, bins, patches = ax1.hist(nawlVal, bins=50, density=False, alpha=0.6, color='g', label = 'Liczba wystąpień')
    ax1.set_xlabel('Walencja')
    ax1.set_ylabel('Liczba wystąpień')
    ax1.set_ylim(0, max(hist_values) * 1.1)
    x = np.linspace(min(nawlVal), max(nawlVal), 100)
    pdf = (1 / (statistics.stdev(nawlVal) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - statistics.mean(nawlVal)) / statistics.stdev(nawlVal))**2)
    ax2.plot(x, pdf, 'r', label='Prawdopodobieństwo wystąpnienia')
    ax2.set_ylabel('Prawdopodobieństwo wystąpnienia')
    ax2.grid(False)
    plt.xlim(-3, 3)
    plt.tight_layout()
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    #ax2.legend(lines2 + lines, labels2 + labels, loc='upper left', bbox_to_anchor=(0.75, 1.2))
    fig = plt.gcf()
    figlegend = plt.figure(figsize=(5, 1))
    figlegend.legend(lines2 + lines, labels2 + labels, loc='center', ncol=1)
    figlegend.subplots_adjust(bottom=0.2)
    #NAWL arousal
    #plt.show()
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    hist_values, bins, patches = ax1.hist(nawlAro, bins=50, density=False, alpha=0.6, color='g', label = 'Liczba wystąpień')
    ax1.set_xlabel('Pobudzenie')
    ax1.set_ylabel('Liczba wystąpień')
    ax1.set_ylim(0, max(hist_values) * 1.1)
    x = np.linspace(min(nawlAro), max(nawlAro), 100)
    pdf = (1 / (statistics.stdev(nawlAro) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - statistics.mean(nawlAro)) / statistics.stdev(nawlAro))**2)
    ax2.plot(x, pdf, 'r', label='Prawdopodobieństwo wystąpnienia')
    ax2.set_ylabel('Prawdopodobieństwo wystąpnienia')
    ax2.grid(False)
    plt.xlim(1, 5)
    plt.tight_layout()
    #Tweets valence
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    hist_values, bins, patches = ax1.hist(tweetVal, bins=50, density=False, alpha=0.6, color='g', label = 'Liczba wystąpień')
    ax1.set_xlabel('Walencja')
    ax1.set_ylabel('Liczba wystąpień')
    ax1.set_ylim(0, max(hist_values) * 1.1)
    x = np.linspace(min(tweetVal), max(tweetVal), 100)
    pdf = (1 / (statistics.stdev(tweetVal) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - statistics.mean(tweetVal)) / statistics.stdev(tweetVal))**2)
    ax2.plot(x, pdf, 'r', label='Prawdopodobieństwo wystąpnienia')
    ax2.set_ylabel('Prawdopodobieństwo wystąpnienia')
    ax2.grid(False)
    plt.xlim(-3, 3)
    plt.tight_layout()
    #Tweets arousal
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    hist_values, bins, patches = ax1.hist(tweetAro, bins=50, density=False, alpha=0.6, color='g', label = 'Liczba wystąpień')
    ax1.set_xlabel('Pobudzenie')
    ax1.set_ylabel('Liczba wystąpień')
    ax1.set_ylim(0, max(hist_values) * 1.1)
    x = np.linspace(min(tweetAro), max(tweetAro), 100)
    pdf = (1 / (statistics.stdev(tweetAro) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - statistics.mean(tweetAro)) / statistics.stdev(tweetAro))**2)
    ax2.plot(x, pdf, 'r', label='Prawdopodobieństwo wystąpnienia')
    ax2.set_ylabel('Prawdopodobieństwo wystąpnienia')
    ax2.grid(False)
    plt.xlim(1, 5)
    plt.tight_layout()
    # PLOTS


    plt.figure()
    # Plot the data from the two lists
    plt.scatter(nawlVal, nawlAro, label='Słowo', marker='x')
    plt.xlabel('Walencja')
    plt.ylabel('Pobudzenie')
    plt.xlim(-3, 3)
    plt.ylim(1, 5)
    plt.legend()

    

    plt.figure()
    # Plot the data from the two lists
    plt.scatter(tweetVal, tweetAro, label='Słowo', marker='x')
    plt.xlabel('Walencja')
    plt.ylabel('Pobudzenie')
    plt.xlim(-3, 3)
    plt.ylim(1, 5)
    plt.legend()

    

    #Histogramy i prawdopodobieństwo szczęście
    plt.figure()
    plt.hist(nawlHapp, bins=50, alpha=0.6, color='g', label = 'Liczba wystąpień')
    plt.xlabel('Siła nacechowania szczęścia')
    plt.ylabel('Ilość wystąpień')
    plt.xlim(1, 7)  
    plt.legend()

    plt.figure()
    plt.hist(tweetHapp, bins=50, alpha=0.6, color='g', label = 'Liczba wystąpień')
    plt.xlabel('Siła nacechowania szczęścia')
    plt.ylabel('Ilość wystąpień')
    plt.xlim(1, 7)
    plt.legend()
    
    plt.figure()
    plt.xlabel('Siła nacechowania szczęścia')
    plt.ylabel('Prawdopodobieństwo wystąpienia')
    plt.xlim(1, 7)
    plt.ylim(0, 1)    
    # Plot the probability density function (PDF)
    x = np.linspace(min(nawlHapp), max(nawlHapp), 100)
    pdf = (1 / (statistics.stdev(nawlHapp) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - statistics.mean(nawlHapp)) / statistics.stdev(nawlHapp))**2)
    plt.plot(x, pdf, color='r', linewidth=2, label = 'w NAWL')
    x = np.linspace(min(tweetHapp), max(tweetHapp), 100)
    pdf = (1 / (statistics.stdev(tweetHapp) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - statistics.mean(tweetHapp)) / statistics.stdev(tweetHapp))**2)
    plt.plot(x, pdf, color='b', linewidth=2, label = 'w Tweetach')
    plt.legend()

    #Histogramy i prawdopodobieństwo złość
    plt.figure()
    plt.hist(nawlAng, bins=50, alpha=0.6, color='g', label = 'Liczba wystąpień')
    plt.xlabel('Siła nacechowania złości')
    plt.ylabel('Ilość wystąpień')
    plt.xlim(1, 7) 
    plt.legend()

    plt.figure()
    plt.hist(tweetAng, bins=50, alpha=0.6, color='g', label = 'Liczba wystąpień')
    plt.xlabel('Siła nacechowania złości')
    plt.ylabel('Ilość wystąpień')
    plt.xlim(1, 7)  
    plt.legend()
    
    plt.figure()
    plt.xlabel('Siła nacechowania złości')
    plt.ylabel('Prawdopodobieństwo wystąpienia')
    plt.xlim(1, 7)
    plt.ylim(0, 1)    
    # Plot the probability density function (PDF)
    x = np.linspace(min(nawlAng), max(nawlAng), 100)
    pdf = (1 / (statistics.stdev(nawlAng) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - statistics.mean(nawlAng)) / statistics.stdev(nawlAng))**2)
    plt.plot(x, pdf, color='r', linewidth=2, label = 'w NAWL')
    x = np.linspace(min(tweetAng), max(tweetAng), 100)
    pdf = (1 / (statistics.stdev(tweetAng) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - statistics.mean(tweetAng)) / statistics.stdev(tweetAng))**2)
    plt.plot(x, pdf, color='b', linewidth=2, label = 'w Tweetach')
    plt.legend()

    #Histogramy i prawdopodobieństwo smutek
    plt.figure()
    plt.hist(nawlSad, bins=50, alpha=0.6, color='g', label = 'Liczba wystąpień')
    plt.xlabel('Siła nacechowania smutku')
    plt.ylabel('Ilość wystąpień')
    plt.xlim(1, 7)  
    plt.legend()

    plt.figure()
    plt.hist(tweetSad, bins=50, alpha=0.6, color='g', label = 'Liczba wystąpień')
    plt.xlabel('Siła nacechowania smutku')
    plt.ylabel('Ilość wystąpień')
    plt.xlim(1, 7)  
    plt.legend()

    plt.figure()
    plt.xlabel('Siła nacechowania smutku')
    plt.ylabel('Prawdopodobieństwo wystąpienia')
    plt.xlim(1, 7)
    plt.ylim(0, 1)    
    # Plot the probability density function (PDF)
    x = np.linspace(min(nawlSad), max(nawlSad), 100)
    pdf = (1 / (statistics.stdev(nawlSad) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - statistics.mean(nawlSad)) / statistics.stdev(nawlSad))**2)
    plt.plot(x, pdf, color='r', linewidth=2, label = 'w NAWL')
    x = np.linspace(min(tweetSad), max(tweetSad), 100)
    pdf = (1 / (statistics.stdev(tweetSad) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - statistics.mean(tweetSad)) / statistics.stdev(tweetSad))**2)
    plt.plot(x, pdf, color='b', linewidth=2, label = 'w Tweetach')
    plt.legend()

    #Histogramy i prawdopodobieństwo strach
    plt.figure()
    plt.hist(nawlFear, bins=50, alpha=0.6, color='g', label = 'Liczba wystąpień')
    plt.xlabel('Siła nacechowania strachu')
    plt.ylabel('Ilość wystąpień')
    plt.xlim(1, 7) 
    plt.legend()

    plt.figure()
    plt.hist(tweetFear, bins=50, alpha=0.6, color='g', label = 'Liczba wystąpień')
    plt.xlabel('Siła nacechowania strachu')
    plt.ylabel('Ilość wystąpień')
    plt.xlim(1, 7)  
    plt.legend()
    
    plt.figure()
    plt.xlabel('Siła nacechowania strachu')
    plt.ylabel('Prawdopodobieństwo wystąpienia')
    plt.xlim(1, 7)
    plt.ylim(0, 1)    
    # Plot the probability density function (PDF)
    x = np.linspace(min(nawlFear), max(nawlFear), 100)
    pdf = (1 / (statistics.stdev(nawlFear) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - statistics.mean(nawlFear)) / statistics.stdev(nawlFear))**2)
    plt.plot(x, pdf, color='r', linewidth=2, label = 'w NAWL')
    x = np.linspace(min(tweetFear), max(tweetFear), 100)
    pdf = (1 / (statistics.stdev(tweetFear) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - statistics.mean(tweetFear)) / statistics.stdev(tweetFear))**2)
    plt.plot(x, pdf, color='b', linewidth=2, label = 'w Tweetach')
    plt.legend()

    #Histogramy i prawdopodobieństwo niesmak
    plt.figure()
    plt.hist(nawlDisg, bins=50, alpha=0.6, color='g', label = 'Liczba wystąpień')
    plt.xlabel('Siła nacechowania niesmaku')
    plt.ylabel('Ilość wystąpień')
    plt.xlim(1, 7)  
    plt.legend()

    plt.figure()
    plt.hist(tweetDisg, bins=50, alpha=0.6, color='g', label = 'Liczba wystąpień')
    plt.xlabel('Siła nacechowania niesmaku')
    plt.ylabel('Ilość wystąpień')
    plt.xlim(1, 7)  
    plt.legend()
    
    plt.figure()
    plt.xlabel('Siła nacechowania niesmaku')
    plt.ylabel('Prawdopodobieństwo wystąpienia')
    plt.xlim(1, 7)
    plt.ylim(0, 1)    
    # Plot the probability density function (PDF)
    x = np.linspace(min(nawlDisg), max(nawlDisg), 100)
    pdf = (1 / (statistics.stdev(nawlDisg) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - statistics.mean(nawlDisg)) / statistics.stdev(nawlDisg))**2)
    plt.plot(x, pdf, color='r', linewidth=2, label = 'w NAWL')
    x = np.linspace(min(tweetDisg), max(tweetDisg), 100)
    pdf = (1 / (statistics.stdev(tweetDisg) * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - statistics.mean(tweetDisg)) / statistics.stdev(tweetDisg))**2)
    plt.plot(x, pdf, color='b', linewidth=2, label = 'w Tweetach')
    plt.legend()

    plt.show()


stop = input("koniec")