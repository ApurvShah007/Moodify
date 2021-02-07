import tweepy
import time
from textblob import TextBlob
import re
from afinn import Afinn
import requests
import json
import text2emotion as te
from textblob import TextBlob
import re
from afinn import Afinn
import text2emotion as te
import nltk

#Sentiment Ananlysis

def clean_string(tweet):
    tweet = re.sub('@[a-zA-Z0-9_]{4,}', '', tweet) # removes twitter handles from the tweet
    tweet = re.sub('#[a-zA-Z0-9_]+', '', tweet) # removes hashtags from the tweet
    tweet = re.sub(r'http\S+', '', tweet) #removes urls from the tweet
    tweet = re.compile('RT @').sub('@', tweet, count=1)
    return tweet

def afinn_sent(tweet):
    afinn = Afinn()
    return afinn.score(tweet)

def get_emotion(text):
    return te.get_emotion(text)

def get_emoticon(text):
    return te.get_emoticon(text)

def decide_emotion(tweet, emotion, afinn):
    if emotion['Sad'] > .2 and (afinn < 0 and (re.search('.+cry.+', tweet) or re.search('.+sad.+', tweet) or re.search('.+bad day.+', tweet))):
        return 'sad boi hours'
    
    elif (emotion['Surprise'] + emotion['Sad'] + emotion['Fear']) >= .75 and (re.search('.+study.+', tweet) or re.search('.+test.+', tweet) or re.search('.+tired.+', tweet) or re.search('.+homework.+', tweet) or re.search('.+hw.+', tweet)):
        return 'you prob have a test tomorrow or need to chill and go to bed'

    elif (emotion['Happy'] > .5) and (afinn > 0):
        return 'happy'

    elif (emotion['Surprise'] > .5) or (emotion['Surprise'] >= .25 and re.search('.+excited.+', tweet) or re.search('.+wow.+', tweet)):
        return 'excited'

    elif (emotion['Angry'] > .5) or (emotion['Angry'] >= .25 and re.search('.+angry.+', tweet) or re.search('.+upset.+', tweet) or re.search('.+anger.+', tweet)):
        return 'anger'

    else:
        probable_emotion = max(emotion['Surprise'], emotion['Angry'], emotion['Fear'], emotion['Happy'], emotion['Sad'])
        emo_list = []
        for item in emotion:
            if emotion[item] == probable_emotion:
                emo_list.append(item)
        if 'Sad' in emo_list and afinn < 0:
            return 'sad boi hours'
        elif 'Anger' in emo_list and afinn < 0:
            return 'anger'
        elif 'Fear' in emo_list and afinn < 0:
            return 'fear'
        elif 'Happy' in emo_list and afinn > 0:
            return 'happy'
        elif 'Surprise' in emo_list and afinn > 0:
            return 'excited'
        else:
            return 'inconclusive'
        
def get_music_genre(emotion):
    
    if emotion == 'sad boi hours':
        return {'seed_genres':'alternative, rock, indie-pop, reggae, sad', 'max_danceability': 0.5,'min_danceability': 0, 'target_danceability': 0.25, 'max_energy': 0.5, 'min_energy': 0,'target_energy': 0.25,  'max_tempo': 100,'min_tempo': 0, 'target_tempo': 50,'max_key': 5, 'min_key': 0,'target_key': 2.5}

    elif emotion == 'happy':
        return {'seed_genres':'pop, happy', 'max_danceability': 1,'min_danceability': 0.5, 'target_danceability': 0.75, 'max_energy': 1, 'min_energy': 0.5,'target_energy': 0.75,  'max_tempo': 200,'min_tempo': 100, 'target_tempo': 150,'max_key': 10, 'min_key': 5,'target_key': 7.5}
        
    elif emotion == 'anger':
        return {'seed_genres':'metal, industrial, punk, rock', 'max_danceability': 1,'min_danceability': 0.5, 'target_danceability': 0.75, 'max_energy': 1, 'min_energy': 0.5,'target_energy': 0.75,  'max_tempo': 200,'min_tempo': 100, 'target_tempo': 150,'max_key': 10, 'min_key': 5,'target_key': 7.5}
        
    elif emotion == 'fear':
        return {'seed_genres':'classical, piano', 'max_danceability': 0.5,'min_danceability': 0, 'target_danceability': 0.25, 'max_energy': 0.5, 'min_energy': 0,'target_energy': 0.25,  'max_tempo': 100,'min_tempo': 0, 'target_tempo': 50,'max_key': 5, 'min_key': 0,'target_key': 2.5}

    elif emotion == 'excited':
        return {'seed_genres':'techno, dance', 'max_danceability': 1,'min_danceability': 0.5, 'target_danceability': 0.75, 'max_energy': 1, 'min_energy': 0.5,'target_energy': 0.75,  'max_tempo': 200,'min_tempo': 100, 'target_tempo': 150,'max_key': 10, 'min_key': 5,'target_key': 7.5}

    elif emotion == 'inconclusive':  
        return {'seed_genres':'pop, country' , 'max_danceability': 1,'min_danceability': 0.1, 'target_danceability': 0.5, 'max_energy': 1, 'min_energy': 0.1,'target_energy': 0.5,  'max_tempo': 200,'min_tempo': 0.1, 'target_tempo': 100,'max_key': 10, 'min_key': 0.1,'target_key': 5}
        
    elif emotion == 'you prob have a test tomorrow or need to chill and go to bed':
        return {'seed_genres':'instrumental, classical', 'max_danceability': 0.5,'min_danceability': 0, 'target_danceability': 0.25, 'max_energy': 0.5, 'min_energy': 0,'target_energy': 0.25,  'max_tempo': 100,'min_tempo': 0, 'target_tempo': 50,'max_key': 5, 'min_key': 0,'target_key': 2.5}

        
#Spotify

def make_playlist_url(tweet):
	tweet = clean_string(tweet)
	afinn = afinn_sent(tweet)

	emotion = get_emotion(tweet)

	users_emotion = decide_emotion(tweet, emotion, afinn)
	music_breakdown = get_music_genre(users_emotion)
	#print('The users emotion is: ' + users_emotion + ', and they will be listening to ' + str(music_breakdown))

	seed_genres = music_breakdown['seed_genres']
	max_danceability = music_breakdown['max_danceability']
	min_danceability = music_breakdown['min_danceability']
	target_danceability = music_breakdown['target_danceability']
	max_energy = music_breakdown['max_energy']
	min_energy = music_breakdown['min_energy']
	target_energy = music_breakdown['target_energy']
	max_tempo = music_breakdown['max_tempo']
	min_tempo = music_breakdown['min_tempo']
	target_tempo = music_breakdown['target_tempo']
	max_key = music_breakdown['max_key']
	min_key = music_breakdown['min_key']
	target_key = music_breakdown['target_key']


	endpoint_url = "https://api.spotify.com/v1/recommendations?"

	# OUR FILTERS
	limit=10
	market="US"

	uris = []

	token = "Your Token"

	query = f'{endpoint_url}limit={limit}&market={market}&seed_genres={seed_genres}'

	songs_response = requests.get(query, headers={"Content-Type":"application/json", "Authorization":token})

	json_response = songs_response.json()
	for track in json_response['tracks']:
	    uris.append(track['uri'])

	music_pal_user_id = "wc4uycfbagztxsg12otuun82x"
	endpoint_url = f"https://api.spotify.com/v1/users/{music_pal_user_id}/playlists"
	request_body = json.dumps({
	          "name": "Your custim playlist!",
	          "description": "Enjoy these handpicked songs to match your mood!",
	          "public": True
	        })
	response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
	                        "Authorization":token})


	playlist_id = response.json()['id']
	playlist_url = response.json()['external_urls']['spotify']
	endpoint_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

	request_body = json.dumps({"uris" : uris})
	response = requests.post(url = endpoint_url, data = request_body, headers={"Content-Type":"application/json", 
	                        "Authorization":token})

	return(playlist_url)

#Tweepy

auth = tweepy.OAuthHandler("Your token", "Your token")
auth.set_access_token("Your token", "Your token")

api = tweepy.API(auth)

FILE_NAME = 'last_seen.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
	last_seen_id = retrieve_last_seen_id(FILE_NAME)
	mentions = api.mentions_timeline(last_seen_id,tweet_mode='extended')

	for mention in reversed(mentions):
	        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
	        txt = clean_string(mention.full_text)
	        last_seen_id = mention.id
	        store_last_seen_id(last_seen_id, FILE_NAME)
	        playlist_url = make_playlist_url(mention.full_text)
	        dm = "Here is your custom Spotify Playlist: " + playlist_url
	        try:
	        	api.send_direct_message(mention.user.id, dm)
	        except:
	        	print("Hello")
	        	api.update_status('@' + mention.user.screen_name + " Here is your custom Spotify Playlist: " + playlist_url, mention.id)


#Running forever!

while True:
    reply_to_tweets()
    time.sleep(15)
