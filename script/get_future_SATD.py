from tqdm import tqdm
from git import Git
import os
import  pandas as pd
import filetype
import mimetypes
import re
import gc

import json


f = open('../data/code_comment(SATD).dic', mode='r', encoding="utf-8")
dic2 = json.load(f)
f.close()
result={}
save_to=''
for name in dic2:
    print(name)
    result[name]={}
    path = "../data/allcode/" + name
    g = Git(path)
    for key in tqdm(dic2[name]):
        result[name][key]={}
        code_list={}
        if len(dic2[name][key]["SATD"])==0:continue


        for SATD in set(dic2[name][key]["SATD"]):
            print(SATD)
            result[name][key][SATD]={}
            commit_id=key.split("+")[1]
            filepath=key.split("^")[0]

            branch = g.execute("git branch --contains " + commit_id + " --all")
            branch = branch.split('\n')
            for b in branch:
                if " -> "in b:
                    continue
                if b[0]=="*":
                    continue
                print(b)
                result[name][key][SATD][b] = {}
                result[name][key][SATD][b]["delete"] = []
                last_commit=g.execute("git log -1 "+b+" --pretty=format:\"%H\"")
                first_commit = g.execute("git log -1 " + commit_id + " --pretty=format:\"%H\"")
                print(last_commit)
                print(first_commit)

                history = g.execute("git log -p "+first_commit+".."+last_commit+' '+b+" --")
                l = re.split(r'commit (?=[\da-zA-Z]{40}\nAuthor:)', history)
                for i in tqdm(l):
                    local={}
                    local_path = ""
                    lines=i.split('\n')
                    commit_local=lines[0]
                    for line in lines:

                        if len(re.findall(r'^\+\+\+',line))>0:
                            local_path='/'.join(line.split('/')[1:])
                            local[local_path]={}
                            local[local_path]["add"]=""
                            local[local_path]["delete"] = ""
                        elif len(re.findall(r'^---',line))>0:
                            pass
                        elif len(re.findall(r'^\+',line))>0:
                            pass
                            #local[local_path]["add"]+=line[1:]
                            #local[local_path]["add"] += '\n'
                        elif len(re.findall(r'^-',line))>0:
                            local[local_path]["delete"] += line[1:]
                            local[local_path]["delete"] += '\n'

                    for i in local:

                        if SATD in local[i]["delete"]:
                            if filepath in g.execute("git log -M90% -p "+commit_local+" --follow -- " +i):
                                result[name][key][SATD][b]["delete"].append(commit_local)
                                print("delete")
                                print(commit_local)
                #del history
                #del l
                #gc.collect()
    file = open(save_to, mode='w', encoding="utf-8")
    json.dump(result, file, ensure_ascii=False, indent=2)
    file.close()






