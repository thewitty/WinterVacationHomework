import requests
import stylecloud
from lxml import etree
import jieba
import re
from bs4 import BeautifulSoup
headers = {
     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'
}

# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r').readlines()]
    return stopwords

# 对句子进行分词
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('stopwords.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr
    
    

def jieba_segment(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        word_list=''
        inputs = open(file_name, 'r', encoding='utf8' )
        for line in inputs:
            line_seg = seg_sentence(line)  # 这里的返回值是字符串
            word_list +=( '\n'+ line_seg)
        inputs.close()
        
        result = word_list #已经分开就不用加了
        #word_list = jieba.cut(f.read(), cut_all=False )
        #result = " ".join(word_list)    # 分词用空格隔开
        
       #f.close()
        return result
        
        
def gen_stylecloud_byText(text_source,pic_name):
        
         stylecloud.gen_stylecloud(text=text_source,  font_path='simsun.ttc', output_name=pic_name)
         return  pic_name


def get_html(url,myheaders):
   
    try:
        html = requests.get(url,headers = myheaders)
        #html.encoding = html.apparent_encoding
        html.encoding =  'utf-8'
        if html.status_code == 200:
            print('成功获取源代码')
    except Exception as e :
        print('获取代码失败:s% ' % e)
    return html.text
    
def get():

    html = get_html(r'https://movie.douban.com/cinema/nowplaying/xian/',headers)
    #整理文档对象
    html = etree.HTML(html)
    id = html.xpath('//*[@id="nowplaying"]//li/@id')
    title = html.xpath('//*[@id="nowplaying"]//li/@data-title')

    data=list(zip(id,title))
    return data
    
    
    

def spider_comment(movie_id, page):
    comment_list = []
    #写出文件
    with open(str(movie_id) +".txt", "a+", encoding='utf-8') as f:
        for i in range(1,page+1):

            url = 'https://movie.douban.com/subject/%s/comments?start=%s&limit=20&sort=new_score&status=P' \
                  % (movie_id, (i - 1) * 20)
            #headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Mobile Safari/537.36'}
            
            text = get_html(url,headers)
            #req = requests.get(url, headers=headers)
            #req.encoding = 'utf-8'
            comments = re.findall('<span class="short">(.*)</span>', text)


            f.writelines('\n'.join(comments))
    #print(comments)
    
    
def movie_analyse(movie_id,page):
	spider_comment(movie_id, page)
	result = jieba_segment(movie_id + ".txt")
	gen_stylecloud_byText(result,str(movie_id) + ".png")
	


# 主函数
if __name__ == '__main__':
    page = 10
    '''
    movie_id = '34841067'
    #你好，李焕英
    movie_analyse(movie_id,page)
    '''
    data=get()
    
    for i in range (len(data)):
        movie_id = data[i][0]
        name=data[i][1]
        print(movie_id)
        print(name)
        movie_analyse(movie_id,page)
        
        




