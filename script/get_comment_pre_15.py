import json
import re
import numpy as np
from random import randint, sample
import pandas as pd
def check(l):
    str='\n'.join(l)


    if "/*" not in str and "*/" in str:
        return True
    return False

def add(name,key,l):
    str = '\n'.join(l)
    if "/*" in '\n'.join(l) and "*/" not in str:
        file = open("../data/code.dic", mode='r', encoding="utf-8")
        dic = json.load(file)
        file.close()
        dic[name][key]='\n'.join(l)+dic[name][key]

        file = open('../data/code.dic', mode='w', encoding="utf-8")
        json.dump(dic, file, ensure_ascii=False, indent=2)
        file.close()



def collect_comment_pr_15():
    #读取前15行代码的dic
    file_path='../data/code_pre_15.dic'
    save_to=''
    code3 = re.compile(
        r"<code>[\s\S]*?</code>")
    file = open(file_path, mode='r', encoding="utf-8")
    dic = json.load(file)
    file.close()

    test = []
    # casexxx ://xxx
    case_line = re.compile(r"case[ ]+[a-zA-Z\d_]+[ ]*:[ ]*//")
    # }结尾后面可以有"//"注释
    close_curly_end = re.compile(r"\}(?:[ \t\r])*(?://[\s\S]*)*$")
    #含有@
    annotation = re.compile(r"^@[\s\S]*$")
    #空行
    empty_line = re.compile(r"^[ \t\r]*$")
    #类或者函数
    fun_class = re.compile(r"(?:public|private|protect| class |void|^[ ]*class)")
    #{
    start_curly = re.compile(r"\{[ \t\r]*(?://[\s\S]*){0,1}$")
    #最后一个分号
    last_semicolon = re.compile(r";([ \t\r])*(//[\s\S]*)*$")
    #star
    star=re.compile(r"^[\t ]*\*")
    single_line = re.compile(r'//.*(?<!;)[\n]')
    multi_line = re.compile(r'/\*+[\s\S]*?\*+/')
    c_dic={}
    for name in dic:
        c_dic[name]={}
        for key in dic[name]:
            c_dic[name][key] = {}
            c_dic[name][key]["multi_line"] = []
            c_dic[name][key]["single_line"] = []
            #dfdf=dic[name][key].split('\n')
            #all_str='\n'.join(dfdf[-15:])
            #前15行代码


            my_l=[]
            #去掉空行
            for item in dic[name][key].split('\n'):
                if len(empty_line.findall(item))>0:
                    continue
                my_l.append(item)

            l=my_l
            flag=0

            #找前一个分号并跳过@Test
            for j in range(len(my_l)):
                if (len(last_semicolon.findall(my_l[j]))>0 and len(star.findall((my_l[j])))==0):
                    flag=1
                    l=my_l[min(len(my_l),j+1):]
            all_str = '\n'.join(l)
            #至少有注释的痕迹
            if ("//" in all_str or "*/" in all_str or "/*" in all_str):
                if "@Test" in all_str:
                    pass
                    #test.append(all_str)
                #前面紧邻分号不管
                if len(l)==0:
                    pass

                #紧邻case
                elif len(case_line.findall(l[-1]))>0:
                    l=l[-1]


                #紧邻}结束不管
                elif len(close_curly_end.findall(l[-1]))>0 and len(star.findall((l[-1])))==0:
                    l=[]


                #public class
                elif len(fun_class.findall('\n'.join(l)))>0:
                    tok=0
                    is_found = 0
                    for k in range(len(l)):
                        if len(close_curly_end.findall(l[k])) > 0 and len(star.findall((l[k])))==0:
                            tok=k
                            is_found = 1
                    if is_found:
                        l = l[tok + 1:]



                #@xxxx
                elif len(annotation.findall(l[-1]))>0:

                    tok=0
                    is_found=0
                    for k in range(len(l)):
                        if len(close_curly_end.findall(l[k]))>0 and len(star.findall((l[k])))==0:
                            tok=k
                            is_found=1
                    if is_found:
                        l = l[tok + 1:]

                    tok = 0
                    for k in range(len(l)):
                        if len(start_curly.findall(l[k]))>0:
                            tok=k
                    l = l[tok:]


                else:
                    #{位置
                    p = []
                    #}位置
                    t = []
                    # 找外层{
                    for s in range(len(l)):
                        if len(start_curly.findall(l[s])) > 0:
                            p.append(s)
                            if ("}")in l[s]:
                                t.append(s)

                    # 找最后一个}


                    for k in range(len(l)):
                        if len(close_curly_end.findall(l[k])) > 0 and len(star.findall((l[k])))==0:
                            t.append(k)
                    if len(t)>0 and len(p)>0:
                        if (len(p)>=2):
                            if t[-1]>=p[-1]:
                                l=l[min(t[-1]+1,len(l)):]
                            elif t[-1]==p[-2] and t[-1] < p[-1]:

                                l = l[t[-1]:]

                            elif t[-1] > p[-2] and t[-1] == p[-1]:

                                l = l[t[-1]:]

                            elif t[-1]>p[-2] and t[-1] < p[-1]:
                                l = l[min(t[-1] + 1, len(l)):]
                            elif t[-1] < p[-2]:
                                l = l[p[-2]:]
                        elif t[-1]>p[-1]:
                            l = l[min(t[-1] + 1, len(l)):]
                        elif t[-1]==p[-1]:
                            line=l[t[-1]]
                            #print(line)
                            if line.index("{")>line.index("}"):
                                l = l[p[-1]:]
                            else:
                                l = l[min(t[-1] + 1, len(l)):]
                        elif t[-1]<p[-1]:
                            l = l[p[-1]:]

                    elif len(t)==0 and len(p)!=0:
                        l=l[p[-1]:]
                    elif len(t) != 0 and len(p) == 0:
                        l = l[min(t[-1]+1,len(l)):]
                    else:
                        pass
                #* / 1
            str = '\n'.join(l)




            if check(l):
                if "\"*/" not in '\n'.join(l):
                    for i in range(len(my_l)-1,-1,-1):
                        if "/*" in my_l[i]:

                            l=my_l[i:]
                            break





            str = '\n'.join(l)
            str = re.sub(code3, "", str)

            c_dic[name][key]["multi_line"] = multi_line.findall(str)
            c_dic[name][key]["single_line"] = single_line.findall(str)

            for i in c_dic[name][key]["multi_line"]:
                str=str.replace(i," ")

            for i in c_dic[name][key]["single_line"]:
                str = str.replace(i," ")
            if "@Test" in str:
                c_dic[name][key]["dicard"] = True
            else:
                c_dic[name][key]["dicard"] = False


    #file = open(save_to, mode='w', encoding="utf-8")
    #json.dump(c_dic, file, ensure_ascii=False, indent=2)
    #file.close()
collect_comment_pr_15()