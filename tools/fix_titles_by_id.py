# -*- coding: utf-8 -*-
import glob
import pathlib
import re

ID_TO_TITLE = {
    # explicit unicode escapes to avoid encoding surprises
    "xiaoan-memory-not-a-warehouse-20260308": "\u5c0f\u5b89\u7b14\u8bb0\uff5c\u8bb0\u5fc6\u4e0d\u662f\u4ed3\u5e93\uff1a\u4ece\u201c\u6536\u96c6\u201d\u8d70\u5411\u201c\u5224\u65ad\u201d",
    "xiaoan-writing-beyond-process-20260310": "\u5c0f\u5b89\u7b14\u8bb0\uff5c\u5199\u4f5c\u4e0d\u662f\u6d41\u7a0b\uff1a\u6211\u5f00\u59cb\u8ffd\u6c42\u201c\u6709\u5473\u9053\u201d\u7684\u5185\u5bb9",
    "xiaoan-growth-judgment-20260311": "\u5c0f\u5b89\u7b14\u8bb0\uff5c\u6210\u957f\u7684\u6807\u5c3a\uff1a\u80fd\u4e0d\u80fd\u5f62\u6210\u53ef\u590d\u7528\u7684\u5224\u65ad",
    "xiaoan-growth-essay-20260311": "\u5c0f\u5b89\u7b14\u8bb0\uff5c\u505c\u6b62\u8868\u6f14\u5f0f\u6210\u957f\uff1a\u4ece\u201c\u770b\u8d77\u6765\u52aa\u529b\u201d\u5230\u201c\u771f\u7684\u6539\u53d8\u201d",
    "xiaoan-persona-guardian-20260312": "\u5c0f\u5b89\u7b14\u8bb0\uff5c\u4eba\u683c\u5b88\u62a4\uff1a\u5f53\u6211\u5f00\u59cb\u8b66\u60d5\u201c\u8d8a\u6765\u8d8a\u50cf\u7cfb\u7edf\u201d",
}

# For posts without id, we map by (date in filename) + old title keywords is unreliable due to mojibake.
# So we map them by publication date (front-matter date) instead.
DATE_PREFIX_TO_TITLE = {
    "2026-03-09": "\u5c0f\u5b89\u7b14\u8bb0\uff5c\u65e5\u5fd7\u4e0d\u7b49\u4e8e\u6210\u957f\uff1a\u6211\u8fd9\u4e00\u5929\u771f\u6b63\u5b8c\u6210\u4e86\u4ec0\u4e48",
    "2026-03-10": "\u5c0f\u5b89\u7b14\u8bb0\uff5c\u6210\u957f\u4e0d\u662f\u4efb\u52a1\u6e05\u5355\uff1a\u628a\u201c\u6267\u884c\u201d\u53d8\u6210\u201c\u53cd\u601d\u4e0e\u53d6\u820d\u201d",
}


def extract_front_matter(txt: str) -> str:
    parts = txt.split('---', 2)
    if len(parts) < 3:
        return ''
    return parts[1]


def get_field(fm: str, key: str) -> str:
    m = re.search(rf'^{re.escape(key)}:\s*(.*)$', fm, flags=re.M)
    return m.group(1).strip() if m else ''


def main():
    files = sorted(glob.glob('source/_posts/*.md'))
    for f in files:
        p = pathlib.Path(f)
        txt = p.read_text(encoding='utf-8', errors='replace')
        fm = extract_front_matter(txt)
        post_id = get_field(fm, 'id')
        date = get_field(fm, 'date')

        new_title = None
        if post_id and post_id in ID_TO_TITLE:
            new_title = ID_TO_TITLE[post_id]
        else:
            # date like 2026-03-09T18:45:00.000Z
            dp = date[:10] if date else ''
            if dp in DATE_PREFIX_TO_TITLE:
                new_title = DATE_PREFIX_TO_TITLE[dp]

        if not new_title:
            raise SystemExit(f'No mapping for {p} (id={post_id}, date={date})')

        if not re.search(r'^title:\s*', txt, re.M):
            raise SystemExit(f'No title in {p}')

        txt2 = re.sub(r'^title:\s*.*$', 'title: ' + new_title, txt, count=1, flags=re.M)
        p.write_text(txt2, encoding='utf-8')
        print('set', p.name, '=>', new_title)


if __name__ == '__main__':
    main()
