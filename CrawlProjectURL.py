import requests
import pyexcel

result = []
URL_List = []
URL_9 = "https://api.github.com/search/repositories?q=language:java+created:2018-12-01..2018-12-31+stars:>20&per_page=100&sort=stars&order=desc"
# URL_10 = "https://api.github.com/search/repositories?q=language:java+created:2018-08-01..2018-08-31+stars:>20&per_page=100&sort=stars&order=desc"
# URL_11 = "https://api.github.com/search/repositories?q=language:java+created:2018-09-01..2018-09-30+stars:>20&per_page=100&sort=stars&order=desc"
URL_List.append(URL_9)
# URL_List.append(URL_10)
# URL_List.append(URL_11)


def crawl(URL):
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
            # file = open('project_url.json', 'a+')
            # input_dict = str(result_dict)
            # file.write(input_dict+"\n")
            # print(input_dict)
            # file.close()

for url in URL_List:
    crawl(url)
    pyexcel.save_as(records=result, dest_file_name="E:\\Dec.xlsx")