# 언어판 공통: _감싸기.py(한국어판)와 _언어판.py(영어·일본어판)가 같이 쓴다
# 한국어판은 /<폴더>/, 번역판은 /<언어>/<폴더>/ — 주소가 따로라 검색엔진이 언어마다 색인한다
I18N = {'shop': ['en', 'ja']}
NAMES = {'ko': '한국어', 'en': 'English', 'ja': '日本語'}

def url_path(lang, folder):
    return f'/{folder}/' if lang == 'ko' else f'/{lang}/{folder}/'

def alternates(folder, site):
    # hreflang: 이 페이지의 다른 언어판이 어디 있는지 구글에 알려 준다
    if folder not in I18N:
        return ''
    langs = ['ko'] + I18N[folder]
    out = ''.join(f'<link rel="alternate" hreflang="{l}" href="{site}{url_path(l, folder)}">\n' for l in langs)
    return out + f'<link rel="alternate" hreflang="x-default" href="{site}{url_path("ko", folder)}">\n'

def switcher(lang, folder):
    # 원본의 <!--lang--> 자리에 들어가는 언어 버튼
    if folder not in I18N:
        return ''
    links = ''.join(
        f'<a href="{url_path(l, folder)}" hreflang="{l}" lang="{l}"' + (' aria-current="page"' if l == lang else '') + f'>{NAMES[l]}</a>'
        for l in ['ko'] + I18N[folder])
    return f'<nav class="lang" aria-label="Language">{links}</nav>'
