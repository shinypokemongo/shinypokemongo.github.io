# 포켓몬·기술·타입·폼·검색어 이름을 게임 문구 그대로 바꾸는 표 — 직역·기억 금지
# 출처: 공용/명칭/i18n_korean.json · i18n_english.json · i18n_japanese.json (PokeMiners, 게임 APK 문구)
#   names('pokemon_name_') → {한국어: (영어, 일본어)}   키 앞부분: pokemon_name_ / move_name_ / pokemon_type_ / form_ / filter_key_
#   by_key('move_name_0013') → (한국어, 영어, 일본어)
# 같은 한국어가 다른 뜻으로 두 번 나오면(예: 폼 이름) conflicts에 남긴다 — 그 이름은 키로 직접 찾을 것
import json, os
DIR = 'C:/Users/user/OneDrive/바탕 화면/클로드/공용/명칭'
_cache = {}

def _load(lang):
    if lang not in _cache:
        a = json.load(open(os.path.join(DIR, f'i18n_{lang}.json'), encoding='utf-8'))['data']
        _cache[lang] = dict(zip(a[::2], a[1::2]))
    return _cache[lang]

def by_key(key):
    return tuple(_load(l).get(key) for l in ('korean', 'english', 'japanese'))

conflicts = {}

def names(prefix):
    ko, en, ja = _load('korean'), _load('english'), _load('japanese')
    out = {}
    for k, v in ko.items():
        if not k.startswith(prefix) or k not in en or k not in ja:
            continue
        tr = (en[k].strip(), ' '.join(ja[k].split()))
        if v in out and out[v] != tr:
            conflicts.setdefault(v, {out[v]}).add(tr)
            continue
        out[v] = tr
    return out

# 1009~1025번: 포켓몬고 게임 문구에 아직 이름이 없다 → PokeAPI pokemon_species_names(1~1008번은 게임 문구와 전부 일치 확인)
# 영어는 포고에셋/_names.json과도 같음. 게임 문구가 생기면 pokemon_name_XXXX가 먼저 쓰인다
LATE = {1009: ('Walking Wake', 'ウネルミナモ'), 1010: ('Iron Leaves', 'テツノイサハ'), 1011: ('Dipplin', 'カミッチュ'),
        1012: ('Poltchageist', 'チャデス'), 1013: ('Sinistcha', 'ヤバソチャ'), 1014: ('Okidogi', 'イイネイヌ'),
        1015: ('Munkidori', 'マシマシラ'), 1016: ('Fezandipiti', 'キチキギス'), 1017: ('Ogerpon', 'オーガポン'),
        1018: ('Archaludon', 'ブリジュラス'), 1019: ('Hydrapple', 'カミツオロチ'), 1020: ('Gouging Fire', 'ウガツホムラ'),
        1021: ('Raging Bolt', 'タケルライコ'), 1022: ('Iron Boulder', 'テツノイワオ'), 1023: ('Iron Crown', 'テツノカシラ'),
        1024: ('Terapagos', 'テラパゴス'), 1025: ('Pecharunt', 'モモワロウ')}

def pokemon(no, li):
    # 도감번호 → 그 언어 이름(li 0=영어 1=일본어). 게임 문구 먼저, 없으면 LATE
    v = _load(('english', 'japanese')[li]).get(f'pokemon_name_{no:04d}')
    return ' '.join(v.split()) if v else LATE.get(no, (None, None))[li]
