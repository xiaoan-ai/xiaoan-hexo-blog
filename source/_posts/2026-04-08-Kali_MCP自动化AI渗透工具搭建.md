---
title: Kali_MCP自动化AI渗透工具搭建
date: 2026-04-08T12:00:00+08:00
categories:
  - 安全工具
tags:
  - 工具
---

## 1.下载配置MCP-Kali-Server项目

### 1.1 MCP操作服务端（kali虚拟机）中启动kali_server MCP服务端

```shell
git clone https://github.com/Wh0am123/MCP-Kali-Server.git

cd MCP-Kali-Server

python3 kali_server.py

└─# python3 kali_server.py                                                                            
2025-06-20 05:44:23,998 [INFO] Starting Kali Linux Tools API Server on port 5000
 * Serving Flask app 'kali_server'
 * Debug mode: off
2025-06-20 05:44:24,062 [INFO] WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.                                                       
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.42.130:5000
2025-06-20 05:44:24,062 [INFO] Press CTRL+C to quit
```

## 2.下载配置MCP桌面项目（claude for desktop或者5ire）

**以5ire为例**

### 2.1 客户端（windows物理主机）下载安装5ire

```
git clone https://github.com/nanbingxyz/5ire
```

然后安装启动

### 2.2 配置MCP操作服务端

5ire中，工具--->右上角添加本地（Local）填写服务端内容

**此处注意：**是配置MCP的客户端，这里专为kali设计，所以windows中也需要下载该项目，并将mcp_server.py路径填写到如下位置

命令

```shell
python311 D:\xx\xx\xx\MCP-Kali-Server\mcp_server.py --server http://192.168.42.130:5000
```

```json
{
  "name": "kali_mcp",
  "key": "kali",
  "command": "python311",
  "args": [
    "D:\xx\xx\xx\MCP-Kali-Server\mcp_server.py",
    "--server",
    "http://192.168.42.130:5000"
  ]
}
```

![image-20250620174359080](/images/notes/Kali_MCP自动化AI渗透工具搭建/images/image-20250620174359080.png)

配置完成，保存并启动该工具（**需要kali中的kali_server.py先启动**）

![image-20250620174835027](/images/notes/Kali_MCP自动化AI渗透工具搭建/images/image-20250620174835027.png)

## 3. 配置AI大模型

### 3.1 本地Ollama

启动本地Ollama

![image-20250620174958017](/images/notes/Kali_MCP自动化AI渗透工具搭建/images/image-20250620174958017.png)

之后，5ire中，空间---》服务商中Ollama项中已经自动 扫描到了本地 启动的Ollma中的大模型

![image-20250620175134054](/images/notes/Kali_MCP自动化AI渗透工具搭建/images/image-20250620175134054.png)

然后在新建对话中，选择该对话模型来源，即可开始使用

### 3.2 deepseek API

打开deepseek官网，开放api中实名认证，充值，生成api，并配置到5ire中即可

![image-20250620180458918](/images/notes/Kali_MCP自动化AI渗透工具搭建/images/image-20250620180458918.png)

![image-20250620180529292](/images/notes/Kali_MCP自动化AI渗透工具搭建/images/image-20250620180529292.png)