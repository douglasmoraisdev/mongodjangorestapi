import requests 

#TODO: Make requests internals works (localhost), is returning 400
def get_books(year, author, req):
    #url = 'http://localhost:8080/reuniaocelula/5899c6a7f6511923031c749a.json'
    url = 'https://bethel-api-dmsantos.c9users.io/reuniaocelula/5899c6a7f6511923031c749a' 
    params = {'year': year, 'author': author}
    r = requests.get(url, params=params, headers={'Authorization': 'Bearer '+str(req.auth)})
    print(r)
    books = r.json()
    books_list = {'books':books}
    return books_list
