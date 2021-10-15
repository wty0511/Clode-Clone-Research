from tqdm import tqdm
from git import Git
import os
import  pandas as pd
import json
def walkFile(file):
    i=0
    dic={}
    save_to=''
    #f = open(code_file,mode='r',encoding="utf-8")
    #dic=json.load(f)
    #f.close()
    #f = open('./buchong.txt', mode='r', encoding="utf-8")
    #skip=[x.strip('\n') for x in f.readlines()]
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
            prject_name=f.split('_')[0]
            path="../data/allcode/"+prject_name
            g=Git(path)
            i+=1
            print(i)
            if i<=0:continue
            code_list=[]
            for tup in df.itertuples():
                l=tup[1].split('+')
                if (len(l)!=2):
                    print(tup)
                    continue
                code_list.append(l[0]+"+"+tup[2])
                code_list.append(l[1] + "+" + tup[2])
            code_list=list(set(code_list))
            code_list.sort()
            temp=dic.get(prject_name,{})
            for item in tqdm(code_list):
                if item in['src/test/java/com/nhn/hippo/testweb/repository/MemberDaoIbatisTest.java^33^47+f4adcaa',
                    'src/test/java/com/nhn/hippo/testweb/repository/MemberDaoHibernateTest.java^33^47+f4adcaa',
                    'src/test/java/com/nhn/hippo/testweb/repository/MemberDaoJdbcTest.java^33^47+f4adcaa']:continue
                #if item not in  skip:
                #    continue
                try:
                    f=item.split("+")

                    file_path,line_start,line_end=f[0].split('^')
                    commit_id=f[1]
                    code=g.execute('git show '+commit_id+ ':'+file_path).split('\n')
                    #print('\n'.join(code[int(line_start) - 1:int(line_end)]))
                    temp[item]='\n'.join(code[0:max(0,int(line_start)-1)]).encode('utf-8').decode('utf-8')

                except Exception as e:
                    print(e)
            dic[prject_name]=temp

            file = open(save_to, mode='w', encoding="utf-8")
            json.dump(dic, file, ensure_ascii=False, indent=2)
            file.close()

def main():
    walkFile("../data/genealogy")


if __name__ == '__main__':
    main()
