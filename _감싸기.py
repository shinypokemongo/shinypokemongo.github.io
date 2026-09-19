# 아티팩트 원본(스켈레톤 없는 html)을 GitHub Pages용 완전한 문서로 감싼다
# 사용: python _감싸기.py <원본 index.html>
import sys
src = open(sys.argv[1], encoding='utf-8').read()
i = src.index('</style>') + len('</style>')
head = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="description" content="포켓몬고 박스 정리 검색어를 누르면 복사. 보낼 후보·반짝반짝 확정·교환 사탕·레거시 기술·배틀리그 검색어를 한국어판에서 직접 확인했습니다.">\n')
out = head + src[:i] + '\n</head>\n<body>\n' + src[i:] + '\n</body>\n</html>\n'
open('C:/Users/user/pogo-site/search/index.html', 'w', encoding='utf-8').write(out)
print('wrapped')
