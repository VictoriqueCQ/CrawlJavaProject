import requests

URL = 'https://api.github.com/search/repositories?q=language:java+created:2018-01-01..2018-02-01+stars:>20&per_page=100&page=1&sort=stars&order=desc'
headers = {"Authorization": "token "}
r = requests.get(URL, headers=headers)
response_dict = r.json()
print("Total repositories:", response_dict['total_count'])
repo_dicts = response_dict['items']
for repo_dict in repo_dicts:
    print("Stars:", repo_dict['stargazers_count'])
    print("Repository:", repo_dict['html_url'])
