import json
import re
import enchant
import Algorithmia
from random import randint, sample
import pandas as pd
from tqdm import tqdm
import numpy as np
slash_star0=re.compile(
    r'\d')
d = enchant.Dict("en_US")
f = open('../data/code_comment(SATD).dic', mode='r', encoding="utf-8")
dic = json.load(f)
f.close()
f=open('../data/html.txt','r',encoding='utf-8')
html=[x.strip('\n') for x in f.readlines()]
f.close()
f=open('../data/emoj.txt','r',encoding='utf-8')
emoj=[x.strip('\n') for x in f.readlines()]
f.close()
html_tag=re.compile(r'|'.join(html))
#double_slash=re.compile(r"^//")
#slash_star=re.compile(r"(^|\n)[ \t\r]*(?:/[\*]+|[\*]+/|\*)")

at_1=re.compile(r"[@]+[a-zA-Z\d_]*(\([\s\S]*?\)){0,1}")
at_2=re.compile(r"\{@[\s\S]*?\}")
xml_tag=re.compile(
    r'<[^<>]*?/>')
star_slash=re.compile(r"[\*]+/($|\n)")
code1 = re.compile(
    r"(?:```(?:[\s\S]*?)```)")
code2 = re.compile(
    r"(?:`(?:[\s\S]*?)`)")
# 超链接
hyperlink = re.compile(
    r"<a href=[\s\S]+?>")
comment = re.compile(
    r"<!--[\s\S]+?-->")


emjo = re.compile(r'|'.join(emoj))

file_path = re.compile(
    r"""(?:(?:[^/ ()\[\]]+/)*(?:[^/ ()\[\]])+(?:\.(?:tex|xml|git|cpp|less|x|html|scala|asciidoc|xls|db|testutils|importorder|gradle|prefab|k|tsx|out|txt|xlsx|conf|X|png|dust|jar|pdf|sh|js|groovy|json|java|properties|css|lua|yam|csv))\b)""")

package = r"(?:[a-zA-Z_][a-zA-Z\d_]*\.)+(?:[a-zA-Z\d_()]+)"

code3 = re.compile(
    r"<code>[\s\S]*?</code>")
url = re.compile(
    r"""(?:(?:http|wss|https|hdfs|gs|file|s3|gg|git|ws|mysql|protocol|scheme|inprocess|tcp|realm|content|single|ha)://[^<>\s]+|(?:http|wss|https|hdfs|gs|file|s3|gg|git|ws|mysql|protocol|scheme|inprocess|tcp|realm)://|(?:(?:(?:[^\s!@#$%^&*()_=+[\]{}\|;:'",.<>/?]+)\.)+(?:ac|ad|aero|ae|af|ag|ai|al|am|an|ao|aq|arpa|ar|asia|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|biz|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|cat|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|coop|com|co|cr|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|edu|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gov|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|info|int|in|io|iq|ir|is|it|je|jm|jobs|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mil|mk|ml|mm|mn|mobi|mo|mp|mq|mr|ms|mt|museum|mu|mv|mw|mx|my|mz|name|na|nc|net|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|org|pa|pe|pf|pg|ph|pk|pl|pm|pn|pro|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tel|tf|tg|th|tj|tk|tl|tm|tn|to|tp|travel|tr|tt|tv|tw|tz|ua|ug|uk|um|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|xn--0zwm56d|xn--11b5bs3a9aj6g|xn--80akhbyknj4f|xn--9t4b11yi5a|xn--deba0ad|xn--g6w251d|xn--hgbk6aj7f53bba|xn--hlcj6aya9esc7a|xn--jxalpdlp|xn--kgbechtv|xn--zckzah|ye|yt|yu|za|zm|zw)\b|(?:(?:[0-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}(?:[0-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]))(?:[;/][^#?<>\s]*)?(?:\?[^#<>\s]*)?(?:#[^<>\s]*)?)""")


include=re.compile(r"#include[\s\S]*?$")
punctuation = re.compile(
    r"""[`~@#$%^&*()\-_=\+\{\}\[\]|\\:;"'<>/,\.\n\r\t]""")
digit = re.compile(
    r"\d")
tag = re.compile('r(?:[a-zA-Z_][a-zA-Z\d_]*)<(?:[a-zA-Z\d_ ,\?\.\-=\*]*)>|<(?:[a-zA-Z\d_ ,\?\.\-=\*]*)>')
space=re.compile(
    r"[ ]+")
# file
str1='@return {success=1, return={funds={usd=0, rur=0, eur=0, btc=0.1, ltc=0, nmc=0}, rights={info=1, trade=1, withdraw=1}, transaction_count=1, open_orders=0, server_time=1357678428}}'
str2='* @return {success=1, return={tradeId={pair=btc_usd, type=sell, amount=1, rate=1, orderId=1234, timestamp=1234}}}'
pattern5=re.compile(r"^[ \t\r]*$")
df=pd.read_csv('../data/code_comment_label.csv',encoding="ANSI",index_col="text")
df = df.replace(np.nan, ' ', regex=True)


model_results = {
                 'text': [],
                 }
count=0
l=[]
#comment=[]
client = Algorithmia.client('sim8TuwYVwfNE1JM7+0fU8B0b331')
algo = client.algo('PetiteProgrammer/ProgrammingLanguageIdentification/0.1.3')
for name in dic:
    for key in tqdm(dic[name]):
        
        for i in range(len(dic[name][key]["single_line"])):

            dic[name][key]["single_line"][i] = re.sub(code3, "", dic[name][key]["single_line"][i])
            s=dic[name][key]["single_line"][i]
            if ";"in s:
                try:
                    dic[name][key]["single_line"][i] = df.loc[s, 'to']

                except:

                    if str1 in s:
                        dic[name][key]["single_line"][i] = dic[name][key]["single_line"][i].replace(str1,"")
                    if str2 in s:
                        dic[name][key]["single_line"][i] = dic[name][key]["single_line"][i].replace(str2,"")

                if ";" in dic[name][key]["single_line"][i]:
                    #comment.append(dic[name][key]["single_line"][i])
                    count+=1



            try:
                #dic[name][key]["single_line"][i] = re.sub(double_slash, "", dic[name][key]["single_line"][i])
                #dic[name][key]["single_line"][i] = re.sub(star_slash, "", dic[name][key]["single_line"][i])
                dic[name][key]["single_line"][i]=re.sub(html_tag, "", dic[name][key]["single_line"][i])
                dic[name][key]["single_line"][i] = re.sub(at_2, "", dic[name][key]["single_line"][i])
                dic[name][key]["single_line"][i] = re.sub(at_1, "", dic[name][key]["single_line"][i])
                dic[name][key]["single_line"][i] = re.sub(xml_tag, "", dic[name][key]["single_line"][i])
                dic[name][key]["single_line"][i] = re.sub(include, "", dic[name][key]["single_line"][i])
                dic[name][key]["single_line"][i] = re.sub(emjo, "", dic[name][key]["single_line"][i])
                dic[name][key]["single_line"][i] = re.sub(file_path, "", dic[name][key]["single_line"][i])
                dic[name][key]["single_line"][i] = re.sub(hyperlink, "", dic[name][key]["single_line"][i])
                dic[name][key]["single_line"][i] = re.sub(comment, "", dic[name][key]["single_line"][i])




                for j in re.compile(package).findall(dic[name][key]["single_line"][i]):
                    if len(re.compile(r"\([\s\S]*?\)").findall(j)) == 0:
                        dic[name][key]["single_line"][i] = dic[name][key]["single_line"][i].replace(j, "")

                dic[name][key]["single_line"][i] = dic[name][key]["single_line"][i].replace('\n', " ").replace('\r', " ").replace(
                    '\t',
                    " ")
                dic[name][key]["single_line"][i] = re.sub(tag, "", dic[name][key]["single_line"][i])
                for j in re.compile(r"""(?:[^/ ()\[\]'"“‘:]+/)+(?:[^/ ()\[\]'"“‘:]+)[/]*""").findall(
                        dic[name][key]["single_line"][i]):
                    flag = 1
                    for word in j.split('/'):
                        if (word != '' and not d.check(word)) or len(slash_star0.findall(word)) > 0 or len(word) == 1:
                            flag = 0
                    if not flag:
                        dic[name][key]["single_line"][i] = dic[name][key]["single_line"][i].replace(j, "")

                dic[name][key]["single_line"][i] = re.sub(url, "", dic[name][key]["single_line"][i])
                dic[name][key]["single_line"][i] = re.sub(punctuation, " ", dic[name][key]["single_line"][i])
                dic[name][key]["single_line"][i] = re.sub(space, " ", dic[name][key]["single_line"][i])
                dic[name][key]["single_line"][i] = re.sub(digit, "", dic[name][key]["single_line"][i])

            except Exception as e:
                pass
                #print(key)
                #print(dic[name][key]["single_line"])


        for i in range(len(dic[name][key]["multi_line"])):

            dic[name][key]["multi_line"][i] = re.sub(code3, "", dic[name][key]["multi_line"][i])
            s = dic[name][key]["multi_line"][i]
            if ";"in s:
                try:
                    dic[name][key]["multi_line"][i]=df.loc[s, 'to']
                    #print(df.loc[s, 'to'])
                except:
                    if str1 in s:
                        dic[name][key]["multi_line"][i] = dic[name][key]["multi_line"][i].replace(str1, "")
                    if str2 in s:
                        dic[name][key]["multi_line"][i] = dic[name][key]["multi_line"][i].replace(str2, "")


                if ";" in dic[name][key]["multi_line"][i]:
                    #comment.append(dic[name][key]["multi_line"][i])
                    count+=1
            try:

                #dic[name][key]["multi_line"][i] = re.sub(slash_star, "", dic[name][key]["multi_line"][i])


                dic[name][key]["multi_line"][i]=re.sub(html_tag, "", dic[name][key]["multi_line"][i])


                dic[name][key]["multi_line"][i] = re.sub(at_2, "", dic[name][key]["multi_line"][i])
                dic[name][key]["multi_line"][i] = re.sub(at_1, "", dic[name][key]["multi_line"][i])
                dic[name][key]["multi_line"][i] = re.sub(xml_tag, "", dic[name][key]["multi_line"][i])
                dic[name][key]["multi_line"][i] = re.sub(include, "", dic[name][key]["multi_line"][i])
                dic[name][key]["multi_line"][i] = re.sub(emjo, "", dic[name][key]["multi_line"][i])
                dic[name][key]["multi_line"][i] = re.sub(file_path, " ", dic[name][key]["multi_line"][i])
                dic[name][key]["multi_line"][i] = re.sub(hyperlink, " ", dic[name][key]["multi_line"][i])
                dic[name][key]["multi_line"][i] = re.sub(comment, " ", dic[name][key]["multi_line"][i])
                dic[name][key]["multi_line"][i] = re.sub(emjo, " ", dic[name][key]["multi_line"][i])


                for j in re.compile(package).findall(dic[name][key]["multi_line"][i]):
                    if len(re.compile(r"\([\s\S]*?\)").findall(j)) == 0:
                        dic[name][key]["multi_line"][i] = dic[name][key]["multi_line"][i].replace(j, "")

                dic[name][key]["multi_line"][i] =dic[name][key]["multi_line"][i].replace('\n', " ").replace('\r', " ").replace(
                    '\t',
                    " ")
                dic[name][key]["multi_line"][i] = re.sub(tag, "", dic[name][key]["multi_line"][i])
                for j in re.compile(r"""(?:[^/ ()\[\]'"“‘:]+/)+(?:[^/ ()\[\]'"“‘:]+)[/]*""").findall(
                        dic[name][key]["multi_line"][i]):
                    flag = 1
                    for word in j.split('/'):
                        if (word != '' and not d.check(word)) or len(slash_star0.findall(word)) > 0 or len(word) == 1:
                            flag = 0
                    if not flag:
                        dic[name][key]["multi_line"][i] = dic[name][key]["multi_line"][i].replace(j, "")

                dic[name][key]["multi_line"][i] = re.sub(url, "", dic[name][key]["multi_line"][i])
                dic[name][key]["multi_line"][i] = re.sub(punctuation, " ", dic[name][key]["multi_line"][i])
                dic[name][key]["multi_line"][i] = re.sub(space, " ", dic[name][key]["multi_line"][i])
                dic[name][key]["multi_line"][i] = re.sub(digit, "", dic[name][key]["multi_line"][i])
            except Exception as e:
                pass
                #print(key)
                #print(dic[name][key]["multi_line"])

        l.extend(dic[name][key]["multi_line"])
        l.extend(dic[name][key]["single_line"])

#file = open('../data/code_comment_clean.dic', mode='w', encoding="utf-8")
#json.dump(dic, file, ensure_ascii=False, indent=2)
#file.close()


#for i in set(comment):
#    print(i)
model_results["text"]=list(set(model_results["text"]))
l=list(set(l))
#pd.DataFrame(model_results).to_csv('./code_biaozhu2.csv', index=False)


'''

print("start")
t=[]
count=0
'''

