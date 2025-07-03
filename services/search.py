import requests

def semantic_scholar_search(query, limit=3):
url = "https://api.semanticscholar.org/graph/v1/paper/search"
params = {"query": query, "limit": limit, "fields": "title,abstract,url"}
resp = requests.get(url, params=params)
return resp.json().get("data", [])