#导入必要的包
import requests
from bs4 import BeautifulSoup
import random
import time
import re
import jieba
import jieba.analyse as analyse
from requests.exceptions import RequestException
from wordcloud import WordCloud
from PIL import Image
import numpy as np   #科学数值计算包，可用来存储和处理大型矩阵
import PIL


user_Agent = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60', 'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0', 'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER','Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)','Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)']
jobs = ['数据挖掘', '图像算法工程师', 'java后端', '互联网产品经理']
citys = {'北京':'010', '上海':'020', '深圳':'050090', '广州':'050020', '武汉':'170020', '杭州':'070020'}
proxy=[ '121.201.38.71:3128',
	   '123.161.16.163:9797',
	   '183.196.170.247:9000',
	   '114.249.119.102:9000',
	   '58.250.21.56:3128',
	   '47.100.171.38:8080',
	   '58.220.95.35:10174',
	   '60.211.218.78:53281',
		'110.243.31.66:9999',
		'112.64.233.130:9991',
		'60.217.64.237:38829',
		'125.46.0.62:53281',
		'223.82.106.253:3128',
		'221.182.31.54:8080',
		'58.220.95.34:10174'
		]


#爬取职位URL
def get_url():
	for job in jobs:
		print("职位："+job)
		for city,cityid in citys.items():
			print("城市："+city)
			for curPage in range(0,3):
				time.sleep(random.randint(1,2))
				#发起访问请求
				url="https://www.liepin.com/zhaopin/?"+'key='+job+'&dqs='+cityid+'&curPage='+str(curPage)
				
				#返回page类
				while True:
					try:
						proxies={ 'http':'http://'+random.choice(proxy),
								 'https':'https://'+random.choice(proxy)
								}
						headers={"User-Agent":random.choice(user_Agent)}
						page=requests.get(url=url,headers=headers,proxies=proxies,timeout=10)
						page.encoding=page.apparent_encoding
						print(page)
						break
					except RequestException as e:
							 print('重新选用ip地址：')
							 print(proxies['https'])
							 time.sleep(random.randint(1,2))

				print(page.status_code)
				# 初始化 soup 对象,page.text为爬取到的带有html标签页面
				soup = BeautifulSoup(page.text,"html.parser")
				# 找到<h3>标签，实质是获取所有包含职位名称及链接的标签内容
				soup = soup.find_all("h3")
				#在每个<h3>中进行抽取链接信息
				for i in soup:
					#有些<h3>标签不包含求职信息，做简要判断
					if i.has_attr("title"):
						#抽取链接内容'
						href=i.find_all("a")[0]["href"]
						if href[0]=='/':
							href="https://www.liepin.com"+href
						filename='url\\'+job+'.txt'
						with open(filename,'a') as file_object:
							file_object.write(href+'\n')
#爬取职位要求 
def get_detail():
	for job in jobs:
		print("职位："+job)
		filename='url\\'+job+'.txt'
		with open(filename,'r') as file_object:
			lines=file_object.readlines()
		for line in lines:
			url=line	
			#time.sleep(random.randint(1,2))
			
			while True:
				try:
					proxies={ 'http':'http://'+random.choice(proxy),
							 'https':'https://'+random.choice(proxy)
							}
					headers={"User-Agent":random.choice(user_Agent)}
					page=requests.get(url=url,headers=headers,proxies=proxies,timeout=10)
					page.encoding=page.apparent_encoding
					print(page)
					break
				except RequestException as e:
						 print('重新选用ip地址：')
						 print(proxies['https'])
						# time.sleep(random.randint(1,2))
		
			soup=BeautifulSoup(page.text,"html.parser")
			#print(soup.title.string)
			try:
				soup=soup.find(name='div',attrs={'class':'content content-word'}).get_text()
				result=re.search('(要求|资格)：?(.*)',soup,re.S).group(2)
				result=result.replace(' ','').replace('\t','').replace('”','').replace('“','').replace(':','').strip()
				if result=='None':
					continue
				else:
					#print(result)
					filename='url\\'+job+'职业要求'+'.txt'
					f=open(filename,'a',encoding='utf-8')
					for x in re.split(r'(?:[；。])',result):
						if x=='':
							continue
						f.write(x.strip()+'\n')
					f.write('\n')
					f.close()
			#职位链接失效
			except AttributeError as e:
				continue


def get_keyword():
	for job in jobs:
		filename='url\\'+job+'职业要求'+'.txt'
		with open(filename,'r',encoding='utf-8') as f:
			data=f.read()
		#数据清洗-结巴分词-精确模式
		seg_list=jieba.lcut(data,cut_all=False)
		#去除停用词,单字
		stopword_file=open('url\\cn_stopwords.txt','r',encoding='utf-8')
		stopword=stopword_file.read().split('\n')
		word_list=[]
		word_num=0
		for key in seg_list:
			if key.strip() not in stopword and len(key.strip())>1:
				word_list.append(key)
				word_num+=1
		word=' '.join(word_list)
		#关键词提取-基于TF-IDF关键字提取
		filename='url\\'+job+'职业要求'+'_keyword.txt'
		keyword_file=open(filename,'w',encoding='utf-8')
		for key,value in analyse.extract_tags(word,topK=(int)(200),withWeight=True):
			keyword_file.write(key+' '+str(value)+'\n')
		keyword_file.close()
		stopword_file.close()


def get_wordcloud():
	for job in jobs:
		filename='url\\'+job+'职业要求'+'_keyword.txt'
		keyword_file=open(filename,'r',encoding='utf-8')
		keywords={}
		for line in keyword_file:
			key_frequencies=line.strip().split(' ')
			keywords[key_frequencies[0]]=float(key_frequencies[1]) 
		#自定义背景图片		
		'''image1=PIL.Image.open(r'url\\paojie.jpg')
		graph=np.array(image1)'''
		#设置词云背景，大小，字体等
		wordcloud=WordCloud(
			font_path="C:\\Windows\\Fonts\\simfang.ttf",
			background_color='white',
			width=1000,
			height=800,
			#mask=graph,
			#color_func=lambda *args, **kwargs: "black"  #所有字体为黑色
			)
		#生成词云
		wordcloud.generate_from_frequencies(keywords)
		#词云保存
		filename='url\\'+job+'_wordcloud.png'
		wordcloud.to_file(filename)


def menu():
	message = input("url爬取请输入1\n职业详情爬取请输入2\n数据清洗请输入3\n词云生成请按4\n")
	if message=='1':
		get_url()
		menu()
	elif message=='2':
		get_detail()
		menu()
	elif message=='3':
		get_keyword()
		menu()
	elif message=='4':
		get_wordcloud()
		menu()
	else:
		 return 0

menu()