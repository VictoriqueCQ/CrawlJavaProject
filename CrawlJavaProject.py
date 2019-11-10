import requests
import os
import time

github_url = dict()
URL_List = []
# for i in range(1, 9):
#     URL = "https://api.github.com/search/repositories?q=language:java+created:2018-0%s-01..2018-0%s-01+stars:>20&per_page=100&sort=stars&order=desc" % (
#         i, i + 1)
#     URL_List.append(URL)

URL_9 = "https://api.github.com/search/repositories?q=language:java+created:2018-07-01..2018-07-31+stars:>20&per_page=100&sort=stars&order=desc"
URL_10 = "https://api.github.com/search/repositories?q=language:java+created:2018-08-01..2018-08-31+stars:>20&per_page=100&sort=stars&order=desc"
URL_11 = "https://api.github.com/search/repositories?q=language:java+created:2018-09-01..2018-09-30+stars:>20&per_page=100&sort=stars&order=desc"
# URL_12 = "https://api.github.com/search/repositories?q=language:java+created:2018-12-01..2018-12-31+stars:>20&per_page=100&sort=stars&order=desc"
URL_List.append(URL_9)
URL_List.append(URL_10)
URL_List.append(URL_11)
# URL_List.append(URL_12)

def clone(URL, stars):
    command = "git clone " + URL
    project_name = URL.split("/")[-1]
    command += " D://javaProjectsFromGithub//" + project_name + "_" + str(stars)
    os.system(command)

def crawl(URL):
    # time.sleep(60)
    print("github_url_length:" + str(len(github_url)))
    headers = {"Authorization": "token "}
    r1 = requests.get(URL, headers=headers)
    # print("r1 status code:", r1.status_code)
    response_dict = r1.json()
    Total_Repos = response_dict['total_count']
    iter_index = Total_Repos // 100 + 1

    for index in range(1, iter_index + 1):
        # time.sleep(60)
        req_URL = URL + "&page=%s" % str(index)
        print(req_URL)
        r2 = requests.get(req_URL, headers=headers)
        # print("r2 status code:", r2.status_code)
        resp_dict = r2.json()
        repo_dicts = resp_dict['items']
        for repo_dict in repo_dicts:
            # print("Stars:", repo_dict['stargazers_count'], end=' ')
            # print("Repository:", repo_dict['html_url'], end=' | ')
            repo_url = repo_dict['html_url']
            github_url[repo_url] = repo_dict['stargazers_count']
            clone(repo_dict['html_url'],repo_dict['stargazers_count'])
        print()


#
# for URL in URL_List[:2]:
#     func(URL)
#
# time.sleep(60)
#
# for URL in URL_List[2:4]:
#     func(URL)
#
# time.sleep(60)
#
# for URL in URL_List[4:6]:
#     func(URL)
#
# time.sleep(60)
#
# for URL in URL_List[6:8]:
#     func(URL)
#
# time.sleep(60)
#
# for URL in URL_List[8:10]:
#     func(URL)
#
# time.sleep(60)
#
# for URL in URL_List[10:]:
#     func(URL)
# print(len(github_url))
# print(github_url)
file = open("url.txt", "w")

for i in URL_List:
    crawl(i)

file.close()

# clone("https://github.com/qunarcorp/imsdk-android",1)

# os.system("git clone https://github.com/qunarcorp/imsdk-android E://javaProjectsFromGithub//ims-android")
