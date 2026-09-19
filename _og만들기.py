# 카톡·디스코드·검색 결과에 뜨는 공유 미리보기 이미지(1200x630)를 og/ 폴더에 만든다
# 사용: python _og만들기.py
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).parent / "og"; OUT.mkdir(exist_ok=True)
FONT = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"
W, H = 1200, 630


def font(size, weight="Black"):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_name(weight)
    return f


def hexa(c): return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


# (파일, 바탕, 포인트색, 배지 바탕, 배지 글자, 제목 두 줄, 설명)
PAGES = [
    ("home", "#0E0D1C", "#FFD166", "#3A331A", "도구", ["이로치수집가", "도구함"], "영상 보고, 여기서 바로 써먹기"),
    ("search", "#0F0D1C", "#6BF2A6", "#0E3B27", "&!", ["검색어", "검사기"], "붙여넣으면 뜻을 풀어주고, 틀린 곳을 고쳐서 복사"),
    ("showcase", "#0C1122", "#FFC94D", "#3A2F12", "1178", ["쇼케이스", "점수 계산기"], "키·몸무게·개체값을 넣으면 몇 점인지"),
    ("powerup", "#100C1F", "#F29BFF", "#3A1745", "Lv", ["강화 비용", "계산기"], "강화 버튼 숫자만 골라도 별의모래가 얼마나 드는지"),
    ("damage", "#0A1020", "#5CC8FF", "#10304A", "×5.3", ["데미지", "배율 쌓기"], "자속·날씨·메가·친구, 다 겹치면 몇 배인지"),
    ("circle", "#0A131F", "#FF7A59", "#3D1A10", "◎", ["원고정", "연습기"], "나이스부터 엑설런트까지, 던지는 타이밍 연습"),
]

for name, bg, accent, badge_bg, badge, title, desc in PAGES:
    im = Image.new("RGB", (W, H), hexa(bg))
    d = ImageDraw.Draw(im)
    # 오른쪽 위에서 번지는 포인트색 빛
    glow = Image.new("RGB", (W, H), hexa(bg)); gd = ImageDraw.Draw(glow)
    for i in range(60, 0, -1):
        r = 14 * i; t = (1 - i / 60) ** 2 * 0.22
        col = tuple(round(b + (a - b) * t) for a, b in zip(hexa(accent), hexa(bg)))
        gd.ellipse((W - 220 - r, 170 - r, W - 220 + r, 170 + r), fill=col)
    im.paste(glow); d = ImageDraw.Draw(im)

    d.text((80, 78), "포켓몬고", font=font(34, "Bold"), fill=(162, 157, 190))
    bw = d.textlength("포켓몬고 ", font=font(34, "Bold"))
    d.text((80 + bw, 78), "이로치 수집가", font=font(34, "Bold"), fill=hexa(accent))

    y = 170
    for i, line in enumerate(title):
        d.text((76, y), line, font=font(112), fill=hexa(accent) if i == 1 else (241, 238, 250))
        y += 138
    d.text((80, y + 26), desc, font=font(36, "Medium"), fill=(200, 196, 222))
    d.text((80, H - 84), "shinypokemongo.github.io", font=font(30, "Bold"), fill=(130, 125, 160))

    # 배지
    S = 260; x0, y0 = W - 80 - S, 150
    d.rounded_rectangle((x0, y0, x0 + S, y0 + S), radius=60, fill=hexa(badge_bg), outline=hexa(accent), width=4)
    size = 150 if len(badge) <= 2 else 92
    f = font(size)
    l, t, r, b = d.textbbox((0, 0), badge, font=f)
    d.text((x0 + (S - (r - l)) / 2 - l, y0 + (S - (b - t)) / 2 - t), badge, font=f, fill=hexa(accent))

    im.save(OUT / f"{name}.png", optimize=True)
    print(name, (OUT / f"{name}.png").stat().st_size // 1024, "KB")
