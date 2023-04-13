# ————————————————————————————————————————————各类库调用——————————————————————————————————————————————————————————
import requests
import re
#应用xpath技术
import lxml.etree as etree
import pandas as pd

#—————————————————————————————————————————————全局变量初始化————————————————————————————————————————————————————
name_list=[]
score_list=[]
date_list=[]
content_list=[]
movie_name=[]


#————————————————————————————————————————————爬取经典电影ID——————————————————————————————————————————————————————
def get_ID():
    '''
    无输入
    输出豆瓣网上的20页经典电影ID列表
    '''
    id_list=[]
    for start in range(20):
        value=start*20
        headers={
            'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64;x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    
        cookies={'cookie':'ll="118172"; bid=VUxXZWobjuY; __utmc=30149280; _vwo_uuid_v2=DCDB60CFEE83F4D4CD5227E3ACDDFA0F9|b03e374ac94c913ec34d73e505bdeb19; __gads=ID=82f927dac17b21d4:T=1594368991:S=ALNI_MbCZ0WN5sy44cXFCUCj9yMQ07udwA; __utma=30149280.683867548.1594368961.1594368961.1594377043.2; __utmz=30149280.1594377043.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ap_v=0,6.0; douban-fav-remind=1; __utmt=1; __utmb=30149280.6.6.1594378424191'}

        url="https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%BB%8F%E5%85%B8&sort=recommend&page_limit=20&page_start=0"+str(value)
    
        res=requests.get(url,headers=headers,cookies=cookies).json()
    
        for j in range(0,20):
            id_=res['subjects'][j]['id']
            id_list.append(id_)

    return id_list



#——————————————————————————————————————————解析网页结构——————————————————————————————————————————————————————————————
def get_content(id,page):
    headers={
            'User-Agent':'Mozilla/5.0(Windows NT 10.0; Win64;x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    cookies={'cookie':'ll="118172"; bid=VUxXZWobjuY; __utmc=30149280; _vwo_uuid_v2=DCDB60CFEE83F4D4CD5227E3ACDDFA0F9|b03e374ac94c913ec34d73e505bdeb19; __gads=ID=82f927dac17b21d4:T=1594368991:S=ALNI_MbCZ0WN5sy44cXFCUCj9yMQ07udwA; __utma=30149280.683867548.1594368961.1594368961.1594377043.2; __utmz=30149280.1594377043.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ap_v=0,6.0; douban-fav-remind=1; __utmt=1; __utmb=30149280.6.6.1594378424191'}
    url="https://movie.douban.com/subject/"+str(id)+"/comments?start="+str(page)+"&limit=20&sort=new_score&status=P"
    res=requests.get(url,headers=headers,cookies=cookies).text
    #使用xpath解析网页
    x=etree.HTML(res)
    
    #获取评论信息
    for i in range(1,21):
        name=x.xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/a/text()'.format(i))#text()获取文本内容
        score=x.xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/span[2]/@title'.format(i))#评论分数
        date=x.xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/span[3]/@title'.format(i))#评论日期
        m='\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'#日期格式
        #如果有人没有评分但是评论了
        try:
            match=re.compile(m).match(score[0])
        except IndexError:
            break
        if match is not None:
            date=score
            score=["null"]
            
        else:
            pass
        
        content=x.xpath('//*[@id="comments"]/div[{}]/div[2]/p/span/text()'.format(i))#评论
         
        name_list.append(str(name))
        score_list.append(str(score).strip('[]\''))
        date_list.append(str(date).strip('[\'').split(' ')[0])
        content_list.append(str(content).strip())


#———————————————————————————————————————————获取原始样本——————————————————————————————————————————————————————————————————— 
def get_sample():        
    
    ids=get_ID()
    for id in ids:
        
        for page in range(10):
            pages=page*10
            get_content(id,pages)

    infos={'name':name_list,'content':content_list,'date':date_list,'score':score_list}
    
    data=pd.DataFrame(infos,columns=['name','content','date','score'])
    
    data.to_csv('film_review.csv',encoding="utf_8_sig")#将数据保存csv文件

#——————————————————————————————————————————主函数————————————————————————
if __name__ == "__main__":
    get_sample()



