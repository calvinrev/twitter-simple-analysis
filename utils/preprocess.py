import re
import ast
import json
import nltk
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
nltk.download('stopwords')

# Remove end-punctuation
def removeEndPunc(tw):
    tw = " ".join(item[:-1] if (item.endswith('.') or item.endswith(',') or item.endswith('2')) else item for item in tw.split())
    return tw

# Remove affix-punctuation
def removeAffixPunc(tw):
    tw = " ".join([w.lstrip('.').lstrip('✅').lstrip('-').lstrip('”').rstrip('”').rstrip('…').rstrip(':') for w in tw.split()])
    return tw

# Remove url(s)
def removeUrl(tw):
    tw = " ".join(item for item in tw.split() if not (item.startswith('https:') or item.startswith('http:')))
    return tw

# Remove hashtag(s)
def removeHashtag(tw):
    tw = " ".join(item for item in tw.split() if not (item.startswith('#')))
    return tw

# Remove mentioned account(s) 
def getMentioned(tw):
    res = re.findall("@([a-zA-Z0-9+_.]{,})", tw.lower())
    if res:
        res = [f'@{i}' for i in res]
        return res
    else:
        return None
        
def removeMention(tw):
    mentioned = getMentioned(tw)
    if mentioned:
        tw = ' '.join(i for i in tw.split() if i not in mentioned)
        return tw
    else:
        return tw

# Remove unused punctuation and reformat number
punc    = set(string.punctuation)
exclude = ['-','%','/','!','?','&','.']
punc    = [i for i in punc if i not in exclude]
def removePunc(tw):
    nbr_old = re.findall("([0-9],[0-9])", tw)
    nbr_new = [i.replace(',','.') for i in nbr_old]
    for i,j in list(zip(nbr_old,nbr_new)):
        tw = tw.replace(i,j)
    tw  = ''.join(i for i in tw if i not in punc)
    return tw

# Formalization text
formFile  = open(f"src/preprocess/reformText.json", "r")
formDict  = json.load(formFile)   
formFile.close()
def formalize(tw):
    tw = ' '.join(formDict[i] if i in formDict.keys() else i for i in tw.split())
    return tw

# Stop word removal
stopWord1 = list(set(stopwords.words('indonesian')))
stopFile  = open(f"src/preprocess/stopWords.txt", "r")
content   = stopFile.read()    
stopWord2 = content.split("\n")
stopFile.close()
stopWord = list(set(stopWord1+stopWord2))
stopWord.remove('tidak')
def stopWordRemoval(tw):
  tw = " ".join([i for i in tw.split() if i not in stopWord])
  return tw
    
# Remove space(s)
def removeSpace(tw):
    tw = tw.strip()
    tw = re.sub('\\s+', ' ', tw)
    return tw

# Tie-up all
def cleanText(tw):
    tw = tw.lower()
    tw = removeSpace(stopWordRemoval(formalize(removePunc(removeMention(removeHashtag(removeUrl(removeAffixPunc(removeEndPunc(tw)))))))))
    return tw

# Stemming Text
stemmer = StemmerFactory().create_stemmer() 
def stemming(tw):
    tw = " ".join(stemmer.stem(w) for w in tw.split())
    return tw

def stemmingClear(tw):
    tw = stemming(tw)
    tw = removeSpace(stopWordRemoval(formalize(tw)))
    return tw