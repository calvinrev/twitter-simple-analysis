import twint
import os
import nest_asyncio
import pandas as pd
from datetime import date
nest_asyncio.apply()

today = date.today().strftime("%Y-%m-%d")
dir   = r'data/raw/'

def scrapKeyword(keyword, since=None, save=True):
    # Configuration
    c = twint.Config()
    keyword  = keyword.lower()
    c.Search = keyword
    # Setup since datetime
    if since:
        c.Since = since
    c.Pandas        = True
    c.Count         = True
    c.Hide_output   = True
    # Run 
    twint.run.Search(c)
    # Store data
    df = twint.storage.panda.Tweets_df
    if save:
        saveData(df,keyword)
    return(df)

def scrapUser(username, keyword=None, since=None, save=True):
    # Configuration
    c = twint.Config()
    c.Username = username
    #If keyword exist
    if keyword:
        c.Search = keyword.lower()
    # Setup since datetime
    if since:
        c.Since = since
    c.TwitterSearch = True
    c.Pandas        = True
    c.Count         = True
    c.Hide_output   = True
    #Run
    twint.run.Search(c)
    # Store data
    df = twint.storage.panda.Tweets_df
    if save:
        if keyword:
            saveData(df,username,keyword)
        else:
            saveData(df,username)
    return df

def saveData(df, name1, name2=None):
    if not os.path.exists(dir):
        os.makedirs(dir)
    if name2:
        df.to_csv(f'{dir}{today}-{name2}-{name1}.csv', encoding = 'utf-8')
    else:
        df.to_csv(f'{dir}{today}-{name1}.csv', encoding = 'utf-8')

def mergeData(data_list):
    df = pd.concat(map(pd.read_csv, data_list), ignore_index=True)
    return df.iloc[: , 1:]