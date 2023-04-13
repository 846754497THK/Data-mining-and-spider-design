# ————————————————————————————————————————————————各类库调用——————————————————————————————————————————————————
import pandas as pd
import re
import jieba

#—————————————————————————————————————————————导入爬取的数据集————————————————————————————————————————

df=pd.read_csv('E:\学习\大二下\数据挖掘\课程设计\\film_review.csv')
df1=df.iloc[:,-1]

#———————————————————————————————————————————————标签重定义————————————————————————————————————————————

#正面,标记为 1
df1.loc[df1=='力荐']='1'
df1.loc[df1=='推荐']='1'
#中性，标记为 0
df1.loc[df1=='还行']='0'
#负面，标记为 -1
df1.loc[df1=='较差']='-1'
df1.loc[df1=='很差']='-1'

df0=df.iloc[:,1:-1]
df=pd.concat([df0,df1],axis=1)

#——————————————————————————————————————————去除符号、单字母、切割文本——————————————————————————————————————————
def remove_fuhao(e):
    
    a=re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+',e,re.S)
    a="".join(a)
    return a

def remove_letter(new_short):

    return re.sub(r'[a-zA-Z]+', '', new_short)

def cut_word(text):
    
    text = jieba.cut(str(text))
    return ' '.join(text)

#依据以上三个自定义函数为依据创建新一列
df2 = df['content'].apply(remove_fuhao).apply(remove_letter).apply(cut_word)


# ————————————————————————————————————————————删除停用词————————————————————————————————————————
#读取停用词表函数
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

# 将短评中的停用词删去
def sentence_div(text):
    
    # 将短评按空格划分成单词并形成列表
    sentence = text.strip().split()
    # 加载停用词的路径
    stopwords = stopwordslist(r'中文停用词表.txt')
    #创建一个空字符串
    outstr = ' '
    # 遍历短评列表中每个单词
    for word in sentence:
        if word not in stopwords: # 判断词汇是否在停用词表里
            if len(word) > 1:  # 单词长度要大于1
                if word != '\t':  # 单词不能为tab
                    if word not in outstr:  # 去重：如果单词在outstr中则不加入
                        outstr += ' '  # 分割
                        outstr += word # 将词汇加入outstr

    #返回字符串
    return outstr

df3= df2.apply(sentence_div)
data=pd.concat([df3,df1],axis=1)

#——————————————————————————————————————————————去重去空——————————————————————————————————————————
data=data[~data['content'].isin([' '])]

data=data.dropna()

data=data.drop_duplicates('content')


#——————————————————————————————————————————————保存清洗后的文件————————————————————————————————
data.to_csv('sample.csv',encoding="utf_8_sig",index=False)



