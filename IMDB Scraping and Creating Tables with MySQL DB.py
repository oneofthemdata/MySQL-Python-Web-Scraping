from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import getpass  # for password protection
import mysql.connector

url = "https://www.imdb.com/list/ls068082370/"


def all_page_link(start_url):
    all_urls = []
    url = start_url
    while url is not None:
        all_urls.append(url)
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        next_links = soup.find_all(class_='flat-button lister-page-next next-page')
        if len(next_links) == 0:
            url = None
        else:
            next_page = "https://www.imdb.com" + next_links[0].get('href')
            url = next_page
    return all_urls


def director_and_actor(director_and_star):
    director_and_star = director_and_star.replace("\n", "")
    director_and_star = director_and_star.replace("|", "")
    director_and_star = director_and_star.split("Stars:")
    director_and_star[0] = director_and_star[0].replace("Director:", "")
    director_and_star[0] = director_and_star[0].replace("Directors:", "")
    for i in range(10):
        director_and_star[0] = director_and_star[0].replace("  ", " ")
    director = director_and_star[0][1:]
    stars = director_and_star[1]
    stars = stars.replace(":", "")
    return director, stars


def votes_and_gross_converter(votes_and_gross):
    votes_and_gross_list = []
    for i in votes_and_gross:
        votes_and_gross_list.append(i.text)
    if len(votes_and_gross) == 2:
        votes_count = votes_and_gross_list[0]
        gross_total = votes_and_gross_list[1]
    else:
        votes_count = votes_and_gross_list[0]
        gross_total = None

    return votes_count, gross_total


movie_array = []
rating_votes_array = []
gross_array = []
for url in tqdm(all_page_link("https://www.imdb.com/list/ls068082370/")):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    for link in soup.find_all(class_='lister-item-content'):
        ID = int(link.find('span', {"class": "lister-item-index unbold text-primary"}).text[:-1])
        Movie = link.find('a').text
        Year = link.find('span', {"class": "lister-item-year text-muted unbold"}).text[1:5]
        Run_Time = link.find('span', {"class": "runtime"}).text
        Genre = link.find('span', {"class": "genre"}).text[1:]
        Rating = link.find('span', {"class": "ipl-rating-star__rating"}).text
        Director, Actors = director_and_actor(link.find_all('p', {"class": "text-muted text-small"})[1].text)
        Votes_Count, Gross_Total = votes_and_gross_converter(link.find_all('span', {"name": "nv"}))
        Votes_Count = int(Votes_Count.replace(",", ""))
        movie_info = [ID, Movie, Year, Run_Time, Genre, Director, Actors]
        rating_votes = [ID, Rating, Votes_Count]
        gross_total_info = [ID, Gross_Total]
        movie_array.append(movie_info)
        rating_votes_array.append(rating_votes)
        gross_array.append(gross_total_info)

# int value stored in str in rating_votes_array
# converting str to int
for e in rating_votes_array:
    for n in range(len(e)):
        if type(e[n]) == str:
            e[n] = float(e[n])

# converting list of list to list of tuples
movie_rows = [tuple(x) for x in movie_array]
rating_votes_rows = [tuple(x) for x in rating_votes_array]
gross_rows = [tuple(x) for x in gross_array]


# making connection to MySQL DB
def getconnection():
    mydb = mysql.connector.connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass.getpass("Enter password: "),
        database="imdbtop250"
    )

    return mydb  # returning mydb to stay connected


connection = getconnection()

create_movies_table_query = """
CREATE TABLE movies(
    ID INT PRIMARY KEY,
    Movie VARCHAR(100),
    Year VARCHAR(4),
    Run_Time VARCHAR(15),
    Genre VARCHAR(80),
    Director VARCHAR(100),
    Actors VARCHAR(100)
)
"""
create_reviews_table_query = """
CREATE TABLE reviews (
    movie_id INT,
    PRIMARY KEY(movie_id),
    FOREIGN KEY(movie_id) REFERENCES movies(ID),
    Rating FLOAT(2,1),
    Total_Rate INT    
)
"""
create_gross_table_query = """
CREATE TABLE gross_total (
    movie_id INT,
    PRIMARY KEY(movie_id),
    FOREIGN KEY(movie_id) REFERENCES movies(ID),
    Gross_Total VARCHAR(10)
)
"""
with connection.cursor() as cursor:
    cursor.execute(create_movies_table_query)
    cursor.execute(create_reviews_table_query)
    cursor.execute(create_gross_table_query)
    connection.commit()
# Inserting records in tables. Using executemany() function instead of execute()
# which well suited for big - real world -  data.
insert_movie_query = """
INSERT INTO movies
(ID, Movie, Year, Run_Time, Genre, Director, Actors)
VALUES ( %s, %s, %s, %s, %s, %s, %s)
"""
insert_reviews_query = """
INSERT INTO reviews
(movie_id, Rating, Total_Rate)
VALUES ( %s, %s, %s)
"""
insert_gross_query = """
INSERT INTO gross_total
(movie_id, Gross_Total)
VALUES ( %s, %s)
"""
# passing arguments into executemany() function. Second argument from IMDB scraping.
with connection.cursor() as cursor:
    cursor.executemany(insert_movie_query, movie_rows)
    cursor.executemany(insert_reviews_query, rating_votes_rows)
    cursor.executemany(insert_gross_query, gross_rows)
    connection.commit()
cursor.close()
connection.close()
