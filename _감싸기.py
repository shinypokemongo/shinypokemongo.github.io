# 아티팩트 원본(스켈레톤 없는 html)을 GitHub Pages용 완전한 문서로 감싼다
# 사용: python _감싸기.py <원본 index.html> <폴더이름> ["<설명 한 줄>"]   ← 설명을 빼면 이미 올라가 있는 설명을 그대로 쓴다
# 공유 미리보기(og) 이미지는 og/<폴더이름>.png — _og만들기.py가 만든다
import sys, os, re
SITE = 'https://shinypokemongo.github.io'
# 방문 집계(GoatCounter, 쿠키 없음) — 통계는 https://shinypokemongo.goatcounter.com
GC = '<script data-goatcounter="https://shinypokemongo.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'
src_path, folder = sys.argv[1], sys.argv[2]
dest = os.path.join('C:/Users/user/pogo-site', folder)
if len(sys.argv) > 3:
    desc = sys.argv[3]
else:
    old = open(os.path.join(dest, 'index.html'), encoding='utf-8').read()
    desc = re.search(r'<meta name="description" content="([^"]*)"', old).group(1)
src = open(src_path, encoding='utf-8').read()
title = re.search(r'<title>(.*?)</title>', src).group(1)
i = src.index('</style>') + len('</style>')
url = f'{SITE}/{folder}/'
head = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f'<meta name="description" content="{desc}">\n'
        f'<link rel="canonical" href="{url}">\n'
        '<meta property="og:type" content="website">\n<meta property="og:site_name" content="이로치수집가 도구함">\n<meta property="og:locale" content="ko_KR">\n'
        f'<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n<meta property="og:url" content="{url}">\n'
        f'<meta property="og:image" content="{SITE}/og/{folder}.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
        '<meta name="twitter:card" content="summary_large_image">\n')
out = head + src[:i] + '\n</head>\n<body>\n' + src[i:] + '\n' + GC + '\n</body>\n</html>\n'
os.makedirs(dest, exist_ok=True)
open(os.path.join(dest, 'index.html'), 'w', encoding='utf-8').write(out)
print('wrapped ->', folder)
