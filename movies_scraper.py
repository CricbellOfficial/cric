import requests
from bs4 import BeautifulSoup


url_list = {}
api_key = "ENTER YOUR API KEY HERE"


def search_movies(query):
    movies_list = []
    movies_details = {}
    website = BeautifulSoup(requests.get(f"https://www.onlinecricketbetting.net/cricket-betting-tips").text, "html.parser")
    m = website.find('div', {'class': 'tips-list tips-today'})
    movies = m.find_all('div', {'class': 'flex-container'})
    for movie in movies:
        if movie:
            movies_details["id"] = f"link2{movies.index(movie)}"
            movies_details["title"] = movie.find('span',{'class': 'text'}).text
            geti = movie.find('a', {'class': 'more'})
            a_tag = movie.find('a', href=True)
            url_list[movies_details["id"]] = a_tag['href']
        movies_list.append(movies_details)
        movies_details = {}        
    return movies_list





def get_movie(query):
    movie_details = {}
    movie_page_link = BeautifulSoup(requests.get(f"https://www.onlinecricketbetting.net/fantasy/dream11/bgl-vs-mpd-08-feb-2023").text, "html.parser")
    chekcurl = url_list[query]
    dreamlink = chekcurl.replace("cricket-betting-tips", "fantasy/dream11")
    movie_page_link2 = BeautifulSoup(requests.get(f"https://www.onlinecricketbetting.net/fantasy/dream11/rsaw-vs-slw-10-feb-2023/").text, "html.parser")  
    
    if movie_page_link:
            title = movie_page_link.find("div", {'class': 'top-picks'})
            t = title.find("p")
                  
            movie_details["title"] = t
    if movie_page_link2:
            
            checkl = ""
            
            
    return movie_details
