from flask import Flask,render_template,request
import datetime
app = Flask(__name__)

#路由解析，通过用户访问的路径，匹配相应的函数
# @app.route('/')
# def hello_world():
#     return '你好'


@app.route('/index')
def index():
    return "你好"

#通过访问路径，获取用户的字符串参数
@app.route('/user/<name>')
def welcom(name):
    return "你好,%s"%name
#匹配数字（多态）
@app.route('/user/<int:id>')
def welcome2(id):
    return "你好,%d号的会员"%id

#路由路径不能重复，用户只能通过唯一路径来访问特定的函数

#返回给用户渲染后的页面
# @app.route('/')
# def index2():
#     return render_template("index.html")

#向页面传递一个变量
@app.route('/')
def index3():
    time = datetime.date.today() #普通变量
    name = ["小张","小王","小赵"]   #列表类型
    task = {"任务":"打扫卫生","时间":"3小时"}#字典类型
    return render_template("index.html",var = time,list = name,task = task)

#表单提交
@app.route('/test/regester')
def register():
    return render_template("test/register.html")

@app.route('/result',methods=['POST','GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template("test/result.html",result = result)



if __name__ == '__main__':
    app.run()
