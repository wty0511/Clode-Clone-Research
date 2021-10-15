from multiprocessing.dummy import Pool as ThreadPool
import json
import time
import requests
import urllib.request
import sys
from requests.exceptions import ConnectionError,ReadTimeout

from github import RateLimitExceededException
from github import Github
from tqdm import tqdm
import requests
import json
from github import Github
import pandas as pd
import datetime
import os
# using an access token
df=pd.read_csv("./pr.csv",header=None,index_col=0)
#print(df)
#g = Github(login_or_token="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")


#dic={}

file = open('./pr_new_3.dic',mode='r', encoding="utf-8")
old = json.load(file)
file.close()


file = open('./commit_pr_all_zaiyici.dic',mode='r', encoding="utf-8")
pr_num = json.load(file)
file.close()
dd=['added_to_project', 'referenced', 'milestoned', 'unassigned', 'closed', 'head_ref_deleted', 'review_requested', 'demilestoned', 'mentioned', 'review_request_removed', 'renamed', 'locked', 'head_ref_restored', 'comment_deleted', 'head_ref_force_pushed', 'unsubscribed', 'reopened', 'merged', 'labeled', 'ready_for_review', 'subscribed', 'moved_columns_in_project', 'review_dismissed', 'base_ref_changed', 'base_ref_force_pushed', 'assigned', 'unlabeled']
data=[]
def get_commit_comment(repo,sha):
    return {
        "commit_comment":[x.raw_data for x in repo.get_commit(sha).get_comments()]
    }

def get_issue_envent(issue):
    return {
        "issue_envent":[x.raw_data for x in issue.get_events()]
    }
def get_pr_file(pr):
    return {
        "file":[x.raw_data for x in pr.get_files()]
    }
def get_timeline_event(issue):
    return {
        "timeline_event":[x.raw_data for x in issue.get_timeline()]
    }

def get_reactions(issue):
    return {
        "reactions":[x.raw_data for x in issue.get_reactions()]
    }
def get_checks(repo,sha):
    return [x.raw_data for x in repo.get_commit(sha).get_check_runs()],[x.raw_data for x in repo.get_commit(sha).get_check_suites()]
def get_all_checks(repo,ids):
    check_runs = []
    check_suites = []
    for sha in ids:
        runs, suites = get_checks(repo, sha)
        check_runs.extend(runs)
        check_suites.extend(suites)
    return check_runs,check_suites
def wait(index,token):

    headers = {"Authorization": "token " + token}

    response = requests.get('https://api.github.com/rate_limit',headers=headers)
    pr_headers=response.headers
    remain = int(pr_headers["x-ratelimit-remaining"])
    #print(pr_headers['X-RateLimit-Limit'])
    if remain < 1:
        #print(token)
        time_now = datetime.datetime.now()
        time_refresh = datetime.datetime.fromtimestamp(int(pr_headers["x-ratelimit-reset"]))
        print("{}:waiting to {}".format(index,time_refresh))
        print(pr_headers['X-RateLimit-Limit'])

        wait_time = (time_refresh - time_now).total_seconds()
        time.sleep(int(wait_time) + 10)
def get_data(pr):
    temp = {}
    temp["pr_info"] = pr.raw_data
    temp["reviews"] = [x.raw_data for x in pr.get_reviews()]
    temp["issue_comments"] = [x.raw_data for x in pr.get_issue_comments()]
    temp["review_comments"] = [x.raw_data for x in pr.get_review_comments()]
    time.sleep(1)
    return temp
def get_pr(input):
    index,start,end,token=input
    g = Github(login_or_token=token)
    error=[]
    this={}
    count=0
    all=data[start:end]
    for name,num in all:
        t=this.get(name, [])
        t.append(str(num))
        this[name]=t
    #print(this)
    try:
        file = open("./data_30/pr_"+str(index)+".dic", mode='r', encoding="utf-8")
        dic = json.load(file)
        file.close()
    except:
        print("not found")
        dic={}
    for name in this:

        l=df.loc[name,1].split('/')
        path=l[3]+"/"+l[4].replace(".git","")
        path_list=[path]
        while (len(path_list) > 0):
            time.sleep(0.5)
            tqdm.write("{}:连接仓库{}" .format(index,name))
            try:
                repo = g.get_repo(path_list.pop())
            except RateLimitExceededException as e:
                path_list.append(path)
                wait(index,token)
                time.sleep(0.5)
            except Exception as e:
                print(e)
                path_list.append(path)
        '''
        for x in repo.get_projects():
            print(x.number)
            for colum in x.get_columns():
                for card in colum.get_cards():
                    print(json.dumps(card.get_content().raw_data, sort_keys=True, indent=4, separators=(',', ':')))

        for i in repo.get_commit("77e6d5e7131cfaea687c268041148be4233d53c4").get_check_runs():
            print(json.dumps(i., sort_keys=True, indent=4, separators=(',', ':')))

        for i in repo.get_commit("77e6d5e7131cfaea687c268041148be4233d53c4").get_check_suites():
            print(json.dumps(i.raw_data, sort_keys=True, indent=4, separators=(',', ':')))
        '''

        #dic[name]=dic.get(name,{})
        dic[name]["path"]=path
        for number in tqdm(this[name],desc=str(index),position=0):

            try:

                if number=="path":continue
                #k=dic[name][number].keys()
                #if "reactions" in k and "issue_envent" in k and "file" in k and "timeline_event" in k:continue

                #pr = repo.get_pull(int(number))
                #issue = repo.get_issue(int(number))
                #dic[name][number] = get_data(pr)
                #dic[name][number].update(get_issue_envent(issue))
                #dic[name][number].update(get_pr_file(pr))
                #dic[name][number].update(get_timeline_event(issue))
                #dic[name][number].update(get_reactions(issue))
                check_runs,check_suites=get_all_checks(repo,dic[name][number]["commit_id"])
                dic[name][number]["check_runs"]=check_runs
                dic[name][number]["check_suites"]=check_suites

                count += 1
                if count % 10 == 0:
                    file = open("./data_30/pr_" + str(index) + ".dic", mode='w', encoding="utf-8")
                    json.dump(dic, file, ensure_ascii=False, indent=2)
                    file.close()

            except RateLimitExceededException as e:
                error.append((path, number))
                wait(index,token)
            except Exception as e:
                error.append((path, number))
                tqdm.write("记录错误")
                print(type(e))

            '''
            except ConnectionError as e:
                print(e)
                tqdm.write("连接失败")
                error.append((path,number))

            except ReadTimeout as e:
                print(e)
                tqdm.write("超时")
                error.append((path,number))

            except KeyError as e:
                print(dic[name].keys())
                print(type(number))
                tqdm.write("？")
                print(name)
                print(e)
                print(index)
                error.append((path, number))
            '''

        while len(error) > 0:
            try:
                tqdm.write("正在处理error")
                path, number = error.pop()
                name = path.split('/')[1]
                repo = g.get_repo(path)
                #pr = repo.get_pull(int(number))
                #issue = repo.get_issue(int(number))
                # dic[name][number] = get_data(pr)
                #dic[name][number].update(get_issue_envent(issue))
                #dic[name][number].update(get_pr_file(pr))
                #dic[name][number].update(get_timeline_event(issue))
                #dic[name][number].update(get_reactions(issue))
                check_runs,check_suites=get_all_checks(repo,dic[name][number]["commit_id"])
                dic[name][number]["check_runs"]=check_runs
                dic[name][number]["check_suites"]=check_suites
            except RateLimitExceededException as e:
                error.append((path, number))
                wait(index,token)

            except Exception as e:
                error.append((path, number))
                tqdm.write("再次报错")
                print(type(e))

        file = open("./data_30/pr_"+str(index)+".dic",mode='w',encoding="utf-8")
        json.dump(dic,file,ensure_ascii=False,indent=2)
        file.close()
        print (str(index)+"+done")

def merge(file,to):
    all={}
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list
        # 遍历文件
        i=0
        for f in files:
            print(f)
            path = os.path.join(root, f)
            file = open(path, mode='r', encoding="utf-8")
            dic = json.load(file)
            file.close()
            for name in dic:
                temp=all.get(name,{})
                temp.update(dic[name])
                all[name]=temp
    file = open("./"+to+".dic", mode='w', encoding="utf-8")
    json.dump(all, file, ensure_ascii=False, indent=2)
    file.close()
    return all



#['head_ref_deleted', 'review_requested', 'base_ref_force_pushed', 'closed', 'demilestoned', 'unlabeled', 'comment_deleted', 'renamed', 'milestoned', 'merged', 'head_ref_force_pushed', 'reopened', 'connected', 'ready_for_review', 'moved_columns_in_project', 'unsubscribed', 'locked', 'review_dismissed', 'referenced', 'removed_from_project', 'mentioned', 'added_to_project', 'unassigned', 'review_request_removed', 'subscribed', 'head_ref_restored', 'labeled', 'assigned', 'base_ref_changed']
def split(n):
    data=[]
    for name in old:
        for num in old[name]:
            data.append((name,num))
    data_len = len(data)
    input=[]
    index = list(range(0, len(data), int(data_len / n + 1)))
    index.append(len(data))
    input=[]

    for i in range(n):
        input.append((index[i],index[i+1]))
    print(input)

    file = open('./pr_time_file_event_reactions.dic', mode='r', encoding="utf-8")
    dic = json.load(file)
    file.close()
    for i in range(n):
        all = data[input[i][0]:input[i][1]]
        temp={}
        for name,num in all:
            temp[name]=temp.get(name,{})
            temp[name][num]=dic[name][num]
        '''
        for name,num in all:
            temp[name]= temp.get(name, {})
            temp[name][num]= {}
            temp[name][num]["commit_id"]=dic[name][num]["commit_id"]
        '''
        file = open("./data_30/pr_" + str(i+1) + ".dic", mode='w', encoding="utf-8")
        json.dump(temp, file, ensure_ascii=False, indent=2)
        file.close()


if __name__ == '__main__':

    #split(20)
    get_all_checks(repo, dic[name][number]["commit_id"])
    '''
    token = ["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", "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",
             "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", "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",
             "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", "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",
             "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", "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",
             "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", "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"]


    mul=20
    pool = ThreadPool(processes=mul)


    for name in old:
        for num in old[name]:
            data.append((name,num))
    data_len=len(data)

    index=list(range(0, len(data), int(data_len/mul+1)))
    input=[]
    index.append(len(data))


    for i in range(mul):
        input.append((i+1,index[i],index[i+1],token[i%int(mul/2)]))
    print(input)
    pool.map(get_pr,input)
    
    pool.close()
    pool.join()
    '''






