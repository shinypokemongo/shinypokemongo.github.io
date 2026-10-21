# 쇼케이스 점수 계산기 /showcase/ 번역표 — _언어판.py가 읽는다. 표의 값은 (영어, 일본어)
# 포켓몬 이름은 도감번호로 게임 문구(pokemon_name_XXXX)에서 찾는다. 지역 폼 앞말은 게임 문구 근거:
#   영어 Galarian Farfetch’d·Hisuian Growlithe(아바타 문구), 일본어 ガラルカモネギ·ヒスイガーディ·アローラナッシー(같은 문구)
# 쇼케이스 = 일본어 게임 문구 「おひろめ」(contest_open_contest·contest_reward_header)
import json, re
from _i18n._이름 import by_key

REGION = {'알로라': ('-a', 'Alolan', 'アローラ'), '가라르': ('-g', 'Galarian', 'ガラル'),
          '히스이': ('-h', 'Hisuian', 'ヒスイ'), '팔데아': ('-p', 'Paldean', 'パルデア')}

# 포켓몬고 게임 문구에 아직 없는 종(1009~1025): 영어 = 포고에셋/_names.json, 일본어 = PokeAPI pokemon-species ja-Hrkt
# (2026-10-21 받음, PokeAPI의 한국어·영어 이름이 우리 표와 17종 모두 같은 것 확인)
LATE = {1009: ('Walking Wake', 'ウネルミナモ'), 1010: ('Iron Leaves', 'テツノイサハ'), 1011: ('Dipplin', 'カミッチュ'),
        1012: ('Poltchageist', 'チャデス'), 1013: ('Sinistcha', 'ヤバソチャ'), 1014: ('Okidogi', 'イイネイヌ'),
        1015: ('Munkidori', 'マシマシラ'), 1016: ('Fezandipiti', 'キチキギス'), 1017: ('Ogerpon', 'オーガポン'),
        1018: ('Archaludon', 'ブリジュラス'), 1019: ('Hydrapple', 'カミツオロチ'), 1020: ('Gouging Fire', 'ウガツホムラ'),
        1021: ('Raging Bolt', 'タケルライコ'), 1022: ('Iron Boulder', 'テツノイワオ'), 1023: ('Iron Crown', 'テツノカシラ'),
        1024: ('Terapagos', 'テラパゴス'), 1025: ('Pecharunt', 'モモワロウ')}

def _data(src, li):
    a = src.index('const DATA = ') + len('const DATA = ')
    b = src.index(';\n', a)
    rows = json.loads(src[a:b])
    out = []
    for r in rows:
        dex, ko = r[0], r[1]
        base = (by_key(f'pokemon_name_{dex:04d}')[1 + li] or LATE.get(dex, ('', ''))[li]).strip()
        if not base:
            raise SystemExit(f'이름 없음: {dex} {ko}')
        suf, pre = '', ''
        if ' ' in ko:
            reg = ko.split(' ')[0]
            suf = REGION[reg][0]
            pre = REGION[reg][1 + li]
        name = (f'{pre} {base}' if li == 0 else f'{pre}{base}') if pre else base
        # 끝에 [아이콘 접미사, 정렬·검색용 원래 이름]을 붙인다(영어 이름엔 띄어쓰기가 있어 한국어판처럼 공백으로 못 가른다)
        out.append(r[:1] + [name] + r[2:6] + [suf, base])
    return src[:a] + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + src[b:]

# 글자 순 목록: 영어는 첫 글자 A~Z, 일본어는 五十音 행
PICK_EN = '''  const KANA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
  const choOf = (n) => { const c = baseName(n).normalize("NFD")[0].toUpperCase(); return KANA.includes(c) ? c : "Z"; };'''
PICK_JA = '''  const KANA = ["ア", "カ", "サ", "タ", "ナ", "ハ", "マ", "ヤ", "ラ", "ワ"];
  const ROWS = ["アイウエオァィゥェォ", "カキクケコ", "サシスセソ", "タチツテトッ", "ナニヌネノ", "ハヒフヘホ", "マミムメモ", "ヤユヨャュョ", "ラリルレロ", "ワヲン"];
  const choOf = (n) => { const c = baseName(n).normalize("NFD")[0]; const i = ROWS.findIndex((r) => r.includes(c)); return KANA[i < 0 ? 0 : i]; };'''

def extra(src, li):
    src = _data(src, li)
    loc = ('en', 'ja')[li]
    # 지역 폼 아이콘 접미사·원래 이름은 데이터 끝 두 칸에서
    src = re.sub(r'  const SUF = \{[^\n]*\n', '', src)
    src = src.replace('const icon = (r) => `mon/${r[0]}${r[1].includes(" ") ? SUF[r[1].split(" ")[0]] : ""}.webp`;',
                      'const icon = (r) => `mon/${r[0]}${r[6]}.webp`;')
    src = src.replace('const baseName = (n) => n.slice(n.lastIndexOf(" ") + 1);',
                      'const baseName = (n) => (byName.get(n) || [])[7] || n;')
    a = src.index('  const CHO = [')
    b = src.index('\n', src.index('  const choOf = (n) =>')) + 1
    src = src[:a] + (PICK_EN, PICK_JA)[li] + '\n' + src[src.index('  const genOf', a):]
    # 위에서 baseName 정의 줄까지 지웠으니 다시 넣는다
    src = src.replace('  const genOf =', '  const baseName = (n) => (byName.get(n) || [])[7] || n;\n  const genOf =', 1)
    src = src.replace('localeCompare(baseName(y[1]), "ko") || x[1].localeCompare(y[1], "ko")',
                      f'localeCompare(baseName(y[1]), "{loc}") || x[1].localeCompare(y[1], "{loc}")')
    return src

def post(src, li):
    # 기본 예시(에레키블)
    ele = by_key('pokemon_name_0466')[1 + li]
    return src.replace('value="에레키블"', f'value="{ele}"').replace('(예: 에레키블)', f'(e.g. {ele})' if li == 0 else f'（例：{ele}）')

TABLE = {
    '<title>이로치수집가 쇼케이스 계산기</title>': ('<title>Showcase Score Calculator · Shiny Collector Tools</title>', '<title>おひろめスコア計算機 · 色違いコレクター</title>'),
    '포켓몬고 <b>이로치 수집가</b> 도구함': ('Pokémon GO <b>Shiny Collector</b> Tools', 'ポケモンGO <b>色違いコレクター</b> ツール'),
    '포켓몬고 <b>이로치 수집가</b>': ('Pokémon GO <b>Shiny Collector</b>', 'ポケモンGO <b>色違いコレクター</b>'),
    '<span class="here">쇼케이스</span>': ('<span class="here">Showcase</span>', '<span class="here">おひろめ</span>'),
    '<h1>쇼케이스 점수 계산기</h1>': ('<h1>Showcase Score Calculator</h1>', '<h1>おひろめスコア計算機</h1>'),
    '>점수 계산<': ('>Score calculator<', '>スコア計算<'),
    '<label for="mon">포켓몬</label>': ('<label for="mon">Pokémon</label>', '<label for="mon">ポケモン</label>'),
    'placeholder="이름 입력 ': ('placeholder="Type a name ', 'placeholder="名前を入力'),
    '>목록에서 고르기<': ('>Pick from list<', '>リストから選ぶ<'),
    'aria-label="이름이 비슷한 포켓몬"': ('aria-label="Similar names"', 'aria-label="似た名前のポケモン"'),
    'aria-label="목록 나누는 기준"': ('aria-label="Group by"', 'aria-label="並べ方"'),
    '>세대별<': ('>By generation<', '>世代別<'),
    '>가나다순<': ('>A–Z<', '>五十音順<'),
    'aria-label="묶음 고르기"': ('aria-label="Pick a group"', 'aria-label="グループを選ぶ"'),
    '<label for="h">키 (m)</label>': ('<label for="h">Height (m)</label>', '<label for="h">高さ (m)</label>'),
    '<label for="w">몸무게 (kg)</label>': ('<label for="w">Weight (kg)</label>', '<label for="w">重さ (kg)</label>'),
    '<label for="a">공격</label>': ('<label for="a">Attack</label>', '<label for="a">こうげき</label>'),
    '<label for="d">방어</label>': ('<label for="d">Defense</label>', '<label for="d">ぼうぎょ</label>'),
    ' 크기에 XXL이라고 떠요 ': (' Its size shows XXL ', ' サイズにXXLと表示される '),
    '키·몸무게는 포켓몬 정보 화면, 개체값은 평가 화면의 값을 그대로 넣으세요.': (
        'Enter height and weight from the Pokémon info screen, and IVs from the appraisal screen, exactly as shown.',
        '高さ・重さはポケモンの詳細画面、個体値はポケモン評価の画面の値をそのまま入れてください。'),
    'aria-label="계산 결과"': ('aria-label="Result"', 'aria-label="計算結果"'),
    '0<small>점</small>': ('0<small>pts</small>', '0<small>点</small>'),
    '<span>키</span>': ('<span>Height</span>', '<span>高さ</span>'),
    '<span>몸무게</span>': ('<span>Weight</span>', '<span>重さ</span>'),
    '<span>개체값</span>': ('<span>IVs</span>', '<span>個体値</span>'),
    '<span>XXL 보너스</span>': ('<span>XXL bonus</span>', '<span>XXLボーナス</span>'),
    'aria-label="더 보기"': ('aria-label="More"', 'aria-label="もっと見る"'),
    '<b>쇼케이스, 영상으로 보기</b><span>점수 구조·참가 규칙·메달 보상까지</span>': (
        '<b>Watch the video (Korean)</b><span>How scoring, entry rules and medal rewards work</span>',
        '<b>動画で見る（韓国語）</b><span>スコアの仕組み・参加ルール・メダル報酬まで</span>'),
    '<b>한 장으로 보는 쇼케이스</b><span>블로그에서 저장해 두고 보기</span>': (
        '<b>Showcases on one page (Korean)</b><span>Save it from the blog</span>',
        '<b>1枚でわかるおひろめ（韓国語）</b><span>ブログで保存して見る</span>'),
    '>점수는 이렇게 나와요<': ('>How the score works<', '>スコアの決まり方<'),
    '만점은 1,178점. 게임 데이터(CONTEST_SETTINGS)에 적힌 배분 그대로입니다.': (
        'The maximum is 1,178 points, split exactly as written in the game data (CONTEST_SETTINGS).',
        '満点は1,178点。ゲームデータ（CONTEST_SETTINGS）に書かれた配分そのままです。'),
    '800<small>키</small>': ('800<small>Height</small>', '800<small>高さ</small>'),
    '그 포켓몬이 가질 수 있는 <b>가장 큰 키</b>에 얼마나 가까운지. 가장 큰 키는 도감 키의 1.55배·1.75배·2배 중 하나로 종마다 정해져 있어요. 점수의 거의 전부라 쇼케이스는 사실상 키 싸움입니다.': (
        'How close it is to the <b>largest height</b> that Pokémon can have. That maximum is 1.55×, 1.75× or 2× the Pokédex height, fixed per species. It is almost the whole score, so a Showcase is really a height contest.',
        'そのポケモンがなれる<b>最大の高さ</b>にどれだけ近いか。最大の高さは図鑑の高さの1.55倍・1.75倍・2倍のどれかで、種類ごとに決まっています。スコアのほとんどなので、おひろめは実質的に高さ勝負です。'),
    '150<small>몸무게</small>': ('150<small>Weight</small>', '150<small>重さ</small>'),
    '그 포켓몬의 최대 몸무게에 얼마나 가까운지. 최대 몸무게 = 도감 몸무게 × (키 배율 + 0.5).': (
        'How close it is to that Pokémon\'s maximum weight. Maximum weight = Pokédex weight × (height multiplier + 0.5).',
        'そのポケモンの最大の重さにどれだけ近いか。最大の重さ = 図鑑の重さ × (高さの倍率 + 0.5)。'),
    '50<small>개체값</small>': ('50<small>IVs</small>', '50<small>個体値</small>'),
    '세 값의 합 ÷ 45 × 50. 100%여도 50점이라 비중이 작아요.': (
        'Sum of the three IVs ÷ 45 × 50. Even a 100% Pokémon only gets 50 points, so it matters little.',
        '3つの値の合計 ÷ 45 × 50。100%でも50点なので比重は小さめです。'),
    '크기가 XXL이면 따로 더해져요. XXL이 아니면 아무리 커도 1,000점을 못 넘습니다.': (
        'Added separately when the size is XXL. Without XXL, no Pokémon can pass 1,000 points however big it is.',
        'サイズがXXLなら別に加算されます。XXLでなければ、どんなに大きくても1,000点を超えません。'),
    '±3<small>오차</small>': ('±3<small>Margin</small>', '±3<small>誤差</small>'),
    '화면의 키·몸무게는 소수 둘째 자리에서 반올림된 값이라, 점수는 몇 점 범위로만 맞힐 수 있어요. 타입 쇼케이스도 종마다 자기 기준으로 계산해서 작은 종과 큰 종이 공평하게 붙습니다.': (
        'The height and weight on screen are rounded to two decimals, so the score can only be pinned down to a range of a few points. Type Showcases also score each species against its own limits, so small and large species compete fairly.',
        '画面の高さ・重さは小数第2位で四捨五入された値なので、スコアは数点の幅でしか当てられません。タイプ別のおひろめも種類ごとの基準で計算するので、小さい種類と大きい種類が公平に競えます。'),
    '내 포켓몬, 쇼케이스 <em>몇 점</em>일까': ('How many points will my Pokémon <em>score</em>?', 'わたしのポケモン、おひろめで<em>何点</em>？'),
    '포켓몬을 고르고 키·몸무게·개체값을 넣으면 점수를 계산합니다. 점수 공식은 게임 데이터에서 직접 꺼냈고, 실제 쇼케이스 점수 3건과 맞춰 봤어요.': (
        'Pick a Pokémon and enter its height, weight and IVs to get its Showcase score. The formula comes straight from the game data and was checked against 3 real Showcase scores.',
        'ポケモンを選んで高さ・重さ・個体値を入れると、おひろめのスコアを計算します。計算式はゲームデータから直接取り出し、実際のおひろめのスコア3件と照らし合わせました。'),
    '점수 배분·최대 키: Pokémon GO 게임 데이터 (2026.9.1판) · XXL 보너스 178: 실제 쇼케이스 점수 3건 역산 + pokemondb. 특수 폼(오리진·지가르데 등)은 아직 목록에 없어요. 아이콘은 게임 아이콘이고, 포켓몬고에 아직 안 나온 종은 포켓몬 홈 그림으로 대신했습니다. 닌텐도·나이언틱과 무관한 팬 도구입니다.': (
        'Score split and max height: Pokémon GO game data (Sept 1, 2026) · XXL bonus 178: worked back from 3 real Showcase scores + pokemondb. Special forms (Origin, Zygarde, etc.) are not in the list yet. Icons are game icons; species not yet in Pokémon GO use Pokémon HOME art. A fan-made tool, not affiliated with Nintendo or Niantic.',
        'スコア配分・最大の高さ：Pokémon GO ゲームデータ（2026.9.1版）· XXLボーナス178：実際のおひろめのスコア3件から逆算 + pokemondb。特別なフォルム（オリジン・ジガルデなど）はまだリストにありません。アイコンはゲームのアイコンで、ポケモンGOに未登場の種類はPokémon HOMEの絵で代用しています。任天堂・Nianticとは関係のないファン製ツールです。'),
    # 스크립트 안 문구
    '`${i + 1}세대`': ('`Gen ${i + 1}`', '`第${i + 1}世代`'),
    '"목록에 없는 이름이에요. 한글 정식 이름으로 입력해 보세요."': ('"That name is not in the list. Try the official English name."', '"リストにない名前です。正式な日本語名で入力してください。"'),
    '`(${name}은 ${XL}m 넘으면 XXL)` : `(${name}은 XXL이 없어요)`': (
        '`(${name}: XXL above ${XL}m)` : `(${name} has no XXL)`',
        '`（${name}は${XL}mを超えるとXXL）` : `（${name}にはXXLがありません）`'),
    '${no(r)} ${name} · 키 만점 <b>${XX}m</b> · 몸무게 만점 <b>${wMax.toFixed(2)}kg</b>': (
        '${no(r)} ${name} · full-score height <b>${XX}m</b> · full-score weight <b>${wMax.toFixed(2)}kg</b>',
        '${no(r)} ${name} · 高さの満点 <b>${XX}m</b> · 重さの満点 <b>${wMax.toFixed(2)}kg</b>'),
    '`${Math.round(T(p)).toLocaleString()}<small>점</small>`': ('`${Math.round(T(p)).toLocaleString()}<small>pts</small>`', '`${Math.round(T(p)).toLocaleString()}<small>点</small>`'),
    '`화면 반올림 때문에 ${a.toLocaleString()}~${b.toLocaleString()}점 사이`': (
        '`Between ${a.toLocaleString()} and ${b.toLocaleString()} pts because of on-screen rounding`',
        '`画面の四捨五入のため ${a.toLocaleString()}～${b.toLocaleString()}点の間`'),
    '[["키", 800 - p.h], ["몸무게", 150 - p.w], ["개체값", 50 - p.i]]': (
        '[["Height", 800 - p.h], ["Weight", 150 - p.w], ["IVs", 50 - p.i]]',
        '[["高さ", 800 - p.h], ["重さ", 150 - p.w], ["個体値", 50 - p.i]]'),
    'lost.push(["XXL 보너스", 178])': ('lost.push(["XXL bonus", 178])', 'lost.push(["XXLボーナス", 178])'),
    '"거의 만점이에요. 이 포켓몬으로는 더 올릴 데가 없어요."': ('"Almost a perfect score. There is nothing left to gain with this Pokémon."', '"ほぼ満点です。このポケモンではもう伸ばせるところがありません。"'),
    '`가장 많이 흘린 건 ${k}: ${v.toFixed(0)}점. ${k === "키" ? "같은 종에서 더 큰 걸 찾는 게 제일 빨라요." : k === "XXL 보너스" ? "XXL 한 마리가 이 차이를 한 번에 뒤집어요." : k === "몸무게" ? "키가 같다면 더 무거운 쪽이 이겨요." : "개체값은 최대 50점이라 키·몸무게가 먼저예요."}`': (
        '`Most points lost: ${k}, ${v.toFixed(0)} pts. ${k === "Height" ? "Finding a bigger one of the same species is the fastest fix." : k === "XXL bonus" ? "One XXL Pokémon closes this gap in one go." : k === "Weight" ? "At the same height, the heavier one wins." : "IVs are worth 50 points at most, so height and weight come first."}`',
        '`一番多く逃しているのは ${k}：${v.toFixed(0)}点。${k === "高さ" ? "同じ種類でもっと大きい個体を探すのが一番の近道です。" : k === "XXLボーナス" ? "XXLが1匹いればこの差を一気に逆転できます。" : k === "重さ" ? "高さが同じなら重い方が勝ちます。" : "個体値は最大50点なので、高さ・重さが先です。"}`'),
}
DESC = ('Pokémon GO PokéStop Showcase score calculator: enter height, weight and IVs to get the score, using the formula from the game data.',
        'ポケモンGOのポケストップおひろめスコア計算機。高さ・重さ・個体値を入れると、ゲームデータの計算式でスコアがわかります。')
