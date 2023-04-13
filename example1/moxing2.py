import gensim
from gensim.models import word2vec
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier


df=pd.read_csv('E:\学习\大二下\数据挖掘\课程设计\\sample.csv')
X=df.iloc[:,0]
y=df.iloc[:,1]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33,random_state=88)

X_train=pd.DataFrame(X_train)
X_train.columns=['content']

X_test=pd.DataFrame(X_test)
X_test.columns=['content']

# 设置输出日志
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# 直接用gemsim提供的API去读取txt文件，读取文件的API有LineSentence 和 Text8Corpus, PathLineSentences等。
sentences = word2vec.LineSentence("E:\学习\大二下\数据挖掘\课程设计\\sample1.csv")

# 训练模型，词向量的长度设置为1000， 迭代次数为8，采用skip-gram模型
model = gensim.models.Word2Vec(sentences, size=100, sg=1, iter=8)  

def to_review_vector(review):
    global word_vec
    word_vec = np.zeros((1,100))
    review=review.split()
    for word in review:
        if word in model:
            word_vec += np.array([model[word]])

    return pd.Series(word_vec.mean(axis = 0))


X_train = X_train.content.apply(to_review_vector)

X_test=X_test.content.apply(to_review_vector)


clf = GaussianNB()

cross_result=cross_val_score(clf,X_train,y_train,cv=5,scoring='accuracy').mean()
print('交叉验证的准确率：'+str(cross_result))

clf.fit(X_train,y_train)
predict=clf.predict(X_test)
f0=accuracy_score(y_test, predict)
print('准确率：',f0)


clf0 = RandomForestClassifier(n_estimators=10)

#交叉验证的准确率
cross_result=cross_val_score(clf0,X_train,y_train,cv=5,scoring='accuracy').mean()
print('交叉验证的准确率：'+str(cross_result))

#进行预测
clf0.fit(X_train,y_train)
predict1 = clf0.predict(X_test)
f1=accuracy_score(y_test, predict1)
print('准确率：',f1)




