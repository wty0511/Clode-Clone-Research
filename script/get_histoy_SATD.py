from tqdm import tqdm
from git import Git
import os
import pandas as pd
import filetype
import mimetypes
import re
import json


f = open('../data/code_comment(SATD).dic', mode='r', encoding="utf-8")
dic2 = json.load(f)
f.close()
result={}
save_to=''
for name in dic2:
    print(name)
    result[name] = {}



    path = "../data/allcode/" + name
    g = Git(path)
    for key in tqdm(dic2[name]):
        result[name][key] = {}
        code_list = {}
        if len(dic2[name][key]["SATD"]) == 0: continue

        for SATD in set(dic2[name][key]["SATD"]):
            print(SATD)
            result[name][key][SATD] = {}
            commit_id = key.split("+")[1]
            filepath = key.split("^")[0]

            branch = g.execute("git branch --contains " + commit_id + " --all")
            branch = branch.split('\n')


            for b in branch:
                if " -> "in b:
                    continue
                if b[0]=="*":
                    continue
                print(b)
                result[name][key][SATD][b] = {}
                result[name][key][SATD][b]["add"] = []
                #last_commit = g.execute("git log -1 " + b + " --pretty=format:\"%H\"")
                first_commit = g.execute("git log -1 " + commit_id + " --pretty=format:\"%H\"")
                #print(last_commit)
                print(first_commit)

                history = g.execute("git log -p " + first_commit + ' ' + b + " -- "+filepath)
                l = re.split(r'commit (?=[\da-zA-Z]{40}\nAuthor:)', history)
                first_commit = ""
                for i in l[1:]:
                    lines = i.split("\n")
                    commit_id_local = lines[0]
                    author = lines[1]
                    date = lines[2]
                    filepath_local = ""
                    for line in lines:

                        if "+++ b/" in line:
                            filepath_local = line.replace("+++ b/", "")

                            break
                    code = g.execute('git show ' + commit_id_local + ':' + filepath_local)
                    if SATD in code:
                        print("add")
                        result[name][key][SATD][b]["add"].append(commit_id_local)


    file = open(save_to, mode='w', encoding="utf-8")
    json.dump(result, file, ensure_ascii=False, indent=2)
    file.close()


