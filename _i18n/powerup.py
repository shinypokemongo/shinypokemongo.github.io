# 강화 비용 계산기 /powerup/ 번역표 — _언어판.py가 읽는다. 표의 값은 (영어, 일본어)
# 게임 용어는 i18n 그대로: 별의모래 Stardust/ほしのすな · 사탕 Candy/アメ · 사탕XL Candy XL/アメXL · 강화 Power Up/強化
# 그림자 Shadow/シャドウ · 정화 Purified/ライト · 반짝반짝 Lucky/キラ · 날씨 부스트 Weather Boost/天候ブースト · GO로켓단 Team GO Rocket/GOロケット団
TABLE = {
    '<title>이로치수집가 강화 비용 계산기</title>': ('<title>Power Up Cost Calculator · Shiny Collector Tools</title>', '<title>強化コスト計算機 · 色違いコレクター</title>'),
    '포켓몬고 <b>이로치 수집가</b> 도구함': ('Pokémon GO <b>Shiny Collector</b> Tools', 'ポケモンGO <b>色違いコレクター</b> ツール'),
    '포켓몬고 <b>이로치 수집가</b>': ('Pokémon GO <b>Shiny Collector</b>', 'ポケモンGO <b>色違いコレクター</b>'),
    '<span class="here">강화</span>': ('<span class="here">Power Up</span>', '<span class="here">強化</span>'),
    '<h1>강화 비용 계산기</h1>': ('<h1>Power Up Cost Calculator</h1>', '<h1>強化コスト計算機</h1>'),
    '>비용 계산<': ('>Cost calculator<', '>コストの計算<'),
    '<i>1</i>어떤 포켓몬인가요': ('<i>1</i>What kind of Pokémon?', '<i>1</i>どんなポケモン？'),
    'aria-label="포켓몬 상태"': ('aria-label="Pokémon type"', 'aria-label="ポケモンの状態"'),
    'aria-pressed="true">일반</button>': ('aria-pressed="true">Normal</button>', 'aria-pressed="true">通常</button>'),
    'aria-pressed="false">그림자</button>': ('aria-pressed="false">Shadow</button>', 'aria-pressed="false">シャドウ</button>'),
    'aria-pressed="false">정화</button>': ('aria-pressed="false">Purified</button>', 'aria-pressed="false">ライト</button>'),
    ' 반짝반짝 포켓몬이에요 <small id="luckyhint">(별의모래 절반)</small>': (' It\'s a Lucky Pokémon <small id="luckyhint">(half Stardust)</small>', ' キラポケモンです <small id="luckyhint">（ほしのすな半分）</small>'),
    '<i>2</i>지금 어디쯤인가요': ('<i>2</i>Where is it now?', '<i>2</i>今どのあたり？'),
    'aria-label="지금 레벨을 고르는 방법"': ('aria-label="How to pick the current level"', 'aria-label="今のレベルの選び方"'),
    '>강화 버튼 숫자로<': ('>By the Power Up button<', '>強化ボタンの数字で<'),
    '>레벨로<': ('>By level<', '>レベルで<'),
    '>강화 버튼에 적힌 별의모래<': ('>Stardust shown on the Power Up button<', '>強化ボタンに書かれたほしのすな<'),
    '>정확한 레벨 (몰라도 돼요)<': ('>Exact level (optional)<', '>正確なレベル（わからなくてもOK）<'),
    '>지금 레벨<': ('>Current level<', '>今のレベル<'),
    '얻고 나서 한 번도 강화 안 했다면 아래에서 고르세요.': ('Never powered up since you got it? Pick below.', '手に入れてから一度も強化していないなら下から選んでください。'),
    '>CP 10짜리<b>1</b>': ('>CP 10<b>1</b>', '>CP 10<b>1</b>'),
    '>리서치 보상<b>15</b>': ('>Research reward<b>15</b>', '>リサーチ報酬<b>15</b>'),
    '>알·레이드<b>20</b>': ('>Egg / Raid<b>20</b>', '>タマゴ・レイド<b>20</b>'),
    '>레이드(날씨 부스트)<b>25</b>': ('>Raid (Weather Boost)<b>25</b>', '>レイド（天候ブースト）<b>25</b>'),
    '>로켓단 그림자<b>8</b>': ('>Team GO Rocket Shadow<b>8</b>', '>GOロケット団のシャドウ<b>8</b>'),
    '>로켓단 그림자(날씨)<b>13</b>': ('>Team GO Rocket Shadow (weather)<b>13</b>', '>GOロケット団のシャドウ（天候）<b>13</b>'),
    '<i>3</i>어디까지 올릴 건가요': ('<i>3</i>How far will you go?', '<i>3</i>どこまで上げる？'),
    'aria-label="목표를 정하는 방법"': ('aria-label="How to set the goal"', 'aria-label="目標の決め方"'),
    '>목표 레벨<': ('>Target level<', '>目標レベル<'),
    '>강화 횟수<': ('>Number of power-ups<', '>強化回数<'),
    '40 <b>사탕만으로 끝</b>': ('40 <b>Candy only</b>', '40 <b>アメだけで済む</b>'),
    '50 <b>최대</b>': ('50 <b>Max</b>', '50 <b>最大</b>'),
    '>3회<': ('>3×<', '>3回<'), '>5회<': ('>5×<', '>5回<'), '>10회<': ('>10×<', '>10回<'), '>15회<': ('>15×<', '>15回<'), '>25회<': ('>25×<', '>25回<'),
    '"포켓몬을 ○회 강화하기" 리서치용. 1회 = 레벨 0.5. 가장 싸게 깨려면 CP 10짜리(레벨 1)로: 15회에 <b>7,000</b>.': (
        'For "Power up Pokémon ○ times" research. 1 power-up = 0.5 levels. Cheapest with a CP 10 Pokémon (level 1): 15 power-ups for <b>7,000</b>.',
        '「ポケモンを○回強化する」リサーチ用。1回 = レベル0.5。一番安く済ませるならCP 10（レベル1）で：15回で<b>7,000</b>。'),
    'aria-label="계산 결과"': ('aria-label="Result"', 'aria-label="計算結果"'),
    '>필요한 별의모래<': ('>Stardust needed<', '>必要なほしのすな<'),
    '<span>사탕</span>': ('<span>Candy</span>', '<span>アメ</span>'),
    '<span>사탕XL</span>': ('<span>Candy XL</span>', '<span>アメXL</span>'),
    '<span>강화 횟수</span>': ('<span>Power-ups</span>', '<span>強化回数</span>'),
    '<span>레벨 1~20 구간</span>': ('<span>Levels 1–20</span>', '<span>レベル1〜20</span>'),
    '<span>레벨 20~30 구간</span>': ('<span>Levels 20–30</span>', '<span>レベル20〜30</span>'),
    '<span>레벨 30~40 구간</span>': ('<span>Levels 30–40</span>', '<span>レベル30〜40</span>'),
    '<span>레벨 40~50 구간 (사탕XL)</span>': ('<span>Levels 40–50 (Candy XL)</span>', '<span>レベル40〜50（アメXL）</span>'),
    '>지금 가진 별의모래<': ('>Stardust you have<', '>今持っているほしのすな<'),
    '>하루에 버는 별의모래<': ('>Stardust earned per day<', '>1日にかせぐほしのすな<'),
    '>가볍게 1만<': ('>Casual 10K<', '>ゆるく1万<'),
    '>매일 3만<': ('>Daily 30K<', '>毎日3万<'),
    '>열심히 5만<': ('>Hard 50K<', '>がんばって5万<'),
    '>이벤트 10만<': ('>Event 100K<', '>イベント10万<'),
    '야생 1마리 <b>100</b> · 날씨 부스트면 <b>125</b> · 진화형(2단계) <b>300</b> · 최종 진화형(3단계) <b>500</b> · 별의조각을 쓰면 1.5배.': (
        'Wild catch <b>100</b> · with Weather Boost <b>125</b> · evolved (stage 2) <b>300</b> · final evolution (stage 3) <b>500</b> · ×1.5 with a Star Piece.',
        '野生1匹 <b>100</b> · 天候ブーストなら <b>125</b> · 進化形（2段階目） <b>300</b> · 最終進化形（3段階目） <b>500</b> · ほしのかけらで1.5倍。'),
    'aria-label="더 보기"': ('aria-label="More"', 'aria-label="もっと見る"'),
    '<b>별의모래, 영상으로 보기</b><span>어디에 쓰고 어디서 아끼는지</span>': (
        '<b>Stardust on video (Korean)</b><span>Where to spend it and where to save</span>',
        '<b>ほしのすなを動画で（韓国語）</b><span>どこで使い、どこで節約するか</span>'),
    '<b>한 장으로 보는 정리</b><span>블로그에서 저장해 두고 보기</span>': (
        '<b>One-page summary (blog, Korean)</b><span>Save it from the blog</span>',
        '<b>1枚でわかるまとめ（ブログ・韓国語）</b><span>ブログで保存して見る</span>'),
    '>강화 비용은 이렇게 정해져요<': ('>How power-up cost is decided<', '>強化コストの決まり方<'),
    'CP가 아니라 레벨로 정해집니다. 같은 CP 1500이어도 종에 따라 비용이 달라요.': (
        'It depends on level, not CP. Two Pokémon at CP 1500 can cost differently depending on the species.',
        'CPではなくレベルで決まります。同じCP 1500でも種類によってコストが違います。'),
    '<small>1회당 레벨</small>': ('<small>levels per power-up</small>', '<small>1回あたりのレベル</small>'),
    '강화 한 번에 레벨이 0.5씩 올라요. 같은 비용이 네 번(두 레벨) 이어지다가 다음 칸으로 넘어갑니다. 그래서 버튼 숫자만 봐도 레벨을 두 레벨 안쪽으로 좁힐 수 있어요.': (
        'Each power-up adds 0.5 levels. The same cost repeats four times (two levels) before moving to the next step, so the number on the button alone narrows the level to within two levels.',
        '1回の強化でレベルが0.5上がります。同じコストが4回（2レベル分）続いてから次の段階に移ります。だからボタンの数字だけでレベルを2レベル以内にしぼれます。'),
    '25만<small>40→50</small>': ('250K<small>40→50</small>', '25万<small>40→50</small>'),
    '레벨 1에서 40까지가 별의모래 약 27만, 40에서 50까지가 25만. 마지막 열 레벨이 그 앞 전체와 맞먹어요. 40부터는 사탕 대신 사탕XL 296개가 들어갑니다.': (
        'Level 1 to 40 takes about 270,000 Stardust; 40 to 50 takes 250,000. The last ten levels cost about as much as everything before them. From 40, it takes 296 Candy XL instead of Candy.',
        'レベル1から40までがほしのすな約27万、40から50までが25万。最後の10レベルがそれまで全部とほぼ同じです。40からはアメの代わりにアメXLが296個必要です。'),
    '<small>반짝반짝</small>': ('<small>Lucky</small>', '<small>キラ</small>'),
    '반짝반짝 포켓몬은 별의모래가 절반이에요. 사탕은 그대로입니다. 50까지 키울 포켓몬이라면 26만을 아끼는 셈이에요.': (
        'Lucky Pokémon cost half the Stardust. Candy stays the same. Taking one to 50 saves about 260,000.',
        'キラポケモンはほしのすなが半分です。アメはそのまま。50まで育てるなら約26万の節約になります。'),
    '<small>그림자</small>': ('<small>Shadow</small>', '<small>シャドウ</small>'),
    '그림자는 별의모래·사탕 모두 1.2배, 정화하면 0.9배. 정화 포켓몬이 반짝반짝까지 되면 0.45배로 가장 쌉니다.': (
        'Shadow Pokémon cost 1.2× Stardust and Candy; Purified cost 0.9×. A Purified Pokémon that is also Lucky is the cheapest at 0.45×.',
        'シャドウはほしのすな・アメとも1.2倍、ライトにすると0.9倍。ライトポケモンがキラにもなると0.45倍で一番安くなります。'),
    '레벨별 비용표 펼치기': ('Show the cost table by level', 'レベル別コスト表を開く'),
    '끝까지 키우려면 별의모래 <em>얼마나</em> 들까': ('<em>How much</em> Stardust to max it out?', '最後まで育てるとほしのすなは<em>どれだけ</em>？'),
    '게임은 포켓몬 레벨을 안 보여 주죠. 그래서 강화 버튼에 적힌 숫자만 골라도 계산되게 만들었어요. 비용표는 게임 데이터에서 직접 꺼냈습니다.': (
        'The game doesn\'t show a Pokémon\'s level, so this works from just the number on the Power Up button. The cost table comes straight from the game data.',
        'ゲームはポケモンのレベルを見せてくれません。だから強化ボタンに書かれた数字を選ぶだけで計算できるようにしました。コスト表はゲームデータから直接取り出しています。'),
    '비용표·배율: Pokémon GO 게임 데이터 POKEMON_UPGRADE_SETTINGS · LUCKY_POKEMON_SETTINGS (2026.9.1판). 레벨 1에서 25회까지는 게임에서 직접 눌러 본 합계 9개와 맞췄어요. 레벨 1부터 키우면 표보다 세 군데서 조금씩 싸서 15회 합계가 7,000입니다. 그 밖의 시작 레벨은 게임 데이터 표 그대로 계산합니다. 그림자·정화의 사탕 수는 배율을 곱해 올림한 값이에요. 무한다이노처럼 전용 사탕을 쓰는 포켓몬은 사탕 수가 다릅니다. 닌텐도·나이언틱과 무관한 팬 도구입니다.': (
        'Cost table and multipliers: Pokémon GO game data POKEMON_UPGRADE_SETTINGS · LUCKY_POKEMON_SETTINGS (Sept 1, 2026). From level 1 up to 25 power-ups, the results match 9 totals checked by actually powering up in the game. Starting from level 1 is a little cheaper than the table in three places, so 15 power-ups total 7,000. Other starting levels use the game data table as is. Candy for Shadow and Purified is the multiplied value rounded up. Pokémon with their own candy cost, like Eternatus, need different Candy amounts. A fan-made tool, not affiliated with Nintendo or Niantic.',
        'コスト表・倍率：Pokémon GOゲームデータ POKEMON_UPGRADE_SETTINGS · LUCKY_POKEMON_SETTINGS（2026.9.1版）。レベル1から25回までは、ゲームで実際に強化した合計9件と一致させました。レベル1から育てると表より3か所で少し安く、15回の合計は7,000です。そのほかの開始レベルはゲームデータの表どおりに計算します。シャドウ・ライトのアメの数は倍率を掛けて切り上げた値です。ムゲンダイナのように専用のアメのコストを使うポケモンはアメの数が違います。任天堂・Nianticとは関係のないファン製ツールです。'),
    # 스크립트 안 문구
    '`<option value="0">모르겠어요</option>`': ('`<option value="0">Not sure</option>`', '`<option value="0">わからない</option>`'),
    '`<option value="${h}">레벨 ${lv(h)}</option>`': ('`<option value="${h}">Level ${lv(h)}</option>`', '`<option value="${h}">レベル ${lv(h)}</option>`'),
    '`버튼에 <b>${fmt(shown(b.base))}</b>이 적혀 있으면 레벨 <b>${lv(b.lo)}~${lv(b.hi)}</b> 사이예요. 정확한 레벨을 모르면 결과를 범위로 보여 드려요.`': (
        '`If the button says <b>${fmt(shown(b.base))}</b>, it is between level <b>${lv(b.lo)} and ${lv(b.hi)}</b>. Without the exact level, results are shown as a range.`',
        '`ボタンに<b>${fmt(shown(b.base))}</b>と書かれていればレベル<b>${lv(b.lo)}〜${lv(b.hi)}</b>の間です。正確なレベルがわからなければ結果を範囲で表示します。`'),
    '"(그림자는 교환이 안 돼서 해당 없음)" : "(별의모래 절반)"': ('"(Shadow Pokémon can\'t be traded, so not possible)" : "(half Stardust)"', '"（シャドウは交換できないので対象外）" : "（ほしのすな半分）"'),
    '`레벨 ${lv(S.to)}까지 필요한 별의모래` : `${S.cnt}회 강화에 필요한 별의모래`': (
        '`Stardust needed to reach level ${lv(S.to)}` : `Stardust needed for ${S.cnt} power-ups`',
        '`レベル${lv(S.to)}まで必要なほしのすな` : `${S.cnt}回の強化に必要なほしのすな`'),
    '`${big.n}회` : `${small.n}~${big.n}회`': ('`${big.n}` : `${small.n}–${big.n}`', '`${big.n}回` : `${small.n}〜${big.n}回`'),
    '"목표가 지금 레벨보다 높아야 계산돼요."': ('"The target must be higher than the current level."', '"目標が今のレベルより高くないと計算できません。"'),
    '`정확한 레벨을 모를 땐 큰 쪽(${fmt(big.dust)})으로 준비하면 안전해요. 위에서 정확한 레벨을 고르면 하나로 좁혀집니다.`': (
        '`Without the exact level, plan for the larger number (${fmt(big.dust)}) to be safe. Pick the exact level above to narrow it to one.`',
        '`正確なレベルがわからないときは大きいほう（${fmt(big.dust)}）で準備すると安心です。上で正確なレベルを選ぶと1つにしぼられます。`'),
    '`가장 많이 드는 곳은 레벨 ${name} 구간: ${fmt(big.seg[top])} (${Math.round(big.seg[top] / big.dust * 100)}%).` : `전부 레벨 ${name} 구간에서 나가요.`': (
        '`Most of it goes to levels ${name}: ${fmt(big.seg[top])} (${Math.round(big.seg[top] / big.dust * 100)}%).` : `All of it is spent in levels ${name}.`',
        '`一番かかるのはレベル${name}：${fmt(big.seg[top])}（${Math.round(big.seg[top] / big.dust * 100)}%）。` : `全部レベル${name}の区間で使います。`'),
    '` 같은 포켓몬이 반짝반짝이었다면 ${fmt(big.dust / 2)}으로 끝났어요.`': ('` If it were Lucky, it would be just ${fmt(big.dust / 2)}.`', '`同じポケモンがキラなら${fmt(big.dust / 2)}で済みました。`'),
    '"지금 가진 별의모래로 <b>바로</b> 끝낼 수 있어요."': ('"You can finish it <b>right now</b> with the Stardust you have."', '"今持っているほしのすなで<b>すぐ</b>終わらせられます。"'),
    '`모자란 별의모래 <b>${fmt(need)}</b> → 하루 ${fmt(per)}씩이면 <b>${fmt(Math.ceil(need / per))}일</b>${isRange ? " (큰 쪽 기준)" : ""}`': (
        '`Stardust short: <b>${fmt(need)}</b> → at ${fmt(per)} a day, <b>${fmt(Math.ceil(need / per))} days</b>${isRange ? " (larger number)" : ""}`',
        '`足りないほしのすな <b>${fmt(need)}</b> → 1日${fmt(per)}ずつなら<b>${fmt(Math.ceil(need / per))}日</b>${isRange ? "（大きいほう基準）" : ""}`'),
    '`모자란 별의모래 <b>${fmt(need)}</b>`': ('`Stardust short: <b>${fmt(need)}</b>`', '`足りないほしのすな <b>${fmt(need)}</b>`'),
    '`(${{ normal: "일반", shadow: "그림자", purified: "정화" }[S.state]}${S.lucky ? " · 반짝반짝" : ""} 기준)`': (
        '`(${{ normal: "Normal", shadow: "Shadow", purified: "Purified" }[S.state]}${S.lucky ? " · Lucky" : ""})`',
        '`（${{ normal: "通常", shadow: "シャドウ", purified: "ライト" }[S.state]}${S.lucky ? " · キラ" : ""}基準）`'),
    '"<tr><th>레벨</th><th>별의모래</th><th>사탕</th><th>사탕XL</th><th>여기서 50까지</th></tr>"': (
        '"<tr><th>Level</th><th>Stardust</th><th>Candy</th><th>Candy XL</th><th>From here to 50</th></tr>"',
        '"<tr><th>レベル</th><th>ほしのすな</th><th>アメ</th><th>アメXL</th><th>ここから50まで</th></tr>"'),
}
DESC = ('Pokémon GO power-up cost calculator: Stardust, Candy and Candy XL to reach any level, from just the number on the Power Up button. Shadow, Purified and Lucky included.',
        'ポケモンGOの強化コスト計算機。強化ボタンの数字だけで、目標レベルまでのほしのすな・アメ・アメXLがわかります。シャドウ・ライト・キラにも対応。')
