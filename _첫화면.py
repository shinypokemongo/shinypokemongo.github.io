# 도구함 첫 화면(index.html, 직접 편집)에서 영어·일본어 첫 화면을 만든다 → en/index.html, ja/index.html
# 사용: python _첫화면.py   — 첫 화면을 고치면 다시 돌릴 것. 한글이 남으면 멈춘다
# 도구 이름은 각 도구 번역판의 h1과 맞춘다
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://shinypokemongo.github.io'
T = {  # 한국어: (영어, 일본어)
    '포켓몬고 이로치 수집가의 도구함 — 검색어 검사기, 쇼케이스 점수 계산기, 강화 비용 계산기, 원고정 연습기, 데미지 배율, 교환 리스트, 레거시 기술 명단. 게임 데이터와 한국어판 실측으로 만들었습니다.': (
        'Pokémon GO tools by Shiny Collector — search string checker, showcase score calculator, IV pick helper, power-up cost calculator, legacy move list, trade list maker, damage multipliers, circle lock practice and shop box calculator. Built from game data.',
        'ポケモンGOの便利ツール集 — 検索ワードチェッカー、おひろめスコア計算機、どれを育てる？、強化コスト計算機、レガシーわざ一覧、交換リスト作成、ダメージ倍率、サークル固定スロー練習、ショップボックス計算機。ゲームデータをもとに作っています。'),
    '포켓몬고 검색어 검사기, 쇼케이스 점수 계산기, 강화 비용 계산기, 원고정 연습기, 데미지 배율, 교환 리스트, 레거시 기술 명단. 게임 데이터와 한국어판 실측으로 만들었습니다.': (
        'Pokémon GO search string checker, showcase score calculator, power-up cost calculator, legacy move list, trade list maker and more. Built from game data.',
        'ポケモンGOの検索ワードチェッカー、おひろめスコア計算機、強化コスト計算機、レガシーわざ一覧、交換リスト作成など。ゲームデータをもとに作っています。'),
    '<title>이로치수집가 도구함</title>': ('<title>Shiny Collector Tools · Pokémon GO</title>', '<title>色違いコレクター ツール · ポケモンGO</title>'),
    'content="이로치수집가 도구함"': ('content="Shiny Collector Tools"', 'content="色違いコレクター ツール"'),
    '<span>포켓몬고 이로치 수집가</span>': ('<span>Pokémon GO Shiny Collector</span>', '<span>ポケモンGO 色違いコレクター</span>'),
    '<h1>이로치수집가 <b>도구함</b></h1>': ('<h1>Shiny Collector <b>Tools</b></h1>', '<h1>色違いコレクター <b>ツール</b></h1>'),
    'aria-label="도구"': ('aria-label="Tools"', 'aria-label="ツール"'),
    'aria-label="채널"': ('aria-label="Channels"', 'aria-label="チャンネル"'),
    '<b>검색어 검사기</b><span>붙여넣으면 뜻을 풀어주고, 틀린 곳을 고쳐서 복사</span>': (
        '<b>Search String Checker</b><span>Paste a search string to see what it means, fix mistakes and copy</span>',
        '<b>検索ワードチェッカー</b><span>貼り付けると意味を解説し、間違いを直してコピー</span>'),
    '<b>쇼케이스 점수 계산기</b><span>키·몸무게·개체값을 넣으면 몇 점인지</span>': (
        '<b>Showcase Score Calculator</b><span>Enter height, weight and IVs to see the score</span>',
        '<b>おひろめスコア計算機</b><span>高さ・重さ・個体値を入れると何点か</span>'),
    '<b>뭘 키울까</b><span>같은 포켓몬 개체값 여러 개 중 뭘 키울지 — 진화한 모습 기준, 타입·기술로도 찾기</span>': (
        '<b>Which one to power up?</b><span>Compare IVs of the same Pokémon — judged as the evolved form, search by type or move too</span>',
        '<b>どれを育てる？</b><span>同じポケモンの個体値を比べてどれを育てるか — 進化後の姿で判定、タイプ・技でも検索</span>'),
    '<b>강화 비용 계산기</b><span>강화 버튼 숫자만 골라도 별의모래가 얼마나 드는지</span>': (
        '<b>Power Up Cost Calculator</b><span>Pick the number on the Power Up button to see how much Stardust it takes</span>',
        '<b>強化コスト計算機</b><span>強化ボタンの数字を選ぶだけで、ほしのすながどれだけ必要か</span>'),
    '<b>레거시 기술 명단</b><span>대단한 기술머신으로만 배우는 기술. 진화 한 줄씩 정리</span>': (
        '<b>Legacy Moves List</b><span>Moves only learnable with an Elite TM, by evolution line</span>',
        '<b>レガシーわざ一覧</b><span>すごいわざマシンでしか覚えない技を進化ごとに整理</span>'),
    '<span class="ic" style="background:#3A2F12;color:#FFD86B">교환</span>': (
        '<span class="ic" style="background:#3A2F12;color:#FFD86B">⇄</span>', '<span class="ic" style="background:#3A2F12;color:#FFD86B">⇄</span>'),
    '<b>포켓몬 교환 리스트</b><span>구해요·드려요를 그림 한 장으로. 이로치·코스튬·배경까지</span>': (
        '<b>Pokémon Trade List Maker</b><span>Your “looking for” and “for trade” lists in one image, with shinies, costumes and backgrounds</span>',
        '<b>ポケモン交換リストを作る</b><span>「求」「譲」を画像1枚に。色違い・コスチューム・背景まで</span>'),
    '<b>데미지 배율 쌓기</b><span>자속·날씨·메가·친구, 다 겹치면 몇 배인지</span>': (
        '<b>Damage Multiplier Stacker</b><span>STAB, weather, Mega, friends — how much it all adds up to</span>',
        '<b>ダメージ倍率の積み上げ</b><span>タイプ一致・天候ブースト・メガ・フレンド、全部重ねると何倍か</span>'),
    '<b>원고정 연습기</b><span>나이스부터 엑설런트까지, 던지는 타이밍 연습</span>': (
        '<b>Circle-Lock Throw Practice</b><span>From Nice to Excellent — practice your throw timing</span>',
        '<b>サークル固定スロー練習</b><span>NiceからExcellentまで、投げるタイミングを練習</span>'),
    '<b>상점 박스 계산기</b><span>박스 가격·구성을 넣으면 진짜 할인율, 레이드 한 판 가격, 역대 최저가</span>': (
        '<b>Shop Box Calculator</b><span>Enter a box price and contents for the real discount, cost per raid and all-time low</span>',
        '<b>ショップボックス計算機</b><span>ボックスの価格と中身を入れると本当の割引率、レイド1回の値段、過去最安</span>'),
    '<b>▶ 유튜브</b><span>@ShinyPokemongo</span>': ('<b>▶ YouTube</b><span>@ShinyPokemongo (Korean)</span>', '<b>▶ YouTube</b><span>@ShinyPokemongo（韓国語）</span>'),
    '<b>▤ 블로그</b><span>한 장으로 보는 정리</span>': ('<b>▤ Blog</b><span>One-page guides (Korean)</span>', '<b>▤ ブログ</b><span>1枚でわかるまとめ（韓国語）</span>'),
    '<h2>영상 보고, <b>여기서 바로</b> 써먹기</h2>': ('<h2>Watch the video, <b>use it right here</b></h2>', '<h2>動画を見て、<b>ここですぐ</b>使う</h2>'),
    '<p>유튜브에서 설명한 내용을 바로 쓸 수 있게 만든 도구들입니다. 게임 데이터와 한국어판에서 직접 확인한 결과로 만들었어요.</p>': (
        '<p>Tools made so you can put what the YouTube videos explain to use right away. Built from game data and results checked in the game.</p>',
        '<p>YouTubeで解説した内容をすぐ使えるように作ったツールです。ゲームデータと、ゲーム内で直接確かめた結果をもとにしています。</p>'),
    '문의 · 질문 · 요청 사항은 <a href="mailto:back6845@gmail.com">back6845@gmail.com</a>으로 연락 주세요.<br>닌텐도·나이언틱과 무관한 팬 도구입니다.': (
        'Questions or requests: <a href="mailto:back6845@gmail.com">back6845@gmail.com</a><br>A fan-made tool, not affiliated with Nintendo or Niantic.',
        'お問い合わせ・ご要望：<a href="mailto:back6845@gmail.com">back6845@gmail.com</a><br>任天堂・Nianticとは関係のないファン製ツールです。'),
}
src = open(os.path.join(HERE, 'index.html'), encoding='utf-8').read()
for li, lang in enumerate(('en', 'ja')):
    s = src.replace('<html lang="ko">', f'<html lang="{lang}">')
    for ko in sorted(T, key=len, reverse=True):
        s = s.replace(ko, T[ko][li])
    s = s.replace(f'<link rel="canonical" href="{SITE}/">', f'<link rel="canonical" href="{SITE}/{lang}/">')
    s = s.replace(f'<meta property="og:url" content="{SITE}/">', f'<meta property="og:url" content="{SITE}/{lang}/">')
    s = s.replace('content="ko_KR"', 'content="en_US"' if lang == 'en' else 'content="ja_JP"')
    s = s.replace(' aria-current="page">한국어<', '>한국어<').replace(f'hreflang="{lang}" lang="{lang}">', f'hreflang="{lang}" lang="{lang}" aria-current="page">')
    s = s.replace('src="shop/ic/', 'src="/shop/ic/')
    if lang == 'ja':
        s = s.replace('word-break: keep-all', 'word-break: normal; line-break: strict')
        s = s.replace('"Apple SD Gothic Neo", "Malgun Gothic"', '"Hiragino Sans", "Yu Gothic", "Meiryo"')
    left = sorted(set(re.findall(r'[가-힣][가-힣 ·]*', s.replace('>한국어<', '><'))))
    if left:
        sys.exit(f'[{lang}] 한글이 남음: {left}')
    os.makedirs(os.path.join(HERE, lang), exist_ok=True)
    open(os.path.join(HERE, lang, 'index.html'), 'w', encoding='utf-8').write(s)
    print('built ->', f'{lang}/')
