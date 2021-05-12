import pandas as pd
import spacy as sp


def LoadCzasDecyzji():
    dfTweets_czas_decyzji = pd.read_csv(filepath_or_buffer="C:\\Users\\48500\\Desktop\\Licencjat\\czasdecyzji_TVP_TVN\\czasdecyzji_TVP_TVN.csv",
                        sep=";",
                        header=0,
                        usecols=[0,4,9,17],
                        names=["Date", "Tekst", "Plec", "DEBATA"],
                        parse_dates=["Date"],
                        encoding="utf-8",
                        dtype={"Tekst wzmianki": str},
                        low_memory= False,
                        skip_blank_lines=True)
    dfTweets_czas_decyzji = dfTweets_czas_decyzji[dfTweets_czas_decyzji['Tekst'].notna()]
    dfTweets_czas_decyzji = dfTweets_czas_decyzji.values.tolist()
    return dfTweets_czas_decyzji

def LoadNAWL_BE():
    NAWL_BE = pd.read_csv(filepath_or_buffer="C:\\Users\\48500\\Desktop\\Licencjat\\czasdecyzji_TVP_TVN\\pone.0132305.s004.csv",
                        sep=";",
                        header=0,
                        usecols=[2,4,6,8,10,12],
                        names=["slowo", "happiness", "ang", "sad","fear","disgust"],
                        encoding="utf-8",
                        dtype={"NAWL_word": str,
                               "hap_M_all": float,
                               "ang_M_all": float,
                               "sad_M_all": float,
                               "fea_M_all": float,
                               "dis_M_all": float},
                        low_memory= False,
                        skip_blank_lines=True)
    NAWL_BE= NAWL_BE.values.tolist()
    return NAWL_BE

def LoadTweets():
    NAWL_BE = pd.read_csv(filepath_or_buffer="C:\\Users\\48500\\Desktop\\Licencjat\\czasdecyzji_TVP_TVN\\Tweety.csv",
                        sep=";",
                        names=["slowo", "happiness", "ang", "sad","fear","disgust"],
                        encoding="utf-8",
                        dtype={"NAWL_word": str,
                               "hap_M_all": float,
                               "ang_M_all": float,
                               "sad_M_all": float,
                               "fea_M_all": float,
                               "dis_M_all": float},
                        low_memory= False,
                        skip_blank_lines=True)
    NAWL_BE= NAWL_BE.values.tolist()
    return NAWL_BE

