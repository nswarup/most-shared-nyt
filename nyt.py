import urllib2
import json
import twitter
import pickle
import os.path

def get_recent_nyts_articles():
    # gets a list of recent NYT articles
    url = "https://api.nytimes.com/svc/mostpopular/v2/mostshared/all-sections/1.json?api-key=API_KEY"
    js = json.loads(urllib2.urlopen(url).read())
    out = []
    for article in js['results']:
        out.append(article['url'])
    return out

def get_popularities(links):
    # Gets the FB share+like count for each of the links in link.
    # links is an array of urls of articles
    # returns an array of (share+like) counts as well as descriptions of the articles
    out = []
    for link in links:
        fb_url = "https://graph.facebook.com/v2.8/" + link + "?access_token=ACC_TOKEN"
        s = urllib2.urlopen(fb_url).read()
        js = json.loads(s)
        descrip = js['og_object']['title']
        pop = js['share']['share_count']
        out.append((pop, descrip, link))
    return out

def get_all_tweets():
    # returns a list of articles that should be tweeted
    articles = get_recent_nyts_articles()
    popularities = get_popularities(articles)
    out = []
    # open the file that keeps track of which articles this account has already tweeted
    if not os.path.isfile("already_tweeted_articles.p"):
        already_tweeted = set()
    else:
        already_tweeted = pickle.load(open("already_tweeted_articles.p"))
    for p in popularities:
        if p[2] in already_tweeted:
            continue
        else:
            if p[0] > 50000:
                out.append(p)
                already_tweeted.add(p[2])
    pickle.dump(already_tweeted, open("already_tweeted_articles.p", "w"))
    return out

def send_tweets(tweets):
    # sends the tweets in the list "tweets"
    api = twitter.Api(consumer_key='KEY',
                      consumer_secret='SECRET',
                      access_token_key='ACESSS',
                      access_token_secret='SECRET')
    for tweet in tweets:
        text_to_post = tweet[2] + " " + tweet[1]
        print text_to_post
        #api.PostUpdate()

tweets = get_all_tweets()
send_tweets(tweets)


