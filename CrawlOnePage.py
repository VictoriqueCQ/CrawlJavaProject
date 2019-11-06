import requests
import os


def clone(URL, stars):
    command = "git clone " + URL
    project_name = URL.split("/")[-1]
    command += " E://javaProjectsFromGithub//" + project_name + "_" + str(stars)
    os.system(command)


URL_1 = "https://api.github.com/search/repositories?q=language:java+created:2018-03-01..2018-04-01+stars:>20&per_page=100&sort=stars&order=desc&page=4"
URL_2 = "https://api.github.com/search/repositories?q=language:java+created:2018-03-01..2018-04-01+stars:>20&per_page=100&sort=stars&order=desc&page=5"
URL_3 = "https://api.github.com/search/repositories?q=language:java+created:2018-03-01..2018-04-01+stars:>20&per_page=100&sort=stars&order=desc&page=6"
def crawl(URL):
    headers = {"Authorization": "token "}
    r1 = requests.get(URL, headers=headers)
    response_dict = r1.json()
    repo_dicts = response_dict['items']
    for repo_dict in repo_dicts:
        # print("Stars:", repo_dict['stargazers_count'], end=' ')
        # print("Repository:", repo_dict['html_url'], end=' | ')
        clone(repo_dict['html_url'], repo_dict['stargazers_count'])
    print()

crawl(URL_1)
crawl(URL_2)
crawl(URL_3)