# 포켓몬 교환 리스트 /trade/ 번역표 — _언어판.py가 읽는다. 표의 값은 (영어, 일본어)
# 데이터(DATA) 속 이름은 extra에서 바꾼다:
#   포켓몬 이름 = 게임 문구 pokemon_name_XXXX (없으면 포고에셋/_names.json 영어)
#   폼 이름 = 게임 문구 form_<종>_<폼> → form_<폼> → 지역 폼은 pokedex_info_form_*
#   코스튬 이름 = 게임에 이름이 없어 그림 파일 이름을 풀어 쓴 것(한국어판도 같음, 발밑에 안내) — 아래 TOKEN 표
#   배경 이름 = 포고에셋/배경/_배경.json 의 name(Bulbapedia 영어). 일본어 배경 이름은 자료가 없어 영어 그대로
import json, re, sys, unicodedata
from pathlib import Path
from ._이름 import _load

ASSET = Path(r'C:\Users\user\포고에셋')
L = lambda i: (_load('english'), _load('japanese'))[i]
KO = lambda: _load('korean')
norm = lambda s: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower())

# 지역 폼: 게임 도감 문구 pokedex_info_form_*
REGION = {'ALOLA': 'pokedex_info_form_alolan', 'GALARIAN': 'pokedex_info_form_galarian', 'HISUIAN': 'pokedex_info_form_hisuian', 'PALDEA': 'pokedex_info_form_paldean'}
# 일반 폼 키(form_<폼>)가 다른 포켓몬 것이라 틀리는 경우 — 직접 키를 댄다
FIXED_KEY = {(931, 'WHITE'): 'form_squakabilly_white', (413, 'WORMADAM_SANDY'): 'form_burmy_sandy', (413, 'WORMADAM_TRASH'): 'form_burmy_trash', (413, 'WORMADAM_PLANT'): 'form_burmy_plant'}
# 영상·게임 문구로 확인한 코스튬 이름 (한국어판 SPECIAL과 짝)
SPECIAL = {'K_2026_A_01': ('Hanbok 2026', '韓服 2026'), 'GOGGLES_2026': ('Goggles 2026', 'ゴーグル 2026'), 'HORIZONS': ('Captain Hat', 'キャプテン帽'), 'JEJU': ('Jeju', '済州'),
           'UNOWN_EXCLAMATION_POINT': ('!', '!'), 'UNOWN_QUESTION_MARK': ('?', '?')}
# 아이돌·하드록 피카츄: 게임 문구 branch_pop_star_title_short / branch_rock_star_title_short
PHRASE = {'ROCK_STAR': ('Rock Star', 'ハードロック'), 'POP_STAR': ('Pop Star', 'アイドル'), 'ONE_YEAR': ('1st', '1'),
          'FIFTY_PERCENT': ('50%', '50%'), 'TEN_PERCENT': ('10%', '10%'), 'EAST_SEA': ('East Sea', 'ひがしのうみ'), 'WEST_SEA': ('West Sea', 'にしのうみ')}
# 그림 파일 이름 낱말 → (영어, 일본어). 지역 이름은 게임 문구 badge_pokedex_entries_* 그대로
TOKEN = {'ANNIVERSARY': ('Anniversary', '周年'), 'FALL': ('Fall', '秋'), 'AUTUMN': ('Fall', '秋'), 'WINTER': ('Winter', '冬'), 'SPRING': ('Spring', '春'), 'SUMMER': ('Summer', '夏'),
         'HOLIDAY': ('Holiday', 'ホリデー'), 'HALLOWEEN': ('Halloween', 'ハロウィン'), 'FASHION': ('Fashion', 'ファッション'), 'GOFEST': ('GO Fest', 'GO Fest'), 'GOTOUR': ('GO Tour', 'GO Tour'),
         'WCS': ('World Championships', 'ワールドチャンピオンシップス'), 'SAFARI': ('Safari Zone', 'サファリゾーン'),
         'KANTO': ('Kanto', 'カントー'), 'JOHTO': ('Johto', 'ジョウト'), 'HOENN': ('Hoenn', 'ホウエン'), 'SINNOH': ('Sinnoh', 'シンオウ'),
         'JAN': ('Jan', '1月'), 'FEB': ('Feb', '2月'), 'APRIL': ('Apr', '4月'), 'MAY': ('May', '5月'), 'NOVEMBER': ('Nov', '11月'),
         'TCG': ('TCG', 'カードゲーム'), 'WILDAREA': ('Wild Area', 'ワイルドエリア'), 'COSTUME': ('Costume', 'コスチューム'),
         'RED': ('Red', '赤'), 'BLUE': ('Blue', '青'), 'YELLOW': ('Yellow', '黄'), 'ORANGE': ('Orange', 'オレンジ'), 'GREEN': ('Green', '緑'),
         'FLYING': ('Flying', 'ひこう'), 'UNOWN': ('', ''), 'GALARIAN': ('Galarian', 'ガラル')}
# 일본어 자료가 없는 낱말은 영어 그대로 쓴다 — 여기 모아 보고한다
JA_FALLBACK = set()


def _form_name(dex, code, li):
    en = _load('english')
    if code in REGION:
        v = L(li)[REGION[code]].strip()
        return v.capitalize() if li == 0 else v
    sp = norm(en.get(f'pokemon_name_{dex:04d}', ''))
    for k in ([FIXED_KEY[(dex, code)]] if (dex, code) in FIXED_KEY else []) + [f'form_{sp}_{code.lower()}', f'form_{code.lower()}']:
        if k in KO() and k in L(li):
            return ' '.join(L(li)[k].split())
    return None


def label(mid, dex, li):
    f = re.search(r'-f([A-Za-z0-9_]+)', mid); c = re.search(r'-c([A-Za-z0-9_]+)', mid)
    parts = []
    for key in (f and f.group(1), c and c.group(1)):
        if not key: continue
        key = key.replace('_NOEVOLVE', '')
        if key in SPECIAL: parts.append(SPECIAL[key][li]); continue
        if key == 'GALARIAN_STANDARD': parts.append(_form_name(dex, 'GALARIAN', li)); continue
        if key == 'GALARIAN_ZEN': parts.append(_form_name(dex, 'GALARIAN', li) + ' · ' + _form_name(dex, 'ZEN', li)); continue
        if not re.search(r'20\d\d', key):
            off = _form_name(dex, key, li)
            if off: parts.append(off); continue
        for p, tr in PHRASE.items(): key = key.replace(p, f'<{tr[li]}>')
        words = []
        for tok in re.findall(r'<[^>]*>|[A-Za-z0-9]+', key):
            if tok.startswith('<'): words.append(tok[1:-1])
            elif tok in TOKEN: words.append(TOKEN[tok][li])
            elif tok.isdigit() or len(tok) <= 2: words.append(tok)
            else:
                words.append(tok.capitalize())
                if li == 1: JA_FALLBACK.add(tok.capitalize())
        parts.append(' '.join(w for w in words if w))
    return ' · '.join(parts)


def bg_names():
    table = json.loads((ASSET / '배경/_배경.json').read_text(encoding='utf-8'))
    out = {f'b{i:03d}': e['name'] for i, e in enumerate(table)}
    # _배경.json 뒤에 붙인 달맞이 배경(에셋만들기.py extra) — 게임 문구에 이름이 없어 그림 파일 이름 sb_MidAutumn 그대로
    out[f'b{len(table):03d}'] = 'Mid-Autumn 2026'
    return out


from ._이름 import pokemon

def extra(src, li):
    a = src.index('const DATA = ') + len('const DATA = '); b = src.index(';\n', a)
    d = json.loads(src[a:b])
    lang = L(li); names = json.loads((ASSET / '_names.json').read_text(encoding='utf-8'))
    for m in d['mons']:
        n = pokemon(m[1], li) or names[str(m[1])]['en']
        m[2] = ' '.join(n.split())
        m[3] = label(m[0], m[1], li) if m[3] else ''
    bn = bg_names()
    for g in d['bgs']:
        n = bn[g[0]]
        g[1] = n if isinstance(n, str) else n[li]
    return src[:a] + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + src[b:]


def post(src, li):
    # 영어 이름은 대소문자 없이 찾게
    src = src.replace('const q = S.q.trim();\n    if (q) return MONS.filter((r) => r[2].includes(q) || r[3].includes(q));',
                      'const q = S.q.trim().toLowerCase();\n    if (q) return MONS.filter((r) => r[2].toLowerCase().includes(q) || r[3].toLowerCase().includes(q));')
    src = src.replace('"shinypokemongo.github.io/trade"', '"shinypokemongo.github.io/en/trade"' if li == 0 else '"shinypokemongo.github.io/ja/trade"')
    return src


SM, SJ = 'Spacial Rend, Roar of Time', 'あくうせつだん、ときのほうこう'  # 게임 기술 이름 move_name
TABLE = {
    '<title>이로치수집가 포켓몬 교환 리스트</title>': ('<title>Pokémon Trade List Maker · Shiny Collector Tools</title>', '<title>ポケモン交換リストメーカー · 色違いコレクター</title>'),
    '포켓몬고 <b>이로치 수집가</b> 도구함': ('Pokémon GO <b>Shiny Collector</b> Tools', 'ポケモンGO <b>色違いコレクター</b> ツール'),
    '포켓몬고 <b>이로치 수집가</b>': ('Pokémon GO <b>Shiny Collector</b>', 'ポケモンGO <b>色違いコレクター</b>'),
    '<span class="here">교환</span>': ('<span class="here">Trade</span>', '<span class="here">交換</span>'),
    '<h1>포켓몬 교환 리스트 만들기</h1>': ('<h1>Pokémon Trade List Maker</h1>', '<h1>ポケモン交換リストを作る</h1>'),
    '>교환 리스트<': ('>Trade list<', '>交換リスト<'),
    'aria-label="구해요와 드려요 목록을 담은 교환 리스트 카드. 칸을 누르면 고칠 수 있습니다."': ('aria-label="Trade list card with Looking for and Can give lists. Tap a slot to edit it."', 'aria-label="ほしい・あげられるリストの交換リストカード。マスをタップすると編集できます。"'),
    '>이미지로 저장<': ('>Save as image<', '>画像で保存<'),
    'aria-label="칸 크기"': ('aria-label="Slot size"', 'aria-label="マスの大きさ"'),
    '>크게<': ('>Large<', '>大<'), '>보통<': ('>Medium<', '>中<'), '>작게<': ('>Small<', '>小<'),
    '고른 칸 빼기': ('Remove selected', '選んだマスを外す'),
    '전부 지우기': ('Clear all', 'すべて消す'),
    'aria-label="이로치 또는 일반"': ('aria-label="Shiny or normal"', 'aria-label="色違いか通常か"'),
    '<button type="button" data-v="1">이로치</button><button type="button" data-v="0">일반</button>': ('<button type="button" data-v="1">Shiny</button><button type="button" data-v="0">Normal</button>', '<button type="button" data-v="1">色違い</button><button type="button" data-v="0">通常</button>'),
    '칸 아래에 적을 말 (기술 이름 등, 비워도 돼요)': ('Text under the slot (move name etc., optional)', 'マスの下に書く文字（わざの名前など、空でもOK）'),
    'placeholder="예: 공간절단, 시간의포효"': (f'placeholder="e.g. {SM}"', f'placeholder="例: {SJ}"'),
    '<button type="button">레거시 기술</button><button type="button">배경 있음</button>': ('<button type="button">Legacy move</button><button type="button">Background</button>', '<button type="button">レガシー技</button><button type="button">背景あり</button>'),
    '`배경: ${BGM.get(t.bg)[1]}` : "배경 고르기"': ('`Background: ${BGM.get(t.bg)[1]}` : "Pick a background"', '`背景: ${BGM.get(t.bg)[1]}` : "背景を選ぶ"'),
    '>배경 고르기<': ('>Pick a background<', '>背景を選ぶ<'),
    'aria-label="앞으로 옮기기"': ('aria-label="Move earlier"', 'aria-label="前へ移動"'),
    'aria-label="뒤로 옮기기"': ('aria-label="Move later"', 'aria-label="後ろへ移動"'),
    '고른 포켓몬이 들어갈 곳': ('Add picked Pokémon to', '選んだポケモンの入れ先'),
    'aria-label="고른 포켓몬이 들어갈 목록"': ('aria-label="List that picked Pokémon go into"', 'aria-label="選んだポケモンが入るリスト"'),
    '<button type="button" data-v="want">구해요</button><button type="button" data-v="give">드려요</button>': ('<button type="button" data-v="want">Looking for</button><button type="button" data-v="give">Can give</button>', '<button type="button" data-v="want">ほしい</button><button type="button" data-v="give">あげられる</button>'),
    '카드 위에 적을 말 (닉네임, 지역 등. 비워도 돼요)': ('Text at the top of the card (nickname, area, etc. Optional)', 'カードの上に書く文字（ニックネーム・地域など。空でもOK）'),
    'placeholder="예: 이로치수집가 · 서울 · 100km 이상 환영"': ('placeholder="e.g. ShinyCollector · Seoul · 100km+ welcome"', 'placeholder="例: 色違いコレクター · 東京 · 100km以上歓迎"'),
    '>포켓몬 추가<': ('>Add Pokémon<', '>ポケモンを追加<'),
    '>고른 칸의 배경<': ('>Background for slot<', '>選んだマスの背景<'),
    '목록에 보일 그림 · 새로 넣을 칸': ('Pictures in the list · new slots', 'リストの絵 · 新しく入れるマス'),
    'aria-label="목록에 보일 그림"': ('aria-label="Pictures in the list"', 'aria-label="リストの絵"'),
    'placeholder="이름으로 찾기 (예: 펄기아, 한복, 할로윈)" aria-label="포켓몬 이름으로 찾기"': ('placeholder="Search by name (e.g. Palkia, Hanbok, Halloween)" aria-label="Search Pokémon by name"', 'placeholder="名前で探す（例: パルキア、韓服、ハロウィン）" aria-label="ポケモンの名前で探す"'),
    '>더 보기</button>': ('>Show more</button>', '>もっと見る</button>'),
    'aria-label="더 보기"': ('aria-label="More"', 'aria-label="もっと見る"'),
    '<b>이로치 영상 보러 가기</b><span>한복 피카츄, 고글 파이리, 성도 이로치 100마리</span>': ('<b>Shiny videos (Korean)</b><span>Hanbok Pikachu, Goggles Charmander, 100 Johto shinies</span>', '<b>色違い動画（韓国語）</b><span>韓服ピカチュウ、ゴーグルヒトカゲ、ジョウト色違い100匹</span>'),
    '<b>한 장으로 보는 정리</b><span>블로그에서 저장해 두고 보기</span>': ('<b>One-page guides (Korean)</b><span>Save them from the blog</span>', '<b>1枚まとめ（韓国語）</b><span>ブログで保存して見る</span>'),
    '>알아 두면 좋은 것<': ('>Good to know<', '>知っておくと便利なこと<'),
    '<b>칸 아래 글씨</b><div>공간절단·시간의포효처럼 <b>지금은 배울 수 없는 기술</b>을 가진 포켓몬은 값어치가 달라요. 칸을 누르고 아래에 기술 이름을 적어 두면 한눈에 보입니다. 개체값은 교환하면 새로 정해지니 적을 필요가 없어요.</div>': (
        '<b>Text under slots</b><div>Pokémon with <b>moves they can\'t learn now</b>, like Spacial Rend or Roar of Time, are worth more. Tap a slot and write the move under it so it stands out. No need to write IVs — they are rerolled when you trade.</div>',
        '<b>マスの下の文字</b><div>あくうせつだん・ときのほうこうのように<b>今は覚えられない技</b>を持つポケモンは価値が違います。マスをタップして下に技の名前を書いておくと一目でわかります。個体値は交換すると新しく決まるので書く必要はありません。</div>'),
    '<b>그림이 있다고 나온 건 아니에요</b><div>여기 있는 이로치는 <b>게임 파일에 그림이 들어 있는 것</b> 전부예요. 그림은 이벤트 몇 주 전에 먼저 들어오기도 하고, 들어만 있고 아직 안 풀린 것도 있습니다.</div>': (
        '<b>A picture doesn\'t mean it\'s released</b><div>The shinies here are <b>every shiny that has a picture in the game files</b>. Pictures sometimes arrive weeks before an event, and some are in the files but not released yet.</div>',
        '<b>絵があっても実装済みとは限りません</b><div>ここにある色違いは<b>ゲームファイルに絵が入っているもの</b>すべてです。絵はイベントの数週間前に先に入ることもあり、入っているだけでまだ出ていないものもあります。</div>'),
    '<b>나온 적 있는 배경</b><div>초록 표시는 <b>그 포켓몬이 그 배경으로 나온 기록</b>이 있다는 뜻이에요. 어떤 코스튬이었는지까지는 기록에 없어서 종 단위로만 표시합니다. 「바탕만」은 달·무늬 같은 효과가 게임 안에서 따로 얹히는 배경이라 실제 화면보다 단순하게 보여요.</div>': (
        '<b>Backgrounds it has appeared with</b><div>A green tag means <b>there is a record of that Pokémon appearing with that background</b>. The records don\'t say which costume, so it\'s shown per species. "Base only" backgrounds get extra effects like moons or patterns in the game, so they look simpler here than on screen.</div>',
        '<b>出たことのある背景</b><div>緑の表示は<b>そのポケモンがその背景で出た記録</b>があるという意味です。どのコスチュームだったかまでは記録にないので、種類ごとに表示しています。「下地のみ」は月や模様などの効果がゲーム内で別に重なる背景なので、実際の画面より簡単に見えます。</div>'),
    '<b>내 목록은 이 기기에만</b><div>만든 목록은 이 브라우저에만 저장돼요. 서버로 보내지 않습니다. 다른 기기에서는 처음부터 다시 만들어야 해요.</div>': (
        '<b>Your list stays on this device</b><div>Your list is saved only in this browser and never sent to a server. On another device you\'ll need to make it again.</div>',
        '<b>リストはこの端末だけに</b><div>作ったリストはこのブラウザだけに保存され、サーバーには送られません。ほかの端末では最初から作り直す必要があります。</div>'),
    '<em>구해요·드려요</em>를 한 장으로': ('<em>Looking for · Can give</em> on one card', '<em>ほしい・あげられる</em>を1枚に'),
    '교환 구할 때 글로 길게 쓰는 대신 그림 한 장으로 보여 주세요. 이로치·코스튬을 고르고, 배경이 붙은 개체는 배경까지 입히고, 레거시 기술은 칸 아래에 적으면 됩니다. 서울·인천·제주 같은 한국 배경도 있어요.': (
        'Instead of writing a long post when you look for trades, show it in one picture. Pick shinies and costumes, add backgrounds to the ones that have them, and write legacy moves under the slots. Korean backgrounds like Seoul, Incheon and Jeju are included too.',
        '交換相手を探すとき、長い文章の代わりに1枚の画像で見せましょう。色違い・コスチュームを選び、背景つきの個体は背景も付けて、レガシー技はマスの下に書くだけ。ソウル・仁川・済州など韓国の背景もあります。'),
    '<a href="../">도구함</a>': ('<a href="../">Tools (Korean)</a>', '<a href="../">ツール（韓国語）</a>'),
    '포켓몬 그림: Pokémon GO 게임 파일(PokeMiners 정리본). 배경 그림과 "나온 적 있음" 기록: Bulbapedia · pogokit.com 정리본. 폼·코스튬 이름은 게임 파일의 이름을 풀어 쓴 것이라 공식 명칭과 다를 수 있어요. 닌텐도·나이언틱과 무관한 팬 도구입니다.': (
        'Pokémon pictures: Pokémon GO game files (compiled by PokeMiners). Background pictures and "has appeared" records: Bulbapedia · pogokit.com. Costume names are spelled out from the game file names and may differ from official names. A fan-made tool, not affiliated with Nintendo or Niantic.',
        'ポケモンの絵：Pokémon GOゲームファイル（PokeMiners整理版）。背景の絵と「出たことあり」の記録：Bulbapedia・pogokit.com。コスチューム名はゲームファイルの名前をもとに書いたもので、公式名と異なる場合があります。背景名は英語表記です。任天堂・Nianticとは関係のないファン製ツールです。'),
    # 스크립트 안 문구
    '[["want", "구해요", "#6BF2A6"], ["give", "드려요", "#FFD86B"]]': ('[["want", "Looking for", "#6BF2A6"], ["give", "Can give", "#FFD86B"]]', '[["want", "ほしい", "#6BF2A6"], ["give", "あげられる", "#FFD86B"]]'),
    'ctx.fillText("포켓몬 교환 리스트", CW / 2, 96)': ('ctx.fillText("Pokémon Trade List", CW / 2, 96)', 'ctx.fillText("ポケモン交換リスト", CW / 2, 96)'),
    '"아래에서 포켓몬을 고르면 여기에 들어가요" : "비어 있어요"': ('"Pick Pokémon below to add them here" : "Empty"', '"下でポケモンを選ぶとここに入ります" : "空です"'),
    'ctx.fillText("포켓몬고 이로치 수집가", PAD, CH - 34)': ('ctx.fillText("Pokémon GO Shiny Collector", PAD, CH - 34)', 'ctx.fillText("ポケモンGO 色違いコレクター", PAD, CH - 34)'),
    '[["c", "코스튬"], ["l", "전설·환상"], ...GENS.map((_, i) => [String(i), `${i + 1}세대`])]': ('[["c", "Costumes"], ["l", "Legendary · Mythical"], ...GENS.map((_, i) => [String(i), `Gen ${i + 1}`])]', '[["c", "コスチューム"], ["l", "伝説・幻"], ...GENS.map((_, i) => [String(i), `第${i + 1}世代`])]'),
    '`${S.q ? `"${S.q}" ` : ""}${rows.length}개 · 누르면 「${S.target === "want" ? "구해요" : "드려요"}」에 들어가요`': (
        '`${S.q ? `"${S.q}" ` : ""}${rows.length} · tap to add to "${S.target === "want" ? "Looking for" : "Can give"}"`',
        '`${S.q ? `「${S.q}」 ` : ""}${rows.length}件 · タップで「${S.target === "want" ? "ほしい" : "あげられる"}」に入ります`'),
    '`더 보기 (${rows.length - S.limit}개 남음)`': ('`Show more (${rows.length - S.limit} left)`', '`もっと見る（残り${rows.length - S.limit}件）`'),
    '"먼저 위 카드에서 칸을 눌러 고르세요."': ('"First tap a slot on the card above."', '"まず上のカードでマスをタップして選んでください。"'),
    '`${r[2]} 나온 적 있는 배경 ${real.length}`': ('`${r[2]} has appeared with ${real.length}`', '`${r[2]}が出た背景 ${real.length}`'),
    '`한국 ${BGS.filter((b) => b[3]).length}`': ('`Korea ${BGS.filter((b) => b[3]).length}`', '`韓国 ${BGS.filter((b) => b[3]).length}`'),
    '`특별 ${BGS.filter((b) => b[2] === "특별").length}`': ('`Special ${BGS.filter((b) => b[2] === "특별").length}`', '`スペシャル ${BGS.filter((b) => b[2] === "특별").length}`'),
    '`지역 ${BGS.filter((b) => b[2] === "지역").length}`': ('`Location ${BGS.filter((b) => b[2] === "지역").length}`', '`ロケーション ${BGS.filter((b) => b[2] === "지역").length}`'),
    '"종 단위 기록이에요. 어떤 코스튬이었는지까지는 알 수 없어요." : `${rows.length}장`': ('"Records are per species — the costume isn\'t known." : `${rows.length}`', '"種類ごとの記録です。どのコスチュームだったかまではわかりません。" : `${rows.length}枚`'),
    '>배경 없음</button>': ('>No background</button>', '>背景なし</button>'),
    '"이로치로 나옴" : "나온 적 있음"': ('"Appeared shiny" : "Has appeared"', '"色違いで出た" : "出たことあり"'),
    '<span class="tag plain">바탕만</span>': ('<span class="tag plain">Base only</span>', '<span class="tag plain">下地のみ</span>'),
    '"「드려요」로" : "「구해요」로"': ('"Move to Can give" : "Move to Looking for"', '"「あげられる」へ" : "「ほしい」へ"'),
    'toast("한 장에 96칸까지만 넣을 수 있어요")': ('toast("Up to 96 slots per card")', 'toast("1枚に入るのは96マスまでです")'),
    'toast(`「${S.target === "want" ? "구해요" : "드려요"}」에 넣었어요`)': ('toast(`Added to "${S.target === "want" ? "Looking for" : "Can give"}"`)', 'toast(`「${S.target === "want" ? "ほしい" : "あげられる"}」に入れました`)'),
    '"한 번 더 누르면 지워요"': ('"Tap again to clear"', '"もう一度押すと消えます"'),
    'toast("전부 지웠어요")': ('toast("Cleared")', 'toast("すべて消しました")'),
    'toast("먼저 포켓몬을 골라 주세요")': ('toast("Pick some Pokémon first")', 'toast("先にポケモンを選んでください")'),
    '"포켓몬_교환_리스트.png"': ('"pokemon_trade_list.png"', '"ポケモン交換リスト.png"'),
    'toast("이미지를 저장했어요")': ('toast("Image saved")', 'toast("画像を保存しました")'),
    '"포켓몬 교환"), document.fonts.load(\'700 26px "IBM Plex Sans KR"\', "공간절단")': ('"Pokemon Trade"), document.fonts.load(\'700 26px "IBM Plex Sans KR"\', "Spacial Rend")', '"ポケモン交換"), document.fonts.load(\'700 26px "IBM Plex Sans KR"\', "あくうせつだん")'),
    # 배경 종류: 데이터와 스크립트에서 같은 낱말로 바꾼다
    '"특별"': ('"Special"', '"スペシャル"'),
    '"지역"': ('"Location"', '"ロケーション"'),
}
DESC = ('Make a Pokémon GO trade list image: pick "Looking for" and "Can give" shinies and costumes, add location backgrounds and legacy moves, then save it as one picture.',
        'ポケモンGOの交換リスト画像を作るツール。「ほしい」「あげられる」の色違い・コスチュームを選び、背景やレガシー技を付けて1枚の画像で保存できます。')
