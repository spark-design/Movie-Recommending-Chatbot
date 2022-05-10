from flask import Flask, redirect, url_for, render_template, request
from bs4 import BeautifulSoup
import requests
#import pymongo
app = Flask(__name__)

titles = []
actors = []
nodelist = []
feedback = ""
a = 0
gen = []
act = ""
templist = []
genrelist = []

def dfs():
    act = request.form["userBox"]
    act = act.lower()
    global nodelist
    global templist
    nodelist.clear()
    templist.clear()
    for x in actors:
        individualactor = x.split(", ")
        nodelist.append(individualactor)
    
    for x in range(0, len(nodelist)):
        for y in range(0, len(nodelist[x])):
            templist.append(nodelist[x][y])
            tempnode = nodelist[x][y]
            tempnode = tempnode.lower()
            if act == tempnode:
                global actorname
                global globaltitle
                globaltitle = titles[x]
                actorname = act
                return True

class Web_crawler_IMDB:
    def __init__(self):
        print('Web Crawler Class Created !!!', '\n==============================')

    # Writing a function that retrives links of next (given number x) pages (Includes given link)
    def url_get(self, links, x):
        self.url = [links]
        self.x = x
        for i in range(self.x):
            url_req_data = requests.get(self.url[-1])
            url_movie_soup = BeautifulSoup(url_req_data.content, 'html.parser')
            url_body = url_movie_soup.find_all('div', {'class': 'desc'})[-1]
            url_page = 'https://www.imdb.com' + url_body.find('a', {'class': 'lister-page-next next-page'}).get(
                'href') + '&ref_=adv_prv'
            self.url.append(url_page)
            print('Fetching URLs...')
        # URL=self.url

        print('------------------------------', "\nURLs Extracted !!!", '\n------------------------------')
        return self.url

    def extract_data(self, link):
        global a
        a = 5
        self.url = link
        # A Function that extracts data like Title, Time Period, Rating, Genre, Duration, Votes, Directors, Stars, Description etc.
        # These Movie data is extracted from IMDB site
        req_data = requests.get(self.url)  # Requesting data of given link
        review_soup = BeautifulSoup(req_data.content, 'html.parser')  # Extracting html content of a page
        body = review_soup.find_all('div', {'class': 'lister-item mode-advanced'})


        # Looping over every listed Movie on a perticular page
        for movie in body:

                # Getting the Title
                title_class = movie.find('h3', {'class': 'lister-item-header'})
                global title
                title = title_class.find('a').text
                titles.append(title)
                print(title)
                print(titles[::])
                
                # Getting the time-period
                try:
                    time_period = title_class.find('span', {'class': 'lister-item-year text-muted unbold'}).text.strip()
                    print(time_period)
                except:
                    time_period = "Not Found"

                # Getting the genre
                try:
                    genre = movie.find('span', {'class': 'genre'}).text.rstrip().replace(' ', '').text.rstrip().replace('\n', '')
                    print(genre)
                    genrelist.append(genre)
                except:
                    genre = "Not Found"

                # Getting Duration of movie
                try:
                    duration = movie.find('span', {'class': 'runtime'}).text[:3]
                    print(duration)
                except:
                    duration = "Not Found"

                # Getting Directors and Stars
                people_inv = movie.find('p', {'class': ""}).text.strip().replace('\n', '').split('|')
                people_inv = [people.strip() for people in people_inv]
                people_inv = [people[people.find(':') + 1:] for people in people_inv]
                if len(people_inv) == 2:
                    directors = people_inv[0]
                    stars = people_inv[1]
                    actors.append(stars)
                    print(directors)
                    print(stars)
                else:
                    actors.append('actor info not available')
                    directors = "Not Found"

                # Getting the Rating
                try:

                    rating = movie.find('strong').text
                    print(rating)
                except:
                    rating = "Not Found"

                # Getting Votes
                try:
                    vot = movie.find('p', {'class': 'sort-num_votes-visible'})
                    votes = vot.find_all('span')[1].text
                    print(votes)
                except:
                    votes = "Not Found"

                # Getting Description
                try:
                    description = movie.find_all("p", class_="text-muted")[-1].text.lstrip()
                    print(description)
                except:
                    description = 'Not Found'
        for item in titles:
            print(item)

    # Function for extracting data of any no of links
    def extract_pages(self, link):
        self.URL = link
        for i in range(len(self.URL)):
            self.extract_data(self.URL[i])
            print("Extracted Data of Page no.:", i)
        print('------------------------------', '\nExtraction Completed !!!', '\n------------------------------')
no_of_next_pages=0
@app.route("/", methods=["POST","GET"])
def home():
    titles.clear()
    actors.clear()
    if request.method == "POST":
        input = request.form["userBox"]
        input = input.lower() # ignore caps
        input = input.replace(" ", "") #ignore spaces
        input = input.replace("-", "") #ignore dash
        if input == "genre":
            return redirect(url_for('genfinder'))
        if input == "rating":
            return redirect(url_for('ratefinder'))
        if input != "genre" and input != "rating":
            return render_template("temp.html", feedback = "Incorrect. Try genre or rating")
    else:
        return render_template("temp.html", feedback = "Enter a category")

@app.route("/rating", methods=["POST","GET"])
def ratefinder():
    titles.clear()
    actors.clear()
    if request.method == "POST":
        rate = request.form["userBox"]
        if ' ' not in rate:
            link = 'https://www.imdb.com/search/title/?genres=Superhero&title_type=feature&count=5'
            return render_template("ratingpage.html", feedback = "Give a number range EX:6.2 8.4")
        rate = rate.replace(" ", "") #ignore spaces
        rate = rate.replace("-", "") #ignore dashes
        rate1 = rate[0:3]
        rate2 = rate[3:6]
        try: 
            rate1 = float(rate1)
            rate2 = float(rate2)
        except:
            link = 'https://www.imdb.com/search/title/?genres=Superhero&title_type=feature&count=5'
            return render_template("ratingpage.html", feedback = "Invalid format. EX:6.2 8.4")
        if rate1 <= 10.0 and rate1 >= 1.0 and rate2 <= 10.0 and rate2 >= 1.0:
            link = 'https://www.imdb.com/search/title/?user_rating='
            rate1 = str(rate1)
            rate2 = str(rate2)
            link = "".join(['https://www.imdb.com/search/title/?user_rating=',rate1,',',rate2,'&count=5'])
        else: 
            link = 'https://www.imdb.com/search/title/?genres=Superhero&title_type=feature&count=5'
            return render_template("ratingpage.html", feedback = "Range not between 1.0 and 10.0")
        abc=Web_crawler_IMDB()

        #Fetching URLs for next pages
        URL=abc.url_get(link,no_of_next_pages)

        #Extracting data for given URLS
        abc.extract_pages(URL)
        #Giving a link. The number after count= determines how many movies you will choose.
        global genname 
        texttemp = "".join(['movies rated ',rate1,' - ',rate2])
        genname = texttemp
        return redirect(url_for('depthfirstsearch'))
    else:
        return render_template("ratingpage.html", feedback = "Enter a range of rating EX:1.0 6.0")

@app.route("/genre", methods=["POST","GET"])
def genfinder():
    titles.clear()
    actors.clear()
    if request.method == "POST":
        gen = request.form["userBox"]
        gen = gen.lower() # ignore caps
        gen = gen.replace(" ", "") #ignore spaces
        gen = gen.replace("-", "") #ignore dash
        if gen == "comedy":
            link = 'https://www.imdb.com/search/title/?genres=comedy&title_type=feature&count=5'
        if gen == "scifi":
            link = 'https://www.imdb.com/search/title/?genres=Sci-Fi&title_type=feature&count=5'
        if gen == "horror":
            link = 'https://www.imdb.com/search/title/?genres=Horror&title_type=feature&count=5'
        if gen == "romance":
            link = 'https://www.imdb.com/search/title/?genres=Romance&title_type=feature&count=5'
        if gen == "action":
            link = 'https://www.imdb.com/search/title/?genres=Action&title_type=feature&count=5'
        if gen == "thriller":
            link = 'https://www.imdb.com/search/title/?genres=Thriller&title_type=feature&count=5'
        if gen == "drama":
            link = 'https://www.imdb.com/search/title/?genres=Drama&title_type=feature&count=5'
        if gen == "mystery":
            link = 'https://www.imdb.com/search/title/?genres=Mystery&title_type=feature&count=5'
        if gen == "crime":
            link = 'https://www.imdb.com/search/title/?genres=Crime&title_type=feature&count=5'
        if gen == "animation":
            link = 'https://www.imdb.com/search/title/?genres=Animation&title_type=feature&count=5'
        if gen == "adventure":
            link = 'https://www.imdb.com/search/title/?genres=Adventure&title_type=feature&count=5'
        if gen == "fantasy":
            link = 'https://www.imdb.com/search/title/?genres=Fantasy&title_type=feature&count=5'
        if gen == "comedyromance":
            link = 'https://www.imdb.com/search/title/?genres=Comedy-Romance&title_type=feature&count=5'
        if gen == "actioncomedy":
            link = 'https://www.imdb.com/search/title/?genres=Action-Comedy&title_type=feature&count=5'
        if gen == "superhero":
            link = 'https://www.imdb.com/search/title/?genres=Superhero&title_type=feature&count=5'
        if gen != "superhero" and gen != "actioncomedy" and gen != "comedyromance" and gen != "fantasy" and gen != "adventure" and gen != "animation" and gen != "crime" and gen != "mystery" and gen != "drama" and gen != "thriller" and gen != "action" and gen != "romance" and gen != "horror" and gen != "scifi" and gen != "comedy":
            link = 'https://www.imdb.com/search/title/?genres=Superhero&title_type=feature&count=5'
            return render_template("genrepage.html", feedback = "Incorrect. Try horror or comedy")
        abc=Web_crawler_IMDB()

        #Fetching URLs for next pages
        URL=abc.url_get(link,no_of_next_pages)

        #Extracting data for given URLS
        abc.extract_pages(URL)
        #Giving a link. The number after count= determines how many movies you will choose.
        global genname 
        genname = gen
        return redirect(url_for('depthfirstsearch'))
    else:
        return render_template("genrepage.html", feedback = "Enter a genre")

@app.route("/dfs", methods=["POST","GET"])
def depthfirstsearch():
    if request.method == "POST": # Do DFS
        dfs()
        if(dfs() == True and actorname != 'actor info not available'):
            return redirect(url_for('finalresults'))
        else:
             return render_template("dfspage.html", movie = titles, actor = actors, nodes = nodelist, feedback="Actor/actress not in list")
    else:
        return render_template("dfspage.html", movie = titles, actor = actors, feedback = "Choose an actor from the list")

@app.route("/results", methods=["POST","GET"])
def finalresults():
    if request.method == "POST": # Do DFS
        response = request.form["userBox"]
        response = response.lower()
        if response == "thank you!":
            return render_template("resultpage.html", movie = titles, actor = actors,  nodes = templist, feedback="You're welcome!", specificactor = actorname, finaltitle = globaltitle, genrename = genname)
    else:
        return render_template("resultpage.html", movie = titles, actor = actors,  nodes = templist, feedback="Your results have been found!", specificactor = actorname, finaltitle = globaltitle, genrename = genname)
if __name__ == "__main__":
    app.run(debug=True)
