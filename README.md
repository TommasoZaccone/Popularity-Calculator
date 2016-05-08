# Popularity Calculator
## What is the idea?
- To make an application to support web news editors, bloggers, online news aggregators etc.
- Application must provides a FUTURE POPULARITY ESTIMATION based on which news draft user have inserted.
- Application also provides informations about situation of trend news and popular articles at the moment of request.

## Preprocessing
The dataset, based on list of urls by mashable.com, was completely made with mashable.com articles from 2013 and 2014.
It's possibile look at the urls list on urls_list.txt.
Tools used for Data Extraction
- Pattern: python tool for textual and sentiment analysis developed by CLiPS (Computational Linguistics & Psycholinguistics)
- LXML: python parser for extract data from web content
In order to run the scripts, it's mandatory to install pattern and lxml on python.
Dataset with
mettere
  37074 instances
● 50 attributes KW_WORST_MIN

    

##Keyword Dictionary
A keyword dictionary file is useful to compute attributes relative to keywords present in each article, 
(keyword_dictionary.csv)including all keywords present in our 37074 articles,
For each keyword is computed the minimum, maximum, and total number of shares considering all the articles including that keyword. The code below is relative to script included in PREPROCESSING folder.

- Keyword Dictionary of 16283 keywords
- Counting all the occurrences of a keyword in the articles
- MIN, MAX, TOT, NUM





