import os
import json
import urllib.request
import sys
import git
from tqdm import tqdm
from git import Git
from git.repo import Repo
from git.repo.fun import is_git_dir
import  pandas as pd
# 遍历文件夹



#和get_issue.py配合使用
#这里获得的是直接可以本地查到的

def walkFile(file):
    file = open('../data/pr_message(NL).dic', mode='r', encoding="utf-8")
    dic = json.load(file)
    file.close()
    res={}
    for project_name in dic.keys():
        print(project_name)
        res[project_name]={}
        path = "../data/allcode/" + project_name
        g = Git(path)
        for num in tqdm(dic[project_name]):
            res[project_name][num]={}
            for sha in dic[project_name][num]['commit_id']:
                res[project_name][num][sha] = {}
                try:
                    res[project_name][num][sha]['commit_title'] = g.execute('git log --pretty=format:"%s" ' +sha + ' -1', shell=True)
                    res[project_name][num][sha]['commit_body'] = g.execute('git log --pretty=format:"%b" ' + sha + ' -1', shell=True)
                except Exception as e:
                    f = open("not_found.txt", 'a')
                    f.write(project_name)
                    f.write('^')
                    f.write(num)
                    f.write('^')
                    f.write(sha)
                    f.write('\n')
                    f.close()


    #file = open('../data/commit_message_in_pr.dic',mode='w',encoding="utf-8")
    #json.dump(res,file,ensure_ascii=False,indent=2)
    #file.close()


def main():
    walkFile("../data/genealogy")


if __name__ == '__main__':
    main()
