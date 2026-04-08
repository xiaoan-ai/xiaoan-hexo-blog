---
title: WindowsTeiminal图片背景美化配置
date: 2026-04-08T12:00:00+08:00
categories:
  - 安全工具
tags:
  - 工具
---

```json
//setting.json
{
    "$help": "https://aka.ms/terminal-documentation",
    "$schema": "https://aka.ms/terminal-profiles-schema",
    "actions": 
    [
        {
            "command": 
            {
                "action": "copy",
                "singleLine": false
            },
            "id": "User.copy.644BA8F2"
        },
        {
            "command": "paste",
            "id": "User.paste"
        },
        {
            "command": "find",
            "id": "User.find"
        },
        {
            "command": 
            {
                "action": "splitPane",
                "split": "auto",
                "splitMode": "duplicate"
            },
            "id": "User.splitPane.A6751878"
        }
    ],
    "copyFormatting": "none",
    "copyOnSelect": false,
    "defaultProfile": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
    "keybindings": 
    [
        {
            "id": "User.copy.644BA8F2",
            "keys": "ctrl+c"
        },
        {
            "id": "User.find",
            "keys": "ctrl+shift+f"
        },
        {
            "id": "User.paste",
            "keys": "ctrl+v"
        },
        {
            "id": "User.splitPane.A6751878",
            "keys": "alt+shift+d"
        }
    ],
    "newTabMenu": 
    [
        {
            "type": "remainingProfiles"
        }
    ],
    "profiles": 
    {
        "defaults": {},
        "list": 
        [
            {
                "backgroundImage": "C:/x/5.png",
                "backgroundImageAlignment": "center",
                "backgroundImageOpacity": 0.9,
                "backgroundImageStretchMode": "uniformToFill",
                "commandline": "%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
                "guid": "{61c54bbd-c2c6-5271-96e7-009a87ff44bf}",
                "hidden": false,
                "name": "Windows PowerShell",
                "opacity": 80,
                "useAcrylic": true
            },
            {
                "backgroundImage": "C:/x/5.png",
                "backgroundImageAlignment": "center",
                "backgroundImageOpacity": 0.9,
                "backgroundImageStretchMode": "uniformToFill",
                "commandline": "%SystemRoot%\\System32\\cmd.exe",
                "guid": "{0caa0dad-35be-5f56-a8ff-afceeeaa6101}",
                "hidden": false,
                "name": "\u547d\u4ee4\u63d0\u793a\u7b26",
                "opacity": 80,
                "useAcrylic": true
            },
            {
                "backgroundImage": "C:/x/5.png",
                "backgroundImageAlignment": "center",
                "backgroundImageOpacity": 0.9,
                "backgroundImageStretchMode": "uniformToFill",
                "guid": "{b453ae62-4e3d-5e58-b989-0a998ec441b8}",
                "hidden": false,
                "name": "Azure Cloud Shell",
                "opacity": 80,
                "source": "Windows.Terminal.Azure",
                "useAcrylic": true
            }
        ]
    },
    "schemes": [],
    "themes": []
}
```

![image-20250709102732491](/images/notes/WindowsTeiminal图片背景美化配置/images/image-20250709102732491.png)