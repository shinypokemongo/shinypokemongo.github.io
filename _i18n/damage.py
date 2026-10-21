# 데미지 배율 쌓기 /damage/ 번역표 — _언어판.py가 읽는다. 표의 값은 (영어, 일본어)
# 타입·날씨·친구 단계·팀 파워·거수참은 게임 문구(i18n) 그대로. 자속은 게임 용어가 아니라 풀어 씀
# 확인 필요: 포에버 프렌드(i18n에 아직 없음), 박스 검색어 @날씨의 영어·일본어(못 찾아서 그 문장은 뺌)
import re
from _i18n._이름 import names

TYPES = names('pokemon_type_')
WEATHER = {  # weather_sunny · weather_partly_cloudy · weather_overcast · weather_rainy · weather_snow · weather_windy · weather_fog
    '맑음': ('Sunny', '晴天'), '약간구름': ('Partly Cloudy', 'ときどき曇り'), '흐림': ('Cloudy', '曇り'),
    '비': ('Rain', '雨'), '눈': ('Snow', '雪'), '강풍': ('Windy', '強風'), '안개': ('Fog', '霧'),
}

TABLE = {
    '<title>이로치수집가 데미지 배율 쌓기</title>': ('<title>Damage Multiplier Stacker · Shiny Collector Tools</title>', '<title>ダメージ倍率の積み上げ · 色違いコレクター</title>'),
    '포켓몬고 <b>이로치 수집가</b> 도구함': ('Pokémon GO <b>Shiny Collector</b> Tools', 'ポケモンGO <b>色違いコレクター</b> ツール'),
    '포켓몬고 <b>이로치 수집가</b>': ('Pokémon GO <b>Shiny Collector</b>', 'ポケモンGO <b>色違いコレクター</b>'),
    '<span class="here">레이드 데미지</span>': ('<span class="here">Raid damage</span>', '<span class="here">レイドダメージ</span>'),
    '<h1>데미지 배율 쌓기</h1>': ('<h1>Damage Multiplier Stacker</h1>', '<h1>ダメージ倍率の積み上げ</h1>'),
    '>배율 계산<': ('>Multiplier calculator<', '>倍率の計算<'),
    'aria-label="지금 배율"': ('aria-label="Current multiplier"', 'aria-label="今の倍率"'),
    '<span>맨몸</span>': ('<span>Base</span>', '<span>素</span>'),
    '<span>지금</span>': ('<span>Now</span>', '<span>今</span>'),
    'aria-label="바로 넣어 보기"': ('aria-label="Quick presets"', 'aria-label="すぐ試す"'),
    '>전부 끄기<': ('>All off<', '>全部オフ<'),
    '>혼자 약점만 찌를 때<': ('>Solo, weakness only<', '>ひとりで弱点を突くだけ<'),
    '>영상의 5.3배 조합<': ('>The 5.3× combo from the video<', '>動画の5.3倍の組み合わせ<'),
    '>그림자까지 얹으면<': ('>Add a Shadow Pokémon<', '>シャドウポケモンも足すと<'),
    'aria-label="더 보기"': ('aria-label="More"', 'aria-label="もっと見る"'),
    '<b>데미지 올리는 6가지, 영상으로</b><span>1위는 딱 한 방, 2위는 남이 받는다</span>': (
        '<b>6 ways to raise damage (video, Korean)</b><span>No. 1 lasts one hit, No. 2 goes to someone else</span>',
        '<b>ダメージを上げる6つの方法（動画・韓国語）</b><span>1位は一発だけ、2位はほかの人が受ける</span>'),
    '<b>한 장으로 보는 정리</b><span>블로그에서 저장해 두고 보기</span>': (
        '<b>One-page summary (blog, Korean)</b><span>Save it from the blog</span>',
        '<b>1枚でわかるまとめ（ブログ・韓国語）</b><span>ブログで保存して見る</span>'),
    '<summary>날씨별 부스트 타입 7종</summary>': ('<summary>Boosted types for the 7 weathers</summary>', '<summary>天候ごとにブーストされるタイプ（7種）</summary>'),
    '<th>날씨</th><th>위력 +20% 받는 기술 타입</th>': ('<th>Weather</th><th>Move types that get +20% power</th>', '<th>天候</th><th>威力+20%になる技のタイプ</th>'),
    # 검색어 @날씨는 영어·일본어 게임 표기를 확인하지 못해 그 문장을 뺀다
    '약간구름과 흐림이 가장 많이 헷갈려요. 박스 검색창에 <b>@날씨</b>를 치면 지금 날씨로 부스트받는 기술을 가진 포켓몬만 나옵니다.': (
        'Partly Cloudy and Cloudy are the two people mix up most.',
        'ときどき曇りと曇りが一番まちがえやすいです。'),
    '>알고 쌓아야 하는 것들<': ('>What to know before you stack<', '>積む前に知っておくこと<'),
    '크기만 보면 안 되는 이유가 하나씩 붙어 있어요.': ('Each one has a catch beyond its size.', 'どれも大きさだけでは判断できない理由があります。'),
    '<small>팀 파워</small>': ('<small>Party Power</small>', '<small>チームパワー</small>'),
    '가장 크지만 <b>다음 스페셜 어택 한 방</b>에만 붙어요. 저절로 걸리지도 않습니다. 노말 어택으로 게이지를 채우고 왼쪽 아래 파란 원을 눌러야 해요.': (
        'The biggest, but it applies only to <b>your next Charged Attack</b>. It doesn\'t trigger by itself: fill the gauge with Fast Attacks, then tap the blue circle at the bottom left.',
        '一番大きいですが、<b>次のスペシャルアタック1発</b>だけに付きます。自動ではかかりません。ノーマルアタックでゲージをためて、左下の青い丸をタップする必要があります。'),
    '<small>메가</small>': ('<small>Mega</small>', '<small>メガ</small>'),
    '상시 보너스 중엔 가장 큰데 <b>내가 아니라 같이 싸우는 다른 트레이너</b>가 받아요. 메가와 타입이 달라도 +10%는 줍니다. 여러 명이 꺼내도 가장 높은 것 하나만 적용돼요.': (
        'The biggest always-on bonus, but it goes to <b>the other Trainers fighting with you, not you</b>. Even moves of a different type than the Mega get +10%. If several people bring one, only the highest applies.',
        '常にかかるボーナスでは一番大きいですが、受けるのは<b>自分ではなく一緒に戦うほかのトレーナー</b>です。メガとタイプが違っても+10%は付きます。何人が出しても一番高いもの1つだけが適用されます。'),
    '<small>날씨</small>': ('<small>Weather</small>', '<small>天候</small>'),
    '공짜지만 <b>보스 기술에도 똑같이 붙어요.</b> 보스 기술 타입이 부스트되는 날씨면 내가 더 빨리 쓰러집니다.': (
        'Free, but <b>it boosts the boss\'s moves too.</b> If the weather boosts the boss\'s move type, you faint faster.',
        'タダですが、<b>ボスの技にも同じく付きます。</b>ボスの技のタイプがブーストされる天候だと、こちらが早く倒れます。'),
    '<small>이중약점</small>': ('<small>Double weakness</small>', '<small>二重弱点</small>'),
    '포켓몬고의 약점은 2배가 아니라 1.6배, 이중약점은 4배가 아니라 2.56배예요. 0배도 없어서 가장 안 먹히는 경우가 0.244배입니다.': (
        'In Pokémon GO a weakness is 1.6×, not 2×, and a double weakness is 2.56×, not 4×. There is no 0× either: the least effective case is 0.244×.',
        'ポケモンGOの弱点は2倍ではなく1.6倍、二重弱点は4倍ではなく2.56倍です。0倍もなく、一番効かない場合で0.244倍です。'),
    '같은 기술인데 <em>1.6배와 5.3배</em>': ('Same move, <em>1.6× or 5.3×</em>', '同じ技なのに<em>1.6倍と5.3倍</em>'),
    '약점만 찌르면 1.6배, 자속·날씨·친구·메가까지 겹치면 같은 기술이 5.3배로 들어갑니다. 스위치를 하나씩 켜 보면서 무엇이 크고 무엇이 함정인지 확인해 보세요. 배율은 영상에서 출처를 맞춰 본 값만 넣었어요.': (
        'Hitting a weakness alone gives 1.6×; stack same-type bonus, weather, friends and Mega and the same move lands at 5.3×. Turn the switches on one by one to see what is big and what is a trap. Only multipliers checked against sources for the video are included.',
        '弱点を突くだけなら1.6倍、タイプ一致・天候・フレンド・メガまで重ねると同じ技が5.3倍になります。スイッチを1つずつオンにして、何が大きくて何が落とし穴かを確かめてください。倍率は動画で出典を照らし合わせた値だけを入れています。'),
    '<a href="../">도구함</a>': ('<a href="../">Tools (Korean)</a>', '<a href="../">ツール（韓国語）</a>'),
    '상성·자속·날씨·메가 배율: Pokétory 「레이드 조건별 대미지 배율」 · PoGoMate 한글판 · Pokémon GO Wiki 세 곳 일치. 그림자 1.2: 게임 데이터. 친구 보너스 %는 공식이 소·중·대로만 밝혀서 커뮤니티 추정치예요. 팀 파워 2배: 공식 한글 공지. 거수참: 공식 pokemongo.com. 닌텐도·나이언틱과 무관한 팬 도구입니다.': (
        'Type, same-type, weather and Mega multipliers: three sources agree (Pokétory raid damage table, PoGoMate Korean edition, Pokémon GO Wiki). Shadow 1.2: game data. Friendship bonus % is a community estimate, since the official numbers are only small/medium/large. Party Power 2×: official Korean announcement. Behemoth Blade: official pokemongo.com. A fan-made tool, not affiliated with Nintendo or Niantic.',
        '相性・タイプ一致・天候・メガの倍率：Pokétory「レイド条件別ダメージ倍率」・PoGoMate韓国語版・Pokémon GO Wikiの3か所で一致。シャドウ1.2：ゲームデータ。フレンドボーナスの%は公式が小・中・大としか公開していないためコミュニティの推定値です。チームパワー2倍：公式韓国語のお知らせ。きょじゅうざん：公式pokemongo.com。任天堂・Nianticとは関係のないファン製ツールです。'),
    # 스크립트 안 문구
    'name: "타입 상성", note: "포켓몬고엔 0배가 없어요. 가장 안 먹히는 경우가 0.244배."': (
        'name: "Type matchup", note: "Pokémon GO has no 0×. The least effective case is 0.244×."',
        'name: "タイプ相性", note: "ポケモンGOに0倍はありません。一番効かない場合で0.244倍。"'),
    '[["이중약점", 2.56], ["약점", 1.6], ["보통", 1], ["반감", 0.625], ["이중반감", 0.390625], ["가장 안 먹힘", 0.244140625]]': (
        '[["Double weak", 2.56], ["Weak", 1.6], ["Neutral", 1], ["Resisted", 0.625], ["Double resisted", 0.390625], ["Least effective", 0.244140625]]',
        '[["二重弱点", 2.56], ["弱点", 1.6], ["等倍", 1], ["半減", 0.625], ["二重半減", 0.390625], ["一番効かない", 0.244140625]]'),
    'name: "자속", note: "기술 타입이 내 포켓몬 타입과 같을 때.", opts: [["없음", 1], ["자속", 1.2]]': (
        'name: "Same-type bonus", note: "When the move\'s type matches your Pokémon\'s type.", opts: [["None", 1], ["Same type", 1.2]]',
        'name: "タイプ一致", note: "技のタイプが自分のポケモンのタイプと同じとき。", opts: [["なし", 1], ["タイプ一致", 1.2]]'),
    'name: "날씨 부스트", note: "<b>보스 기술에도 똑같이 붙어요.</b> GO 배틀리그에는 없습니다.", opts: [["없음", 1], ["부스트", 1.2]]': (
        'name: "Weather Boost", note: "<b>It boosts the boss\'s moves too.</b> Not in GO Battle League.", opts: [["None", 1], ["Boosted", 1.2]]',
        'name: "天候ブースト", note: "<b>ボスの技にも同じく付きます。</b>GOバトルリーグにはありません。", opts: [["なし", 1], ["ブースト", 1.2]]'),
    'name: "그림자 포켓몬", note: "공격이 1.2배인 대신 <b>받는 데미지도 1.2배</b>예요.", opts: [["일반", 1], ["그림자", 1.2]]': (
        'name: "Shadow Pokémon", note: "Attack is 1.2×, but <b>damage taken is 1.2× too</b>.", opts: [["Normal", 1], ["Shadow", 1.2]]',
        'name: "シャドウポケモン", note: "攻撃が1.2倍になる代わりに<b>受けるダメージも1.2倍</b>です。", opts: [["通常", 1], ["シャドウ", 1.2]]'),
    'name: "메가진화 (같이 싸우는 사람 것)", note: "<b>내가 아니라 다른 트레이너가 받아요.</b> 여러 명이 꺼내도 가장 높은 것 하나만.",\n      opts: [["없음", 1], ["타입 다름", 1.1], ["같은 타입", 1.3]]': (
        'name: "Mega Evolution (a teammate\'s)", note: "<b>Other Trainers get it, not you.</b> If several bring one, only the highest counts.",\n      opts: [["None", 1], ["Different type", 1.1], ["Same type", 1.3]]',
        'name: "メガシンカ（一緒に戦う人の）", note: "<b>自分ではなくほかのトレーナーが受けます。</b>何人が出しても一番高いもの1つだけ。",\n      opts: [["なし", 1], ["タイプ違い", 1.1], ["同じタイプ", 1.3]]'),
    # friendship_level_1~4. 포에버는 i18n에 없어 확인 필요
    'name: "친구와 함께", tag: "추정치", note: "공식은 소·중·대로만 밝혀요. 포에버 프렌드는 최단 180일.",\n      opts: [["없음", 1], ["굿", 1.03], ["그레이트", 1.05], ["울트라", 1.07], ["베스트", 1.1], ["포에버", 1.12]]': (
        'name: "With a friend", tag: "estimate", note: "Officially only small/medium/large. Forever Friend takes at least 180 days.",\n      opts: [["None", 1], ["Good", 1.03], ["Great", 1.05], ["Ultra", 1.07], ["Best", 1.1], ["Forever", 1.12]]',
        'name: "フレンドと一緒", tag: "推定値", note: "公式は小・中・大としか公開していません。フォーエバーは最短180日。",\n      opts: [["なし", 1], ["友達", 1.03], ["仲良し", 1.05], ["親友", 1.07], ["大親友", 1.1], ["フォーエバー", 1.12]]'),
    'name: "자시안 거수참", note: "6분에 별의모래 5,000 + 자시안 사탕 5. 어드벤처 이펙트는 <b>한 번에 하나만</b> 켜져요.", opts: [["없음", 1], ["켬", 1.1]]': (
        'name: "Zacian Behemoth Blade", note: "6 minutes for 5,000 Stardust + 5 Zacian Candy. Only <b>one adventure effect at a time</b>.", opts: [["None", 1], ["On", 1.1]]',
        'name: "ザシアン きょじゅうざん", note: "6分でほしのすな5,000 + ザシアンのアメ5。アドベンチャーエフェクトは<b>一度に1つだけ</b>。", opts: [["なし", 1], ["オン", 1.1]]'),
    'name: "팀 파워", note: "<b>다음 스페셜 어택 한 방만.</b> 게이지를 채우고 왼쪽 아래 파란 원을 눌러야 걸려요.", opts: [["없음", 1], ["발동", 2]]': (
        'name: "Party Power", note: "<b>Only your next Charged Attack.</b> Fill the gauge and tap the blue circle at the bottom left.", opts: [["None", 1], ["Active", 2]]',
        'name: "チームパワー", note: "<b>次のスペシャルアタック1発だけ。</b>ゲージをためて左下の青い丸をタップするとかかります。", opts: [["なし", 1], ["発動", 2]]'),
    '<b>따로 보는 것</b><span>아래 둘은 위의 배율들과 같은 식으로 곱해지는지 확인된 적이 없어요. 그래서 큰 숫자에는 넣지 않고 따로 보여 드립니다.</span>': (
        '<b>Shown separately</b><span>Nobody has confirmed that the two below multiply the same way as the ones above. So they are left out of the big number and shown on their own.</span>',
        '<b>別に表示するもの</b><span>下の2つは、上の倍率と同じように掛け算されるか確認されたことがありません。そのため大きな数字には入れず、別に表示します。</span>'),
    '`${fx(sure)}<small>배</small>`': ('`${fx(sure)}`', '`${fx(sure)}<small>倍</small>`'),
    '`맨몸으로 <b>100</b> 들어가던 기술이<br><b>${Math.round(sure * 100).toLocaleString("ko-KR")}</b> 들어가요`': (
        '`A move that did <b>100</b><br>now does <b>${Math.round(sure * 100).toLocaleString("ko-KR")}</b>`',
        '`素で<b>100</b>入っていた技が<br><b>${Math.round(sure * 100).toLocaleString("ko-KR")}</b>入ります`'),
    # 곱셈 줄의 짧은 이름: 한국어는 이름 첫 낱말을 쓰는데, 영어·일본어는 낱말 첫머리가 이름이 안 돼서 따로 둔다
    'it.name.split(" ")[0]': (
        '({ stab: "Same type", weather: "Weather", shadow: "Shadow", mega: "Mega", friend: "Friend" }[it.id])',
        '({ stab: "タイプ一致", weather: "天候", shadow: "シャドウ", mega: "メガ", friend: "フレンド" }[it.id])'),
    '"아래에서 하나씩 켜 보세요"': ('"Turn things on below, one by one"', '"下から1つずつオンにしてみてください"'),
    '`${names.join("·")}까지 같은 식으로 곱해진다면 <b>약 ${fx(all)}</b>. ${S.party ? "팀 파워는 그 한 방에만요." : "확인된 적은 없는 계산이에요."}`': (
        '`If ${names.join(" and ")} multiplied the same way: <b>about ${fx(all)}</b>. ${S.party ? "Party Power only for that one hit." : "This calculation has never been confirmed."}`',
        '`${names.join("・")}まで同じように掛け算されるなら<b>約${fx(all)}</b>。${S.party ? "チームパワーはその1発だけです。" : "確認されたことのない計算です。"}`'),
}
DESC = ('Pokémon GO raid damage multiplier stacker: type, same-type bonus, weather, Shadow, Mega and friendship — see what really multiplies and what is a trap.',
        'ポケモンGOのレイドダメージ倍率を積み上げる計算機。タイプ相性・タイプ一致・天候・シャドウ・メガ・フレンドで何倍になるかがわかります。')

def extra(src, li):
    # 날씨표: 날씨 이름과 타입 이름
    def row(m):
        w = WEATHER[m[2]][li]
        ts = (' · ' if li == 0 else '・').join(TYPES[t.strip()][li] for t in m[3].split('·'))
        return f'<tr><td>{m[1]} {w}</td><td>{ts}</td></tr>'
    return re.sub(r'<tr><td>(\S+) ([가-힣]+)</td><td>([가-힣 ·]+)</td></tr>', row, src)
