# 아티팩트 원본(스켈레톤 없는 html)을 GitHub Pages용 완전한 문서로 감싼다
# 사용: python _감싸기.py <원본 index.html> <폴더이름> "<설명 한 줄>"
import sys, os
src_path, folder, desc = sys.argv[1], sys.argv[2], sys.argv[3]
src = open(src_path, encoding='utf-8').read()
i = src.index('</style>') + len('</style>')
head = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        f'<meta name="description" content="{desc}">\n')
out = head + src[:i] + '\n</head>\n<body>\n' + src[i:] + '\n</body>\n</html>\n'
dest = os.path.join('C:/Users/user/pogo-site', folder)
os.makedirs(dest, exist_ok=True)
open(os.path.join(dest, 'index.html'), 'w', encoding='utf-8').write(out)
print('wrapped →', folder)
