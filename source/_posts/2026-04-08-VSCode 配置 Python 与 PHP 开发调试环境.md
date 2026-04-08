---
title: VSCode 配置 Python 与 PHP 开发调试环境
date: 2026-04-08T12:00:00+08:00
categories:
  - 安全工具
tags:
  - 工具
---

# VSCode 配置 Python 与 PHP 开发调试环境 

---

## ✅ 一、准备工作

### 🧩 安装 VSCode

- 官网下载：https://code.visualstudio.com  
- 安装建议勾选：  
  - 添加到右键菜单  
  - 将 VSCode 添加到 PATH  

### 🧩 安装插件（扩展）

打开 VSCode → 左侧扩展（插件）图标 → 搜索并安装以下插件：

| 插件名称             | 作者         | 作用说明                                                     |
| -------------------- | ------------ | ------------------------------------------------------------ |
| **Python**           | Microsoft    | 提供 Python 开发环境支持，包括运行、调试、Linter 等          |
| **Pylance**          | Microsoft    | 提供 Python 代码补全、类型推导、高亮、错误提示等（推荐与 Python 搭配） |
| **Python Debugger**  | Microsoft    | Python 调试支持（一般自动随 Python 插件一起装）              |
| **PHP**              | DEVSENSE     | 提供 PHP 语法高亮和基础支持                                  |
| **PHP Debug**        | Felix Becker | 支持通过 Xdebug 进行 PHP 脚本调试                            |
| **PHP Intelephense** | Ben Mewburn  | 强大的 PHP 智能提示、跳转、格式检查等（推荐）                |
| **PHP IntelliSense** | DEVSENSE     | PHP 补全与参数提示（和 Intelephense 功能重合，可选）         |
| **Code Runner**      | Jun Han      | 通过快捷键一键运行 Python/PHP/JS 等代码                      |

> ✅ 推荐组合：`PHP + PHP Debug + PHP Intelephense` + `Python + Pylance + Python Debugger`

---

## ✅ 二、配置 Python 开发环境

### 🐍 步骤 1：安装 Python

- 官网下载：https://www.python.org/downloads/  
- 安装时务必勾选：**Add Python to PATH**

### 🐍 步骤 2：VSCode 设置 Python 路径

VSCode 会自动识别系统中已安装的 Python，  
但可以通过以下方式手动指定默认解释器：

快捷键 `Ctrl+Shift+P` → 输入 `Python: Select Interpreter` → 选择你希望默认使用的版本。

或者在 `settings.json` 中添加：

```jsonc
"python.defaultInterpreterPath": "C:/路径/python.exe"
```

### 🐍 步骤 3：运行 Python 脚本

创建 `hello.py`：

```python
print("Hello, VSCode + Python!")
```

按 `Ctrl + Alt + N`（Code Runner 快捷键）运行。

### 🐍 步骤 4：Python 调试配置

1. 打开左侧“运行和调试”面板  
2. 创建 `launch.json`，选择 Python  

示例配置：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: 当前文件",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    }
  ]
}
```

---

## ✅ 三、配置 PHP 开发环境

### 🐘 步骤 1：准备 PHP 环境

使用 phpStudy（或其它 PHP 安装包）

假设你路径如下：

```
D:/Mytools/Web_tools/Comprehensive_Tools/phpStudy/PHPTutorial/php/php-7.1.13-nts
```

### 🐘 步骤 2：配置 VSCode 设置 `settings.json`

快捷键 `Ctrl+Shift+P` → 输入 `Open Settings (JSON)` → 粘贴以下内容：

```jsonc
{
  "[python]": {
    "diffEditor.ignoreTrimWhitespace": false,
    "editor.defaultColorDecorators": "never",
    "editor.formatOnType": true,
    "editor.wordBasedSuggestions": "off"
  },

  "[php]": {
    // PHP 调试使用的 php.exe 路径
    "php.debug.executablePath": "D:/Mytools/Web_tools/Comprehensive_Tools/phpStudy/PHPTutorial/php/php-7.1.13-nts/php.exe",
    // PHP 语法校验的 php.exe 路径
    "php.validate.executablePath": "D:/Mytools/Web_tools/Comprehensive_Tools/phpStudy/PHPTutorial/php/php-7.1.13-nts/php.exe",
    // PHP 运行时的 php.exe 路径
    "php.executablePath": "D:/Mytools/Web_tools/Comprehensive_Tools/phpStudy/PHPTutorial/php/php-7.1.13-nts/php.exe"
  },

  // Code Runner 运行 PHP/python 代码时使用的路径，防止找不到 php/python
  "code-runner.executorMap": {
    "php": "\"D:/Mytools/Web_tools/Comprehensive_Tools/phpStudy/PHPTutorial/php/php-7.1.13-nts/php.exe\"",
    "python": "D:/Mytools/Python_path/python39/python39.exe"
  },
    "code-runner.runInTerminal": true,//让code-runner插件启动运行在系统终端
    "code-runner.clearPreviousOutput": true,
    "python.createEnvironment.trigger": "off",
}
```

### 🐘 步骤 3：安装和启用 Xdebug

1. 查看 PHP 扩展目录：

```
D:/Mytools/Web_tools/Comprehensive_Tools/phpStudy/PHPTutorial/php/php-7.1.13-nts/ext
```

2. 下载匹配版本的 Xdebug：https://xdebug.org/download  
   - 例如版本：php_xdebug-2.5.5-7.1-vc14-nts.dll  
   - 下载后改名为 `php_xdebug.dll`  
3. 把 `php_xdebug.dll` 放入 `ext/` 目录

### 🐘 步骤 4：配置 `php.ini`

打开：

```
D:/Mytools/Web_tools/Comprehensive_Tools/phpStudy/PHPTutorial/php/php-7.1.13-nts/php.ini
```

末尾添加：

```ini
[xdebug]
zend_extension="D:/Mytools/Web_tools/Comprehensive_Tools/phpStudy/PHPTutorial/php/php-7.1.13-nts/ext/php_xdebug.dll"
xdebug.remote_enable=1
xdebug.remote_autostart=1
xdebug.remote_host=127.0.0.1
xdebug.remote_port=9000
xdebug.remote_handler=dbgp
xdebug.idekey=VSCODE
```

✅ 保存后，重启 Apache/Nginx。

### 🐘 步骤 5：调试配置 `launch.json`

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Listen for Xdebug",
      "type": "php",
      "request": "launch",
      "port": 9000,
      "log": true,
      "pathMappings": {
        "/": "D:/Mytools/Web_tools/Comprehensive_Tools/phpStudy/PHPTutorial/WWW"
      }
    }
  ]
}
```

`pathMappings` 的作用是将服务器路径 `/` 映射到本地项目目录，确保调试器正确定位文件。

---

## ✅ 四、网页中断点调试（GET / POST 支持）

### 🌐 示例 test.php：

```php
<?php
$name = isset($_GET['name']) ? $_GET['name'] : 'Guest';
$age = isset($_POST['age']) ? $_POST['age'] : 'Unknown';
echo "你好，{$name}，你的年龄是 {$age}";
```

### 🌐 浏览器访问方式

- GET 请求示例：

```
http://localhost/mydebugtest/test.php?name=张三
```

- POST 表单示例：

```html
<form method="post" action="test.php?name=李四">
  <input name="age" value="25">
  <input type="submit" value="提交">
</form>
```

### 🌐 调试流程

1. 在 VSCode 启动“Listen for Xdebug”调试配置  
2. 在 `test.php` 中设置断点  
3. 浏览器访问 URL 或提交表单  
4. VSCode 自动中断，进入调试状态  

---

## 🛠️ 配置中遇到的问题与解决方案

### 问题 1：运行 PHP 脚本时报错 `'php' 不是内部或外部命令`

- **原因**：Code Runner 默认使用系统 PATH 下的 `php`，但系统没配置。  
- **解决方案**：在 `settings.json` 中显式配置 `code-runner.executorMap` 的 PHP 路径，指向你安装的 php.exe。

### 问题 2：Xdebug 未启用，无法调试

- **原因**：PHP 没正确加载 Xdebug 扩展。  
- **解决方案**：  
  - 下载对应版本的 `php_xdebug.dll`，放入 `ext` 目录  
  - 修改 `php.ini` 加载该扩展  
  - 重启服务，运行命令 `php -i | findstr xdebug` 验证  

### 问题 3：网页访问 PHP 文件未触发断点

- **原因**：`launch.json` 中 `pathMappings` 配置不正确，调试器无法对应文件路径。  
- **解决方案**：  
  - 确认 `pathMappings` 配置正确映射了本地项目绝对路径  
  - 确认 VSCode 中调试监听已启动，浏览器访问路径正确  

### 问题 4：Notice: Undefined variable: name

- **原因**：代码中访问了未定义的变量。  
- **解决方案**：使用 `isset()` 或 Null 合并操作符 `??` 进行安全处理，避免未定义变量错误。

---

## ✅ 五、总结

| 功能                 | Python | PHP  | 说明                                |
| -------------------- | ------ | ---- | ----------------------------------- |
| 编辑 / 补全          | ✅      | ✅    | 默认插件支持 + Pylance/Intelephense |
| 代码运行             | ✅      | ✅    | Code Runner + settings 配置路径     |
| 命令行调试           | ✅      | ✅    | `launch.json` 配置启动              |
| 网页调试             | ❌      | ✅    | 依赖 Xdebug 和 `pathMappings`       |
| 表单调试（GET/POST） | ❌      | ✅    | 浏览器 + Xdebug 实现                |

---

## 附录：你的最终 `settings.json` 配置示例

```json
{
    "[python]": {
        "diffEditor.ignoreTrimWhitespace": false,
        "editor.defaultColorDecorators": "never",
        "editor.formatOnType": true,
        "editor.wordBasedSuggestions": "off"
    },

    "[php]":{
        "php.debug.executablePath": "D:/Mytools/Web_tools/Comprehensive_Tools/phpStudy/PHPTutorial/php/php-7.1.13-nts/php.exe",
        "php.validate.executablePath": "D:/Mytools/Web_tools/Comprehensive_Tools/phpStudy/PHPTutorial/php/php-7.1.13-nts/php.exe",
        "php.executablePath": "D:/Mytools/Web_tools/Comprehensive_Tools/phpStudy/PHPTutorial/php/php-7.1.13-nts/php.exe"
    },
        // 设置 Code Runner 的 PHP 路径，方便“运行代码”
    "code-runner.executorMap": {
        "php": "\"D:/Mytools/Web_tools/Comprehensive_Tools/phpStudy/PHPTutorial/php/php-7.1.13-nts/php.exe\"",
        "python": "D:/Mytools/Python_path/python39/python39.exe"

    },
    "code-runner.runInTerminal": true,//让code-runner插件启动运行在系统终端
    "code-runner.clearPreviousOutput": true,
    "python.createEnvironment.trigger": "off",

}
```