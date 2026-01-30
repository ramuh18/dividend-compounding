import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# 시스템 인코딩 강제 설정 (외계어 방지)
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [설정]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "Dividend Master"
# ★ 2호기 주소로 꼭 변경!
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
# ★ 본진 주소 (수익의 핵심)
MAIN_HQ_URL = "https://empire-analyst.digital/"
HISTORY_FILE = "history.json"

# ==========================================
# [강력 세척] AI 혼잣말 & 생각 과정 제거
# ==========================================
def clean_ai_output(text):
    if not text: return ""
    # 1. JSON 형태의 생각 과정 삭제
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = re.sub(r'reasoning_content":".*?"', '', text, flags=re.DOTALL)
    
    # 2. "Let's count words", "Draft:" 같은 잡담 삭제
    patterns = [
        r"Draft:", r"Word count:", r"Let's write", r"Note:", r"Internal Monologue:",
        r"I'll count manually", r"Now count words", r"Start directly with the content"
    ]
    for p in patterns:
        text = re.sub(p, "", text, flags=re.IGNORECASE)
    
    # 3. 불필요한 기호 및 따옴표 정리
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    return text.strip()

# ==========================================
# [주제 선정] 6시간마다 새로운 뉴스 가져오기
# ==========================================
def get_hot_topic():
    try:
        # 뉴스 소스: 개인 금융 & 투자 뉴스
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:10]).title
    except: raw_news = "The Power of Passive Income and Dividends"

    prompt = f"Rewrite '{raw_news}' into a high-end financial title (MAX 9 WORDS). Focus on dividend growth. English Only. NO intro/outro."
    
    title = "Dividend Growth Intelligence"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.1}}, timeout=15)
        if resp.status_code == 200:
            title = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: pass
    return title

# ==========================================
# [본문 생성] 본진으로 트래픽을 몰아주는 페르소나
# ==========================================
def generate_part(topic, focus):
    prompt = f"Write a professional report on '{topic}'. Focus: {focus}. Emphasize compounding wealth and dividends. Institutional tone. English Only. Output ONLY final article text. NO thinking, NO counting."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.2}}, timeout=30)
        if resp.status_code == 200:
            return clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: pass
    return "Market analysis in progress..."

def create_professional_html(topic, img_url, body_html, canonical_url):
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} | Dividend Master</title>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Merriweather', serif; line-height: 1.8; color: #334155; max-width: 850px; margin: 0 auto; padding: 20px; }}
        header {{ background: #0f172a; color: white; padding: 50px 20px; text-align: center; border-radius: 15px; margin-bottom: 40px; border-bottom: 5px solid #fbbf24; }}
        .hq-link {{ display: inline-block; background: #fbbf24; color: #0f172a; padding: 12px 25px; border-radius: 8px; font-weight: bold; text-decoration: none; margin-top: 20px; transition: 0.3s; }}
        .hq-link:hover {{ transform: scale(1.05); }}
        h1 {{ font-size: 2.8rem; color: #0f172a; margin: 30px 0; line-height: 1.2; }}
        .featured-img {{ width: 100%; border-radius: 12px; margin-bottom: 35px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
        .newsletter-box {{ background: #f1f5f9; padding: 40px; border-radius: 15px; text-align: center; margin-top: 60px; border: 1px solid #cbd5e1; }}
        .sub-btn {{ background: #b91c1c; color: white; border: none; padding: 12px 35px; border-radius: 6px; font-weight: bold; cursor: pointer; }}
    </style></head>
    <body>
    <header>
        <div style="font-size: 2.2rem; font-weight: 900; letter-spacing: 1px;">DIVIDEND MASTER</div>
        <p style="opacity: 0.8;">Institutional Grade Research on Compound Wealth</p>
        <a href="{MAIN_HQ_URL}" class="hq-link">Expert Analysis at Empire Analyst HQ →</a>
    </header>
    <main>
        <div style="color: #b91c1c; font-weight: bold; text-transform: uppercase; letter-spacing: 1px;">{current_date} • Intelligence Report</div>
        <h1>{topic}</h1>
        <img src="{img_url}" class="featured-img">
        <div class="content">{body_html}</div>
    </main>
    <div class="newsletter-box">
        <h3>📩 Secure Your Financial Future</h3>
        <p>Subscribe to our Weekly Dividend Digest and get our '2026 High-Yield' watchlist.</p>
        <form action="YOUR_NEWSLETTER_URL" method="post">
            <input type="email" placeholder="Your best email address" required style="padding: 13px; width: 65%; border-radius: 6px; border: 1px solid #cbd5e1; margin-bottom:10px;">
            <button type="submit" class="sub-btn">Join Now</button>
        </form>
    </div>
    <footer style="margin-top: 80px; text-align: center; color: #94a3b8; font-size: 0.85rem; border-top: 1px solid #e2e8f0; padding-top: 30px;">
        &copy; 2026 Dividend Master. A strategic node of <a href="{MAIN_HQ_URL}" style="color:#64748b;">Empire Analyst Network</a>.
    </footer>
    </body></html>"""

def main():
    log("🏁 Striker #2 (Dividend) Active")
    topic = get_hot_topic()
    log(f"🔥 Subject: {topic}")
    
    content = ""
    content += generate_part(topic, "Macro-Economic Impact on Yields") + "\n\n"
    content += generate_part(topic, "Long-term Compounding Strategies")
    
    html_body = markdown.markdown(content)
    # 이미지 생성 (차트 느낌)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional stock market chart showing upward trend, luxury financial theme, gold and navy')}"
    
    file_timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    archive_filename = f"post_{file_timestamp}.html"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    new_entry = {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_filename}
    history.insert(0, new_entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_professional_html(topic, img_url, html_body, f"{BLOG_BASE_URL}{archive_filename}")
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_filename, "w", encoding="utf-8") as f: f.write(full_html)
    log("✅ Mission Complete")

if __name__ == "__main__": main()
