# ————————————————————————————————————————————————各类库调用——————————————————————————————————————————
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import cross_val_score

import jieba
import numpy as np
from PIL import Image
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
from collections import Counter

df=pd.read_csv('E:\学习\大二下\数据挖掘\课程设计\\sample.csv')


X=df.iloc[:,0]
y=df.iloc[:,1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33,random_state=88)


#————————————————降维，特征提取————————————
max_df=1200
min_df=3
vec=CountVectorizer(max_df=max_df,min_df=min_df)

X_train=vec.fit_transform(X_train)

#——————————————————————————————————朴素贝叶斯——————————————————————————————————————————————
#使用贝叶斯预测分类
clf0 = MultinomialNB()
#交叉验证的准确率
cross_result=cross_val_score(clf0,X_train,y_train,cv=5,scoring='accuracy').mean()
print('交叉验证的准确率：'+str(cross_result))

#进行预测
clf0.fit(X_train,y_train)
y_pred = clf0.predict(vec.transform(X_test))

#准确率测试
accuracy=metrics.accuracy_score(y_test,y_pred)
print('准确率：'+str(accuracy))

#混淆矩阵
print('混淆矩阵：'+str(metrics.confusion_matrix(y_test,y_pred)))

#——————————————————————重新组合——————————————
X_test=list(X_test)
X_test=pd.DataFrame(X_test)

y_test=list(y_test)
y_test=pd.DataFrame(y_test)

y_pred=pd.DataFrame(y_pred)
x_true=pd.concat([X_test,y_test],axis=1)
x_pre=pd.concat([X_test,y_pred],axis=1)

x_true.columns=['content','score']
x_pre.columns=['content','score']

#—————————————————————整理划分————————————————————————
#选取标签为1（正面）的
x_true1=x_true[x_true['score'].isin(['1'])]
x_true1=x_true.iloc[:,0]

x_pre1=x_pre[x_pre['score'].isin(['1'])]
x_pre1=x_pre.iloc[:,0]

cut_text1="".join(x_true1)
cut_text2="".join(x_pre1)

#选取标签为0（中性）的
x_true2=x_true[x_true['score'].isin(['0'])]
x_true2=x_true.iloc[:,0]

x_pre2=x_pre[x_pre['score'].isin(['0'])]
x_pre2=x_pre.iloc[:,0]

cut_text3="".join(x_true2)
cut_text4="".join(x_pre2)

#选取标签为-1（负面）的
x_true3=x_true[x_true['score'].isin(['-1'])]
x_true3=x_true.iloc[:,0]

x_pre3=x_pre[x_pre['score'].isin(['-1'])]
x_pre3=x_pre.iloc[:,0]

cut_text5="".join(x_true3)
cut_text6="".join(x_pre3)

#———————————————————————————————画出词云————————————————————
#词云函数
def word_cloud(name,cut_text):
    
    img="E:\学习\大二下\数据挖掘\课程设计\\timg.jpg"
    background_image=np.array(Image.open(img))
    wordcloud=WordCloud(
        font_path="C:/Window/Fonts/simfang.ttf",
        background_color="white",
        mask=background_image
        ).generate(cut_text)

    plt.imshow(wordcloud,interpolation="bilinear")
    plt.axis("off")
    plt.show()
    wordcloud.to_file(name+".png")

print('贝叶斯实际分类与预测分类词云图（正面）：\n')
word_cloud('正面(实际)',cut_text1)
word_cloud('正面(预测)',cut_text2)

print('贝叶斯实际分类与预测分类词云图（中性）：\n')
word_cloud('中性(实际)',cut_text3)
word_cloud('中性(预测)',cut_text4)

print('贝叶斯实际分类与预测分类词云图（负面）：\n')
word_cloud('负面(实际)',cut_text5)
word_cloud('负面(预测)',cut_text6)
































