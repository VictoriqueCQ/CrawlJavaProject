import requests
import os
import pyexcel

github_url = dict()
URL_List = []

URL = "https://api.github.com/search/repositories?q=language:java+created:2016-04-01..2016-04-30+stars:>20&per_page=100&sort=stars&order=desc"
URL_List.append(URL)


def clone(URL, id, stars):
    command = "git clone " + URL
    project_name = URL.split("/")[-1]
    command += " E://javaProjectsFromGithub//2016//Apr//" + project_name + "_" + str(id) + "_" + str(stars)
    os.system(command)


result = []


def crawl(URL):
    print("github_url_length:" + str(len(github_url)))
    headers = {"Authorization": "token "}
    r1 = requests.get(URL, headers=headers)
    response_dict = r1.json()
    Total_Repos = response_dict['total_count']
    iter_index = Total_Repos // 100 + 1
    for index in range(1, iter_index + 1):
        req_URL = URL + "&page=%s" % str(index)
        r2 = requests.get(req_URL, headers=headers)
        resp_dict = r2.json()
        repo_dicts = resp_dict['items']
        for repo_dict in repo_dicts:
            result_dict = dict()
            repo_id = repo_dict['id']
            repo_name = repo_dict['name']
            repo_url = repo_dict['html_url']
            repo_star = repo_dict['stargazers_count']
            repo_create_time = repo_dict['created_at']
            result_dict['id'] = repo_id
            result_dict['name'] = repo_name
            result_dict['url'] = repo_url
            result_dict['star'] = repo_star
            result_dict['create_time'] = repo_create_time
            print(result_dict)
            result.append(result_dict)
            clone(repo_url, repo_id, repo_star)
        print()


for i in URL_List:
    crawl(i)
    pyexcel.save_as(records=result, dest_file_name="D:\\2016_Apr.xlsx")
