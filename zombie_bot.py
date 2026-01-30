import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [시스템] 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [설정]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "Dividend Master"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
MAIN_HQ_URL = "https://empire-analyst.digital/"

# [수익화]
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_TAG = "empireanalyst-20"
AMAZON_LINK = f"https://www.amazon.com/s?k=ledger+nano+x&tag={AMAZON_TAG}"

HISTORY_FILE = "history.json"

def clean_ai_output(text):
    if not text: return ""
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = re.sub(r'reasoning_content":".*?"', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    patterns = [r"Draft:", r"Word count:", r"Note:", r"Internal Monologue:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

# ==========================================
# [강력한 본문 생성] 1,300자 확보용 4단계 로직
# ==========================================
def generate_long_content(topic):
    sections = [
        "Current Market Landscape & Institutional Dividend Trends",
        "Deep Analysis of High-Yield Compounding Strategies",
        "Quantitative Wealth Projections for the Next Decade",
        "Strategic Portfolio Allocation & Global Risk Management"
    ]
    
    full_article = ""
    for section in sections:
        log(f"✍️ Writing Section: {section}")
        prompt = f"Act as a professional financial analyst. Write a deep-dive analysis on '{topic}' focusing on '{section}'. Min 350 words. Institutional tone. Use Markdown. English Only. NO intro/outro."
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.4}}, timeout=40)
            if resp.status_code == 200:
                full_article += "## " + section + "\n\n"
                full_article += clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text']) + "\n\n"
        except Exception as e:
            log(f"Error in {section}: {e}")
    return full_article

def get_hot_topic():
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:10]).title
    except: raw_news = "The Future of Dividend Investing in 2026"
    return clean_ai_output(raw_news)

# ==========================================
# [슬림 헤더 디자인] 본문이 바로 보이는 템플릿
# ==========================================
def create_professional_html(topic, img_url, body_html, sidebar_html):
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} | Dividend Master</title>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #0f172a; --gold: #fbbf24; }}
        body {{ font-family: 'Merriweather', serif; line-height: 1.7; color: #334155; max-width: 1100px; margin: 0 auto; padding: 20px; }}
        /* 헤더 슬림화 */
        header {{ background: var(--primary); color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-radius: 8px; margin-bottom: 20px; }}
        .header-title {{ font-size: 1.2rem; font-weight: 900; letter-spacing: 1px; }}
        /* 경고 배너 슬림화 */
        .hq-alert {{ background: #fff3cd; padding: 10px; text-align: center; border-radius: 6px; font-weight: bold; border: 1px solid var(--gold); margin-bottom: 20px; font-size: 0.9rem; }}
        .container {{ display: grid; grid-template-columns: 1fr; gap: 30px; }}
        @media(min-width: 900px) {{ .container {{ grid-template-columns: 2.8fr 1.2fr; }} }}
        .featured-img {{ width: 100%; border-radius: 10px; margin-bottom: 20px; }}
        .content h2 {{ color: var(--primary); border-bottom: 2px solid var(--gold); padding-bottom: 5px; margin-top: 30px; }}
        .ad-btn {{ display: block; padding: 12px; margin-bottom: 8px; border-radius: 6px; text-decoration: none; text-align: center; font-weight: bold; border: 1px solid #ddd; font-size: 0.9rem; }}
        .btn-hq {{ background: var(--gold); color: var(--primary); border-color: var(--gold); }}
    </style></head>
    <body>
    <header>
        <div class="header-title">DIVIDEND MASTER</div>
        <a href="{MAIN_HQ_URL}" style="color:var(--gold); font-size: 0.8rem; text-decoration:none;">Visit HQ →</a>
    </header>
    <div class="hq-alert">⚠️ <a href="{MAIN_HQ_URL}" style="color:#b91c1c;">Get the 'Elite 2026 Dividend Blueprint' at Empire Analyst HQ Now</a></div>
    <div class="container">
        <main>
            <div style="font-size: 0.8rem; color: #64748b; font-weight: bold;">{current_date} • INSTITUTIONAL REPORT</div>
            <h1 style="font-size: 2.2rem; margin: 10px 0;">{topic}</h1>
            <img src="{img_url}" class="featured-img">
            <div class="content">{body_html}</div>
        </main>
        <aside>
            <h4 style="border-bottom: 2px solid var(--primary); padding-bottom: 5px;">STRATEGIC ACCESS</h4>
            <a href="{MAIN_HQ_URL}" class="ad-btn btn-hq">EMPIRE ANALYST HQ</a>
            <a href="{AFFILIATE_LINK}" class="ad-btn">💰 BYBIT $30,000 BONUS</a>
            <a href="{AMAZON_LINK}" class="ad-btn">🛡️ SECURE YOUR LEDGER</a>
            <h4 style="margin-top:30px; border-bottom: 2px solid var(--primary); padding-bottom: 5px;">RECENT REPORTS</h4>
            <ul style="list-style:none; padding:0; font-size: 0.85rem;">{sidebar_html}</ul>
        </aside>
    </div>
    </body></html>"""

def main():
    log("🏁 Striker #2 (Slim-Optimized) Engaged")
    topic = get_hot_topic()
    full_markdown = generate_long_content(topic)
    html_body = markdown.markdown(full_markdown)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional financial dividends gold chart 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li style='margin-bottom:10px;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#334155;'>• {h['title']}</a></li>" for h in history[:6]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_professional_html(topic, img_url, html_body, sidebar_html)
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log(f"✅ Mission Complete: {len(full_markdown)} characters published.")

if __name__ == "__main__": main()
