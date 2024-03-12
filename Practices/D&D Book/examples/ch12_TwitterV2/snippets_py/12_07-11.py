# Section 12.7-12.11 snippets because those sections are one running IPython session

# 12.7 Authenticating with Twitter Via Tweepy to Access Twitter v2 APIs
import tweepy
import keys

# Creating a Client Object
client = tweepy.Client(bearer_token=keys.bearer_token,
                       wait_on_rate_limit=True)

# 12.8 Getting Information About a Twitter Account
nasa = client.get_user(username='NASA', 
    user_fields=['description', 'public_metrics'])

# tweepy.Response Object
# Getting a User’s Basic Account Information
nasa.data.id

nasa.data.name

nasa.data.username

nasa.data.description

# Getting the Number of Accounts That Follow This Account and the Number of Accounts This Account Follows
nasa.data.public_metrics['followers_count']

nasa.data.public_metrics['following_count']

# Getting Your Own Account’s Information

# 12.9 Intro to Tweepy Paginators: Getting More than One Page of Results
# 12.9.1 Determining an Account’s Followers
followers = []

# Creating a Paginator
paginator = tweepy.Paginator(
    client.get_users_followers, nasa.data.id, max_results=5)

# Getting Results
for follower in paginator.flatten(limit=10):
    followers.append(follower.username)
    
print('Followers:', 
      ' '.join(sorted(followers, key=lambda s: s.lower())))

# 12.9.2 Determining Whom an Account Follows
following = []

paginator = tweepy.Paginator(
    client.get_users_following, nasa.data.id, max_results=5)

for user_followed in paginator.flatten(limit=10):
    following.append(user_followed.username)
    
print('Following:', 
      ' '.join(sorted(following, key=lambda s: s.lower())))


# 12.9.3 Getting a User’s Recent Tweets
nasa_tweets = client.get_users_tweets(
    id=nasa.data.id, max_results=5)

for tweet in nasa_tweets.data:
    print(f"NASA: {tweet.data['text']}\n")

# Grabbing Recent Tweets from Your Own Timeline

# 12.10 Searching Recent Tweets; Intro to Twitter v2 API Search Operators
# Utility Function print_tweets from tweetutilities.py
from tweetutilities import print_tweets

# Searching for Specific Words
tweets = client.search_recent_tweets(
    query='Webb Space Telescope', 
    expansions=['author_id'], tweet_fields=['lang'])

print_tweets(tweets)

# Searching with Twitter v2 API Search Operators

# Operator Documentation and Tutorial

# Searching for Tweets From NASA Containing Links
tweets = client.search_recent_tweets(
    query='from:NASA has:links', 
    expansions=['author_id'], tweet_fields=['lang'])

print_tweets(tweets)

# Searching for a Hashtag
tweets = client.search_recent_tweets(query='#metaverse', 
    expansions=['author_id'], tweet_fields=['lang'])

print_tweets(tweets)

# 12.11 Spotting Trending Topics
auth = tweepy.OAuth2BearerHandler(keys.bearer_token)

api = tweepy.API(auth=auth, wait_on_rate_limit=True)

# 12.11.1 Places with Trending Topics
# Note: This part of the Twitter APIs has not been migrated from v1.1 to v2
# yet and is accessible only to "Elevated" and "Academic Research" access.
available_trends = api.available_trends()

len(available_trends)

available_trends[0]

available_trends[1]

# 12.11.2 Getting a List of Trending Topics
# Worldwide Trending Topics
world_trends = api.get_place_trends(id=1)

trends_list = world_trends[0]['trends']

trends_list[0]

trends_list = [t for t in trends_list if t['tweet_volume']]

from operator import itemgetter 
trends_list.sort(key=itemgetter('tweet_volume'), reverse=True) 

for trend in trends_list:
    print(trend['name'])

# New York City Trending Topics
nyc_trends = api.get_place_trends(id=2459115) 

nyc_list = nyc_trends[0]['trends']

nyc_list = [t for t in nyc_list if t['tweet_volume']]

nyc_list.sort(key=itemgetter('tweet_volume'), reverse=True) 

for trend in nyc_list[:5]:
    print(trend['name'])

# 12.11.3 Create a Word Cloud from Trending Topics
topics = {}

for trend in nyc_list:
    topics[trend['name']] = trend['tweet_volume']

from wordcloud import WordCloud

wordcloud = WordCloud(width=1600, height=900,
    prefer_horizontal=0.5, min_font_size=10, colormap='prism', 
    background_color='white')       

wordcloud = wordcloud.fit_words(topics)

wordcloud = wordcloud.to_file('TrendingTwitter.png')



##########################################################################
# (C) Copyright 2019 by Deitel & Associates, Inc. and                    #
# Pearson Education, Inc. All Rights Reserved.                           #
#                                                                        #
# DISCLAIMER: The authors and publisher of this book have used their     #
# best efforts in preparing the book. These efforts include the          #
# development, research, and testing of the theories and programs        #
# to determine their effectiveness. The authors and publisher make       #
# no warranty of any kind, expressed or implied, with regard to these    #
# programs or to the documentation contained in these books. The authors #
# and publisher shall not be liable in any event for incidental or       #
# consequential damages in connection with, or arising out of, the       #
# furnishing, performance, or use of these programs.                     #
##########################################################################
