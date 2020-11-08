import jieba
from os import path
from PIL import Image
import numpy as  np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.font_manager as fm
from ImageProcessing import set_delimiter, INPUT_DIR,OUTPUT_DIR




if __name__ == '__main__':
    bg = np.array(Image.open(set_delimiter(INPUT_DIR, "1.jpg")))
    stopwords_path = set_delimiter(INPUT_DIR,'stopwords\\scu_stopwords.txt')
    jieba.add_word("侯亮平")
    # 读取要分析的文本，读取格式
    text = open(set_delimiter(INPUT_DIR, "userdict.txt"), encoding="utf8").read()


    # 定义个函数式用于分词
    def jiebaclearText(text):
        # 定义一个空的列表，将去除的停用词的分词保存
        mywordList = []
        # 进行分词
        seg_list = jieba.cut(text, cut_all=False)
        # 将一个generator的内容用/连接
        listStr = '/'.join(seg_list)
        # 打开停用词表
        f_stop = open(stopwords_path, encoding="utf8")
        # 读取
        try:
            f_stop_text = f_stop.read()
        finally:
            f_stop.close()  # 关闭资源
        # 将停用词格式化，用\n分开，返回一个列表
        f_stop_seg_list = f_stop_text.split("\n")
        # 对默认模式分词的进行遍历，去除停用词
        for myword in listStr.split('/'):
            # 去除停用词
            if not (myword.split()) in f_stop_seg_list and len(myword.strip()) > 1:
                mywordList.append(myword)
        return ' '.join(mywordList)


    text1 = jiebaclearText(text)

    # 生成
    wc = WordCloud(
        background_color="white",
        max_words=150,
        mask=bg,  # 设置图片的背景
        max_font_size=60,
        random_state=42,
        font_path='C:/Windows/Fonts/simkai.ttf'  # 中文处理，用系统自带的字体
    ).generate(text1)
    # 为图片设置字体
    my_font = fm.FontProperties(fname='C:/Windows/Fonts/simkai.ttf')
    # 产生背景图片，基于彩色图像的颜色生成器
    image_colors = ImageColorGenerator(bg)
    # 开始画图
    plt.imshow(wc, interpolation="bilinear")
    # 为云图去掉坐标轴
    plt.axis("off")
    # 画云图，显示
    # plt.figure()
    plt.show()
    # 为背景图去掉坐标轴
    plt.axis("off")
    plt.imshow(bg, cmap=plt.cm.gray)
    # plt.show()

    # 保存云图
    wc.to_file(set_delimiter(OUTPUT_DIR, 'new.png'))