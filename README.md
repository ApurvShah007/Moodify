

# Moodify
Music for your Mood! Tweet at us and we got you covered!

Team - [Apurv Shah](https://apurvshah007.github.io/), Jiaru (Kelly) Li, Rachel Allgaier, Shalin Patel

***Won the best ML Hack at Hacklytics 2021.*** [Check out the project submission](https://devpost.com/software/moodify-bjkw5v). Leave a like if you like the project!

[![Click here to watch the demonstration video!](http://img.youtube.com/vi/8CGkC-EL1L0/0.jpg)](http://www.youtube.com/watch?v=8CGkC-EL1L0)

[Click here](https://www.youtube.com/watch?v=8CGkC-EL1L0) to watch the demonstartion video!
## Project Description

### Inspiration

We draw inspiration for this project from the recent rise and neglect of the very real mental health issues that are being openly vented out on public forums and still being ignored. We believe that not everyone has the time or money to go to an online counselling session during this day and age. We believe that music helps a lot when it comes to helping cope with tough times. It is also a great addition when you are happy or excited or scared/nervous. We wanted to make something that can provide a playlist based on your current mood as not all user playlists fit all moods and not everyone has a playlist for every mood.

### What it Does

Our ultimate goal is to make a software that takes your recent comment, posts, tweets etc and analyzes them and based on your mood gives you a playlist of around 10 songs that are relevant to your mood and how you are feeling which is decided by extensive sentiment analysis of your text. 

We have started off with the first deliverable which is a Twitter Bot that when mentioned in your Tweet, analyzes you tweet, makes a custom playlist that suits your mood and then DMs you the custom playlist that suits your mood! How cool is that? It's the best way to discover new music that suits your mood. And trust us when we say, Music helps!

### How We Built it 

We started off by integrating the Twitter API for our Moodify bot Twitter account, and got the authorization set up. We then interacted with the Spotify API through our Moodify Spotify account. We then worked on intensive sentiment analysis of the tweets that were coming in, trying to classify the tweets according to the mood. We then sent that data to query the Spotify API and make a custom playlist and then it ends with the Twitter Bot sending a DM to the user with that custom playlist.

This bot is written in Python, uses the Twitter API, Spotify API, multiple sentiment analysis frameworks and libraries like text2emotion.

Working Timeline:
Twitter API(getting tweets) -> Sentiment Analysis -> Spotify API(Getting the songs and playlist) -> Twitter API (Sending back the DM)

### Challenges we ran into

We ran into a lot of challenges when it came to the permissions and documentations with the Twitter API. We faced a challenge when the user had set the permission such that not everyone can DM them or when the authorization expired. 

We were also stuck on the fact that the Spotify auth tokens only work for a few minutes and need to be reset every time. We had to find a workaround to get a more permanent setting. 

But these were all technical issues that could be fixed with little playing around and google searches. The biggest challenge the team faced is to convert the prediction from the sentiment analysis to music features, because there is no existing standard for this mapping. What we have done is to search online, for example, what genre of music a happy person should listen to? And we also add a range for features such as Danceability, Energy, Tempo, and Key to make sure the music is upbeat.

### Accomplishments we are proud of 
 
We are very proud of the fact that we all stepped out of our comfort zone, met up with people who were strangers at the beginning of the hackathon and still successfully made a deliverable. 

We are very proud of the fact that our hack tries to tackle real issues with mental health through the medium of technology and spreading awareness of such issues and how music can help. We are happy that we could make a working product that has infinite potential to be achieved in the coming future. 

### What we learnt

We learnt a lot during this process. We learnt how to code a twitter bot and how much planning goes into making an actual working software. We also learnt how to use various very popular APIs and how to do some basic level sentiment analysis of text. 

### Whats next for Moodify

For the future improvement, we want to personalize the playlist according to the user to improve the user satisfaction. We also plan to develop a chrome extension for better interfacing and an app to which users can tell how they feel and the app suggests a playlists or individual songs based on the user history so they don't have to always. 
