# Artist Explorer
> 🏜️ Deserter Series:
> Due to the pandemic, I started many different projects but, never finished them. In effort to complete what I started- this series was born. Look forward to my upcoming deserter projects and the variety of my interests!
> 
Inspired by this Vox video: [We measured pop music's falsetto obession](https://youtu.be/qJT2h5uGAC0?si=BubAY0m4ptVo3NfD). I wanted to do my little exploration on my favourite artists after hearing about Spotify’s metadata on track features.

This simple tool compares artists’ track metadata by collecting their top tracks and related feature information to then aggregate into visual analysis.

## Metadata Information 
What specific metadata is used to compare artists' profile?
Spotify audio feature information is classified into:
1. acousticness
2. danceability
3. energy
4. instrumentalness
5. liveness
6. loudness - measured in decibels (dB); values typically range between -60 and 0dB
7. speechiness - detects the presence of spoken word
8. tempo - overall estimated tempo of a track in BPM (beats per minute)
9. valence - describes the musical positiveness

Deatils related to the description can be found in the [Spotify Web API Guide](https://developer.spotify.com/documentation/web-api/reference/get-audio-features)
 
### Cleaning of Data
All feature information but tempo and loudness is expressed in the range of 0.0 to 1.0. The closer to 1.0 the more prevalent the feature is in the song and vice versa.
To ensure that every data point has the same scale and each feature is equally important, min-max normalization was used to normalize tempo and loudness data.

## Use Case
One of my favourite classical music periods is Baroque. I always questioned if my favourite classical musicians have any connections with my favourite modern counterparts.
Artists I ended up choosing for Analysis: Johann Sebastian Bach, Tomaso Albinoni, Berlioz and Laufey.
|![artist_comp_overview](https://github.com/rsures/artistExplorer/blob/main/pictures/fig1_artistInfo.png)|
|:--:|
|Fig. 1 - Artist Overview</b>|

After user selection, a brief overview of each artist allows for a simple comparison (fig.1). It was interesting to see Laufey’s genre categorized as gen-z instead of bossa nova or even jazz.
After identifying each artist's information, a musical profile was created based on the top 10 songs and the features that describe each audio trait. However, the aggregated average of the top 10 songs and their feature are used to visualize each artist’s music (fig. 2).
|![artist_comp_overview](https://github.com/rsures/artistExplorer/blob/main/pictures/fig2.png)|
|:--:|
|Fig. 2 - Artist Song Metadata</b>|

Using the Plotly library a radar chart (fig.3) is created to have a holistic view of each artist’s musical profile.
|![artist_comp_overview](https://github.com/rsures/artistExplorer/blob/main/pictures/raderPlot.png)|
|:--:|
|Fig. 2 - Artist Song Metadata</b>|

From these results, it’s interesting to see how similar in characteristics from each other, considering how different their genres are (classical vs jazz house).
