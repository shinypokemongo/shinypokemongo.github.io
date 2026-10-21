# 상점 박스 계산기 /shop/ 번역표 — _언어판.py가 읽는다. 표의 값은 (영어, 일본어)
import re

ITEMS = {  # 한국어: (영어, 일본어) — 게임 문구 키는 공용/명칭/고정명칭.tsv 근거 칸
    '프리미엄 배틀패스': ('Premium Battle Pass', 'プレミアムバトルパス'),
    '리모트 레이드패스': ('Remote Raid Pass', 'リモートレイドパス'),
    '부화장치': ('Egg Incubator', 'ふかそうち'),
    '슈퍼 부화장치': ('Super Incubator', 'スーパーふかそうち'),
    '행복의알': ('Lucky Egg', 'しあわせタマゴ'),
    '별의조각': ('Star Piece', 'ほしのかけら'),
    '향로': ('Incense', 'おこう'),
    '루어모듈': ('Lure Module', 'ルアーモジュール'),
    '스페셜 루어모듈': ('Special Lure Module', '特殊ルアーモジュール'),  # 묶음 이름(게임 문구 아님), 아래 sub에 공식 이름
    '다이버섯': ('Max Mushroom', 'ダイキノコ'),
    '맥스 파티클 팩': ('Max Particle Pack', 'マックス粒子パック'),
    '기력의덩어리': ('Max Revive', 'げんきのかたまり'),
    '풀회복약': ('Max Potion', 'まんたんのくすり'),
    '몬스터볼': ('Poké Ball', 'モンスターボール'),
    '하이퍼볼': ('Ultra Ball', 'ハイパーボール'),
    '포핀': ('Poffin', 'ポフィン'),
    '로켓레이더': ('Rocket Radar', 'ロケットレーダー'),
    '가방 업그레이드': ('Bag Upgrade', 'バッグ アップグレード'),
    '포켓몬 박스 업그레이드': ('Pokémon Storage Upgrade', 'ポケモンボックス アップグレード'),
    '기술머신노말': ('Fast TM', 'わざマシン ノーマル'),
    '기술머신스페셜': ('Charged TM', 'わざマシン スペシャル'),
    '대단한 기술머신노말': ('Elite Fast TM', 'すごいわざマシン ノーマル'),
    '대단한 기술머신스페셜': ('Elite Charged TM', 'すごいわざマシン スペシャル'),
}
TABLE = {  # 한국어: (영어, 일본어). 긴 것부터 치환하므로 순서는 상관없다
    '<title>이로치수집가 상점 박스 계산기</title>': ('<title>Shop Box Calculator · Shiny Collector Tools</title>', '<title>ショップボックス計算機 · 色違いコレクター</title>'),
    '포켓몬고 <b>이로치 수집가</b> 도구함': ('Pokémon GO <b>Shiny Collector</b> Tools', 'ポケモンGO <b>色違いコレクター</b> ツール'),
    '포켓몬고 <b>이로치 수집가</b>': ('Pokémon GO <b>Shiny Collector</b>', 'ポケモンGO <b>色違いコレクター</b>'),
    '<span class="here">상점</span>': ('<span class="here">Shop</span>', '<span class="here">ショップ</span>'),
    '<h1>상점 박스 계산기</h1>': ('<h1>Shop Box Calculator</h1>', '<h1>ショップボックス計算機</h1>'),
    '>박스 입력<': ('>Box input<', '>ボックス入力<'),
    '"예시 불러오기"': ('"Load an example"', '"例を読み込む"'),
    '>예시<': ('>Examples<', '>例<'),
    '나들이 박스 2,825': ('Explorer Box 2,825', '散歩ボックス 2,825'),
    '하이퍼 레이드박스 5,425': ('Ultra Raid Box 5,425', 'ハイパーレイドボックス 5,425'),
    '리모트 레이드 박스 500': ('Remote Raid Box 500', 'リモートレイドボックス 500'),
    '커뮤니티 데이 박스 1,350': ('Community Day Box 1,350', 'コミュニティデイボックス 1,350'),
    '>비우기<': ('>Clear<', '>クリア<'),
    '박스 가격(코인)': ('Box price (coins)', 'ボックスの価格（コイン）'),
    '<i>1</i>박스 가격': ('<i>1</i>Box price', '<i>1</i>ボックスの価格'),
    'placeholder="코인"': ('placeholder="coins"', 'placeholder="コイン"'),
    '<i>2</i>들어 있는 것 <span class="hint">눌러서 넣고 개수 입력</span>': ('<i>2</i>What\'s inside <span class="hint">tap to add, then set the count</span>', '<i>2</i>中身 <span class="hint">タップして追加し、個数を入力</span>'),
    '같이 든 아이템도 값으로 치기': ('Count the other items\' value too', 'ほかのアイテムも価値に含める'),
    '기본은 레이드패스만 계산하고 부화장치·별의조각 같은 나머지는 0코인(덤)으로 쳐요. 나머지도 꼭 쓴다면 체크하세요.': (
        'By default only raid passes are counted, and the rest (Egg Incubators, Star Pieces, etc.) count as 0 coins — freebies. Check this if you\'ll really use them too.',
        '初期設定ではレイドパスだけを計算し、ふかそうち・ほしのかけらなどほかのアイテムは0コイン（おまけ）として扱います。ほかのアイテムも必ず使うならチェックしてください。'),
    '<i>3</i>코인은 어디서 샀나요 <span class="hint">원화 환산용</span>': ('<i>3</i>What did you pay for coins? <span class="hint">to convert to real money</span>', '<i>3</i>コインの購入価格 <span class="hint">実際の金額に換算</span>'),
    '"원화 계산 방법"': ('"How to convert"', '"換算方法"'),
    '목록에서 고르기': ('Pick from list (Korea)', 'リストから選ぶ（韓国）'),
    'Web Store·게임 숍 코인 묶음': ('Web Store · in-game shop coin bundles (KRW)', 'Web Store・ゲーム内ショップのコイン（ウォン）'),
    '"코인 산 곳"': ('"Where you bought coins"', '"コインの購入先"'),
    '>직접 입력<': ('>Enter what you paid<', '>払った金額を入力<'),
    '세일·보너스 등 실제로 낸 돈과 받은 코인': ('The money you actually paid and the coins you got (sales and bonuses included)', '実際に払った金額ともらったコイン（セール・ボーナス込み）'),
    'placeholder="낸 돈" aria-label="낸 돈(원)"': ('placeholder="paid" aria-label="Amount paid"', 'placeholder="金額" aria-label="払った金額"'),
    '<span class="unit">원에</span>': ('<span class="unit">paid</span>', '<span class="unit">で</span>'),
    'placeholder="받은 코인" aria-label="받은 코인"': ('placeholder="coins" aria-label="Coins received"', 'placeholder="コイン" aria-label="もらったコイン"'),
    '<span class="unit">코인</span>': ('<span class="unit">coins</span>', '<span class="unit">コイン</span>'),
    '>결과<': ('>Results<', '>結果<'),
    '상점이 보여주는 할인': ('Discount the shop shows', 'ショップ表示の割引'),
    '묶음으로 따진 진짜 할인': ('Real discount vs. bundles', 'まとめ買いと比べた本当の割引'),
    '아끼는 코인': ('Coins saved', '節約できるコイン'),
    '박스를 원으로': ('Box in real money', 'ボックスを金額で'),
    '<th>아이템</th><th>이 박스에선 1개당</th><th>정가 1개당</th><th>역대 최저</th>': (
        '<th>Item</th><th>Per item in this box</th><th>Regular, per item</th><th>All-time low</th>',
        '<th>アイテム</th><th>このボックスで1個あたり</th><th>通常価格1個あたり</th><th>過去最安</th>'),
    '이 박스에선 1개당 = 박스 할인을 아이템 값 비율대로 나눈 값. 정가 1개당 = 상점 단품·묶음 중 가장 싼 값. 역대 최저 = 2023년 4월(리모트 레이드패스 가격 인상) 이후 상점 박스 중 박스 가격 ÷ 그 아이템 개수가 가장 낮았던 값(같이 든 아이템은 덤)과 실제 화면 캡처 날짜. 지역 한정이 의심되는 박스는 뺐어요.': (
        'Per item in this box = the box discount split by each item\'s value. Regular, per item = the cheapest of the shop\'s single and bundle prices. All-time low = the lowest box price ÷ that item\'s count among shop boxes since April 2023 (when Remote Raid Pass prices went up), other items treated as freebies, with the date of an actual screenshot. Boxes that looked region-limited are left out.',
        'このボックスで1個あたり = ボックスの割引をアイテムの価値の比率で分けた値。通常価格1個あたり = ショップの単品・まとめ買いのうち最も安い値。過去最安 = 2023年4月（リモートレイドパス値上げ）以降のショップボックスで、ボックス価格 ÷ そのアイテムの個数が最も低かった値（ほかのアイテムはおまけ扱い）と、実際の画面キャプチャの日付。地域限定と思われるボックスは除いています。'),
    '상점의 "46% OFF", <em>진짜</em>일까': ('Is the shop\'s "46% OFF" <em>real</em>?', 'ショップの「46% OFF」は<em>本当</em>？'),
    '상점이 줄 그어 보여주는 원래 가격은 안에 든 아이템을 <b>하나씩</b> 샀을 때 값이에요. 그런데 배틀패스는 3장 묶음이면 1장에 83코인이라, 묶음으로 따지면 진짜 할인은 더 작아요. 박스 가격과 구성만 넣으면 진짜 할인율, 레이드 한 판 가격, 지금까지 가장 쌌던 때와 비교해 드려요.': (
        'The crossed-out "original price" in the shop is what the items cost if you bought them <b>one by one</b>. But a 3-pack of Premium Battle Passes works out to 83 coins each, so the real discount against bundles is smaller. Enter the box price and contents to see the real discount, the cost of one raid, and how it compares with the cheapest it has ever been.',
        'ショップで線を引いて表示される元の価格は、中身を<b>1個ずつ</b>買ったときの値段です。でもプレミアムバトルパスは3枚セットなら1枚83コインなので、まとめ買いと比べた本当の割引はもっと小さくなります。ボックスの価格と中身を入れるだけで、本当の割引率、レイド1回の値段、これまでで一番安かった時との比較がわかります。'),
    '정가는 2026년 10월 10일 게임 상점·Web Store 화면에서 직접 확인했어요. 역대 최저가는 날짜가 남아 있는 실제 화면 캡처와 이벤트 기록만 모았어요.': (
        'Regular prices were checked directly in the in-game shop and Web Store (Korea) on October 10, 2026. All-time lows use only dated screenshots and event records.',
        '通常価格は2026年10月10日に韓国のゲーム内ショップ・Web Storeの画面で直接確認しました。過去最安は日付の残っている実際の画面キャプチャとイベント記録だけを集めています。'),
    '유튜브로 가기': ('YouTube (Korean)', 'YouTube（韓国語）'),
    '블로그로 가기': ('Blog (Korean)', 'ブログ（韓国語）'),
    '정가·코인 가격: 게임 상점·Pokémon GO Web Store 화면(한국, 2026.10.10). 상점 박스는 계정·날짜마다 다르게 뜰 수 있어요. 하이퍼볼·기술머신처럼 상점에서 단품으로 안 파는 아이템은 0코인으로 계산합니다. 닌텐도·나이언틱과 무관한 팬 도구입니다.': (
        'Regular and coin prices: in-game shop and Pokémon GO Web Store (Korea, Oct 10, 2026). Shop boxes can differ by account, date and region. Items not sold alone in the shop, like Ultra Balls and TMs, are counted as 0 coins. A fan-made tool, not affiliated with Nintendo or Niantic.',
        '通常価格・コイン価格：ゲーム内ショップ・Pokémon GO Web Storeの画面（韓国、2026.10.10）。ショップのボックスはアカウント・日付・地域によって異なる場合があります。ハイパーボール・わざマシンのようにショップで単品販売されていないアイテムは0コインで計算します。任天堂・Nianticとは関係のないファン製ツールです。'),
    # 스크립트 안 문구
    'sub: "아이스·허브·마그네틱·레이니"': ('sub: "Glacial · Mossy · Magnetic · Rainy"', 'sub: "アイス・ハーブ・マグネット・レイニー"'),
    'sub: "6개 180"': ('sub: "6 for 180"', 'sub: "6個 180"'),
    'sub: "10개 200"': ('sub: "10 for 200"', 'sub: "10個 200"'),
    'sub: "20개 100"': ('sub: "20 for 100"', 'sub: "20個 100"'),
    '"게임 숍 ': ('"In-game shop ', '"ゲーム内ショップ '),
    '위에서 박스에 든 아이템을 눌러 주세요': ('Tap the items in the box above', '上からボックスに入っているアイテムをタップしてください'),
    '"정가 1개당 " + fmt(unit(it), 1).replace(/\\.0$/, "") + "코인" : "상점 단품 없음 · 0으로 계산"': (
        '"Regular " + fmt(unit(it), 1).replace(/\\.0$/, "") + " coins each" : "Not sold alone · counted as 0"',
        '"通常 1個 " + fmt(unit(it), 1).replace(/\\.0$/, "") + "コイン" : "単品販売なし · 0で計算"'),
    'aria-label="하나 빼기"': ('aria-label="One less"', 'aria-label="1つ減らす"'),
    'aria-label="하나 더"': ('aria-label="One more"', 'aria-label="1つ増やす"'),
    'aria-label="${it.ko} 개수"': ('aria-label="${it.ko} count"', 'aria-label="${it.ko}の個数"'),
    'aria-label="${it.ko} 빼기"': ('aria-label="Remove ${it.ko}"', 'aria-label="${it.ko}を外す"'),
    '`낱개 합계 ${fmt(list)}코인`': ('`Sum of singles: ${fmt(list)} coins`', '`単品の合計 ${fmt(list)}コイン`'),
    '`${only ? "레이드패스만 " : ""}묶음 합계 ${fmt(bund)}코인`': ('`${only ? "Raid passes only · " : ""}Bundle total: ${fmt(bund)} coins`', '`${only ? "レイドパスのみ · " : ""}まとめ買い合計 ${fmt(bund)}コイン`'),
    'fmt(Math.abs(save)) + "코인"': ('fmt(Math.abs(save)) + " coins"', 'fmt(Math.abs(save)) + "コイン"'),
    '"묶음으로 따로 사는 것보다"': ('"vs. buying bundles separately"', '"まとめ買いで別々に買うより"'),
    '"묶음으로 따로 사는 게 더 쌈"': ('"Buying bundles separately is cheaper"', '"まとめ買いで別々に買う方が安い"'),
    # 원화가 아니라 그 나라 돈: 반올림 자리만 1코인 값에 맞춘다
    '"약 " + fmt(Math.round(price * wpc / 10) * 10) + "원"': ('"≈ " + fmt(price * wpc, wpc < 1 ? 2 : 0)', '"約 " + fmt(price * wpc, wpc < 1 ? 2 : 0)'),
    '`1코인 ${fmt(wpc, 2)}원 기준`': ('`at ${fmt(wpc, wpc < 1 ? 4 : 2)} per coin`', '`1コイン ${fmt(wpc, 2)} で計算`'),
    '"낸 돈과 받은 코인을 넣어 주세요"': ('"Enter what you paid and the coins you got"', '"払った金額ともらったコインを入力してください"'),
    '["레이드 한 판", "프리미엄 배틀패스 1장"]': ('["One raid", "1 Premium Battle Pass"]', '["レイド1回", "プレミアムバトルパス1枚"]'),
    '["리모트 레이드 한 판", "리모트 레이드패스 1장"]': ('["One remote raid", "1 Remote Raid Pass"]', '["リモートレイド1回", "リモートレイドパス1枚"]'),
    '`${fmt(per, 1)}코인 · 약 ${fmt(Math.round(per * wpc))}원`': ('`${fmt(per, 1)} coins · ≈ ${fmt(per * wpc, wpc < 1 ? 2 : 0)}`', '`${fmt(per, 1)}コイン · 約 ${fmt(per * wpc, wpc < 1 ? 2 : 0)}`'),
    '${RAID[k][0]}(${RAID[k][1]})': ('${RAID[k][0]} (${RAID[k][1]})', '${RAID[k][0]}（${RAID[k][1]}）'),
    '`${fmt(per, 1)}코인`':('`${fmt(per, 1)} coins`', '`${fmt(per, 1)}コイン`'),
    '`3장 묶음(1장 ${fmt(base, 1)}코인)보다 싸요 → 이득`': ('`Cheaper than the 3-pack (${fmt(base, 1)} coins each) → good deal`', '`3枚セット（1枚 ${fmt(base, 1)}コイン）より安い → お得`'),
    '`3장 묶음(1장 ${fmt(base, 1)}코인)보다 비싸요 → 묶음이 나아요`': ('`Pricier than the 3-pack (${fmt(base, 1)} coins each) → buy the 3-pack`', '`3枚セット（1枚 ${fmt(base, 1)}コイン）より高い → セットの方がお得`'),
    '"같이 든 아이템은 0코인(덤)으로 치고 레이드패스만 계산했어요. 나머지도 쓴다면 위의 「같이 든 아이템도 값으로 치기」를 체크하세요."': (
        '"Other items count as 0 coins (freebies), so only raid passes were counted. If you\'ll use the rest too, check “Count the other items\' value too” above."',
        '"ほかのアイテムは0コイン（おまけ）として、レイドパスだけで計算しました。ほかも使うなら、上の「ほかのアイテムも価値に含める」にチェックしてください。"'),
    '`같이 든 아이템 값(${fmt(rest)}코인, 묶음 기준)을 빼고 계산했어요. 체크를 끄면 레이드패스만으로 계산해요.`': (
        '`Subtracted the other items\' value (${fmt(rest)} coins at bundle prices). Uncheck to count raid passes only.`',
        '`ほかのアイテムの価値（${fmt(rest)}コイン、まとめ買い基準）を引いて計算しました。チェックを外すとレイドパスだけで計算します。`'),
    'here == null ? "덤"': ('here == null ? "Freebie"', 'here == null ? "おまけ"'),
    '"<span class=lo>역대 최저보다 쌈!</span>"': ('"<span class=lo>Below the all-time low!</span>"', '"<span class=lo>過去最安より安い！</span>"'),
    '"<span class=lo>역대 최저와 같음</span>"': ('"<span class=lo>Ties the all-time low</span>"', '"<span class=lo>過去最安と同じ</span>"'),
    '" · 정가가 더 쌈"': ('" · regular price is cheaper"', '" · 通常価格の方が安い"'),
    '`${zeros.join(" · ")}: 상점에서 단품으로 안 팔아서 0코인으로 계산했어요(덤).`': (
        '`${zeros.join(" · ")}: not sold alone in the shop, so counted as 0 coins (freebie).`',
        '`${zeros.join(" · ")}：ショップで単品販売されていないので0コイン（おまけ）で計算しました。`'),
}
DESC = ('Pokémon GO shop box calculator: the real discount against bundles, the cost of one raid, and all-time lows for each item.',
             'ポケモンGOのショップボックス計算機。まとめ買いと比べた本当の割引率、レイド1回あたりの値段、アイテムごとの過去最安がわかります。')

def extra(src, li):
    for ko, tr in ITEMS.items():
        src = src.replace(f'ko: "{ko}"', f'ko: "{tr[li]}"')
    # 코인 산 곳 목록(한국 원화) — 번역판에선 숨기지만 문구는 옮겨 둔다
    src = re.sub(r'(\d[\d,]*)원 → ([\d,]+)코인', (lambda m: f'₩{m[1]} → {m[2]} coins') if li == 0 else (lambda m: f'{m[1]}ウォン → {m[2]}コイン'), src)
    # 원화 목록은 한국 가격이라 빼고, 처음부터 「낸 돈 직접 입력」으로
    src = src.replace('let startMode = "list"; try { if (localStorage.getItem("shopcalc-mode") === "custom") startMode = "custom"; } catch (e) {}', 'let startMode = "custom";')
    src = src.replace('</style>', '  .opt[data-mode="list"] { display: none; }\n</style>', 1)
    lang = ('en', 'ja')[li]
    src = src.replace('"shopcalc-', f'"shopcalc-{lang}-')  # 한국어판에 넣은 원화 값이 섞이지 않게
    return src

