import urllib
from lxml.html import fromstring
from pattern.en import *
from pattern.vector import *
from collections import Counter
from datetime import date
import csv
n_ex=0
class Keyword(object):

    def __init__(self, a0, a1, a2,a3):
        self.min = a0
        self.max = a1
        self.tot = a2
        self.num = a3

#get dictionary from file
dictionary={}
file=open("keyword_dictionary_fixed_5.CSV", "r")
reader = csv.reader(file)
for row_ls in reader:
  a=Keyword(row_ls[1],row_ls[2],row_ls[3],row_ls[4])
  dictionary[row_ls[0]]=a

with open('DATASET_0.csv', 'w') as fp:
  r = csv.writer(fp, delimiter=',')
  data=[['URL',
    'WORDS_IN_TITLE',
    'WORDS_IN_CONTENT',
    'RATE_UNIQUE_WORDS_IN_CONTENT',
    'RATE_NON_STOP_WORDS_IN_CONTENT', 
    'RATE_UNIQUE_NON_STOP_WORDS_IN_CONTENT',
    'NUMBER_LINKS',
    'EMBEDDED_FACEBOOK_POSTS',
    'EMBEDDED_TWITTER_POSTS',
    'EMBEDDED_INSTAGRAM_POSTS',
    'NUMBER_IMAGES', 
    'NUMBER_VIDEOS',
    'WEEKDAY_IS_MONDAY',
    'WEEKDAY_IS_TUESDAY',
    'WEEKDAY_IS_WEDNESDAY',
    'WEEKDAY_IS_THURSDAY', 
    'WEEKDAY_IS_FRIDAY', 
    'WEEKDAY_IS_SATURDAY',
    'WEEKDAY_IS_SUNDAY',
    'DATA_CHANNEL_IS_LIFESTYLE',
    'DATA_CHANNEL_IS_ENTERTAIMENT',
    'DATA_CHANNEL_IS_BUS',
    'DATA_CHANNEL_IS_SOCHMED',
    'DATA_CHANNEL_IS_TECH',
    'DATA_CHANNEL_IS_WORLD', 
    'AVERAGE_TOKEN_LENGHT',
    'NUMBER_KEYWORDS',
    'KW_WORST_MIN',
    'KW_WORST_MAX',
    'KW_WORST_AVG',
    'KW_BEST_MIN',
    'KW_BEST_MAX',
    'KW_BEST_AVG', 
    'KW_MEDIUM_MIN',
    'KW_MEDIUM_MAX',
    'KW_MEDIUM_AVG',
    'GLOBAL_SUBJECTIVITY',
    'GLOBAL_SENTIMENT_POLARITY', 
    'RATE_NEGATIVE_ON_NON_STOP',
    'RATE_POSITIVE_ON_NON_STOP', 
    'GLOBAL_RATE_POSITIVE',
    'GLOBAL_RATE_NEGATIVE',
    'MIN_POSITIVE_POLARITY',
    'MAX_POSITIVE_POLARITY',
    'AVG_POSITIVE_POLARITY', 
    'MIN_NEGATIVE_POLARITY',
    'MAX_NEGATIVE_POLARITY',
    'AVG_NEGATIVE_POLARITY', 
    'TITLE_SUBJECTIVITY', 
    'TITLE_POLARITY',
    'SHARES' 
    ]]
  r.writerows(data)

  url_list=open('URL_COMPLETE_LIST.txt','r')
  url_list=url_list.readlines()


  for u in url_list:
    url=u
    content = urllib.urlopen(url).read()
    doc = fromstring(content)
    doc.make_links_absolute(url)

    kw_vector_total=[]
    kw_ls0=[]
    kw_v_ord=[]

    kw= doc.xpath('.//meta[@name="keywords"]/@content')
    kw_ls=kw[0].split(', ')
    s=0
    for i in kw_ls:
      if (i != 'uncategorized'):
        kw_vector_total.append(dictionary[i].tot)
        kw_ls0.append(i)
        x=int(dictionary[i].tot)
        kw_v_ord.append(x)
        s=s+1


    if(len(kw_vector_total)==0):
        kw_vector_total.append(dictionary['uncategorized'].tot)
        kw_ls0.append('uncategorized')
        x=int(dictionary['uncategorized'].tot)
        kw_v_ord.append(x)
        s=s+1

    #best kewyord
    best_i=kw_vector_total.index(max(kw_vector_total))

    max_best=dictionary[kw_ls0[best_i]].max
    min_best=dictionary[kw_ls0[best_i]].min
    avg_best=float(dictionary[kw_ls0[best_i]].tot)/float(dictionary[kw_ls0[best_i]].num)

    #worst kewyord
    worst_i=kw_vector_total.index(min(kw_vector_total))

    max_worst=dictionary[kw_ls0[worst_i]].max
    min_worst=dictionary[kw_ls0[worst_i]].min
    avg_worst=float(dictionary[kw_ls0[worst_i]].tot)/float(dictionary[kw_ls0[worst_i]].num)

    #medium keyword
    #sort the array by num of shares field a.tot
    kw_v_ord=sorted(kw_v_ord, key=int)
    med_i_tot=int(float(s/2))

    #return the index of medium element in term of shares 
    medtot=kw_v_ord[med_i_tot]
    med_i=kw_vector_total.index(str(medtot))


    max_med=dictionary[kw_ls0[med_i]].max
    min_med=dictionary[kw_ls0[med_i]].min
    avg_med=float(dictionary[kw_ls0[med_i]].tot)/float(dictionary[kw_ls0[med_i]].num)


    #retrieve title and content
    title= doc.find(".//title").text
    #print title

    el=doc.find_class("article-content")
    text = el[0].text_content()

    #number of fb embedded
    fb_posts=el[0].find_class("fb-post")
    #print ("Facebook Posts embedded: ")+str(len(fb_posts))
    links_fb=0
    embedded_facebook_posts=0
    if(len(fb_posts)!=0):
      embedded_facebook_posts=len(fb_posts)  
      for f in fb_posts:
        l_fb = f.xpath(".//a/@href")
        links_fb = links_fb +len(l_fb)
        #print ('len   fb    ') + str(len(l_fb))

      
    #number of instagram post embedded
    instagram_posts=el[0].find_class("instagram-media")
    #print ("Instagram Posts embedded: ")+str(len(instagram_posts))
    links_instg=0
    embedded_instagram_posts=0
    if(len(instagram_posts)!=0):
      embedded_instagram_posts=len(instagram_posts)
      for g in instagram_posts:
        l_instg = g.xpath(".//a/@href")
        links_instg=links_instg+len(l_instg)


    #number of twitter posts embedded
    tweets=el[0].find_class("twitter-tweet")
    #print ("Tweets embedded: ")+str(len(tweets))
    links_twt=0
    embedded_twitter_posts=0
    if(len(tweets)!=0):
      embedded_twitter_posts=len(tweets)
      for t in tweets:
        l_tw = t.xpath(".//a/@href")
        links_twt=links_twt+len(l_tw)

    #number of link in text
    links = el[0].xpath(".//a/@href")

    n_links= sum(1 for x in links)

    number_links=n_links-links_instg-links_twt-links_fb

    #print ('n_links: ') + str(number_links)

    #number of images
    images= el[0].xpath(".//img")
    n_images= sum(1 for x in images)

    article_image=doc.find_class("article-image")
    ls_a_images=article_image[0].getchildren()
    if(len(ls_a_images) >0):
        n_images=int(n_images)+1
    #print('n_images: ') + str(n_images)

    #number of videos
    videos= el[0].xpath(".//iframe")
    n_videos = sum(1 for x in videos)
    #print('n_videos: ') + str(n_videos)
    
    #numbers of keywords
    kw= doc.xpath('.//meta[@name="keywords"]/@content')
    #print('keywords ') + str(kw)
    n_kws=len(kw[0].split())
    #print('number of keywords: ') + str(n_kws)

    #data-channel
    data_channel_el=doc.find_class("page-header channel")
    data_channel_name_ls = data_channel_el[0].xpath('./@data-channel')
    data_channel_name=data_channel_name_ls[0]
    #print ('data_channel_name ') + str(data_channel_name)

    data_channel= [0,0,0,0,0,0]


    if(data_channel_name=='lifestyle'):
      data_channel[0]='1'
    if(data_channel_name=='entertainment'):
      data_channel[1]='1'
    if(data_channel_name=='bus'or data_channel_name=='business'):
      data_channel[2]='1'
    if(data_channel_name=='socmed' or data_channel_name=='social-media'):
      data_channel[3]='1'
    if(data_channel_name=='tech'):
      data_channel[4]='1'
    if(data_channel_name=='world'):
      data_channel[5]='1'

    #numbers of word in title
    w_title_filtered=words(title, 
           filter = lambda w: w.strip("'").isalnum(),
      punctuation = '.,;:!?()[]{}`''\"@#$^&*+-|=~_')
    words_title=len(w_title_filtered)
    #print('words_title: ') + str(words_title)


    #print('text: ') + text
    #numbers of word in text
    w_text_filtered=words(text, 
           filter = lambda w: w.strip("'").isalnum(),
      punctuation = '.,;:!?()[]{}`''\"@#$^&*+-|=~_')
    words_text=len(w_text_filtered)
    #print('words_text: ') + str(words_text)

    #numbers of unique word
    ls_unique_words =list(Counter(w_text_filtered))
    number_unique_words=len(ls_unique_words)
    #print ('number_unique_words ')+ str(number_unique_words)

    #rate unique words
    if (words_text==0):
        rate_unique_words=0
    else:
        rate_unique_words=(float(number_unique_words)/words_text)
    #print ('rate_unique_words ')+ str(rate_unique_words)


    #returns a dictionary of non-stop words {word, count}
    ls_nstop_text=count(
          words = w_text_filtered, 
            top = None,         # Filter words not in the top most frequent (int).
      threshold = 0,            # Filter words whose count <= threshold.
        stemmer = LEMMA,         # PORTER | LEMMA | function | None
        exclude = [],           # Filter words in the exclude list.
      stopwords = False,        # Include stop words?
       language = 'en')         # en, es, de, fr, it, nl
    

    nstop_text_words=0
    for i in ls_nstop_text:
        nstop_text_words=nstop_text_words+ls_nstop_text[i]


    #rate of non-stop word
    #print ('nstop_text_words ')+ str(nstop_text_words)

    if(words_text==0):
        rate_nstop_words=0
    else:
        rate_nstop_words=(float(nstop_text_words)/words_text)
    #print ('rate_nstop_words ')+ str(rate_nstop_words)


    #rate of unique non-stop 
    #ls_unique_ns_words =list(Counter(ls_nstop_text))
    number_unique_ns_words=len(ls_nstop_text)
    #print ('number_unique_ns_words ')+ str(number_unique_ns_words)

    if(words_text==0):
        rate_unique_ns_words=0
    else:
        rate_unique_ns_words=(float(number_unique_ns_words)/words_text)
    #print('rate_unique_ns_words ')+ str(rate_unique_ns_words)

    #average lenght of words
    ln=0;
    for i in ls_nstop_text:
    	ln=(len(i) + ln)

    if(nstop_text_words==0):
        avg_len_words=0
    else:
        avg_len_words=float(ln)/float(nstop_text_words)

    #print('avg_len_words: ')+ str(avg_len_words)


    #global subjectivity/polarity
    global_sp=sentiment(text)
    ls_global_sp=sentiment(text).assessments

    global_subjectivity=global_sp[1]
    global_sentiment_polarity=global_sp[0]
    #print('\n')

    #print global_subjectivity
    #print global_sentiment_polarity

    global_number_positive=0
    global_number_negative=0
    for i in ls_global_sp:
        if (i[1]>0):
            global_number_positive=global_number_positive+1
        if (i[1]<0):
            global_number_negative=global_number_negative+1


    if(words_text==0):
        global_rate_positive=0
    else:
        global_rate_positive = float(global_number_positive)/float(words_text)


    #global number/global rate negative
    if(words_text==0):
        global_rate_negative=0
    else:
        global_rate_negative = float(global_number_negative)/float(words_text)

    #print('global_number_positive ')+ str(global_number_positive)
    #print('global_rate_positive ')+ str(global_rate_positive)
    #print('global_number_negative ')+ str(global_number_negative)
    #print('global_rate_negative ')+ str(global_rate_negative)
    

    #rate positive among non-stop
    sp=sentiment(ls_nstop_text)
    ls_sp=sentiment(ls_nstop_text).assessments

    number_positive=0
    number_negative=0
    for i in ls_sp:
        if (i[1]>=0):
            number_positive=number_positive+1
        if (i[1]<0):
            number_negative=number_negative+1


    #number/rate positive 
    if(nstop_text_words==0):
        rate_positive=0
    else:
        rate_positive = float(number_positive)/float(nstop_text_words)

    #print('number_positive ')+ str(number_positive)
    #print('rate_positive ')+ str(rate_positive)

    # number/rate negative
    if(nstop_text_words==0):
        rate_negative=0
    else:
        rate_negative = float(number_negative)/float(nstop_text_words)
    
    #print('number_negative ')+ str(number_negative)
    #print('rate_negative ')+ str(rate_negative)


    #weekday Monday=0,etc
    w= doc.xpath('.//meta[@name="date"]/@content')
    #print w[0]
    wd=str(w[0])
    wdls=wd.split(' ')
    date_time=wdls[0].split('-')

    year=int(date_time[0])
    month=int(date_time[1])
    day=int(date_time[2])

    weekday=date(year,month,day).weekday()
    #print('weekday :')+ str(weekday)
    #print weekday

    #set day of the week
    week_days= [0,0,0,0,0,0,0]
    week_days[int(weekday)]=1

    #min/max pos polarity
    max_positive_polarity=0.001
    min_positive_polarity=1
    total_positive_polarity=0
    for i in ls_sp:
        if(float(i[1])>0):
            if(float(i[1])>max_positive_polarity):
                max_positive_polarity = float(i[1])
            if(float(i[1])<min_positive_polarity):
                min_positive_polarity = float(i[1])
            total_positive_polarity = total_positive_polarity + float(i[1])

    #avg pos polarity
    if(number_positive!=0):
        avg_positive_polarity = total_positive_polarity / number_positive
    else:
        avg_positive_polarity=0
        max_positive_polarity=0 
        min_positive_polarity=0

    #min/max neg polarity
    max_negative_polarity=-1
    min_negative_polarity=-0.001
    total_negative_polarity=0
    for i in ls_sp:
        if(float(i[1])<0):
            if(float(i[1])>max_negative_polarity):
                max_negative_polarity = float(i[1])
            if(float(i[1])<min_negative_polarity):
                min_negative_polarity = float(i[1])
            total_negative_polarity = total_negative_polarity + float(i[1])

    #avg neg pol
    if(number_negative!=0):
        avg_negative_polarity = total_negative_polarity / number_negative
    else:
        avg_negative_polarity=0
        max_negative_polarity=0
        min_negative_polarity=0
    #title subjectivity and polarity
    title_sp=sentiment(title)

    title_subjectivity=title_sp[1]
    title_polarity=title_sp[0]


    sh=doc.find_class("total-shares")
    shares_str=sh[0].text_content().split()[0]
    if(shares_str.find('k')!=-1):
      s=shares_str.split('k')[0]
      shares=float(s)*1000
      shares=int(shares)
    else:
      if(shares_str.find('M')!=-1):
        s=shares_str.split('M')[0]
        shares=float(s)*1000000
        shares=int(shares)
      else:
        if(shares_str.find(',')!=-1):
          s=shares_str.split(',')[0]
          s0=shares_str.split(',')[1]
          n=s+s0
          shares=int(n)
        else:
          shares=int(shares_str)
    
    n_ex=n_ex+1
    print str(n_ex) 
    
    data=[[url,
    words_title,
    words_text,
    rate_unique_words,
    rate_nstop_words,
    rate_unique_ns_words,
    number_links,
    embedded_facebook_posts,
    embedded_twitter_posts,
    embedded_instagram_posts,
    n_images,
    n_videos,
    week_days[0],
    week_days[1],
    week_days[2],
    week_days[3],
    week_days[4],
    week_days[5],
    week_days[6],
    data_channel[0],
    data_channel[1],
    data_channel[2],
    data_channel[3],
    data_channel[4],
    data_channel[5],
    avg_len_words,
    n_kws,
    min_worst,
    max_worst,
    avg_worst,
    min_best,
    max_best,
    avg_best,
    min_med,
    max_med,
    avg_med,
    global_subjectivity,
    global_sentiment_polarity,
    rate_negative,
    rate_positive,
    global_rate_positive,
    global_rate_negative,
    min_positive_polarity,
    max_positive_polarity,
    avg_positive_polarity,
    min_negative_polarity,
    max_negative_polarity,
    avg_negative_polarity,
    title_subjectivity,
    title_polarity,
    shares
    ]]
    r.writerows(data)
    





