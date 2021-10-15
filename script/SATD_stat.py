import time
import json
import numpy as np
from git import Git
import re
def time_long(time1, time2, type="day"):

    day1 = time.strptime(str(time1), '%Y-%m-%d')
    day2 = time.strptime(str(time2), '%Y-%m-%d')
    if type == 'day':
        day_num = (int(time.mktime(day2)) - int(time.mktime(day1))) / (
        24 * 60 * 60)
        return abs(int(day_num))
file_history=''

f = open(file_history, mode='r', encoding="utf-8")
result1 = json.load(f)
f.close()
file_future=''
f = open(file_future, mode='r', encoding="utf-8")
result2 = json.load(f)
f.close()
merge={}
for name in result2:
    for key in result2[name]:
        g = Git("./allcode/"+name)
    
        merge[name][key]={}
        for SATD in result2[name][key]:
            merge[name][key][SATD]={}
            for b in result2[name][key][SATD]:
                add=result2[name][key][SATD][b]["add"][-1]
                r1 = g.execute("git log " + add + " -1")
                r2=None
                if len(result1[name][key][SATD][b]["delete"])>0:
                    delete = result1[name][key][SATD][b]["delete"][0]
                    filepath=""
                    history = g.execute("git log -p "+delete+' -1 '+b+" --")
    
    
                    local={}
                    local_path = ""
                    lines=history.split('\n')
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
                        elif len(re.findall(r'^-',line))>0:
                            local[local_path]["delete"] += line[1:]
                            local[local_path]["delete"] += '\n'
    
                    for i in local:
    
                        if SATD in local[i]["delete"]:
                            filepath=i
    
    
                    code = g.execute('git show ' + delete + ':' + filepath)
                    if SATD in code:
                        delete="None"
    
                    else:
                        r2 = g.execute("git log " + delete + " -1")
                else:
                    delete= "None"
    
    
    
                r1_s=r1.split('\n')
    
    
                merge[name][key][SATD][b]={}
                merge[name][key][SATD][b]["add_time"]=r1_s[2].split(":")[-1]
                merge[name][key][SATD][b]["add_author"]=r1_s[1].replace("Author: ",'')
                if delete!="None":
    
                    r2_s=r2.split('\n')
                    merge[name][key][SATD][b]["delete_time"]= r2_s[2].split(":")[-1]
                    merge[name][key][SATD][b]["delete_author"]=r2_s[1].replace("Author: ",'')
                else:
                    merge[name][key][SATD][b]["delete_time"]= "None"
                    merge[name][key][SATD][b]["delete_author"]= "None"
    
                merge[name][key][SATD][b]["deleted"]= not merge[name][key][SATD][b]["delete_time"]=="None"
                if merge[name][key][SATD][b]["delete_time"] == "None":
                    merge[name][key][SATD][b]["time_span"]="None"
                else:
                    merge[name][key][SATD][b]["time_span"] =time_long(merge[name][key][SATD][b]["add_time"],merge[name][key][SATD][b]["delete_time"])
    
                merge[name][key][SATD][b]["delete_by_author"] =merge[name][key][SATD][b]["add_author"]==merge[name][key][SATD][b]["delete_author"]

file = open('../data/SATD.dic', mode='w', encoding="utf-8")
json.dump(merge, file, ensure_ascii=False, indent=2)
file.close()


time=[]
removed=0
removed_by_author=0
all=0
for name in merge:
    for key in merge[name]:
        for SATD in merge[name][key]:
            for b in merge[name][key][SATD]:
                all+=1
                if merge[name][key][SATD][b]["time_span"]!="None":
                    time.append(int(merge[name][key][SATD][b]["time_span"]))
                if merge[name][key][SATD][b]["deleted"]:
                    removed+=1
                    if merge[name][key][SATD][b]["delete_by_author"]:
                        removed_by_author+=1
                    else:
                        print(SATD)
print(all)
print(removed)
print(removed_by_author)
print(np.mean(time))
print(np.median(time))
