### necessary imports ### 
from flask import Flask, render_template, request
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import random
# FalconSQL Login https://api.plot.ly/

"""Create and configure an instance of the Flask application"""
app = Flask(__name__)
### local development ###
app.config["TESTING"] = True
app.config["STATIC_AUTO_RELOAD"] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.run(debug=True)
### home page ###
@app.route('/')
def root():
    return render_template('home.html')

    ####################
    ### text image creator ###
@app.route('/textimage')
def text_image():
    
    return render_template('textimageentry.html')

@app.route('/textimage', methods = ['POST'])

def text_image2():
    # user_input = "jay z"
    user_input = request.form['user_input']
    user_input = user_input.replace(' ', '-')
    user_input = user_input.replace(' ', '')

    ### start timer ###
    start = datetime.now()

    ### scraping song links ###
    print('--- scraping song links ---')
    source = requests.get(f'https://www.songlyrics.com/{user_input}-lyrics/').text
    soup = BeautifulSoup(source, 'lxml')
    songlist = soup.find('div', class_='listbox')
    tracklist = songlist.find('table', class_='tracklist').tbody
    song_links = []
    artist_details = []
    for song in tracklist.find_all('tr', itemprop="itemListElement"):
        if song.td.text in [str(x) for x in range(200 + 1)]:
            link = song.find('a')['href']
            if link not in song_links:
                song_links.append(link)

    ### collecting song details ###
    print('--- scraping song details text ---')
    for val in song_links:
        song_title = val[27:-1].split('/', 1)[1]
        song_title = song_title[:-6].replace('-', ' ').capitalize()
        artist_name = user_input.replace('-', ' ').capitalize()

    ### scraping song text ###
        songsource = requests.get(val).text
        soup2 = BeautifulSoup(songsource, 'lxml')
        block = soup2.find('div', id='songLyricsContainer')
        if block.find('p').text != False:
            text = block.find('p').text
            permitted = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
            songtext = text.lower()
            songtext = ' '.join(word for word in songtext.split() if word[0]!='[')
            songtext = songtext.replace("\n", " ").strip()
            songtext = "".join(c for c in songtext if c in permitted)
            songtext = songtext.replace("    ", " ")
            songtext = songtext.replace("   ", " ")
            songtext = songtext.replace("  ", " ")
            artist_details.append(songtext)

    print('--- combining song text ---')
    textblock = ' '.join([str(w) for w in random.sample(artist_details, len(artist_details))])
    textblock = textblock * 2
    print('--- length of text ---')
    print(len(textblock))
    # textblock = '. '.join(artist_details)
    print(f'songs = {len(artist_details)}')
    print(len(textblock))
    print(textblock)

    #### finish timer ###
    print('--- runtime ---')
    break1 = datetime.now()
    print("Elapsed time: {0}".format(break1-start)) # show timer
    
    # text = text1
    # permitted = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
    # text = text.replace("\n", " ").strip()
    # # text = "".join(c for c in text if c in permitted)
    # text = text.replace("    ", " ")
    # text = text.replace("   ", " ")
    # text = text.replace("  ", " ")
    # text = text.lower()
    # textblock = text * 100
    return render_template('textimagedone.html', text=textblock)


    #### finish timer ###
    print('--- runtime ---')
    break1 = datetime.now()
    print("Elapsed time: {0}".format(break1-start)) # show timer


