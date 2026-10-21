# 뭘 키울까 /pick/ 번역표 — _언어판.py가 읽는다. 표의 값은 (영어, 일본어)
# 내장 데이터(data_all.json)의 포켓몬·폼·타입·기술 이름은 extra에서 JSON째 바꾼다 — 게임 문구(_이름.py) 그대로
# 검색: 영어는 대소문자 무시, 일본어는 히라가나로 쳐도 가타카나 이름이 걸리게. 가나다순 → A–Z / 50음순
import json, re
from pathlib import Path
from ._이름 import by_key, names

SRC_DIR = Path('C:/Users/user/OneDrive/바탕 화면/클로드/2_블로그/예전원고/개체값비교')
# build_all.py와 같은 폼 키(도감번호 → 키). 테오키스는 한글 키(form_attack…)의 일본어에 'A' 같은 글자가 붙어 있어서
# 같은 폼의 form_deoxys_* 키를 쓴다(한국어판은 그대로)
SP = {
    386: ['form_deoxys_normal', 'form_attack', 'form_defense', 'form_speed'],
    413: ['form_plant_cloak', 'form_sandy_cloak', 'form_trash_cloak'],
    479: ['form_rotom_normal', 'form_rotom_heat', 'form_rotom_wash', 'form_rotom_frost', 'form_rotom_fan', 'form_rotom_mow'],
    483: ['form_dialga_normal', 'form_dialga_origin'], 484: ['form_palkia_normal', 'form_palkia_origin'],
    487: ['form_giratina_altered', 'form_giratina_origin'], 492: ['form_shaymin_land', 'form_shaymin_sky'],
    641: ['form_tornadus_incarnate', 'form_tornadus_therian'], 642: ['form_thundurus_incarnate', 'form_thundurus_therian'],
    645: ['form_landorus_incarnate', 'form_landorus_therian'], 905: ['form_incarnate', 'form_therian'],
    646: ['form_kyurem_normal', 'form_kyurem_black', 'form_kyurem_white'], 720: ['form_hoopa_confined', 'form_hoopa_unbound'],
    745: ['form_lycanroc_midday', 'form_lycanroc_midnight', 'form_lycanroc_dusk'],
    800: ['form_necrozma_normal', 'form_necrozma_dusk_mane', 'form_necrozma_dawn_wings'],
    888: ['form_zacian_hero', 'form_zacian_crowned_sword'], 889: ['form_zamazenta_hero', 'form_zamazenta_crowned_shield'],
    710: [f'form_pumpkaboo_{s}' for s in ('small', 'average', 'large', 'super')],
    711: [f'form_gourgeist_{s}' for s in ('small', 'average', 'large', 'super')],
    718: ['form_zygarde_ten_percent', 'form_zygarde_fifty_percent', 'form_zygarde_complete'],
    876: ['form_male', 'form_female'], 916: ['form_oinkologne_male', 'form_oinkologne_female'],
    128: ['form_paldea_combat', 'form_paldea_blaze', 'form_paldea_aqua'],
}
FIX = {'form_attack': 'form_deoxys_attack', 'form_defense': 'form_deoxys_defense', 'form_speed': 'form_deoxys_speed'}
# 지역 폼: 영어는 'Alolan Raichu'(도감 머리글 Alolan Form 등), 일본어는 'ライチュウ（アローラのすがた）'(alola_pokedex_header 등)
REG = {'알로라': 'alola', '가라르': 'galarian', '히스이': 'hisuian', '팔데아': 'paldean'}
def _reg(r):
    ko, en, ja = by_key(f'{r}_pokedex_header')
    return en.split()[0].capitalize(), ja.strip()
# 1009~1025는 게임 문구(i18n)에 아직 없다 → PokeAPI pokemon_species_names.csv(2026-10-21).
# 같은 표의 1~1008번이 게임 문구와 일본어·한국어 1,008/1,008 일치, 영어도 일치(' 모양만 2건 차이) · 영어는 포고에셋/_names.json과도 같음
LATE = {1009: ('Walking Wake', 'ウネルミナモ'), 1010: ('Iron Leaves', 'テツノイサハ'), 1011: ('Dipplin', 'カミッチュ'),
        1012: ('Poltchageist', 'チャデス'), 1013: ('Sinistcha', 'ヤバソチャ'), 1014: ('Okidogi', 'イイネイヌ'),
        1015: ('Munkidori', 'マシマシラ'), 1016: ('Fezandipiti', 'キチキギス'), 1017: ('Ogerpon', 'オーガポン'),
        1018: ('Archaludon', 'ブリジュラス'), 1019: ('Hydrapple', 'カミツオロチ'), 1020: ('Gouging Fire', 'ウガツホムラ'),
        1021: ('Raging Bolt', 'タケルライコ'), 1022: ('Iron Boulder', 'テツノイワオ'), 1023: ('Iron Crown', 'テツノカシラ'),
        1024: ('Terapagos', 'テラパゴス'), 1025: ('Pecharunt', 'モモワロウ')}
LATE_KO = {1009: '굽이치는물결', 1010: '무쇠잎새', 1011: '과미르', 1012: '차데스', 1013: '그우린차', 1014: '조타구', 1015: '이야후',
           1016: '기로치', 1017: '오거폰', 1018: '브리두라스', 1019: '과미드라', 1020: '꿰뚫는화염', 1021: '날뛰는우레',
           1022: '무쇠암석', 1023: '무쇠감투', 1024: '테라파고스', 1025: '복숭악동'}
def _sp(d):
    if d in LATE: return LATE[d]
    _, en, ja = by_key(f'pokemon_name_{d:04d}')
    return en.strip(), ' '.join(ja.split())
def _form(k):
    _, en, ja = by_key(FIX.get(k, k))
    return en.strip(), ' '.join(ja.split())

def mon_name(dex, n, li):
    sp = _sp(dex)[li]
    reg = n.split(' ', 1)[0]
    if reg in REG and ' ' in n:
        r = _reg(REG[reg])[li]
        m = re.fullmatch(r'\S+ \S+ \((.+)\)', n)  # 팔데아 켄타로스 (컴뱃종)
        if m:
            k = next(k for k in SP[dex] if by_key(k)[0].strip() == m[1])
            lab = _form(k)[li]
            return f'{r} {sp} ({lab})' if li == 0 else f'{sp}（{lab}）'
        return f'{r} {sp}' if li == 0 else f'{sp}（{r}）'
    if dex in SP:
        for k in SP[dex]:
            lab_ko = by_key(k)[0].strip()
            if n == lab_ko:
                return _form(k)[li]
            if n == f'{_sp_ko(dex)} ({lab_ko})':
                lab = _form(k)[li]
                return f'{sp} ({lab})' if li == 0 else f'{sp}（{lab}）'
    if n == _sp_ko(dex):
        return sp
    raise SystemExit(f'pick: 이름을 못 바꿈 {dex} {n}')
def _sp_ko(d):
    return LATE_KO[d] if d in LATE_KO else by_key(f'pokemon_name_{d:04d}')[0].strip()

TYPES = ['normal', 'fire', 'water', 'grass', 'electric', 'ice', 'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']

def extra(src, li):
    raw = (SRC_DIR / 'data_all.json').read_text(encoding='utf-8')
    assert src.count(raw) == 1, 'pick: 내장 데이터를 못 찾음(만들기.py 다시 돌릴 것)'
    d = json.loads(raw)
    for row in d['mons']:
        row[1] = mon_name(row[0], row[1], li)
        row[2] = _sp(row[0])[li]
    assert [by_key(f'pokemon_type_{t}')[0] for t in TYPES] == d['types']
    d['types'] = [by_key(f'pokemon_type_{t}')[1 + li] for t in TYPES]
    mv = names('move_name_')
    miss = [x for x in d['moves'] if x not in mv]
    if miss: raise SystemExit(f'pick: 기술 이름 없음 {miss}')
    d['moves'] = [mv[x][li] for x in d['moves']]
    dup = {r[1] for r in d['mons'] if [x[1] for x in d['mons']].count(r[1]) > 1}
    if dup: print('pick: 이름 중복', sorted(dup))
    # indent=0: 항목마다 줄을 나눠 둔다 — 한 줄 4MB면 엔진의 주석 정규식(//…줄 끝)이 그림 base64 속 '//'마다 줄 끝까지 훑어 몇 분 걸린다
    return src.replace(raw, json.dumps(d, ensure_ascii=False, indent=0, separators=(',', ':')))

# 검색·정렬 코드(언어마다 다름) — 표 치환 뒤 post에서 바꾼다
SEARCH_KO = [
    "const head = idx.filter(i => M[i].ko.startsWith(q) || M[i].b.startsWith(q));",
    "const named = [...head, ...idx.filter(i => !head.includes(i) && M[i].ko.includes(q))];",
    "const ty = D.types.findIndex(x => x === qq);",
    "const moves = qq.length >= 2 ? D.moves.map((x, k) => [x, k]).filter(([x]) => x.startsWith(qq)).slice(0, 3) : [];",
]
SEARCH_NEW = [
    "const nq = nz(q); const head = idx.filter(i => nz(M[i].ko).startsWith(nq) || nz(M[i].b).startsWith(nq));",
    "const named = [...head, ...idx.filter(i => !head.includes(i) && nz(M[i].ko).includes(nq))];",
    "const ty = D.types.findIndex(x => nz(x) === nz(qq));",
    "const moves = qq.length >= 2 ? D.moves.map((x, k) => [x, k]).filter(([x]) => nz(x).startsWith(nz(qq))).slice(0, 3) : [];",
]
NZ = ("const nz = s => s.normalize('NFKC').toLowerCase()"
      ".replace(/[\\u3041-\\u3096]/g, c => String.fromCharCode(c.charCodeAt(0) + 0x60)).replace(/[\\s・·.'’:-]/g, '');\n")
SORT_KO = """const CHO = ['ㄱ', 'ㄱ', 'ㄴ', 'ㄷ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅂ', 'ㅅ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'];
const KANA = ['ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'];
const choOf = m => { const c = m.b.charCodeAt(0) - 0xAC00; return c >= 0 && c < 11172 ? CHO[Math.floor(c / 588)] : 'ㅎ'; };"""
SORT_EN = """const KANA = ['A–C', 'D–F', 'G–I', 'J–L', 'M–O', 'P–R', 'S', 'T–V', 'W–Z'];
const KANA_OF = ['ABC', 'DEF', 'GHI', 'JKL', 'MNO', 'PQR', 'S', 'TUV', 'WXYZ'];
const choOf = m => { const c = m.b.normalize('NFD')[0].toUpperCase(); const k = KANA_OF.findIndex(x => x.includes(c)); return KANA[k < 0 ? KANA.length - 1 : k]; };"""
SORT_JA = """const KANA = ['ア', 'カ', 'サ', 'タ', 'ナ', 'ハ', 'マ', 'ヤ', 'ラ', 'ワ'];
const KANA_OF = ['アイウエオヴァィゥェォ', 'カキクケコ', 'サシスセソ', 'タチツテト', 'ナニヌネノ', 'ハヒフヘホ', 'マミムメモ', 'ヤユヨャュョ', 'ラリルレロ', 'ワヲン'];
const choOf = m => { const c = m.b.normalize('NFD')[0]; const k = KANA_OF.findIndex(x => x.includes(c)); return KANA[k < 0 ? KANA.length - 1 : k]; };"""

def post(src, li):
    for a, b in zip(SEARCH_KO, SEARCH_NEW):
        assert src.count(a) == 1, a
        src = src.replace(a, b)
    src = src.replace('const $ = id => document.getElementById(id);\n', 'const $ = id => document.getElementById(id);\n' + NZ, 1)
    assert SORT_KO in src
    src = src.replace(SORT_KO, (SORT_EN, SORT_JA)[li])
    src = src.replace(".localeCompare(M[y].b, 'ko')", f".localeCompare(M[y].b, '{('en', 'ja')[li]}')").replace(".localeCompare(M[y].ko, 'ko')", f".localeCompare(M[y].ko, '{('en', 'ja')[li]}')")
    src = src.replace("q.replace(/\\s*타입$/, '')", ("q.replace(/\\s*type$/i, '')", "q.replace(/\\s*タイプ$/, '')")[li])
    # 코드 뒤에 붙은 한글 주석(줄째 지우면 코드가 사라지므로 주석만)
    src = re.sub(r'(?<=[;{}),\s])//[^\n]*[가-힣][^\n]*', '', src)
    return src

_ex = names('move_name_')['코멧펀치']
_dratini, _dragon = _sp(147), by_key('pokemon_type_dragon')[1:]
TABLE = {
    "M.findIndex(m => m.ko === '망나뇽')": ("M.findIndex(m => m.dex === 149)", "M.findIndex(m => m.dex === 149)"),
    '<title>이로치수집가 뭘 키울까</title>': ('<title>Which to Power Up? · Shiny Collector Tools</title>', '<title>どれを育てる？ · 色違いコレクター</title>'),
    '<a class="home" href="https://shinypokemongo.github.io/">포켓몬고 <b>이로치 수집가</b> 도구함</a>': (
        '<a class="home" href="/en/">Pokémon GO <b>Shiny Collector</b> Tools</a>', '<a class="home" href="/ja/">ポケモンGO <b>色違いコレクター</b> ツール</a>'),
    '<span class="here">개체값 비교</span>': ('<span class="here">IV compare</span>', '<span class="here">個体値比較</span>'),
    '<h1>뭘 키울까? 같은 포켓몬 개체값 비교</h1>': ('<h1>Which one to power up? Compare IVs of the same Pokémon</h1>', '<h1>どれを育てる？ 同じポケモンの個体値比較</h1>'),
    '>입력<': ('>Input<', '>入力<'),
    '<i>1</i>어떤 포켓몬인가요': ('<i>1</i>Which Pokémon?', '<i>1</i>どのポケモン？'),
    '"포켓몬 이름, 타입 또는 기술 이름"': ('"Pokémon name, type or move name"', '"ポケモンの名前、タイプ、わざの名前"'),
    'placeholder="이름·타입·기술 (예: 미뇽, 드래곤, 코멧펀치)"': (
        f'placeholder="Name, type or move (e.g. {_dratini[0]}, {_dragon[0]}, {_ex[0]})"', f'placeholder="名前・タイプ・わざ（例：{_dratini[1]}、{_dragon[1]}、{_ex[1]}）"'),
    '>목록</button>': ('>List</button>', '>リスト</button>'),
    '"이름이 비슷한 포켓몬"': ('"Pokémon with similar names"', '"名前が似ているポケモン"'),
    '"목록 나누는 기준"': ('"How to group the list"', '"リストの分け方"'),
    '>세대별<': ('>By generation<', '>世代別<'),
    '>가나다순<': ('>A–Z<', '>50音順<'),
    '"묶음 고르기"': ('"Pick a group"', '"グループを選ぶ"'),
    '어떤 모습으로 비교할까요': ('Compare as which form?', 'どの姿で比べる？'),
    '"비교할 진화 모습"': ('"Evolution to compare"', '"比べる進化の姿"'),
    '<i>2</i>어디에 쓸 건가요': ('<i>2</i>Where will you use it?', '<i>2</i>どこで使う？'),
    '"쓰는 곳"': ('"Where it will be used"', '"使う場所"'),
    '>레이드</button>': ('>Raids</button>', '>レイド</button>'),
    '>배틀리그</button>': ('>GO Battle League</button>', '>GOバトルリーグ</button>'),
    '"레이드 인원"': ('"Raid group size"', '"レイドの人数"'),
    '>여럿이 (5명 이상)<': ('>Big group (5+)<', '>大人数（5人以上）<'),
    '>소수·솔로<': ('>Small group · solo<', '>少人数・ソロ<'),
    'aria-label="리그"': ('aria-label="League"', 'aria-label="リーグ"'),
    '>슈퍼리그 1,500<': ('>Great League 1,500<', '>スーパーリーグ 1,500<'),
    '>하이퍼리그 2,500<': ('>Ultra League 2,500<', '>ハイパーリーグ 2,500<'),
    '>마스터리그<': ('>Master League<', '>マスターリーグ<'),
    '<i>3</i>어디까지 키울 건가요': ('<i>3</i>How far will you power it up?', '<i>3</i>どこまで育てる？'),
    '"목표 레벨"': ('"Target level"', '"目標レベル"'),
    '>레벨 40<': ('>Level 40<', '>レベル40<'),
    '>레벨 50 (사탕XL)<': ('>Level 50 (Candy XL)<', '>レベル50（アメXL）<'),
    '"레벨 상한"': ('"Level cap"', '"レベル上限"'),
    '>레벨 50까지<': ('>Up to level 50<', '>レベル50まで<'),
    '>51까지 (베스트 파트너)<': ('>Up to 51 (Best Buddy)<', '>51まで（最高の相棒）<'),
    '배틀리그는 CP 한도 안에서 <b>올릴 수 있는 가장 높은 레벨</b>까지 키운다고 보고 계산해요.': (
        'For GO Battle League, it assumes you power up to <b>the highest level that fits under the CP cap</b>.',
        'GOバトルリーグは、CP上限の中で<b>上げられるいちばん高いレベル</b>まで育てるとして計算します。'),
    '<i>4</i>가진 개체를 넣어 주세요': ('<i>4</i>Enter the Pokémon you have', '<i>4</i>持っている個体を入れてください'),
    '공격·방어·체력은 0~15. <b>CP까지 넣으면</b> 야생·레이드·교환 어디서 잡았든 지금 레벨을 알아내서, 목표 레벨까지 드는 별의모래를 정확히 계산해요. 비워 두면 레벨 20으로 가정해요.': (
        'Attack, Defense and HP are 0–15. <b>Add the CP too</b> and it works out the current level — wild, raid or trade — to give the exact Stardust to the target level. Left blank, level 20 is assumed.',
        'こうげき・ぼうぎょ・HPは0〜15。<b>CPまで入れると</b>、野生・レイド・交換のどれで手に入れても今のレベルを割り出し、目標レベルまでのほしのすなを正確に計算します。空欄ならレベル20と仮定します。'),
    '>+ 개체 추가<': ('>+ Add a Pokémon<', '>+ 個体を追加<'),
    '>결과<': ('>Results<', '>結果<'),
    '이 개체를 키우세요': ('Power up this one', 'この個体を育てよう'),
    '성능 차이 1% 안쪽 · 거의 같아요': ('Within 1% · about the same', '性能差1%以内 · ほぼ同じ'),
    '<h2>이렇게 골라요</h2>': ('<h2>How it picks</h2>', '<h2>選び方</h2>'),
    '<li>같은 포켓몬이라 기술은 같다고 보고, <b>목표 레벨에서의 공격·방어·체력</b>만 비교해요.</li>': (
        '<li>Since it is the same Pokémon, moves are assumed to be the same; only <b>Attack, Defense and HP at the target level</b> are compared.</li>',
        '<li>同じポケモンなので技は同じとみなし、<b>目標レベルでのこうげき・ぼうぎょ・HP</b>だけを比べます。</li>'),
    '<li>이름 칸에 <b>타입</b>(예: 드래곤)이나 <b>기술 이름</b>(예: 코멧펀치)을 쳐도 해당 포켓몬 목록이 나와요. 이름을 치면 같은 진화 줄도 같이 보여요.</li>': (
        f'<li>Type a <b>type</b> (e.g. {_dragon[0]}) or a <b>move name</b> (e.g. {_ex[0]}) in the name box to get a list of matching Pokémon. Typing a name also shows its evolution family.</li>',
        f'<li>名前の欄に<b>タイプ</b>（例：{_dragon[1]}）や<b>わざの名前</b>（例：{_ex[1]}）を入れても、当てはまるポケモンの一覧が出ます。名前を入れると同じ進化の仲間も一緒に出ます。</li>'),
    '<li>진화 전 포켓몬을 고르면 <b>진화한 모습</b>으로 비교할 수 있어요. 개체값은 진화해도 그대로라, 미뇽 중 어느 걸 망나뇽으로 키울지 고를 때 쓰면 돼요. 진화에 드는 사탕은 별의모래 칸에 넣지 않았어요.</li>': (
        f'<li>Pick a Pokémon before evolution and you can compare it as <b>its evolved form</b>. IVs stay the same when it evolves, so use this to decide which {_dratini[0]} to raise into {_sp(149)[0]}. Candy for evolving is not included in the Stardust column.</li>',
        f'<li>進化前のポケモンを選ぶと<b>進化後の姿</b>で比べられます。個体値は進化しても変わらないので、どの{_dratini[1]}を{_sp(149)[1]}に育てるか決めるときに使えます。進化に使うアメは、ほしのすなの欄に入れていません。</li>'),
    '<li><b>여럿이</b> 하는 레이드는 빨리 끝내는 게 중요해서 공격을 크게 쳐요. <b>소수·솔로</b>는 오래 버티는 힘도 같이 쳐요.</li>': (
        '<li>In <b>big-group</b> raids, finishing fast matters, so Attack is weighted heavily. For <b>small groups and solo</b>, staying power counts too.</li>',
        '<li><b>大人数</b>のレイドは早く倒すことが大事なので、こうげきを重く見ます。<b>少人数・ソロ</b>は長く耐える力も一緒に見ます。</li>'),
    '<li>그림자는 주는 피해 1.2배, 받는 피해 1.2배로 계산해요.</li>': (
        '<li>Shadow Pokémon are calculated as dealing 1.2× damage and taking 1.2× damage.</li>',
        '<li>シャドウポケモンは与えるダメージ1.2倍、受けるダメージ1.2倍で計算します。</li>'),
    '<li>성능 차이가 1% 안쪽이면 <b>별의모래가 덜 드는 쪽</b>(반짝반짝, 이미 키운 개체)을 골라요.</li>': (
        '<li>If the difference is within 1%, it picks <b>the one that needs less Stardust</b> (Lucky, or already powered up).</li>',
        '<li>性能差が1%以内なら<b>ほしのすなが少なくて済む方</b>（キラ、すでに育てた個体）を選びます。</li>'),
    '<li>특정 보스 상대로 한 대당 피해가 같게 나오는 경우(브레이크포인트)는 아직 반영하지 않아요.</li>': (
        '<li>Cases where the damage per hit against a specific boss comes out the same (breakpoints) are not reflected yet.</li>',
        '<li>特定のボスに対して1回あたりのダメージが同じになる場合（ブレイクポイント）はまだ反映していません。</li>'),
    '<li><b>배틀리그</b>는 CP 한도 안에서 가장 높은 레벨에 맞췄을 때의 <b>공격×방어×체력(스탯 곱)</b>으로 비교해요. 순위는 같은 포켓몬 개체값 4,096가지 중 몇 위인지예요.</li>': (
        '<li><b>GO Battle League</b> compares <b>Attack × Defense × HP (stat product)</b> at the highest level under the CP cap. The rank is its place among all 4,096 IV combinations of the same Pokémon.</li>',
        '<li><b>GOバトルリーグ</b>は、CP上限の中でいちばん高いレベルに合わせたときの<b>こうげき×ぼうぎょ×HP（ステータス積）</b>で比べます。順位は同じポケモンの個体値4,096通りの中で何位かです。</li>'),
    '<li>배틀리그에서 공격이 같을 때 누가 먼저 쓰나(공격 우선권), 특정 상대와의 브레이크포인트는 반영하지 않아요.</li>': (
        '<li>Who moves first when Attack ties (CMP) and breakpoints against specific opponents are not reflected.</li>',
        '<li>GOバトルリーグでこうげきが同じときにどちらが先に撃つか（CMP）、特定の相手とのブレイクポイントは反映していません。</li>'),
    '<li>지금 CP가 이미 리그 한도를 넘은 개체는 레벨을 내릴 수 없어서 그 리그엔 못 써요.</li>': (
        '<li>A Pokémon whose current CP is already over the league cap cannot go down in level, so it cannot be used in that league.</li>',
        '<li>今のCPがすでにリーグ上限を超えている個体は、レベルを下げられないのでそのリーグでは使えません。</li>'),
    # 스크립트 안 문구
    '· 종족값 공 ${m.a} / 방 ${m.d} / 체 ${m.s}`': ('· Base Attack ${m.a} / Defense ${m.d} / HP ${m.s}`', '· 種族値 こうげき ${m.a} / ぼうぎょ ${m.d} / HP ${m.s}`'),
    '`지금 모습(${M[i].ko})`': ('`Now (${M[i].ko})`', '`今の姿（${M[i].ko}）`'),
    "'진화시킬 생각이면 진화한 모습을 눌러 보세요. 진화해도 개체값은 그대로예요.'": (
        "'If you plan to evolve it, tap the evolved form. IVs stay the same when it evolves.'", "'進化させるつもりなら、進化後の姿を押してください。個体値は進化しても変わりません。'"),
    "`개체값은 진화해도 그대로라, ${e.ko}${jo(e.ko, '이', '가')} 됐을 때 기준으로 비교해요. CP는 지금 모습(${m.ko})의 CP를 넣으면 돼요.`": (
        '`IVs stay the same after evolving, so this compares them as ${e.ko}. Enter the CP of its current form (${m.ko}).`',
        '`個体値は進化しても変わらないので、${e.ko}になったときで比べます。CPは今の姿（${m.ko}）のCPを入れてください。`'),
    "const jo = (w, a, b) => { const c = w.charCodeAt(w.length - 1) - 0xAC00; return c >= 0 && c < 11172 && c % 28 ? a : b; };": ('', ''),
    '`${D.types[ty]} 타입`': ('`${D.types[ty]} type`', '`${D.types[ty]}タイプ`'),
    '`기술 ‘${x}’`': ('`move “${x}”`', '`わざ「${x}」`'),
    '${s.more.label} 포켓몬 보기': ('See ${s.more.label} Pokémon', '${s.more.label}のポケモンを見る'),
    '${s.more.list.length}마리': ('${s.more.list.length}', '${s.more.list.length}匹'),
    '`${FOUND.label} · ${FOUND.list.length}마리`': ('`${FOUND.label} · ${FOUND.list.length}`', '`${FOUND.label} · ${FOUND.list.length}匹`'),
    '`${i + 1}세대`': ('`Gen ${i + 1}`', '`第${i + 1}世代`'),
    '<label>공격<input': ('<label>Attack<input', '<label>こうげき<input'),
    '<label>방어<input': ('<label>Defense<input', '<label>ぼうぎょ<input'),
    '<label>체력<input': ('<label>HP<input', '<label>HP<input'),
    '<label>지금 CP<input': ('<label>Current CP<input', '<label>今のCP<input'),
    'placeholder="선택"': ('placeholder="optional"', 'placeholder="任意"'),
    'aria-label="종류"': ('aria-label="Kind"', 'aria-label="種類"'),
    '>일반</option>': ('>Regular</option>', '>通常</option>'),
    '>그림자</option>': ('>Shadow</option>', '>シャドウ</option>'),
    '>정화</option>': ('>Purified</option>', '>ライト</option>'),
    '>반짝반짝</label>': ('>Lucky</label>', '>キラ</label>'),
    'aria-label="${k + 1}번 개체 빼기"': ('aria-label="Remove #${k + 1}"', 'aria-label="${k + 1}番目を外す"'),
    "`${mc.ko}의 `": ('`${mc.ko}: `', '`${mc.ko}の`'),
    "'CP가 이 개체값과 안 맞아요. 포켓몬·개체값·CP를 다시 확인해 주세요. (일단 레벨 20으로 계산)'": (
        "'This CP does not match these IVs. Check the Pokémon, IVs and CP again. (Calculated as level 20 for now)'",
        "'CPがこの個体値と合いません。ポケモン・個体値・CPをもう一度確認してください。（ひとまずレベル20で計算）'"),
    '`이 CP는 레벨 ${ls[0]}~${ls[ls.length - 1]}에서 똑같이 나와요. 가장 낮은 레벨 ${ls[0]}로 계산했어요.`': (
        '`This CP comes out the same at levels ${ls[0]}–${ls[ls.length - 1]}. Calculated with the lowest, level ${ls[0]}.`',
        '`このCPはレベル${ls[0]}〜${ls[ls.length - 1]}で同じになります。いちばん低いレベル${ls[0]}で計算しました。`'),
    "`지금 CP ${fmt(r.cp)}가 이미 ${capCp ? fmt(capCp) : ''} 한도를 넘었어요. 레벨은 내릴 수 없어서 이 리그엔 못 써요.`": (
        "`Its current CP ${fmt(r.cp)} is already over the ${capCp ? fmt(capCp) : ''} cap. Levels cannot be lowered, so it cannot be used in this league.`",
        "`今のCP ${fmt(r.cp)}がすでに${capCp ? fmt(capCp) : ''}の上限を超えています。レベルは下げられないので、このリーグでは使えません。`"),
    "r.kind === 'shadow' ? '그림자' : r.kind === 'purified' ? '정화' : '', r.lucky ? '반짝반짝' : ''": (
        "r.kind === 'shadow' ? 'Shadow' : r.kind === 'purified' ? 'Purified' : '', r.lucky ? 'Lucky' : ''",
        "r.kind === 'shadow' ? 'シャドウ' : r.kind === 'purified' ? 'ライト' : '', r.lucky ? 'キラ' : ''"),
    "S.league === 1500 ? '슈퍼리그' : S.league === 2500 ? '하이퍼리그' : '마스터리그'": (
        "S.league === 1500 ? 'Great League' : S.league === 2500 ? 'Ultra League' : 'Master League'",
        "S.league === 1500 ? 'スーパーリーグ' : S.league === 2500 ? 'ハイパーリーグ' : 'マスターリーグ'"),
    '`CP ${fmt(S.league)} 안에서 버티는 힘이 중요해요. 공격이 조금 낮아도 방어·체력이 높은 개체가 순위가 높아요.`': (
        '`Under the ${fmt(S.league)} CP cap, bulk matters. A Pokémon with slightly lower Attack but higher Defense and HP ranks higher.`',
        '`CP ${fmt(S.league)}以内では耐える力が大事です。こうげきが少し低くても、ぼうぎょ・HPが高い個体が上位になります。`'),
    "'마스터리그는 CP 한도가 없어서 레벨 끝까지 키운 뒤 공격·방어·체력이 다 높은 개체가 좋아요.'": (
        "'Master League has no CP cap, so after maxing the level, the one high in Attack, Defense and HP all round is best.'",
        "'マスターリーグはCP上限がないので、レベルを最後まで上げたうえでこうげき・ぼうぎょ・HPがすべて高い個体が有利です。'"),
    '<tr><th>개체</th><th>${lname} 순위</th><th>스탯 곱</th><th>맞출 레벨 · CP</th><th>별의모래</th></tr>': (
        '<tr><th>Pokémon</th><th>${lname} rank</th><th>Stat product</th><th>Level · CP</th><th>Stardust</th></tr>',
        '<tr><th>個体</th><th>${lname}順位</th><th>ステータス積</th><th>合わせるレベル · CP</th><th>ほしのすな</th></tr>'),
    '`넣은 개체 모두 지금 CP가 ${fmt(S.league)}를 넘어서 ${lname}엔 못 써요.`': (
        '`Every Pokémon you entered is already over ${fmt(S.league)} CP, so none can be used in ${lname}.`',
        '`入れた個体はすべて今のCPが${fmt(S.league)}を超えているので、${lname}では使えません。`'),
    '`스탯 곱 차이가 1% 안쪽이라 거의 같아요. 굳이 고르면 ${pick.r.a}/${pick.r.d}/${pick.r.s}가 ${lname} ${fmt(pick.rank)}위로 조금 앞서요.`': (
        '`The stat products are within 1%, so they are about the same. If you must pick, ${pick.r.a}/${pick.r.d}/${pick.r.s} is slightly ahead at ${lname} rank ${fmt(pick.rank)}.`',
        '`ステータス積の差が1%以内なので、ほぼ同じです。あえて選ぶなら${pick.r.a}/${pick.r.d}/${pick.r.s}が${lname} ${fmt(pick.rank)}位で少し上です。`'),
    '`스탯 곱 차이가 1% 안쪽이라 거의 같아요. 대신 맞출 레벨까지 별의모래가 ${fmt(other.cost.dust - pick.cost.dust)} 덜 들어서 이쪽이 이득이에요.`': (
        '`The stat products are within 1%, so they are about the same. But this one needs ${fmt(other.cost.dust - pick.cost.dust)} less Stardust to reach its level, so it is the better deal.`',
        '`ステータス積の差が1%以内なので、ほぼ同じです。そのかわり、合わせるレベルまでのほしのすなが${fmt(other.cost.dust - pick.cost.dust)}少なくて済むので、こちらがお得です。`'),
    '`${lname} 4,096가지 중 ${fmt(pick.rank)}위예요. 다음 개체(${second.r.a}/${second.r.d}/${second.r.s}, ${fmt(second.rank)}위)보다 스탯 곱이 ${((pick.sp / second.sp - 1) * 100).toFixed(1)}% 높아요.`': (
        '`Rank ${fmt(pick.rank)} of 4,096 in ${lname}. Its stat product is ${((pick.sp / second.sp - 1) * 100).toFixed(1)}% higher than the next one (${second.r.a}/${second.r.d}/${second.r.s}, rank ${fmt(second.rank)}).`',
        '`${lname}で4,096通り中${fmt(pick.rank)}位です。次の個体（${second.r.a}/${second.r.d}/${second.r.s}、${fmt(second.rank)}位）よりステータス積が${((pick.sp / second.sp - 1) * 100).toFixed(1)}%高いです。`'),
    '`${lname} 4,096가지 중 ${fmt(pick.rank)}위예요. 나머지는 CP가 한도를 넘어 못 써요.`': (
        '`Rank ${fmt(pick.rank)} of 4,096 in ${lname}. The others are over the CP cap and cannot be used.`',
        '`${lname}で4,096通り中${fmt(pick.rank)}位です。ほかはCPが上限を超えていて使えません。`'),
    "' 배틀리그는 공격이 낮아야 레벨을 더 올릴 수 있어서 순위가 높아지는 경우가 많아요.'": (
        "' In GO Battle League, lower Attack lets you raise the level further, so it often ranks higher.'",
        "' GOバトルリーグでは、こうげきが低いほどレベルを上げられるので、順位が高くなることが多いです。'"),
    '<span class="tag">지금 Lv ${x.lv}</span>': ('<span class="tag">Now Lv ${x.lv}</span>', '<span class="tag">今 Lv ${x.lv}</span>'),
    '<span class="tag">Lv 20 가정</span>': ('<span class="tag">Lv 20 assumed</span>', '<span class="tag">Lv 20と仮定</span>'),
    'CP 한도를 넘어 못 씀': ('Over the CP cap', 'CP上限を超えて使えない'),
    '<td>${fmt(x.rank)}위<span': ('<td>#${fmt(x.rank)}<span', '<td>${fmt(x.rank)}位<span'),
    '<tr><th>개체</th><th>레이드 성능</th><th>공격</th><th>튼튼함</th><th id="costh">별의모래</th></tr>': (
        '<tr><th>Pokémon</th><th>Raid performance</th><th>Attack</th><th>Bulk</th><th id="costh">Stardust</th></tr>',
        '<tr><th>個体</th><th>レイド性能</th><th>こうげき</th><th>耐久</th><th id="costh">ほしのすな</th></tr>'),
    "'사람이 많으면 빨리 깨는 게 중요해요. 공격을 크게 쳐요.'": (
        "'With many players, winning fast matters most, so Attack is weighted heavily.'", "'人数が多いときは早く倒すことが大事なので、こうげきを重く見ます。'"),
    "'사람이 적으면 기절하고 다시 들어가는 시간이 아까워요. 버티는 힘도 같이 쳐요.'": (
        "'With few players, the time lost fainting and rejoining adds up, so staying power counts too.'", "'人数が少ないと、ひんしになって入り直す時間がもったいないので、耐える力も一緒に見ます。'"),
    '`성능 차이가 1% 안쪽이라 레이드에서 체감되지 않아요. 아무거나 키워도 되고, 굳이 고르면 ${pick.r.a}/${pick.r.d}/${pick.r.s} 쪽이 조금 앞서요.`': (
        '`The difference is within 1%, so you will not feel it in raids. Either is fine; if you must pick, ${pick.r.a}/${pick.r.d}/${pick.r.s} is slightly ahead.`',
        '`性能差が1%以内なので、レイドでは体感できません。どれを育ててもよく、あえて選ぶなら${pick.r.a}/${pick.r.d}/${pick.r.s}の方が少し上です。`'),
    '`성능 차이가 1% 안쪽이라 체감되지 않아요. 대신 레벨 ${S.target}까지 별의모래가 ${fmt(save)} 덜 들어서 이쪽이 이득이에요.`': (
        '`The difference is within 1%, so you will not feel it. But this one needs ${fmt(save)} less Stardust to reach level ${S.target}, so it is the better deal.`',
        '`性能差が1%以内なので体感できません。そのかわり、レベル${S.target}までのほしのすなが${fmt(save)}少なくて済むので、こちらがお得です。`'),
    "'그림자라 주는 피해가 1.2배예요.'": ("'It is a Shadow Pokémon, so it deals 1.2× damage.'", "'シャドウなので与えるダメージが1.2倍です。'"),
    "'공격도 튼튼함도 앞서요.'": ("'Ahead in both Attack and bulk.'", "'こうげきも耐久も上です。'"),
    '`튼튼함은 ${pct(b)}지만 공격이 ${pct(a)} 앞서요.`': ('`Bulk is ${pct(b)}, but Attack is ${pct(a)} ahead.`', '`耐久は${pct(b)}ですが、こうげきが${pct(a)}上です。`'),
    "`공격은 ${pct(a)}지만 튼튼함이 ${pct(b)} 앞서서, ${S.mode === 'few' ? '소수 레이드에선' : '결과적으로'} 이쪽이 나아요.`": (
        "`Attack is ${pct(a)}, but bulk is ${pct(b)} ahead, so ${S.mode === 'few' ? 'in small raids' : 'overall'} this one is better.`",
        "`こうげきは${pct(a)}ですが、耐久が${pct(b)}上なので、${S.mode === 'few' ? '少人数レイドでは' : '結果的に'}こちらが有利です。`"),
    '`다음 개체(${second.r.a}/${second.r.d}/${second.r.s})보다 레이드 성능이 ${gap}% 높아요. ${reason}`': (
        '`Raid performance is ${gap}% higher than the next one (${second.r.a}/${second.r.d}/${second.r.s}). ${reason}`',
        '`次の個体（${second.r.a}/${second.r.d}/${second.r.s}）よりレイド性能が${gap}%高いです。${reason}`'),
    '`별의모래 (→레벨 ${S.target})`': ('`Stardust (→Lv ${S.target})`', '`ほしのすな（→レベル${S.target}）`'),
    "'기준'": ("'Base'", "'基準'"),
}
DESC = ('Pokémon GO IV comparison: pick which of the same Pokémon to power up for raids or GO Battle League, with the Stardust needed.',
        'ポケモンGOの個体値比較。同じポケモンのどれをレイド・GOバトルリーグ用に育てるか、必要なほしのすなと一緒にわかります。')
