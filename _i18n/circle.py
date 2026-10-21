# 원고정 연습기 /circle/ 번역표 — _언어판.py가 읽는다. 표의 값은 (영어, 일본어)
# 판정 글자 Nice!/Great!/Excellent!는 게임 화면 그대로(일본어 게임도 영어로 뜬다). 그림자 Shadow/シャドウ, 커브볼 Curveball/カーブボール
# 확인 필요: '원고정'은 게임 용어가 아니라 설명형 이름으로 둠(Circle-Lock Throw Practice / サークル固定スロー練習)
TABLE = {
    '<title>이로치수집가 원고정 연습기</title>': ('<title>Circle-Lock Throw Practice · Shiny Collector Tools</title>', '<title>サークル固定スロー練習 · 色違いコレクター</title>'),
    '포켓몬고 <b>이로치 수집가</b> 도구함': ('Pokémon GO <b>Shiny Collector</b> Tools', 'ポケモンGO <b>色違いコレクター</b> ツール'),
    '포켓몬고 <b>이로치 수집가</b>': ('Pokémon GO <b>Shiny Collector</b>', 'ポケモンGO <b>色違いコレクター</b>'),
    '<span class="here">원고정</span>': ('<span class="here">Circle lock</span>', '<span class="here">サークル固定</span>'),
    '<h1>원고정 연습기</h1>': ('<h1>Circle-Lock Throw Practice</h1>', '<h1>サークル固定スロー練習</h1>'),
    '>연습장<': ('>Practice<', '>練習場<'),
    'aria-label="연습 단계"': ('aria-label="Practice level"', 'aria-label="練習の段階"'),
    'aria-pressed="true">나이스</button>': ('aria-pressed="true">Nice</button>', 'aria-pressed="true">Nice</button>'),
    'aria-pressed="false">그레이트</button>': ('aria-pressed="false">Great</button>', 'aria-pressed="false">Great</button>'),
    'aria-pressed="false">엑설런트</button>': ('aria-pressed="false">Excellent</button>', 'aria-pressed="false">Excellent</button>'),
    'aria-label="연속 성공"><span>연속</span>': ('aria-label="Streak"><span>Streak</span>', 'aria-label="連続成功"><span>連続</span>'),
    'aria-label="볼 조작 영역. 스페이스를 누르고 있으면 원이 줄어들고, 위쪽 화살표로 던집니다."': (
        'aria-label="Ball control area. Hold Space to shrink the circle, press the up arrow to throw."',
        'aria-label="ボール操作エリア。スペースを押し続けるとサークルが縮み、上矢印で投げます。"'),
    '<b>시작</b>아래 볼을 꾹 누르고 있어 보세요. 돌릴 필요 없이 누르고만 있어도 원이 줄어듭니다.': (
        '<b>Start</b>Press and hold the ball below. No need to spin it: just holding shrinks the circle.',
        '<b>スタート</b>下のボールを長押ししてみてください。回さなくても、押しているだけでサークルが縮みます。'),
    '<li>볼을 꾹 눌러 원 줄이고 손 떼기</li>': ('<li>Hold the ball to shrink the circle, then let go</li>', '<li>ボールを長押ししてサークルを縮め、指を離す</li>'),
    '<li>날뛸 때까지 기다리기</li>': ('<li>Wait for it to attack</li>', '<li>暴れるまで待つ</li>'),
    '<li>날뛰기 시작하면 볼 잡기</li>': ('<li>When it starts, grab the ball</li>', '<li>暴れ始めたらボールをつかむ</li>'),
    '<li>끝나기 1초 전에 던지기</li>': ('<li>Throw 1 second before it ends</li>', '<li>終わる1秒前に投げる</li>'),
    '<span class="lab">포켓몬</span>': ('<span class="lab">Pokémon</span>', '<span class="lab">ポケモン</span>'),
    'aria-label="포켓몬 종류"': ('aria-label="Pokémon kind"', 'aria-label="ポケモンの種類"'),
    '>일반 · 가끔 날뜀<': ('>Normal · sometimes<', '>通常 · ときどき暴れる<'),
    '>그림자 · 자주 날뜀<': ('>Shadow · often<', '>シャドウ · よく暴れる<'),
    '<span class="lab">동작 길이</span>': ('<span class="lab">Attack length</span>', '<span class="lab">動きの長さ</span>'),
    'aria-label="포켓몬 동작 길이"': ('aria-label="Length of the Pokémon\'s attack"', 'aria-label="ポケモンの動きの長さ"'),
    '>짧게 0.8초<': ('>Short 0.8 s<', '>短い 0.8秒<'),
    '>길게 1.8초<': ('>Long 1.8 s<', '>長い 1.8秒<'),
    ' 도움 표시 (기준선·타이밍 글자)': (' Show hints (guide lines, timing text)', ' ヒントを表示（目安の線・タイミングの文字）'),
    '<span>던진 횟수</span>': ('<span>Throws</span>', '<span>投げた回数</span>'),
    '<span>성공</span>': ('<span>Hits</span>', '<span>成功</span>'),
    '<span>최고 연속</span>': ('<span>Best streak</span>', '<span>最高連続</span>'),
    '키보드: <kbd>Space</kbd> 누르고 있기 = 볼 잡기 · <kbd>↑</kbd> = 던지기': ('Keyboard: hold <kbd>Space</kbd> = grab the ball · <kbd>↑</kbd> = throw', 'キーボード：<kbd>Space</kbd>長押し = ボールをつかむ · <kbd>↑</kbd> = 投げる'),
    'aria-label="더 보기"': ('aria-label="More"', 'aria-label="もっと見る"'),
    '<b>원고정, 영상으로 보기</b><span>실제 포획에서 두 번 연속 엑설런트</span>': (
        '<b>Circle lock on video (Korean)</b><span>Two Excellent throws in a row on a real catch</span>',
        '<b>サークル固定を動画で（韓国語）</b><span>実際の捕獲で2回連続Excellent</span>'),
    '<b>한 장으로 보는 정리</b><span>블로그에서 저장해 두고 보기</span>': (
        '<b>One-page summary (blog, Korean)</b><span>Save it from the blog</span>',
        '<b>1枚でわかるまとめ（ブログ・韓国語）</b><span>ブログで保存して見る</span>'),
    '>원고정, 다섯 단계<': ('>Circle lock in five steps<', '>サークル固定の5ステップ<'),
    '원을 원하는 크기에 멈춰 두고, 포켓몬이 날뛰는 틈에 던져서 매번 같은 크기에 맞히는 방법이에요.': (
        'Freeze the circle at the size you want, throw while the Pokémon is attacking, and hit the same size every time.',
        'サークルを好きな大きさで止めておき、ポケモンが暴れているすきに投げて、毎回同じ大きさに当てる方法です。'),
    '<strong>볼을 눌러 원을 줄이고 손 떼기</strong>누르고만 있어도 원이 줄어요. 돌릴 필요 없습니다. 원하는 크기에서 손을 떼면 원은 안 보여도 그 크기로 남아 있어요.': (
        '<strong>Hold the ball to shrink the circle, then let go</strong>Just holding shrinks it; no need to spin. Let go at the size you want: the circle disappears but stays at that size.',
        '<strong>ボールを押してサークルを縮め、指を離す</strong>押しているだけでサークルが縮みます。回す必要はありません。好きな大きさで指を離すと、サークルは見えなくてもその大きさのまま残ります。'),
    '<strong>날뛸 때까지 기다리기</strong>가만히 있을 때 던지면 날아가는 사이에 날뛰기 시작해서 튕겨낼 수 있어요. 기다리는 게 기술의 절반입니다.': (
        '<strong>Wait for it to attack</strong>Throw while it\'s still and it may start attacking mid-flight and knock the ball away. Waiting is half the trick.',
        '<strong>暴れるまで待つ</strong>じっとしているときに投げると、飛んでいる間に暴れ始めてはじかれることがあります。待つのが技術の半分です。'),
    '<strong>날뛰기 시작하면 볼 잡기</strong>날뛰는 동안엔 원이 줄지 않아요. 다만 동작이 끝난 뒤에도 계속 잡고 있으면 다시 줄다가 큰 원으로 돌아가니, 잡으면 바로 던질 준비를 하세요.': (
        '<strong>When it starts, grab the ball</strong>The circle doesn\'t shrink while it attacks. But if you keep holding after the attack ends, it shrinks again and resets to the big circle, so be ready to throw as soon as you grab.',
        '<strong>暴れ始めたらボールをつかむ</strong>暴れている間はサークルが縮みません。ただ、動きが終わってもつかんだままだと、また縮んでから大きなサークルに戻るので、つかんだらすぐ投げる準備をしてください。'),
    '<strong>끝나기 1초 전에 던지기</strong>볼이 날아가는 데 1초쯤 걸려요. 동작이 끝난 걸 보고 던지면 늦습니다. 던지는 순간이 아니라 도착하는 순간에 포켓몬이 가만히 있어야 해요. 그래서 끝나는 모습을 잘 봐 둬야 합니다.': (
        '<strong>Throw 1 second before it ends</strong>The ball takes about 1 second to fly. If you wait to see the attack end, you\'re too late. The Pokémon has to be still when the ball arrives, not when you throw, so watch closely how the attack ends.',
        '<strong>終わる1秒前に投げる</strong>ボールが飛ぶのに1秒ほどかかります。動きが終わったのを見てから投げると遅れます。投げる瞬間ではなく、届く瞬間にポケモンがじっとしている必要があります。だから終わり方をよく見ておきましょう。'),
    '<strong>나이스 → 그레이트 → 엑설런트</strong>처음부터 작은 원을 노리면 타이밍을 못 익혀요. 큰 원으로 타이밍부터 손에 붙이고 원을 줄여 가세요.': (
        '<strong>Nice → Great → Excellent</strong>Aim for the small circle from the start and you won\'t learn the timing. Get the timing down with a big circle first, then shrink it.',
        '<strong>Nice → Great → Excellent</strong>最初から小さなサークルを狙うとタイミングが身につきません。大きなサークルでタイミングを覚えてから、サークルを縮めていきましょう。'),
    '>실제 게임과 다른 점<': ('>How this differs from the game<', '>実際のゲームとの違い<'),
    '포켓몬마다 날뛰는 동작의 길이와 모양이 달라요. 그림자 포켓몬은 훨씬 자주 날뛰고요. 여기서는 일반·그림자, 짧은 동작·긴 동작으로만 연습하니, 게임에서는 잡으려는 포켓몬의 동작이 어떻게 끝나는지 먼저 한두 번 지켜보세요. 커브볼은 넣지 않았습니다. 곧게 미는 것만으로 타이밍을 익히는 데는 충분해요.': (
        'Each Pokémon\'s attack differs in length and shape, and Shadow Pokémon attack much more often. Here you only practice normal/Shadow and short/long attacks, so in the game, watch how your target\'s attack ends once or twice first. Curveballs aren\'t included: straight throws are enough to learn the timing.',
        'ポケモンごとに暴れる動きの長さと形が違います。シャドウポケモンはずっとよく暴れます。ここでは通常・シャドウ、短い動き・長い動きだけで練習するので、ゲームでは捕まえたいポケモンの動きがどう終わるかを先に1〜2回見てください。カーブボールは入れていません。まっすぐ投げるだけでもタイミングを覚えるには十分です。'),
    '원고정, <em>손에 익을 때까지</em>': ('Circle lock, <em>until it\'s in your fingers</em>', 'サークル固定を<em>手が覚えるまで</em>'),
    '영상으로 봐도 손이 안 따라가는 기술이라 여기서 바로 연습할 수 있게 만들었어요. 나이스부터 시작해서 세 번 연속 성공하면 다음 단계로 올라갑니다. 볼이 아까울 일도 없어요.': (
        'Watching a video doesn\'t make your hands follow, so this lets you practice right here. Start at Nice; three hits in a row moves you up a level. No Poké Balls wasted.',
        '動画を見ても手がついてこない技なので、ここですぐ練習できるようにしました。Niceから始めて3回連続で成功すると次の段階に上がります。ボールがもったいないこともありません。'),
    '손을 떼도 원 크기가 남는 것, 볼이 날아가는 시간은 직접 찍은 포획 영상 두 편을 0.1초 단위로 재서 맞췄어요. 연습용 포켓몬은 이 도구를 위해 그린 그림입니다. 닌텐도·나이언틱과 무관한 팬 도구입니다.': (
        'That the circle size stays after you let go, and the ball\'s flight time, were matched by timing two of our own catch recordings to 0.1 s. The practice Pokémon is an original drawing made for this tool. A fan-made tool, not affiliated with Nintendo or Niantic.',
        '指を離してもサークルの大きさが残ること、ボールが飛ぶ時間は、自分で撮った捕獲動画2本を0.1秒単位で測って合わせました。練習用のポケモンはこのツールのために描いた絵です。任天堂・Nianticとは関係のないファン製ツールです。'),
    # 스크립트 안 문구
    'ko: "나이스"': ('ko: "Nice"', 'ko: "Nice"'), 'ko: "그레이트"': ('ko: "Great"', 'ko: "Great"'), 'ko: "엑설런트"': ('ko: "Excellent"', 'ko: "Excellent"'),
    'text: "튕겨냈다!"': ('text: "Knocked away!"', 'text: "はじかれた！"'),
    '"너무 빨랐어요", `동작이 끝나기 ${early.toFixed(1)}초 전에 도착했어요. 딱 그만큼만 늦게 던지면 됩니다.`': (
        '"Too early", `It arrived ${early.toFixed(1)} s before the attack ended. Throw just that much later.`',
        '"早すぎました", `動きが終わる${early.toFixed(1)}秒前に届きました。ちょうどその分だけ遅く投げればOKです。`'),
    '"튕겨냈어요", "던진 뒤에 날뛰기 시작했어요. 이래서 원고정을 씁니다. 날뛰는 걸 보고 나서 던지면 이런 일이 없어요."': (
        '"Knocked away", "It started attacking after you threw. That\'s why circle lock exists: throw after you see the attack start and this won\'t happen."',
        '"はじかれました", "投げたあとに暴れ始めました。だからサークル固定を使います。暴れるのを見てから投げればこうなりません。"'),
    'text: "빗나감"': ('text: "Miss"', 'text: "はずれ"'),
    '"빗나갔어요", "옆으로 흘렀어요. 손가락을 위로 곧게 밀어 보세요."': ('"Missed", "It drifted sideways. Swipe straight up."', '"はずれました", "横にそれました。指をまっすぐ上にはじいてみてください。"'),
    'text: "원 밖"': ('text: "Outside"', 'text: "サークル外"'),
    '"원 밖에 맞았어요", "포켓몬에는 맞았지만 원 안이 아니라 판정 글자가 안 떠요. 원이 작을수록 더 곧게 던져야 합니다."': (
        '"Outside the circle", "It hit the Pokémon but not inside the circle, so no throw bonus. The smaller the circle, the straighter you need to throw."',
        '"サークルの外に当たりました", "ポケモンには当たりましたがサークルの中ではないので判定の文字が出ません。サークルが小さいほどまっすぐ投げる必要があります。"'),
    '`타이밍은 맞았는데 원이 아직 커요. ${need.ko} 크기까지 줄인 다음에 손을 떼세요.`': (
        '`Good timing, but the circle is still too big. Shrink it to ${need.ko} size before letting go.`',
        '`タイミングは合っていましたが、サークルがまだ大きいです。${need.ko}の大きさまで縮めてから指を離してください。`'),
    '`${gr.ko}, 그런데`, "가만히 있을 때 던져서 맞은 거라 운이 섞였어요. 연속 기록은 날뛰는 중에 던진 것만 셉니다."': (
        '`${gr.ko}, but`, "You threw while it was still, so luck was involved. The streak only counts throws made during an attack."',
        '`${gr.ko}、でも`, "じっとしているときに投げて当たったので運もありました。連続記録は暴れている間に投げたものだけ数えます。"'),
    '`동작이 끝나고 ${after.toFixed(1)}초 뒤에 도착했어요. ${after < 0.5 ? "딱 좋은 타이밍이에요." : "맞았어요. 조금 더 일찍 던져도 됩니다."}`': (
        '`It arrived ${after.toFixed(1)} s after the attack ended. ${after < 0.5 ? "Perfect timing." : "A hit. You can throw a little earlier."}`',
        '`動きが終わって${after.toFixed(1)}秒後に届きました。${after < 0.5 ? "ちょうどいいタイミングです。" : "当たりました。もう少し早く投げても大丈夫です。"}`'),
    '"세 번 연속!", `이제 ${GRADES[S.stage].ko} 크기로 올라갑니다. 원을 더 줄이고 손을 떼세요.`': (
        '"Three in a row!", `Moving up to ${GRADES[S.stage].ko} size. Shrink the circle more before letting go.`',
        '"3回連続！", `${GRADES[S.stage].ko}の大きさに上がります。サークルをもっと縮めてから指を離してください。`'),
    # 캔버스 안내 글자 — 지금 해야 할 일. '!'로 끝나면 주황색(급할 때)
    'cue = "원부터 줄여야 해요"': ('cue = "Shrink the circle first"', 'cue = "まずサークルを縮めて"'),
    '"아직… 잡고만 있기" : "지금 던져요!"': ('"Not yet… just hold" : "Throw now!"', '"まだ…つかんだまま" : "今投げて!"'),
    'cue = "지금 볼을 잡아요!"': ('cue = "Grab the ball now!"', 'cue = "今ボールをつかんで!"'),
    '"지금 손 떼기!" : "꾹 누르고 있기"': ('"Let go now!" : "Keep holding"', '"今指を離して!" : "長押しのまま"'),
    '"날뛸 때까지 기다리기…" : "볼을 꾹 누르기"': ('"Wait for it to attack…" : "Press and hold the ball"', '"暴れるまで待って…" : "ボールを長押し"'),
    'G.cue.includes("지금")': ('G.cue.endsWith("!")', 'G.cue.endsWith("!")'),
    '"연속" : `연속 ${S.streak}`': ('"Streak" : `Streak ${S.streak}`', '"連続" : `連続 ${S.streak}`'),
    '"원은 조금만 줄이고 손을 떼도 돼요. 날뛰는 중에 던져서 끝난 뒤에 도착시키는 타이밍부터 익히세요." : `점선 안쪽까지 원이 줄었을 때 손을 떼세요. 세 번 연속이면 ${S.stage === 1 ? "엑설런트로 올라갑니다." : "완성입니다."}`': (
        '"You can let go after shrinking the circle just a little. First learn to throw during the attack so the ball arrives after it ends." : `Let go once the circle is inside the dotted line. Three in a row ${S.stage === 1 ? "moves you up to Excellent." : "and you\'re done."}`',
        '"サークルは少し縮めるだけで指を離してもOK。暴れている間に投げて、終わったあとに届くタイミングから覚えましょう。" : `点線の内側までサークルが縮んだら指を離してください。3回連続で${S.stage === 1 ? "Excellentに上がります。" : "完成です。"}`'),
    '"긴 동작" : "짧은 동작", S.long ? "볼이 날아가는 시간보다 동작이 길어요. 시작하자마자 던지면 튕겨냅니다. 잡고 기다렸다가 끝나기 1초 전에 던지세요." : "동작이 짧아서 날뛰기 시작한 걸 보고 바로 던지면 맞아요."': (
        '"Long attack" : "Short attack", S.long ? "The attack lasts longer than the ball\'s flight. Throw as soon as it starts and it gets knocked away. Grab, wait, and throw 1 second before it ends." : "The attack is short, so throwing right when it starts will hit."',
        '"長い動き" : "短い動き", S.long ? "ボールが飛ぶ時間より動きが長いです。始まってすぐ投げるとはじかれます。つかんで待ってから、終わる1秒前に投げてください。" : "動きが短いので、暴れ始めたのを見てすぐ投げれば当たります。"'),
    '"그림자 포켓몬" : "일반 포켓몬", S.shadow ? "쉴 틈 없이 날뜁니다. 한 번 놓쳐도 금방 또 날뛰니, 원만 줄여 두면 기회는 많아요. 대신 가만히 있을 때 던지면 거의 튕겨냅니다." : "가끔씩만 날뜁니다. 원을 줄여 두고 느긋하게 기다리세요."': (
        '"Shadow Pokémon" : "Normal Pokémon", S.shadow ? "It attacks nonstop. Miss one and another comes soon, so with the circle shrunk you get plenty of chances. But throw while it\'s still and it almost always knocks the ball away." : "It only attacks now and then. Shrink the circle and wait calmly."',
        '"シャドウポケモン" : "通常のポケモン", S.shadow ? "休みなく暴れます。1回逃してもすぐまた暴れるので、サークルを縮めておけばチャンスは多いです。ただし、じっとしているときに投げるとほぼはじかれます。" : "ときどきしか暴れません。サークルを縮めて、のんびり待ちましょう。"'),
}
DESC = ('Practice the circle-lock throw for Pokémon GO in your browser: freeze the circle, wait for the attack, and land Nice, Great and Excellent throws in a row.',
        'ポケモンGOのサークル固定スローをブラウザで練習。サークルを止めて、暴れるのを待ち、Nice・Great・Excellentを連続で決めましょう。')

def extra(src, li):
    # 기록은 언어마다 따로 저장(한국어판과 섞이지 않게)
    return src.replace('"circlelock"', f'"circlelock-{("en", "ja")[li]}"')
