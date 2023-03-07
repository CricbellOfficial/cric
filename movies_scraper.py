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
    #movie_page_link = BeautifulSoup(requests.get(f"https://www.onlinecricketbetting.net/fantasy/dream11/bgl-vs-mpd-08-feb-2023").text, "html.parser")
    chekcurl = url_list[query]
    #dreamlink = chekcurl.replace("cricket-betting-tips", "fantasy/dream11")
    movie_page_link = BeautifulSoup(requests.get(f"{chekcurl}").text, "html.parser")  
    
    if movie_page_link:
            movie_details["title"] = movie_page_link.find("div", {'class': 'box'}).h2.text
            text = movie_page_link.find("div", {'class': 'pick'}).strong.text
            movie_details["pick"] = text
            c  = movie_page_link.find("div", {'class': 'wizard'})
            t1 =  c.find_all("div", {'class': 'name'})
            text = "t1"
            text2 = "t2"
            for ll in t1:
                cc = f"{ll}"
                rep = cc.replace('<div class="name">','')
                rep = rep.replace('</div>','')
                if text=="t1":
                    text = f"{rep}"
                else:
                    text2 = f"{rep}"
            movie_details["t1"] = f"{text}"
            movie_details["t2"] = f"{text2}"
            prob =  c.find_all("div", {'class': 'prob'})
            pt = "0"
            pt2 = "0"
            for pp in prob:
                cc = f"{pp}"
                rep = cc.replace('<div class="name">','')
                rep = rep.replace('</div>','')
                if pt=="0":
                    pt = f"{rep}"
                else:
                    pt2 = f"{rep}"
                movie_details["t1p"] = f"{pt}"
                movie_details["t2p"] = f"{pt2}"
            
            
    return movie_details
