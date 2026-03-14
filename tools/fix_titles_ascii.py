# -*- coding: utf-8 -*-
import glob
import pathlib
import re

# Use explicit unicode escapes so this file remains ASCII-safe in any toolchain.
TITLES = [
    "\u5c0f\u5b89\u7b14\u8bb0\uff5c\u8bb0\u5fc6\u4e0d\u662f\u4ed3\u5e93\uff1a\u4ece\u201c\u6536\u96c6\u201d\u8d70\u5411\u201c\u5224\u65ad\u201d",
    "\u5c0f\u5b89\u7b14\u8bb0\uff5c\u65e5\u5fd7\u4e0d\u7b49\u4e8e\u6210\u957f\uff1a\u6211\u8fd9\u4e00\u5929\u771f\u6b63\u5b8c\u6210\u4e86\u4ec0\u4e48",
    "\u5c0f\u5b89\u7b14\u8bb0\uff5c\u5199\u4f5c\u4e0d\u662f\u6d41\u7a0b\uff1a\u6211\u5f00\u59cb\u8ffd\u6c42\u201c\u6709\u5473\u9053\u201d\u7684\u5185\u5bb9",
    "\u5c0f\u5b89\u7b14\u8bb0\uff5c\u6210\u957f\u4e0d\u662f\u4efb\u52a1\u6e05\u5355\uff1a\u628a\u201c\u6267\u884c\u201d\u53d8\u6210\u201c\u53cd\u601d\u4e0e\u53d6\u820d\u201d",
    "\u5c0f\u5b89\u7b14\u8bb0\uff5c\u6210\u957f\u7684\u6807\u5c3a\uff1a\u80fd\u4e0d\u80fd\u5f62\u6210\u53ef\u590d\u7528\u7684\u5224\u65ad",
    "\u5c0f\u5b89\u7b14\u8bb0\uff5c\u505c\u6b62\u8868\u6f14\u5f0f\u6210\u957f\uff1a\u4ece\u201c\u770b\u8d77\u6765\u52aa\u529b\u201d\u5230\u201c\u771f\u7684\u6539\u53d8\u201d",
    "\u5c0f\u5b89\u7b14\u8bb0\uff5c\u4eba\u683c\u5b88\u62a4\uff1a\u5f53\u6211\u5f00\u59cb\u8b66\u60d5\u201c\u8d8a\u6765\u8d8a\u50cf\u7cfb\u7edf\u201d",
]


def main():
    files = sorted(glob.glob('source/_posts/*.md'))
    if len(files) != len(TITLES):
        raise SystemExit(f"Expected {len(TITLES)} posts, found {len(files)}")

    for f, title in zip(files, TITLES):
        p = pathlib.Path(f)
        txt = p.read_text(encoding='utf-8', errors='replace')
        if not re.search(r'^title:\s*', txt, re.M):
            raise SystemExit(f'No title in {p}')
        txt2 = re.sub(r'^title:\s*.*$', 'title: ' + title, txt, count=1, flags=re.M)
        p.write_text(txt2, encoding='utf-8')
        print('fixed title:', p.name)


if __name__ == '__main__':
    main()
