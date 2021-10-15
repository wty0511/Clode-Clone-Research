import re
import json


code_file=''
save_to=''
f = open(code_file,mode='r',encoding="utf-8")
dic=json.load(f)
f.close()
dic2={}
for key in dic.keys():
    dic2[key]={}
    print(key)
    for item in dic[key].keys():
        dic2[key][item] = {}
        s=dic[key][item]
        pattern1 = re.compile(r'/\*+[\s\S]*?\*+/')
        result1 = pattern1.findall(s)
        pattern2 = re.compile(r'//.*(?<!;)[\n]')
        result2 = pattern2.findall(s)
        dic2[key][item]['multi_line'] = result1
        dic2[key][item]['single_line'] =result2
    file = open(save_to, mode='w', encoding="utf-8")
    json.dump(dic2, file, ensure_ascii=False, indent=2)
    file.close()