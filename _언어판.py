# 한국어 원본에서 영어·일본어판을 만든다 → pogo-site/<언어>/<폴더>/index.html
# 사용: python _언어판.py <원본 html> <폴더이름>
# 번역표는 도구마다 _i18n/<폴더>.py:
#   TABLE = {한국어: (영어, 일본어)}  — 긴 것부터 문자열 치환
#   DESC = (영어 설명, 일본어 설명)
#   extra(src, li) — (선택) 표 치환 전에 돌리는 함수. li 0=영어 1=일본어. 데이터 속 이름 바꾸기 등
#   post(src, li)  — (선택) 표 치환 뒤에 돌리는 함수
# 포켓몬·기술·타입 이름은 _i18n/_이름.py(게임 문구 i18n_*.json)로 바꾼다 — 직역 금지
# 끝에 한글이 하나라도 남으면 멈춘다(언어 버튼의 '한국어'만 허용) — 원본 문구를 바꾸면 표도 같이 고칠 것
# 그림·데이터 같은 상대 주소는 <base href="/<폴더>/">로 한국어판 것을 같이 쓴다
import sys, os, re, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _언어 import I18N, alternates, switcher
SITE = 'https://shinypokemongo.github.io'
GC = '<script data-goatcounter="https://shinypokemongo.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'
LANGS = ('en', 'ja')

def translate(raw, folder, li, mod):
    lang = LANGS[li]
    src = mod.extra(raw, li) if hasattr(mod, 'extra') else raw
    for ko in sorted(mod.TABLE, key=len, reverse=True):
        src = src.replace(ko, mod.TABLE[ko][li])
    if hasattr(mod, 'post'):
        src = mod.post(src, li)
    src = re.sub(r'[ \t]*/\*[^*]*[가-힣][^*]*\*/\n?', '', src)       # 한글 CSS·JS 블록 주석
    src = re.sub(r'(?m)^[ \t]*//[^\n]*[가-힣][^\n]*\n', '', src)                  # 한글 JS 주석만 있는 줄
    src = re.sub(r'(?m)([;{},)\]])[ \t]+//[^\n\'"`]*[가-힣][^\n\'"`]*$', r'\1', src)  # 코드 뒤에 붙은 한글 주석(코드는 남김)
    src = re.sub(r'<!--(?!lang-->)[^>]*?[가-힣][\s\S]*?-->', '', src)  # 한글 HTML 주석
    src = src.replace('"ko-KR"', '"en-US"' if lang == 'en' else '"ja-JP"').replace("'ko-KR'", "'en-US'" if lang == 'en' else "'ja-JP'")
    src = src.replace('<!--lang-->', switcher(lang, folder))
    src = src.replace('class="home" href="../"', f'class="home" href="/{lang}/"')  # 도구함 버튼은 그 언어 첫 화면으로
    if lang == 'ja':
        # 일본어는 띄어쓰기가 없어 keep-all이면 줄이 안 바뀐다. 글꼴도 일본어 글꼴부터
        src = src.replace('word-break: keep-all', 'word-break: normal; line-break: strict')
        src = src.replace('"Apple SD Gothic Neo", "Malgun Gothic"', '"Hiragino Sans", "Yu Gothic", "Meiryo"')
    return src

def build(src_path, folder):
    raw = open(src_path, encoding='utf-8').read()
    mod = importlib.import_module(f'_i18n.{folder}')
    for li, lang in enumerate(LANGS):
        src = translate(raw, folder, li, mod)
        left = sorted(set(re.findall(r'[가-힣][가-힣 ·]*', src.replace('>한국어<', '><'))))
        if left:
            sys.exit(f'[{lang}/{folder}] 한글이 남음 {len(left)}개: {left[:80]}')
        title = re.search(r'<title>(.*?)</title>', src).group(1)
        desc = mod.DESC[li]
        url = f'{SITE}/{lang}/{folder}/'
        i = src.index('</style>') + len('</style>')
        head = (f'<!doctype html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
                f'<base href="/{folder}/">\n'
                '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                f'<meta name="description" content="{desc}">\n'
                f'<link rel="canonical" href="{url}">\n' + alternates(folder, SITE) +
                f'<meta property="og:type" content="website">\n<meta property="og:site_name" content="Shiny Collector Tools">\n<meta property="og:locale" content="{"en_US" if lang == "en" else "ja_JP"}">\n'
                f'<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n<meta property="og:url" content="{url}">\n'
                f'<meta property="og:image" content="{SITE}/og/{folder}.png">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
                '<meta name="twitter:card" content="summary_large_image">\n')
        out = head + src[:i] + '\n</head>\n<body>\n' + src[i:] + '\n' + GC + '\n</body>\n</html>\n'
        dest = os.path.join(HERE, lang, folder)
        os.makedirs(dest, exist_ok=True)
        open(os.path.join(dest, 'index.html'), 'w', encoding='utf-8').write(out)
        print('built ->', f'{lang}/{folder}')

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2])
