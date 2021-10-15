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
def walkFile(file):
    i=0
    l=[]
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        for f in files:
            print(f)
            str = os.path.join(root, f)
            df = pd.read_csv(str)
            path="../data/allcode/"+f.split('_')[0]
            g=Git(path)
            i+=1
            print(i)
            if(i<=0):
                continue
            for tup in tqdm(df.itertuples()):
                try:
                    df.loc[tup[0],'commit_title']=g.execute('git log --pretty=format:"%s" '+tup[2]+' -1',shell=True)
                    df.loc[tup[0], 'commit_body'] = g.execute('git log --pretty=format:"%b" ' + tup[2] + ' -1',shell=True)
                except:
                    l.append(tup[2])

            df.to_csv(str,index=None)
            print(list(set(l)))


def main():
    walkFile("../data/genealogy")


if __name__ == '__main__':
    main()
