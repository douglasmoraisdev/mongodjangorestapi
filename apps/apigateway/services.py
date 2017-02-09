import requests 

def get_books(year, author, req):
    url = 'http://dmsantos-bethel-api-4356050/reuniaocelula/5899c6a7f6511923031c749a'
    #url = 'https://bethel-api-dmsantos.c9users.io/reuniaocelula/5899c6a7f6511923031c749a' 
    params = {'year': year, 'author': author}
    r = requests.get(url, params=params, headers={'Authorization': 'Bearer '+str(req.auth)})
    books = r.json()
    books_list = {'books':books}
    return books_list
