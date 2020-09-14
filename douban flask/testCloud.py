import jieba                            #分词
from matplotlib import pyplot as plt    #绘图，数据可视化
from wordcloud import WordCloud         #词云
from PIL import Image                   #图片处理
import numpy as np                      #矩阵运算
import  sqlite3                         #数据库操作

#准备词云所需的文本
con = sqlite3.connect('movie.db')
cur = con.cursor()
sql = 'select introduction from movie250'
data = cur.execute(sql)
text = ""
for item in data:
    text = text + item[0]
    # print(item[0])
cur.close()
con.close()

#分词
cut = jieba.cut(text)
string = ' '.join(cut)
print(len(string))

#绘图
img = Image.open(r'.\static\assets\img\tree.jpg')#打开图片
img_array = np.array(img)
wc = WordCloud(
    background_color='white',
    mask = img_array,
    font_path="STHUPO.TTF" #字体所在位置C:\Windows\Fonts
)
wc.generate_from_text(string)


#绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')


# plt.show()
plt.savefig(r'.\static\assets\img\word.jpg',dpi=500)





