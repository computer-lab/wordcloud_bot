import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import tweepy #https://github.com/tweepy/tweepy
import csv
import json
import random
import re
from scipy.misc import imread
from pprint import pprint
from time import sleep
import os

def twitter_api(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def search(dictionary, text):
  for k in dictionary.keys():
    if k in text:
      return dictionary[k]
      break
  whoops = random.choice(dictionary.keys())
  return dictionary[whoops]


def creds():
  with open('creds.json') as data_file:
        data = json.load(data_file)
        consumer_key = data['creds'][0]['consumer_key']
        consumer_secret = data['creds'][0]['consumer_secret']
        access_token = data['creds'][0]['access_token']
        access_token_secret = data['creds'][0]['access_token_secret']
        #return consumer_key, consumer_secret
        return consumer_key, consumer_secret, access_token, access_token_secret

def listen(consumer_key, consumer_secret, access_key, access_secret,since_id):


  #authorize twitter, initialize tweepy
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_key, access_secret)
  api = tweepy.API(auth)
  mentions = api.mentions_timeline(count=200,since_id=since_id)
  return mentions


def get_all_tweets(screen_name, consumer_key, consumer_secret, access_key, access_secret):
  #Twitter only allows access to a users most recent 3240 tweets with this method

  #authorize twitter, initialize tweepy
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_key, access_secret)
  api = tweepy.API(auth)

  #initialize a list to hold all the tweepy Tweets
  alltweets = []

  #initialize a list to hold all of the words
  tweet_text =[]

  #make initial request for most recent tweets (200 is the maximum allowed count)
  new_tweets = api.user_timeline(screen_name = screen_name,count=200)

  #save most recent tweets
  alltweets.extend(new_tweets)

  #save the id of the oldest tweet less one
  oldest = alltweets[-1].id - 1

  #keep grabbing tweets until there are no tweets left to grab

  while len(new_tweets) > 0:

    #all subsiquent requests use the max_id param to prevent duplicates
    new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

    #save most recent tweets
    alltweets.extend(new_tweets)

    #update the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1


  #transform the tweepy tweets into a 2D array that will populate the csv
  for i in alltweets:
    tweet = i.text.encode("utf-8").replace('&amp;','&')
    tweet_text.append(re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*|\@\w+', '',tweet))

  return tweet_text



consumer_key, consumer_secret, access_key, access_secret = creds()

masks = {'dog':['dog_shit.png','shitting dog'],'facebook':['facebook_avatar.png','facebook shape'],'twitter':['twitter_mask.png','twitter bird'],
'bat':['bat.png','bat shape'],'bong':['bong.png','bong'],'horse':['horse.png','horse'],'penis':['penis.png','penis']
,'woman':['sexy_lady.png','sexualized female'],'weed':['weed_leaf.png','weed leaf'],'comic sans':['Comic Sans MS.ttf','comic sans']
,'jumpman':['jumpman.png','jumpman'],'kms':['kms.png','kms'],'honk':['goose.png','honk'], 'manning':['manning.png','michael manning color palette']
,'pope hat':['pope_hat.png','pope hat'],'cat':['cat.png','cat'],'shrek':['shrek.png','shrek'],'pepe':['pepe.png','pepe']
, 'banana':['banana.png','banana']}
seen = []
log = open('log.txt','r')
for l in log:
  last = int(l)
  seen.append(last+1)
log.close()
log = open('log.txt','ab')
while len(seen) > 0:
  last_mention = max(seen)
  try:
    mentions =  listen(consumer_key, consumer_secret, access_key, access_secret,last_mention)
  except Exception:
    print 'some sort of drama when listening'
    sleep(420)
    pass
  if len(mentions) < 1:
    sleep(420)
    print 'no new mentions, taking a 420 second break'
  else:
    for i in mentions:
      request_id = i.id_str
      seen.append(int(request_id)+1)
      log.write(request_id + '\n')
      print i.text

      hashtags = i.entities['hashtags']
      for h in hashtags:
        ht = h['text']
        if 'wordcloud' in ht:
          sender = i.user.screen_name
          request_id = i.id_str
          ats = i.entities['user_mentions']
          if ats:
            for a in ats:
              sn = a['screen_name']
              if sn != 'computerlab_':
                user = sn
              else:
                user = sender
          text = i.text
          text = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*|\@\w+|\#\w+', '',text)
          image,msg_text = search(masks,text)
          if image == 'facebook_avatar.png':
            flatten = False
            background_color = 'white'
            font = './HelveticaNeue-Bold.ttf'
          elif image == 'jumpman.png':
            flatten = False
            background_color = 'black'
            font = './HelveticaNeue-Bold.ttf'
          elif image == 'Comic Sans MS.ttf':
            flatten = True
            background_color = 'black'
            font = './Comic Sans MS.ttf'
            image = False
          elif image == 'twitter_mask.png':
            flatten = False
            background_color = 'white'
            font = './HelveticaNeue-Bold.ttf'
          elif image == 'weed_leaf.png':
            flatten = False
            background_color = 'white'
            font = './HelveticaNeue-Bold.ttf'
          elif image == 'goose.png':
            flatten = False
            background_color = 'black'
            font = './HelveticaNeue-Bold.ttf'
          elif image == 'manning.png':
            flatten = False
            background_color = 'white'
            font = './Comic Sans MS.ttf'
          elif image == 'pope_hat.png':
            flatten = False
            background_color = 'black'
            font = './HelveticaNeue-Bold.ttf'
          elif image == 'shrek.png':
            flatten = False
            background_color = 'white'
            font = './Comic Sans MS.ttf'
          elif image == 'pepe.png':
            flatten = False
            background_color = 'white'
            font = './Comic Sans MS.ttf'
          elif image == 'banana.png':
            flatten = False
            background_color = 'white'
            font = './Comic Sans MS.ttf'
          else:
            flatten = True
            background_color = 'black'
            font = './HelveticaNeue-Bold.ttf'

          if image == 'manning.png':
            msg = '@'+user+' look a '+msg_text+' tweet wordcloud from your tweets'
          elif sender == 'computerlab_':
            msg = '@'+user+' cool '+msg_text+' tweet wordcloud that we generated for you!'
          elif user != sender:
            msg = '@'+user+' '+msg_text+' tweet wordcloud @'+sender+' generated for you!'
          else:
            msg = '@'+user+' thanks for using our wordcloud generator nice '+msg_text+' wordcloud'


          # join tweets to a single string
          words = ' '.join(get_all_tweets(user,consumer_key, consumer_secret, access_key, access_secret))

          # remove URLs, RTs, and twitter handles
          no_urls_no_tags = " ".join([word for word in words.split()
                                      if 'http' not in word
                                          and not word.startswith('@')
                                          and word.lower()  != 'rt'
                                          and word.lower() != 'n'
                                          and word.lower()  != 'w'
                                          and word.lower()  != 'u'
                                          and word.lower() != 'got'
                                      ])
          if image:
            twitter_mask = imread('./'+image, flatten=flatten)
            if flatten is False:
              image_colors = ImageColorGenerator(twitter_mask)
            wordcloud = WordCloud(
                                  font_path=font,
                                  stopwords=STOPWORDS,
                                  background_color=background_color,
                                  width=1800,
                                  height=1400,
                                  mask=twitter_mask
                                 ).generate(no_urls_no_tags)
          else:
            wordcloud = WordCloud(
                      font_path=font,
                      stopwords=STOPWORDS,
                      background_color=background_color,
                      width=1800,
                      height=1400
                     ).generate(no_urls_no_tags)

          plt.imshow(wordcloud)
          plt.axis('off')
          if flatten is False:
            plt.imshow(wordcloud.recolor(color_func=image_colors))
          filename1 = 'resized_image.png'
          #plt.savefig(filename1, bbox_inches='tight', pad_inches=0)
          plt.savefig(filename1, dpi=300)
          api = twitter_api(consumer_key, consumer_secret, access_key, access_secret)
          try:
            api.update_with_media(filename1, status=msg)
            os.remove(filename1)
            print 'tweeted '+msg
            sleep(30)
          except Exception:
            print 'couldnt tweet'
            sleep(30)
            pass

