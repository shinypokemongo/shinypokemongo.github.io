# 검색어 검사기 /search/ 번역표 — _언어판.py가 읽는다. 표의 값은 (영어, 일본어)
# 검색 키워드는 언어마다 다르다: 게임 문구 filter_key_* (공용/명칭/i18n_*.json)에서 가져온다
# 한국어판의 "확인됨"은 한국어 폰 실측이라 영어·일본어엔 옮기지 않는다 → 화면에 "게임 문구 기준, 폰 미확인" 노란 상자
# 게임 문구에 검색 키워드로 없는 것(진화 가능·즐겨찾기·파트너·@날씨)은 번역판에서 뺐다 — 추측 금지
# 스크립트는 한국어판 로직을 옮긴 SCRIPT(문구는 T, 키워드는 K)로 통째로 바꾼다. 한국어판 로직을 고치면 여기도 고칠 것
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _i18n._이름 import by_key, names

def kw(key):  # filter_key_* → (영어, 일본어)
    _, en, ja = by_key('filter_key_' + key)
    return (en, ja)

# 키워드 (영어, 일본어). en은 게임 검색창이 대소문자를 안 가리므로 소문자로
W = {
    'shiny': kw('shiny'), 'legend': kw('legendary'), 'myth': kw('mythical'), 'ub': kw('ultra_beasts'),
    'lucky': kw('lucky'), 'shadow': kw('shadow'), 'costume': kw('costume'), 'bg': kw('any_background'),
    'legacy': tuple('@' + x for x in kw('special_move')), 'evolvenew': kw('evolve_to_new'), 'item': kw('evolve_with_item'),
    'quest': kw('evolve_with_quest'), 'tradeevo': kw('can_evolve_with_trading'), 'mega': kw('evolve_mega'),
    'dmax': kw('bread'), 'gmax': kw('dough'), 'defender': kw('defender'), 'traded': kw('traded'),
    'hatched': kw('hatched'), 'purified': kw('purified'), 'raid': kw('raid'), 'research': kw('research'),
    'rocket': kw('rocket'), 'candyxl': kw('candyxl'), 'eggsonly': kw('baby'), 'locbg': kw('location_card'),
    'distance': kw('distance'), 'age': kw('age'), 'year': kw('year'), 'attack': kw('attack'), 'defense': kw('defense'),
}
W = {k: (v[0].lower(), v[1]) for k, v in W.items()}
TYPE_ORDER = ['노말', '불꽃', '물', '풀', '전기', '얼음', '격투', '독', '땅', '비행', '에스퍼', '벌레', '바위', '고스트', '드래곤', '악', '강철', '페어리']
TYPE_NAMES = names('pokemon_type_')

def K(li):
    w = {k: v[li] for k, v in W.items()}
    types = [TYPE_NAMES[t][li].lower() if li == 0 else TYPE_NAMES[t][li] for t in TYPE_ORDER]
    en = li == 0
    D = {  # 키워드 뜻
        'shiny': ('shiny', '色違い'), 'legend': ('legendary', '伝説のポケモン'), 'myth': ('mythical', 'まぼろし'),
        'ub': ('Ultra Beast', 'ウルトラビースト'), 'lucky': ('lucky', 'キラ'), 'shadow': ('shadow', 'シャドウ'),
        'costume': ('costume (event)', 'とくべつ（イベント）'), 'bg': ('has a background', '背景あり'),
        'legacy': ('knows a legacy move', 'レガシー技を覚えている'), 'evolvenew': ('evolving adds a new Pokédex entry', '進化すると図鑑に新しく登録される'),
        'item': ('evolves with an item', 'どうぐで進化する'), 'quest': ('evolves with a condition', '条件で進化する'),
        'tradeevo': ('evolves for fewer or no Candy if traded', '交換すると進化のアメが減る・いらない'), 'mega': ('can Mega Evolve now', '今メガシンカできる'),
        'dmax': ('can Dynamax', 'ダイマックスできる'), 'gmax': ('can Gigantamax', 'キョダイマックスできる'),
        'defender': ('defending a Gym', 'ジムを守っている'), 'traded': ('received in a trade', '交換でもらった'),
        'hatched': ('hatched from an Egg', 'タマゴからかえった'), 'purified': ('purified', 'ライト（リトレーンした）'),
        'raid': ('caught in a raid', 'レイドで捕まえた'), 'research': ('caught from research', 'リサーチで捕まえた'),
        'rocket': ('obtained from Team GO Rocket', 'GOロケット団から手に入れた'), 'candyxl': ('powered up with XL Candy', 'アメXLで強化した'),
        'eggsonly': ('only hatches from Eggs', 'タマゴからだけ出る'), 'locbg': ('has a location background', 'ロケーション背景あり'),
    }
    terms = [[w[k], D[k][li]] for k in D] + [['xxl', 'XXL' if en else 'XXL（とても大きい）'], ['xxs', 'XXS' if en else 'XXS（とても小さい）']]
    one = '0*,1*,2*&' + '&'.join('!' + w[k] for k in ['shiny', 'legend', 'myth', 'ub', 'lucky', 'shadow', 'costume', 'bg', 'legacy']) + '&!#'
    keep = '4*,' + ','.join(w[k] for k in ['shiny', 'lucky', 'legend', 'myth', 'shadow', 'costume', 'bg']) + ',#'
    A, Df, H = w['attack'], w['defense'], 'hp'
    if en:
        recipes = [
            {'id': 'cd', 'label': 'After Community Day', 'steps': [
                ['Evolve first', 'Ones that would add a new Pokédex entry if evolved. Do this before cleaning up.', w['evolvenew'], 'NewDex'],
                ['Check exclusive moves', 'Ones with a legacy move — keep them for trades even with low IVs.', w['legacy'], 'Legacy'],
                ['Clean up today\'s catches', 'Today\'s 0–2 star catches, without shiny, lucky, costume or background ones.', f"{w['age']}0&0*,1*,2*&!{w['shiny']}&!{w['lucky']}&!{w['costume']}&!{w['bg']}", 'TodayClean']]},
            {'id': 'full', 'label': 'Storage full', 'steps': [
                ['Evolve first', 'Fill the Pokédex before transferring.', w['evolvenew'], 'NewDex'],
                ['Transfer candidates', 'Only 0–2 stars, with the valuable ones taken out. Still give it a quick look before transferring.', one, 'Transfer'],
                ['Check what to keep', 'Everything you should keep, at a glance.', keep, 'Keep']]},
            {'id': 'trade', 'label': 'Before trading', 'steps': [
                ['Guaranteed lucky', 'Pokémon caught in 2020 or earlier become guaranteed lucky when traded (45 per person). IVs at least 12, half the Stardust to power up.', f"{w['year']}-2020", 'LuckyTrade'],
                ['3 Candy from a trade', 'Caught more than 100 km apart. Remote-raid legendaries are taken out.', f"{w['distance']}100-&!{w['legend']}", 'Candy3'],
                ['Evolve without Candy', 'Evolve for fewer or no Candy if traded.', w['tradeevo'], 'TradeEvo'],
                ['Legacy moves', 'Moves stay the same in a trade; only the IVs are rerolled. Saves an Elite TM.', w['legacy'], 'Legacy']]},
            {'id': 'pvp', 'label': 'GO Battle League season', 'steps': [
                ['Strict', 'Lowest Attack range, Defense and HP at 15.', f'0-1{A}&4{Df}&4{H}', 'PvPStrict'],
                ['Wider', 'Defense and HP from 11 to 15.', f'0-1{A}&3-4{Df}&3-4{H}', 'PvPWide']]},
            {'id': 'raid', 'label': 'Before a raid', 'steps': [
                ['Both moves the same type', 'Attackers whose Fast and Charged moves are both that type.', 'TYPE', 'Attackers']]},
        ]
    else:
        recipes = [
            {'id': 'cd', 'label': 'コミュニティ・デイのあと', 'steps': [
                ['まず進化', '進化させると図鑑に新しく登録されるポケモン。整理する前に先に。', w['evolvenew'], '新図鑑'],
                ['限定技の確認', 'レガシー技を覚えているもの — 個体値が低くても送らず交換用に。', w['legacy'], 'レガシー'],
                ['今日捕まえた分の整理', '今日捕まえた星0〜2のうち、色違い・キラ・とくべつ・背景つきを除いたもの。', f"{w['age']}0&0*,1*,2*&!{w['shiny']}&!{w['lucky']}&!{w['costume']}&!{w['bg']}", '今日整理']]},
            {'id': 'full', 'label': 'ボックスがいっぱい', 'steps': [
                ['まず進化', '送る前に図鑑を埋められるものから進化。', w['evolvenew'], '新図鑑'],
                ['送る候補', '星0〜2だけが出て、大事なものはすべて除いたリスト。それでも送る前に一度見直してください。', one, '送る候補'],
                ['残すものの確認', '送る前に残すべきものだけをひと目で。', keep, '残す']]},
            {'id': 'trade', 'label': '交換に行く前', 'steps': [
                ['キラ確定', '2020年までに捕まえたポケモンは交換するとキラ確定（1人45回）。個体値は最低12、強化のほしのすなは半分。', f"{w['year']}-2020", 'キラ確定'],
                ['交換でアメ3個', '100km以上離れて捕まえたもの。リモートレイドの伝説は除いておきます。', f"{w['distance']}100-&!{w['legend']}", 'アメ3個'],
                ['アメなしで進化', '交換すると進化のアメが減る・いらないもの。', w['tradeevo'], '交換進化'],
                ['レガシー技', '交換しても技はそのまま、個体値だけ引き直し。すごいわざマシン1個分の節約。', w['legacy'], 'レガシー']]},
            {'id': 'pvp', 'label': 'GOバトルリーグのシーズン', 'steps': [
                ['厳しめ', 'こうげきはいちばん低い区間、ぼうぎょ・HPは15。', f'0-1{A}&4{Df}&4{H}', 'リーグ厳しめ'],
                ['広め', 'ぼうぎょ・HPを11〜15まで。', f'0-1{A}&3-4{Df}&3-4{H}', 'リーグ広め']]},
            {'id': 'raid', 'label': 'レイドに行く前', 'steps': [
                ['技が2つとも同じタイプ', 'ノーマル技とスペシャル技がどちらもそのタイプのアタッカー。', 'TYPE', 'アタッカー']]},
        ]
    L = (lambda e, j: e if en else j)
    excl = [['shiny', L('Shiny', '色違い'), w['shiny'], True], ['legend', L('Legendary', '伝説'), w['legend'], True], ['myth', L('Mythical', 'まぼろし'), w['myth'], True],
            ['ub', L('Ultra Beast', 'ウルトラビースト'), w['ub'], True], ['lucky', L('Lucky', 'キラ'), w['lucky'], True], ['shadow', L('Shadow', 'シャドウ'), w['shadow'], True],
            ['costume', L('Costume', 'とくべつ'), w['costume'], True], ['bg', L('Background', '背景'), w['bg'], True],
            ['legacy', L('Legacy move', 'レガシー技'), w['legacy'], True], ['tag', L('Tagged', 'タグつき'), '#', True], ['dmax', L('Dynamax', 'ダイマックス'), w['dmax'], False]]
    cond = [['newdex', L('New Pokédex entry if evolved', '進化で図鑑に新登録'), w['evolvenew']], ['item', L('Evolves with an item', 'どうぐで進化'), w['item']],
            ['quest', L('Evolves with a condition', '条件で進化'), w['quest']], ['trade', L('Trade evolution', '交換進化'), w['tradeevo']], ['mega', L('Can Mega Evolve', 'メガシンカできる'), w['mega']]]
    stars = [['0*', L('0 stars', '星0')], ['1*', L('1 star', '星1')], ['2*', L('2 stars', '星2')], ['3*', L('3 stars', '星3')], ['4*', L('4 stars (100)', '星4（100）')]]
    year = [['', L('Any', '指定なし')], [f"{w['year']}-2020", L('2020 or earlier (guaranteed lucky when traded)', '2020年まで（交換でキラ確定）')], [f"{w['year']}2016", L('2016 (the first year)', '2016年（最初の年）')]]
    dist = [['', L('Any', '指定なし')], [f"{w['distance']}100-", L('100 km or more (3 Candy from a trade)', '100km以上（交換でアメ3個）')], [f"{w['distance']}1000-", L('1,000 km or more', '1,000km以上')]]
    samples = [[L('Exclamation trap', 'びっくりマークの罠'), f"!{w['shiny']},{w['legend']}"],
               [L('No dash', 'ダッシュなし'), f"{w['distance']}100&!{w['legend']}"],
               [L('Missing star', '星マークなし'), f"{w['dmax']}&4"],
               [L('Transfer candidates in one line', '送る候補を1行で'), one]]
    return {'terms': terms, 'types': types, 'w': w, 'recipes': recipes, 'excl': excl, 'cond': cond, 'stars': stars,
            'year': year, 'dist': dist, 'samples': samples, 'iceType': types[5],
            'stat': {A: L('Attack', 'こうげき'), Df: L('Defense', 'ぼうぎょ'), 'hp': 'HP'},
            'statKw': {'atk': A, 'def': Df, 'hp': 'HP'}, 'default': f"0*,1*,2*&!{w['shiny']},{w['legend']}&{w['distance']}100"}

T_EN = {
    'copied': 'Copied · paste it into the in-game search', 'blocked': 'Auto-copy was blocked · long-press the text to copy',
    'copiedBtn': 'Copied', 'longPress': 'Long-press to copy', 'copy': 'Copy',
    'star': {'0': '0 stars (appraisal 49% or less)', '1': '1 star (51–64%)', '2': '2 stars (67–80%)', '3': '3 stars (82–98%)', '4': '4 stars (100%)'},
    'rAB': '{a}–{b}{u}', 'rUp': '{a}{u} or more', 'rDown': '{b}{u} or less', 'not': 'not {w}', 'or': ' or ',
    'tag': "tagged '{t}'", 'iv': '{s} IV {r}', 'cp': 'CP {r}', 'cpExact': ' exactly',
    'distIn': 'caught within {n} km of where you are now', 'distR': 'caught {r} away from where you are now', 'km': ' km',
    'age0': 'caught today (within 24 hours)', 'ageN': 'caught {n} days ago', 'ageR': 'caught {r} ago', 'days': ' days',
    'yearN': 'caught in {n}', 'yearTo': 'caught in or before {n}', 'yearR': 'caught in {r}',
    'move': 'has a {t}-type {k}', 'moveK': {'1': 'Fast move', '2': 'Charged move', '3': 'second Charged move'}, 'moveAny': 'move',
    'family': 'the whole {t} evolution family', 'dex': 'Pokédex No. {t}', 'type': '{t} type', 'name': "Pokémon whose name starts with '{t}'",
    'pasteT': 'Paste a search string', 'pasteB': 'Or tap one of the examples.',
    'parenT': 'Parentheses don\'t work', 'parenB': 'The in-game search ignores parentheses. Build the order with the rule that commas group before &.',
    'negT': 'An exclamation mark only applies to the one word right after it',
    'negB': '{code} reads as "{read}", so what you wanted to exclude comes back in. Exclude things one at a time with &! . (The fixed line below excludes all of them.)',
    'starT': "'{t}' searches a Pokédex number", 'starB': 'For a star count, add the star: {code}',
    'dashT': "No dash means 'within'", 'dashB': '{code} means within {n} km. To find ones caught far away, use {code2}',
    'remoteT': 'Remote raids are measured from the Gym', 'remoteB': 'Searching for far-away catches pulls in lots of remote-raid legendaries. For trades, add {code}.',
    'unkT': 'Unknown words are read as a name search', 'unkB': "{codes} — if it isn't a Pokémon name or nickname, it may be a typo.",
    'okT': 'The syntax looks right', 'okB': 'It reads like this:',
    'fixCopy': 'Copy the fixed line', 'only': 'Only these', 'excl': 'Excluded', 'mixed': 'Mixed ⚠', 'orSpan': 'or', 'none': 'Nothing yet',
    'typeLabel': 'Type', 'fav': 'Suggested favorite name:', 'pickCond': '(choose some conditions)', 'cleared': 'All choices cleared',
    'pickSeg': '(tap the bars to choose ranges)', 'statName': {'atk': 'Attack', 'def': 'Defense', 'hp': 'HP'},
}
T_JA = {
    'copied': 'コピーしました · ゲームの検索欄に貼り付けてください', 'blocked': '自動コピーがブロックされました · 文字を長押ししてコピーしてください',
    'copiedBtn': 'コピー済み', 'longPress': '長押しでコピー', 'copy': 'コピー',
    'star': {'0': '星0（評価49%以下）', '1': '星1（51〜64%）', '2': '星2（67〜80%）', '3': '星3（82〜98%）', '4': '星4（100%）'},
    'rAB': '{a}〜{b}{u}', 'rUp': '{a}{u}以上', 'rDown': '{b}{u}以下', 'not': '{w}以外', 'or': ' または ',
    'tag': '「{t}」タグ', 'iv': '{s}の個体値 {r}', 'cp': 'CP {r}', 'cpExact': ' ちょうど',
    'distIn': '今いる場所から{n}km以内で捕まえた', 'distR': '今いる場所から{r}離れた所で捕まえた', 'km': 'km',
    'age0': '今日（24時間以内）捕まえた', 'ageN': '{n}日前に捕まえた', 'ageR': '捕まえてから{r}', 'days': '日',
    'yearN': '{n}年に捕まえた', 'yearTo': '{n}年までに捕まえた', 'yearR': '{r}に捕まえた',
    'move': '{t}タイプの{k}を覚えている', 'moveK': {'1': 'ノーマル技', '2': 'スペシャル技', '3': '2つ目のスペシャル技'}, 'moveAny': '技',
    'family': '{t}の進化系統すべて', 'dex': '図鑑番号{t}番', 'type': '{t}タイプ', 'name': '名前が「{t}」で始まるポケモン',
    'pasteT': '検索ワードを貼り付けてみてください', 'pasteB': '例のボタンを押してもOKです。',
    'parenT': 'かっこは使えません', 'parenB': 'ゲームの検索欄はかっこを無視します。カンマが&より先にまとまるルールで順番を組みます。',
    'negT': 'びっくりマークはすぐ後ろの1語にしか付きません',
    'negB': '{code} は「{read}」と読まれるので、除きたいものが戻ってきます。除くものは1つずつ &! でつないでください。（下の修正版はすべて除く意味に直しました）',
    'starT': '「{t}」は図鑑番号で検索されます', 'starB': '星の数なら星マークまで：{code}',
    'dashT': 'ダッシュがないと「以内」です', 'dashB': '{code} は{n}km以内。遠くで捕まえたものを探すなら {code2}',
    'remoteT': 'リモートレイドはジムの場所で測ります', 'remoteB': '遠くで捕まえたものを探すと、リモートレイドの伝説がたくさん混ざります。交換用なら {code} を付けてください。',
    'unkT': '知らない言葉は名前検索として読まれます', 'unkB': '{codes} — ポケモンの名前・ニックネームでなければ打ち間違いかもしれません。',
    'okT': '書き方は合っています', 'okB': 'このように読まれます。',
    'fixCopy': '直してコピー', 'only': 'これだけ', 'excl': '除く', 'mixed': '混在 ⚠', 'orSpan': 'または', 'none': 'まだなし',
    'typeLabel': 'タイプ', 'fav': 'お気に入り名のおすすめ：', 'pickCond': '（条件を選んでください）', 'cleared': '選択をすべて消しました',
    'pickSeg': '（バーを押して区間を選んでください）', 'statName': {'atk': 'こうげき', 'def': 'ぼうぎょ', 'hp': 'HP'},
}

SCRIPT = r'''<script>
  const T = __T__, K = __K__;
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
  const fill = (s, o) => s.replace(/\{(\w+)\}/g, (_, k) => o[k] ?? "");
  const reEsc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  let toastT;
  async function copy(text, btn) {
    let ok = false;
    try { await navigator.clipboard.writeText(text); ok = true; } catch (e) {}
    if (!ok) {
      const ta = document.createElement("textarea"); ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select(); try { ok = document.execCommand("copy"); } catch (e) {} ta.remove();
    }
    const t = $("toast"); t.textContent = ok ? T.copied : T.blocked;
    t.classList.add("on"); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove("on"), 1800);
    if (btn) { const o = btn.textContent; btn.textContent = ok ? T.copiedBtn : T.longPress; btn.classList.add("done"); setTimeout(() => { btn.textContent = o; btn.classList.remove("done"); }, 1500); }
  }
  document.addEventListener("click", (e) => { const b = e.target.closest("[data-copy]"); if (b) copy(b.dataset.copy, b); });

  /* checker */
  const KW = Object.fromEntries(K.terms.map(([k, d]) => [k.toLowerCase(), d]));
  const TYPES = K.types, W = K.w;
  const BUCKET = { "0": "0", "1": "1~5", "2": "6~10", "3": "11~14", "4": "15" };
  const STAT_RE = new RegExp(`^([0-4])(?:-([0-4]))?(${Object.keys(K.stat).map(reEsc).join("|")})$`);
  const kwRe = (k) => new RegExp(`^${reEsc(k)}\\s?(\\d*)(-?)(\\d*)$`, "i");
  function range(a, b, dash, unit) {
    if (a && b) return fill(T.rAB, { a, b, u: unit });
    if (a && dash) return fill(T.rUp, { a, u: unit });
    if (b) return fill(T.rDown, { b, u: unit });
    return null;
  }
  function readTerm(raw) {
    const t = raw.trim(); if (!t) return null;
    let neg = false, s = t;
    if (s.startsWith("!")) { neg = true; s = s.slice(1).trim(); }
    const low = s.toLowerCase();
    let m, what = null, known = true, note = null;
    if (KW[low] !== undefined) what = KW[low];
    else if (/^#.+/.test(s)) what = fill(T.tag, { t: s.slice(1) });
    else if ((m = s.match(/^([0-4])\*$/))) what = T.star[m[1]];
    else if ((m = low.match(STAT_RE))) what = fill(T.iv, { s: K.stat[m[3]], r: m[2] ? `${BUCKET[m[1]].split("~")[0]}~${BUCKET[m[2]].split("~").pop()}` : BUCKET[m[1]] });
    else if ((m = low.match(/^cp(\d*)(-?)(\d*)$/)) && (m[1] || m[3])) what = fill(T.cp, { r: range(m[1], m[3], m[2], "") || m[1] }) + (m[1] && !m[2] && !m[3] ? T.cpExact : "");
    else if ((m = s.match(kwRe(W.distance))) && (m[1] || m[3])) {
      if (m[1] && !m[2]) what = fill(T.distIn, { n: m[1] });
      else what = fill(T.distR, { r: range(m[1], m[3], m[2], T.km) });
    }
    else if ((m = s.match(kwRe(W.age))) && (m[1] || m[3])) {
      if (m[1] === "0" && !m[2]) what = T.age0;
      else if (m[1] && !m[2]) what = fill(T.ageN, { n: m[1] });
      else what = fill(T.ageR, { r: range(m[1], m[3], m[2], T.days) });
    }
    else if ((m = s.match(kwRe(W.year))) && (m[1] || m[3])) {
      if (m[1] && !m[2]) what = fill(T.yearN, { n: m[1] });
      else if (!m[1] && m[3]) what = fill(T.yearTo, { n: m[3] });
      else what = fill(T.yearR, { r: range(m[1], m[3], m[2], "") });
    }
    else if ((m = low.match(/^@([123])?(.+)$/)) && TYPES.includes(m[2])) what = fill(T.move, { t: m[2], k: T.moveK[m[1]] || T.moveAny });
    else if (/^\+.+/.test(s)) what = fill(T.family, { t: s.slice(1) });
    else if (/^\d+$/.test(s)) { what = fill(T.dex, { t: s }); note = "star"; }
    else if (TYPES.includes(low)) what = fill(T.type, { t: s });
    else { what = fill(T.name, { t: s }); known = false; }
    return { raw: t, neg, what, known, core: s, note };
  }

  function analyze(input) {
    const issues = [];
    const text = input.replace(/\s*&\s*/g, "&").trim();
    if (!text) return { issues: [{ lvl: "warn", title: T.pasteT, body: T.pasteB }], groups: [], fixed: "" };
    if (/[()]/.test(text)) issues.push({ lvl: "bad", title: T.parenT, body: T.parenB });
    const groups = text.split("&").map((g) => g.split(/[,;:]/).map(readTerm).filter(Boolean)).filter((g) => g.length);
    const fixedGroups = [];
    for (const g of groups) {
      const negs = g.filter((t) => t.neg);
      if (g.length > 1 && negs.length) {
        const plain = g.filter((t) => !t.neg);
        const read = negs.map((t) => fill(T.not, { w: t.what })).join(T.or) + (plain.length ? T.or + plain.map((t) => t.what).join(T.or) : "");
        issues.push({ lvl: "bad", title: T.negT, body: fill(T.negB, { code: `<code>${esc(g.map((t) => t.raw).join(","))}</code>`, read: esc(read) }) });
        for (const t of g) fixedGroups.push(["!" + t.core]);
        continue;
      }
      fixedGroups.push(g.map((t) => (t.neg ? "!" : "") + t.core));
    }
    const distOnly = kwRe(W.distance);
    for (const g of groups) for (const t of g) {
      if (t.note === "star") issues.push({ lvl: "warn", title: fill(T.starT, { t: t.core }), body: fill(T.starB, { code: `<code>${esc(t.core)}*</code>` }) });
      const dm = t.core.match(distOnly);
      if (dm && dm[1] && !dm[2] && !dm[3]) issues.push({ lvl: "warn", title: T.dashT, body: fill(T.dashB, { code: `<code>${esc(t.core)}</code>`, n: dm[1], code2: `<code>${esc(t.core.replace(/\s/g, ""))}-</code>` }) });
      if (dm && !t.neg) issues.push({ lvl: "warn", title: T.remoteT, body: fill(T.remoteB, { code: `<code>&amp;!${esc(W.legend)}</code>` }) });
    }
    const unknown = groups.flat().filter((t) => !t.known);
    if (unknown.length) issues.push({ lvl: "warn", title: T.unkT, body: fill(T.unkB, { codes: unknown.map((t) => `<code>${esc(t.core)}</code>`).join(" ") }) });
    const fixed = fixedGroups.map((g) => g.join(",")).join("&");
    if (!issues.some((i) => i.lvl === "bad")) issues.unshift({ lvl: "ok", title: T.okT, body: T.okB });
    return { issues, groups, fixed: fixed !== text ? fixed : "" };
  }

  function renderChecker() {
    const { issues, groups, fixed } = analyze($("q").value);
    $("verdict").innerHTML = issues.map((i) => `<div class="issue ${i.lvl}"><b>${esc(i.title)}</b><div>${i.body}</div></div>`).join("")
      + (fixed ? `<div class="fixed"><code>${esc(fixed)}</code><button class="btn" type="button" data-copy="${esc(fixed)}">${T.fixCopy}</button></div>` : "");
    $("rows").innerHTML = groups.map((g) => {
      const allNeg = g.every((t) => t.neg), anyNeg = g.some((t) => t.neg);
      const cls = !anyNeg ? "show" : (allNeg && g.length === 1 ? "hide" : "unk");
      const tag = !anyNeg ? T.only : (allNeg && g.length === 1 ? T.excl : T.mixed);
      const what = g.map((t) => `${esc(t.neg ? fill(T.not, { w: t.what }) : t.what)}<code>${esc(t.raw)}</code>`).join(`<span class="or">${T.orSpan}</span>`);
      return `<div class="row"><span class="tag ${cls}">${tag}</span><span class="what">${what}</span></div>`;
    }).join("") || `<div class="row"><span class="tag unk">—</span><span class="what">${T.none}</span></div>`;
  }
  $("q").value = K.default;
  $(`samples`).innerHTML = K.samples.map(([l, s]) => `<button type="button" data-s="${esc(s)}">${esc(l)}</button>`).join("");
  $("q").addEventListener("input", renderChecker);
  document.querySelectorAll(".samples button").forEach((b) => b.addEventListener("click", () => { $("q").value = b.dataset.s; renderChecker(); }));
  renderChecker();

  /* recipes */
  const RECIPES = K.recipes;
  let curType = K.iceType;
  const typeQ = (t) => `@1${t}&@2${t},@3${t}`;
  function renderRecipe(id) {
    const r = RECIPES.find((x) => x.id === id);
    document.querySelectorAll("#tabs button").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.id === id)));
    $("recipe").innerHTML = r.steps.map(([t, why, q, fav], i) => {
      const qq = q === "TYPE" ? typeQ(curType) : q;
      const pick = q === "TYPE" ? `<div class="typepick"><label for="tp" style="font-size:13px;color:var(--dim)">${T.typeLabel}</label><select id="tp">${TYPES.map((x) => `<option ${x === curType ? "selected" : ""}>${x}</option>`).join("")}</select></div>` : "";
      return `<div class="step"><span class="n">${i + 1}</span><div class="body"><div class="t">${esc(t)}</div><div class="why">${esc(why)}</div>${pick}
        <div class="q"><code>${esc(qq)}</code><button class="btn" type="button" data-copy="${esc(qq)}">${T.copy}</button></div>
        <div class="fav">${T.fav} <b>${esc(fav)}</b></div></div></div>`;
    }).join("");
    const tp = $("tp"); if (tp) tp.addEventListener("change", () => { curType = tp.value; renderRecipe(id); });
  }
  $("tabs").innerHTML = RECIPES.map((r) => `<button type="button" role="tab" data-id="${r.id}">${esc(r.label)}</button>`).join("");
  $("tabs").addEventListener("click", (e) => { const b = e.target.closest("button[data-id]"); if (b) renderRecipe(b.dataset.id); });
  renderRecipe("cd");

  /* builder */
  const B_EXCL = K.excl, B_COND = K.cond, B_STARS = K.stars, B_YEAR = K.year, B_DIST = K.dist;
  let chipN = 0;
  function chip(group, type, value, label, code, checked) {
    const id = `${group}-${chipN++}`;
    return `<div class="chip"><input type="${type}" id="${id}" name="${group}" value="${esc(value)}" ${checked ? "checked" : ""}><label for="${id}">${esc(label)}${code ? ` <code>${esc(code)}</code>` : ""}</label></div>`;
  }
  $("stars").innerHTML = B_STARS.map(([v, l]) => chip("stars", "checkbox", v, l, "", ["0*", "1*", "2*"].includes(v))).join("");
  $("excl").innerHTML = B_EXCL.map(([k, l, term, on]) => chip("excl", "checkbox", k, l, term === "#" ? "#" : "", on)).join("");
  $("cond").innerHTML = B_COND.map(([k, l, term]) => chip("cond", "checkbox", k, l, term, false)).join("");
  $("year").innerHTML = B_YEAR.map(([v, l], i) => chip("year", "radio", v, l, v, i === 0)).join("");
  $("dist").innerHTML = B_DIST.map(([v, l], i) => chip("dist", "radio", v, l, v, i === 0)).join("");
  function bRange(prefix, a, b) {
    const lo = $(a).value.trim(), hi = $(b).value.trim();
    if (lo === "" && hi === "") return "";
    if (lo !== "" && hi !== "") return lo === hi ? `${prefix}${lo}` : `${prefix}${lo}-${hi}`;
    return lo !== "" ? `${prefix}${lo}-` : `${prefix}-${hi}`;
  }
  function build() {
    const parts = [];
    const onC = new Set([...document.querySelectorAll('input[name="cond"]:checked')].map((i) => i.value));
    for (const [k, , term] of B_COND) if (onC.has(k)) parts.push(term);
    const cp = bRange("cp", "cpMin", "cpMax"), days = bRange(W.age, "dayMin", "dayMax");
    if (cp) parts.push(cp);
    if (days) parts.push(days);
    for (const g of ["year", "dist"]) { const v = document.querySelector(`input[name="${g}"]:checked`)?.value; if (v) parts.push(v); }
    const stars = [...document.querySelectorAll('input[name="stars"]:checked')].map((i) => i.value);
    if (stars.length && stars.length < B_STARS.length) parts.push(stars.join(","));
    const onE = new Set([...document.querySelectorAll('input[name="excl"]:checked')].map((i) => i.value));
    for (const [k, , term] of B_EXCL) if (onE.has(k)) parts.push("!" + term);
    const q = parts.join("&") || T.pickCond;
    $("bq").textContent = q; $("bcopy").dataset.copy = q;
  }
  document.querySelector(".builder").addEventListener("change", build);
  $("breset").addEventListener("click", () => {
    document.querySelectorAll('input[name="stars"], input[name="excl"], input[name="cond"]').forEach((i) => { i.checked = false; });
    document.querySelectorAll('input[name="year"], input[name="dist"]').forEach((i) => { i.checked = i.value === ""; });
    for (const id of ["cpMin", "cpMax", "dayMin", "dayMax"]) $(id).value = "";
    build();
    const t = $("toast"); t.textContent = T.cleared; t.classList.add("on"); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove("on"), 1400);
  });
  document.querySelector(".builder").addEventListener("input", (e) => { if (e.target.matches(".num input")) build(); });
  build();

  /* appraisal */
  const SEG = [["0", "0"], ["1", "1~5"], ["2", "6~10"], ["3", "11~14"], ["4", "15"]];
  const sel = { atk: [0, 1], def: [4, 4], hp: [4, 4] };
  function renderAppraisal() {
    document.querySelectorAll(".stat").forEach((st) => {
      const k = st.dataset.stat, [a, b] = sel[k];
      st.querySelector(".segs").innerHTML = SEG.map(([n, r], i) =>
        `<button type="button" class="seg ${i >= a && i <= b ? "on" : ""} ${i === 4 && i >= a && i <= b ? "full" : ""}" data-i="${i}" aria-pressed="${i >= a && i <= b}" aria-label="${T.statName[k]} ${r}">${n}<small>${r}</small></button>`).join("");
      st.querySelector(".lab em").textContent = a === b ? SEG[a][1] : `${SEG[a][1].split("~")[0]}~${SEG[b][1].split("~").pop()}`;
    });
    const part = (k) => { const [a, b] = sel[k]; return a === 0 && b === 4 ? "" : `${a === b ? a : `${a}-${b}`}${K.statKw[k]}`; };
    const q = ["atk", "def", "hp"].map(part).filter(Boolean).join("&") || T.pickSeg;
    $("apq").textContent = q; $("apcopy").dataset.copy = q;
  }
  document.querySelector(".appraisal").addEventListener("click", (e) => {
    const s = e.target.closest(".seg"); const p = e.target.closest("button[data-p]");
    if (s) {
      const k = s.closest(".stat").dataset.stat, i = +s.dataset.i, [a, b] = sel[k];
      sel[k] = a === b && i !== a ? [Math.min(a, i), Math.max(a, i)] : [i, i];
      renderAppraisal();
    }
    if (p) { const v = p.dataset.p.split(","); ["atk", "def", "hp"].forEach((k, j) => { const [a, b = a] = v[j].split("-").map(Number); sel[k] = [a, b]; }); renderAppraisal(); }
  });
  renderAppraisal();
</script>'''

def extra(src, li):
    a = src.index('<script>'); b = src.index('</script>', a) + len('</script>')
    k = K(li)
    js = SCRIPT.replace('__T__', json.dumps((T_EN, T_JA)[li], ensure_ascii=False)).replace('__K__', json.dumps(k, ensure_ascii=False))
    src = src[:a] + js + src[b:]
    # 예시 버튼·기본 검색어는 스크립트가 채운다
    s0 = src.index('<div class="samples">'); s1 = src.index('</div>', s0) + len('</div>')
    src = src[:s0] + '<div class="samples">' + ('Examples:' if li == 0 else '例：') + '<span id="samples"></span></div>' + src[s1:]
    src = re.sub(r'(<textarea id="q"[^>]*>)[^<]*(</textarea>)', r'\1\2', src)
    # 평가 막대 키는 언어와 무관한 atk/def/hp로
    src = src.replace('data-stat="공격"', 'data-stat="atk"').replace('data-stat="방어"', 'data-stat="def"').replace('data-stat="HP"', 'data-stat="hp"')
    w = k['w']
    src = src.replace('슈퍼리그면 결과 앞에 cp-1500&amp; 를 붙이세요.', 'SL_CP_NOTE')
    src = src.replace('<b>전설</b>', f'<b>{w["legend"]}</b>')
    return src

def post(src, li):
    # 번역판 키워드는 폰에서 쳐 보지 않은 게임 문구 — 노란 상자로 밝힌다
    note = ('<div class="issue warn"><b>Keywords from the game\'s English text — not yet tested on a phone</b><div>The symbol rules (&amp; , ! -) were tested in the Korean version. The English words come from the game\'s own text but haven\'t been typed into the English game yet.</div></div>',
            '<div class="issue warn"><b>キーワードはゲームの日本語テキストから — スマホでは未確認</b><div>記号のルール（&amp; , ! -）は韓国語版で確認しました。日本語のキーワードはゲーム内テキストから取りましたが、日本語版ではまだ実際に入力していません。</div></div>')[li]
    src = src.replace('<div class="verdict" id="verdict" aria-live="polite"></div>', note + '\n      <div class="verdict" id="verdict" aria-live="polite"></div>')
    src = src.replace('SL_CP_NOTE', ('For Great League, add cp-1500&amp; in front of the result.', 'スーパーリーグなら結果の前に cp-1500&amp; を付けてください。')[li])
    return src

TABLE = {
    '<title>이로치수집가 검색어 검사기</title>': ('<title>Search String Checker · Shiny Collector Tools</title>', '<title>検索ワードチェッカー · 色違いコレクター</title>'),
    '포켓몬고 <b>이로치 수집가</b> 도구함': ('Pokémon GO <b>Shiny Collector</b> Tools', 'ポケモンGO <b>色違いコレクター</b> ツール'),
    '포켓몬고 <b>이로치 수집가</b>': ('Pokémon GO <b>Shiny Collector</b>', 'ポケモンGO <b>色違いコレクター</b>'),
    '<span class="here">박스 검색어</span>': ('<span class="here">Storage search</span>', '<span class="here">ボックス検索</span>'),
    '<h1>검색어 검사기</h1>': ('<h1>Search String Checker</h1>', '<h1>検索ワードチェッカー</h1>'),
    '내 검색어, 제대로 쓴 걸까?': ('Is my search string right?', '自分の検索ワード、合ってる？'),
    '>검색어</label>': ('>Search string</label>', '>検索ワード</label>'),
    '<h3>이렇게 읽혀요</h3>': ('<h3>How it reads</h3>', '<h3>こう読まれます</h3>'),
    '"더 보기"': ('"More"', '"もっと見る"'),
    '<b>검색어, 영상으로 보기</b><span>9,168마리 박스가 한 줄로 2,003마리가 되는 과정</span>': ('<b>Watch the video (Korean)</b><span>How one line takes a 9,168-Pokémon storage down to 2,003</span>', '<b>動画で見る（韓国語）</b><span>9,168匹のボックスが1行で2,003匹になるまで</span>'),
    '<b>한 장으로 보는 검색어</b><span>블로그에서 저장해 두고 보기</span>': ('<b>Search strings on one page (Korean)</b><span>Save it from the blog</span>', '<b>1枚で見る検索ワード（韓国語）</b><span>ブログで保存して見る</span>'),
    '>상황별 레시피<': ('>Recipes<', '>場面別レシピ<'),
    '지금 뭐 하려고요?': ('What are you about to do?', '今から何をしますか？'),
    '순서대로 복사해서 쓰세요. 한 번 쓴 건 최근 검색을 길게 눌러 즐겨찾기로 저장해 두면 다음부터 편합니다.': ('Copy them in order. Long-press a recent search to save it as a favorite, and next time is easier.', '順番にコピーして使ってください。一度使ったものは最近の検索を長押ししてお気に入りに保存すると次から楽です。'),
    '>직접 만들기<': ('>Build your own<', '>自分で作る<'),
    '눌러서 조립하기': ('Tap to build', 'タップで組み立て'),
    '고르면 바로 아래에 검색어가 만들어져요. 쉼표·느낌표·대시는 알아서 맞춰 드립니다.': ('Your search string appears right below as you choose. Commas, exclamation marks and dashes are handled for you.', '選ぶとすぐ下に検索ワードができます。カンマ・びっくりマーク・ダッシュは自動で合わせます。'),
    '보여줄 평가<span>아무것도 안 고르면 전체</span>': ('Appraisal to show<span>none chosen = all</span>', '表示する評価<span>何も選ばなければ全部</span>'),
    '빼고 볼 것<span>하나씩 느낌표가 붙어요</span>': ('Exclude<span>each gets its own exclamation mark</span>', '除くもの<span>1つずつびっくりマークが付きます</span>'),
    '진화 · 기술 조건<span>고른 건 모두 만족해야 나와요</span>': ('Evolution conditions<span>all chosen must match</span>', '進化の条件<span>選んだものをすべて満たすものだけ</span>'),
    'CP · 잡은 지 며칠<span>한쪽만 적어도 돼요</span>': ('CP · days since caught<span>one side is enough</span>', 'CP · 捕まえてからの日数<span>片方だけでもOK</span>'),
    '>최소 CP<': ('>Min CP<', '>最小CP<'), '>최대 CP<': ('>Max CP<', '>最大CP<'),
    '>최소 일수<': ('>Min days<', '>最小日数<'), '>최대 일수<': ('>Max days<', '>最大日数<'),
    'placeholder="예: ': ('placeholder="e.g. ', 'placeholder="例: '),
    '일수 0 = 오늘(24시간 안). 최대 CP 1500 = 슈퍼리그, 2500 = 하이퍼리그.': ('Days 0 = today (within 24 hours). Max CP 1500 = Great League, 2500 = Ultra League.', '日数0 = 今日（24時間以内）。最大CP 1500 = スーパーリーグ、2500 = ハイパーリーグ。'),
    '잡은 해<span>하나만</span>': ('Year caught<span>one only</span>', '捕まえた年<span>1つだけ</span>'),
    '잡은 곳 거리<span>대시는 숫자 뒤 = 이상</span>': ('Distance from where caught<span>dash after the number = or more</span>', '捕まえた場所の距離<span>数字の後ろのダッシュ = 以上</span>'),
    '>복사<': ('>Copy<', '>コピー<'),
    '↺ 초기화': ('↺ Reset', '↺ リセット'),
    '리모트 레이드로 잡은 포켓몬은 거리를 레이드한 체육관 위치로 잽니다. 거리 검색엔 ': ('Pokémon caught in remote raids are measured from the raid Gym. For distance searches, also exclude ', 'リモートレイドで捕まえたポケモンは、レイドしたジムの場所で距離を測ります。距離検索では '),
    '도 빼 두면 편해요.': (' to make it easier.', ' も除いておくと便利です。'),
    '>배틀리그<': ('>GO Battle League<', '>バトルリーグ<'),
    '평가 막대로 고르기': ('Pick with appraisal bars', '評価バーで選ぶ'),
    '게임 평가 화면처럼 칸을 누르세요. 누른 구간에 들어가는 포켓몬만 나오는 검색어가 만들어집니다.': ('Tap the bars like the in-game appraisal. You get a search string that shows only Pokémon in the ranges you tapped.', 'ゲームの評価画面のようにバーを押してください。押した区間に入るポケモンだけが出る検索ワードができます。'),
    '<b>개체값 구간</b>': ('<b>IV ranges</b>', '<b>個体値の区間</b>'),
    '<div class="lab">공격 <em>': ('<div class="lab">Attack <em>', '<div class="lab">こうげき <em>'),
    '<div class="lab">방어 <em>': ('<div class="lab">Defense <em>', '<div class="lab">ぼうぎょ <em>'),
    '<div class="lab">체력 <em>': ('<div class="lab">HP <em>', '<div class="lab">HP <em>'),
    '>배틀리그 엄격<': ('>PvP strict<', '>リーグ厳しめ<'), '>배틀리그 넓게<': ('>PvP wide<', '>リーグ広め<'),
    '>100개체<': ('>100% IV<', '>個体値100<'), '>0개체<': ('>0% IV<', '>個体値0<'),
    '공격이 낮을수록 CP 상한 안에서 레벨을 더 올릴 수 있어요. ': ('The lower the Attack, the higher the level you can reach under a CP cap. ', 'こうげきが低いほど、CP上限の中でレベルを上げられます。'),
    '기호는 네 개': ('Just four symbols', '記号は4つ'),
    '쉼표는 &amp;보다 먼저 묶이고, 괄호는 안 됩니다.': ('Commas group before &amp;, and parentheses don\'t work.', 'カンマは&amp;より先にまとまり、かっこは使えません。'),
    '<span>그리고</span>': ('<span>and</span>', '<span>かつ</span>'),
    '<span>또는</span>': ('<span>or</span>', '<span>または</span>'),
    '<span>바로 뒤 한 단어 빼고</span>': ('<span>exclude the next word</span>', '<span>すぐ後ろの1語を除く</span>'),
    '<span>숫자 뒤 = 이상</span>': ('<span>after a number = or more</span>', '<span>数字の後ろ = 以上</span>'),
    '기호 하나면 <em>이로치 전설</em>이 <strong>보낼 목록</strong>에': ('One symbol, and your <em>shiny legendaries</em> end up in the <strong>transfer list</strong>', '記号ひとつで<em>色違いの伝説</em>が<strong>送るリスト</strong>に'),
    '어디서 가져온 검색어든 붙여넣어 보세요. 무슨 뜻인지 말로 풀어주고, 틀린 곳은 짚어서 고친 걸 복사해 드립니다. 한국어판 게임에서 직접 쳐본 결과로 만들었어요.': (
        'Paste a search string from anywhere. It explains what it means in plain words, points out mistakes and gives you a fixed version to copy. The rules were tested by typing them into the Korean version of the game; the English keywords come from the game\'s text.',
        'どこで見つけた検索ワードでも貼り付けてみてください。意味を言葉で説明し、間違いを指摘して直したものをコピーできます。ルールは韓国語版のゲームで実際に入力して確かめ、日本語のキーワードはゲーム内テキストから取りました。'),
    '한국어판에서 직접 확인 (2026.9.19). 결합 규칙 Pokémon GO Wiki · 교환 사탕 Bulbapedia·Pokétory · 반짝반짝 확정 Pokétory·pogoalley. 게임 업데이트로 검색어가 바뀔 수 있어요.': (
        'Rules checked in the Korean version (Sep 19, 2026); English keywords from the game\'s text, not yet tested on a phone. Combining rules: Pokémon GO Wiki · trade Candy: Bulbapedia, Pokétory · guaranteed lucky: Pokétory, pogoalley. Search keywords may change with game updates.',
        'ルールは韓国語版で確認（2026.9.19）、日本語キーワードはゲーム内テキストから（スマホ未確認）。組み合わせルール Pokémon GO Wiki · 交換のアメ Bulbapedia・Pokétory · キラ確定 Pokétory・pogoalley。ゲームのアップデートで検索ワードが変わることがあります。'),
}
DESC = ('Pokémon GO search string checker: paste a search string to see what it means, catch mistakes, and build strings for storage cleanup, trades and GO Battle League.',
        'ポケモンGOの検索ワードチェッカー。検索ワードを貼り付けると意味を説明し、間違いを直します。ボックス整理・交換・バトルリーグ用の検索ワードも作れます。')
