import os
import json
import urllib.request
import sys

import time
import requests
from tqdm import tqdm
import git
from tqdm import tqdm
from git import Git
from git.repo import Repo
from git.repo.fun import is_git_dir
import  pandas as pd
# 遍历文件夹

def walkFile(file):
    max=0
    max_sh=None
    i=0
    dic={}
    name_url=pd.read_csv('../data/pr.csv',header=None,index_col=0)
    #f = open('../data/commit_pr(final version).dic', mode='r', encoding="utf-8")
    #dic = json.load(f)
    #f.close()
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:

            print(f)
            ss = os.path.join(root, f)
            df = pd.read_csv(ss)
            project_name=f.split('_')[0]
            i+=1
            print(i)

            l = list(set(df['start_commit'].tolist()))
            l.sort()


            au = name_url.loc[project_name, 1].replace('.git', '') + '/pull'
            dic[project_name]={}
            progress=0
            total=len(l)
            for sha in l:
                progress+=1

                #if progress<=1999:
                #    continue
                print('{}/{}'.format(progress,total))
                if progress%100==0:
                    pass
                    #file = open('./commit_pr_all_zaiyici.dic', mode='w', encoding="utf-8")
                    #json.dump(dic, file, ensure_ascii=False, indent=2)
                    #file.close()
                page = 1
                while(1):
                    try:
                        item = "https://api.github.com/search/issues?"+"&q=sha:" + sha +"&per_page=100&page="+str(page)
                        headers = {"Authorization": "token " + "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"}

                        r = requests.get(item, headers=headers).json()
                        #time.sleep(0.5)
                        prs = [{'number': pr['number'], 'url': pr['html_url']} for pr in r["items"]]

                        print('{},{}'.format(page,len(prs)))
                        time.sleep(0.5)
                        for pr in prs:

                            if (au in pr['url']):
                                temp=dic[project_name].get(sha, [])
                                # print("PR #{}: {}".format(pr['number'], pr['url']))
                                print("match")
                                temp.append(pr['number'])
                                dic[project_name][sha]=temp
                        page += 1
                        if len(prs)<100:
                            break
                    except Exception as e:

                        print("error occur")
                        f = open("pr_number_error.txt", 'a')
                        f.write(au)
                        f.write('^')
                        f.write(item)
                        f.write('\n')
                        f.close()
                        break

            file = open('../data/commit_pr(final version).dic', mode='w', encoding="utf-8")
            json.dump(dic, file, ensure_ascii=False, indent=2)
            file.close()



def main():
    walkFile("../data/genealogy")


if __name__ == '__main__':
    main()
