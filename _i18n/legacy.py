# 레거시 기술 명단 /legacy/ 번역표 — _언어판.py가 읽는다. 표의 값은 (영어, 일본어)
# 포켓몬은 도감번호(pokemon_name_XXXX), 기술은 기술 번호(move_name_XXXX)로 게임 문구에서 찾는다 — 한국어 이름 대조 안 함
import json, re
from _i18n._이름 import by_key, names

TYPES = names('pokemon_type_')
PM, MV = names('pokemon_name_'), names('move_name_')
# 게임 APK 문구가 move_name_0487 에서 끊김. 0488은 PokeMiners Latest Remote 문구(English.txt·Japanese.txt, 2026-10-21)
MOVE_EXTRA = {488: ('Chilling Water', 'ひやみず')}
# 영어·일본어 게임 문구가 아직 없는 기술 — 지어내지 않는다. 게임 데이터 기술 id를 그대로 보이고 「확인 전」 표시
MOVE_PENDING = {490: 'BEAK_BLAST', 491: 'MIND_BLOWN', 494: 'GIGATON_HAMMER', 590: '#590'}
FORMS = {  # 폼 이름 게임 문구: pokedex_info_form_alolan·galarian(대문자라 첫 글자만 크게), form_therian
    '알로라': ('Alolan', 'アローラ'), '가라르': ('Galarian', 'ガラル'), '영물': ('Therian Forme', 'れいじゅうフォルム')}

def _move_name(m, li):
    num = m[8]
    if num in MOVE_EXTRA:
        return MOVE_EXTRA[num][li]
    if num in MOVE_PENDING:
        return MOVE_PENDING[num]
    tr = by_key('move_name_%04d' % num)[1 + li]
    assert tr, f'기술 {num} {m[0]} 게임 문구 없음'
    return ' '.join(tr.split())

def extra(src, li):
    a = src.index('const DATA = ') + len('const DATA = ')
    b = src.index(';\n', a)
    d = json.loads(src[a:b])
    pending = []
    for i, m in enumerate(d['moves']):
        m[0] = _move_name(m, li)
        m[1] = TYPES[m[1]][li]
        if m[8] in MOVE_PENDING:
            pending.append(i)
    for L in d['lines']:
        L['t'] = [TYPES[t][li] for t in L['t']]
        for s in L['s']:
            s[0] = ' '.join(by_key('pokemon_name_%04d' % s[2])[1 + li].split())
            s[1] = FORMS[s[1]][li] if s[1] else ''
    src = src[:a] + json.dumps(d, ensure_ascii=False, separators=(',', ':')) + src[b:]
    # 타입 색 표의 열쇠도 그 언어 타입 이름으로
    t0 = src.index('const TC = {'); t1 = src.index('};', t0)
    tc = src[t0:t1]
    for ko, tr in TYPES.items():
        tc = re.sub(rf'(?<![\w"]){ko}:', f'"{tr[li]}":', tc)
    src = src[:t0] + tc + src[t1:]
    # 「확인 전」은 한글 여부가 아니라 게임 문구가 없는 기술
    src = re.sub(r'const UNCHECKED = new Set\([^\n]*\);', f'const UNCHECKED = new Set({json.dumps(pending)});', src)
    # 영어는 대소문자, 일본어는 히라가나·가타카나 구분 없이 찾기
    src = src.replace('const S = { q:', 'const norm = (x) => x.toLowerCase().replace(/[\\u3041-\\u3096]/g, (c) => String.fromCharCode(c.charCodeAt(0) + 0x60));\n  const S = { q:', 1)
    src = src.replace('const q = S.q.trim();', 'const q = norm(S.q.trim());')
    src = src.replace('return namesOf(L).includes(q) || movesOf(L).some((i) => MOVES[i][0].includes(q));',
                      'return norm(namesOf(L)).includes(q) || movesOf(L).some((i) => norm(MOVES[i][0]).includes(q));')
    # 도구함 첫 화면도 같은 언어판으로
    lang = ('en', 'ja')[li]
    src = src.replace('class="home" href="../"', f'class="home" href="/{lang}/"').replace('<a href="../">도구함</a>', f'<a href="/{lang}/">도구함</a>')
    return src

def _ex(li):
    # 설명에 드는 예시: 뿔카노 → 거대코뿌리 암석포
    return PM['뿔카노'][li], PM['거대코뿌리'][li], MV['암석포'][li]
(RH_E, RP_E, RW_E), (RH_J, RP_J, RW_J) = _ex(0), _ex(1)

TABLE = {
    '<title>이로치수집가 레거시 기술 명단</title>': ('<title>Legacy Moves List · Shiny Collector Tools</title>', '<title>レガシーわざ一覧 · 色違いコレクター</title>'),
    '포켓몬고 <b>이로치 수집가</b> 도구함': ('Pokémon GO <b>Shiny Collector</b> Tools', 'ポケモンGO <b>色違いコレクター</b> ツール'),
    '포켓몬고 <b>이로치 수집가</b>': ('Pokémon GO <b>Shiny Collector</b>', 'ポケモンGO <b>色違いコレクター</b>'),
    '<span class="here">레거시</span>': ('<span class="here">Legacy</span>', '<span class="here">レガシー</span>'),
    '<h1>레거시 기술 명단</h1>': ('<h1>Legacy Moves List</h1>', '<h1>レガシーわざ一覧</h1>'),
    '>찾아보기<': ('>Search<', '>さがす<'),
    'placeholder="포켓몬 이름이나 기술 이름 (예: 뿔카노, 암석포)"': (f'placeholder="Pokémon or move name (e.g. {RH_E}, {RW_E})"', f'placeholder="ポケモン名かわざ名（例：{RH_J}、{RW_J}）"'),
    '"포켓몬 이름이나 기술 이름으로 찾기"': ('"Search by Pokémon or move name"', '"ポケモン名かわざ名でさがす"'),
    '"포켓몬 타입"': ('"Pokémon type"', '"ポケモンのタイプ"'),
    'aria-label="정렬"': ('aria-label="Sort"', 'aria-label="並べ替え"'),
    '>도감순<': ('>Pokédex order<', '>図鑑順<'),
    '>오래 안 나온 순<': ('>Longest wait first<', '>解禁から長い順<'),
    '"보여줄 수치"': ('"Stats to show"', '"表示する数値"'),
    '>레이드·체육관<': ('>Raids & Gyms<', '>レイド・ジム<'),
    '>트레이너 배틀<': ('>Trainer Battles<', '>トレーナーバトル<'),
    '>더 보기</button>': ('>Show more</button>', '>もっと見る</button>'),
    'aria-label="더 보기"': ('aria-label="More"', 'aria-label="もっと見る"'),
    '<b>레거시 기술, 영상으로 보기</b><span>진화 순서 하나로 성능이 갈립니다</span>': (
        '<b>Legacy moves on video (Korean)</b><span>One evolution at the right time changes everything</span>',
        '<b>レガシーわざを動画で（韓国語）</b><span>進化のタイミングひとつで性能が変わります</span>'),
    '<b>한 장으로 보는 정리</b><span>블로그에서 저장해 두고 보기</span>': (
        '<b>One-page summary (Korean)</b><span>Save it from the blog</span>',
        '<b>1枚でわかるまとめ（韓国語）</b><span>ブログで保存して見る</span>'),
    '>알아 두면 좋은 것<': ('>Good to know<', '>知っておくと便利なこと<'),
    '<b>진화하는 순간에 붙습니다</b><div>레거시 기술은 대부분 <b>진화시킬 때</b> 그 자리에서 붙어요. 뿔카노를 들고 있어도 암석포는 거대코뿌리가 돼야 생깁니다. 그래서 이벤트 기간이 지난 뒤에 진화시키면 못 받아요.</div>': (
        f'<b>Added when you evolve</b><div>Most legacy moves are added <b>the moment you evolve</b>. Even if you have a {RH_E}, {RW_E} only appears once it becomes {RP_E}. Evolve after the event ends and you won\'t get it.</div>',
        f'<b>進化した瞬間に覚えます</b><div>レガシーわざの多くは<b>進化させたとき</b>にその場で覚えます。{RH_J}を持っていても、{RW_J}は{RP_J}になってから。だからイベント期間が終わってから進化させてももらえません。</div>'),
    '<b>기술머신이 네 종류입니다</b><div>가방에 <b>기술머신노말 · 기술머신스페셜 · 대단한 기술머신노말 · 대단한 기술머신스페셜</b>이 따로 있어요. 레거시는 「대단한」 쪽으로만 배웁니다. 빠른 공격이면 노말, 스페셜 어택이면 스페셜이에요.</div>': (
        '<b>Four kinds of TMs</b><div>Your bag holds <b>Fast TM · Charged TM · Elite Fast TM · Elite Charged TM</b> separately. Legacy moves can only be learned with the “Elite” ones: Elite Fast TM for Fast Attacks, Elite Charged TM for Charged Attacks.</div>',
        '<b>わざマシンは4種類</b><div>バッグには<b>わざマシン ノーマル・わざマシン スペシャル・すごいわざマシン ノーマル・すごいわざマシン スペシャル</b>が別々にあります。レガシーわざは「すごい」ほうでしか覚えられません。ノーマルアタックならノーマル、スペシャルアタックならスペシャルです。</div>'),
    '<b>교환해도 기술은 그대로</b><div>교환하면 개체값만 다시 정해지고 <b>기술은 유지됩니다.</b> 그래서 개체값이 아쉬운 이로치는 이벤트 안에 진화시켜 레거시를 달아 두는 게 이득이에요.</div>': (
        '<b>Trading keeps the moves</b><div>When you trade, only the IVs are rerolled — <b>the moves stay.</b> So for a shiny with disappointing IVs, it pays to evolve it during the event and lock in the legacy move.</div>',
        '<b>交換してもわざはそのまま</b><div>交換すると個体値だけが決め直され、<b>わざはそのまま残ります。</b>だから個体値がいまひとつの色違いも、イベント中に進化させてレガシーわざを付けておくとお得です。</div>'),
    '<b>언제 풀렸는지도 적어 뒀어요</b><div>커뮤니티데이·연말 총집편 같은 <b>이벤트로 나눠 준 날짜</b>는 마지막으로 풀린 날을 적었습니다. 오래됐을수록 다시 나오기까지 기다려야 한다는 뜻이에요. 2021년 6월보다 전부터 레거시인 것은 이벤트가 아니라 옛 기술 개편으로 남은 것이라 날짜가 없습니다.</div>': (
        '<b>When it was last available</b><div>For moves <b>handed out through events</b> like Community Day and the year-end recap Community Days, the last date is listed. The older it is, the longer the wait for a return. Moves that were already legacy before June 2021 are left over from old move rebalances, not events, so they have no date.</div>',
        '<b>いつ解禁されたかも書いています</b><div>コミュニティデイや年末のまとめイベントのように<b>イベントで配られた日付</b>は、最後に解禁された日を書きました。古いほど、次に出るまで待つことになります。2021年6月より前からレガシーのものは、イベントではなく昔のわざ調整で残ったものなので日付がありません。</div>'),
    '<b>도감에서 직접 확인돼요</b><div>도감 → 그 포켓몬 → <b>배틀 탭</b> 맨 아래에 「대단한 기술머신으로 배울 수 있는 기술」 칸이 있어요. 위력까지 적혀 있습니다.</div>': (
        '<b>Check it in the Pokédex</b><div>Pokédex → the Pokémon → at the bottom of the <b>BATTLE tab</b> there\'s an “ELITE TM ATTACKS” section, with power listed too.</div>',
        '<b>図鑑で直接確認できます</b><div>図鑑 → そのポケモン → <b>バトルタブ</b>のいちばん下に「すごいわざマシンで覚えるわざ」の欄があります。威力も書いてあります。</div>'),
    '이 포켓몬, <em>진화시키면</em> 뭘 배우지': ('What does it learn <em>when it evolves</em>?', 'このポケモン、<em>進化させると</em>何を覚える？'),
    '대단한 기술머신으로만 배울 수 있는 기술을 진화 한 줄씩 묶어 정리했습니다. 뿔카노를 찾아도 거대코뿌리가 암석포를 배운다는 게 같이 나와요. 위력과 에너지는 게임 데이터에 적힌 값 그대로입니다.': (
        f'Moves that can only be learned with Elite TMs, grouped by evolution line. Search for {RH_E} and you\'ll also see that {RP_E} learns {RW_E}. Power and energy are exactly as written in the game data.',
        f'すごいわざマシンでしか覚えられないわざを、進化の系列ごとにまとめました。{RH_J}で探しても、{RP_J}が{RW_J}を覚えることが一緒に出てきます。威力とエネルギーはゲームデータの値そのままです。'),
    '>도구함</a>': ('>Tools</a>', '>ツール</a>'),
    '풀린 날짜는 Serebii 커뮤니티데이 전체 이력(재개최·연말 총집편 포함), "언제부터 레거시인지"는 PokeMiners 에 보관된 게임 데이터 240판(2021-06 ~ 현재)을 대조해 찾았습니다. 기술 한글명은 게임 안 한국어 문구를 그대로 썼어요. 게임에 새 기술이 추가되면 이 명단도 같이 갱신합니다. 닌텐도·나이언틱과 무관한 팬 도구입니다.': (
        'Release dates come from Serebii\'s full Community Day history (including re-runs and year-end recaps); “legacy since when” was found by comparing 240 versions of the game data archived by PokeMiners (2021-06 to now). Pokémon and move names are the game\'s own English text. This list is updated when new moves are added. A fan-made tool, not affiliated with Nintendo or Niantic.',
        '解禁日はSerebiiのコミュニティデイ全履歴（再開催・年末のまとめイベントを含む）、「いつからレガシーか」はPokeMinersに保管されたゲームデータ240版（2021-06〜現在）を照らし合わせて調べました。ポケモン名・わざ名はゲーム内の日本語テキストのままです。ゲームに新しいわざが追加されたら、この一覧も更新します。任天堂・Nianticとは関係のないファン製ツールです。'),
    # 스크립트 안 문구
    'return "이번 달";': ('return "this month";', 'return "今月";'),
    'return `${mo}개월 전`;': ('return `${mo} mo ago`;', 'return `${mo}か月前`;'),
    'return m ? `${y}년 ${m}개월 전` : `${y}년 전`;': ('return m ? `${y} yr ${m} mo ago` : `${y} yr ago`;', 'return m ? `${y}年${m}か月前` : `${y}年前`;'),
    '`<span class="when">마지막으로 풀린 때 <b>${w[1]}</b> <span class="ago">(${ago(w[1])})</span>${w[2] > 1 ? ` · 지금까지 ${w[2]}번` : ""}</span>`': (
        '`<span class="when">Last available <b>${w[1]}</b> <span class="ago">(${ago(w[1])})</span>${w[2] > 1 ? ` · ${w[2]} times so far` : ""}</span>`',
        '`<span class="when">最後の解禁 <b>${w[1]}</b> <span class="ago">（${ago(w[1])}）</span>${w[2] > 1 ? ` · これまで${w[2]}回` : ""}</span>`'),
    '`<span class="when"><b>${w[1]}</b> ~ <b>${w[2]}</b> 사이에 레거시가 됐어요</span>`': (
        '`<span class="when">Became legacy between <b>${w[1]}</b> and <b>${w[2]}</b></span>`',
        '`<span class="when"><b>${w[1]}</b>〜<b>${w[2]}</b>のあいだにレガシーになりました</span>`'),
    '`<span class="when old">${OLDEST.slice(0, 4)}년 ${+OLDEST.slice(5, 7)}월 전부터 레거시예요 · 이벤트가 아니라 옛 기술 개편으로 남은 것</span>`': (
        '`<span class="when old">Legacy since before ${OLDEST.slice(0, 7)} · left over from an old move rebalance, not an event</span>`',
        '`<span class="when old">${OLDEST.slice(0, 4)}年${+OLDEST.slice(5, 7)}月より前からレガシー · イベントではなく昔のわざ調整で残ったもの</span>`'),
    '.join(" · ")} 이(가) 배워요</span>': ('.join(" · ")} can learn</span>', '.join(" · ")} が覚える</span>'),
    '대단한 기술머신${m[2] ? "스페셜" : "노말"}': ('${m[2] ? "Elite Charged TM" : "Elite Fast TM"}', '${m[2] ? "すごいわざマシン スペシャル" : "すごいわざマシン ノーマル"}'),
    "'<span class=\"chk\">한글명 확인 전</span>'": ("'<span class=\"chk\">name not in game text yet</span>'", "'<span class=\"chk\">名称未確認</span>'"),
    '`<span>위력 <b>${m[6]}</b></span><span>에너지 <b>${m[7]}</b></span>`': ('`<span>Power <b>${m[6]}</b></span><span>Energy <b>${m[7]}</b></span>`', '`<span>威力 <b>${m[6]}</b></span><span>エネルギー <b>${m[7]}</b></span>`'),
    '`<span>위력 <b>${m[3]}</b></span><span>${m[2] ? "에너지" : "에너지 회복"} <b>${m[4]}</b></span><span>시전 <b>${m[5]}</b>초</span>`': (
        '`<span>Power <b>${m[3]}</b></span><span>${m[2] ? "Energy" : "Energy gain"} <b>${m[4]}</b></span><span>Duration <b>${m[5]}</b>s</span>`',
        '`<span>威力 <b>${m[3]}</b></span><span>${m[2] ? "エネルギー" : "エネルギー回復"} <b>${m[4]}</b></span><span>発動 <b>${m[5]}</b>秒</span>`'),
    '[["", "전부"]': ('[["", "All"]', '[["", "すべて"]'),
    '`진화 <b>${r.length}</b>줄 · 레거시를 배우는 포켓몬 <b>${nmon}</b>마리 · 기술 <b>${npair}</b>개`': (
        '`<b>${r.length}</b> evolution lines · <b>${nmon}</b> Pokémon with legacy moves · <b>${npair}</b> moves`',
        '`進化の系列 <b>${r.length}</b> · レガシーわざを覚えるポケモン <b>${nmon}</b>匹 · わざ <b>${npair}</b>個`'),
    '찾는 이름이 없어요. 포켓몬 이름이나 기술 이름으로 찾아 보세요.': ('No match. Try a Pokémon or move name.', '見つかりませんでした。ポケモン名かわざ名でさがしてみてください。'),
    '`더 보기 (${r.length - S.limit}줄 남음)`': ('`Show more (${r.length - S.limit} lines left)`', '`もっと見る（残り${r.length - S.limit}系列）`'),
    '`Pokémon GO 게임 데이터(eliteQuickMove·eliteCinematicMove 전수) 기준 ${LINES.length}줄 · 기술 ${all}개. 위력·에너지·시전 시간은 데이터에 적힌 값 그대로입니다.`': (
        '`Based on every eliteQuickMove / eliteCinematicMove entry in the Pokémon GO game data: ${LINES.length} lines · ${all} moves. Power, energy and duration are exactly as written in the data.`',
        '`Pokémon GOのゲームデータ（eliteQuickMove・eliteCinematicMove全件）をもとに ${LINES.length}系列 · わざ${all}個。威力・エネルギー・発動時間はデータの値そのままです。`'),
}
DESC = ('Pokémon GO legacy moves list: every move learnable only with an Elite TM, grouped by evolution line, with when each was last available.',
        'ポケモンGOのレガシーわざ一覧。すごいわざマシンでしか覚えられないわざを進化の系列ごとにまとめ、最後に解禁された日も載せています。')
