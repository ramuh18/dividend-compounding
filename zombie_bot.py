import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [시스템] 인코딩 및 출력 최적화
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [설정]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "Dividend Master Intelligence"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
MAIN_HQ_URL = "https://empire-analyst.digital/"

# [수익화 링크]
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_TAG = "empireanalyst-20"
AMAZON_LINK = f"https://www.amazon.com/s?k=ledger+nano+x&tag={AMAZON_TAG}"

HISTORY_FILE = "history.json"

def clean_ai_output(text):
    if not text: return ""
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = re.sub(r'reasoning_content":".*?"', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    patterns = [r"Draft:", r"Word count:", r"Note:", r"Internal Monologue:", r"Thinking:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

# ==========================================
# [초정밀 파트별 생성] 1,300자 이상 확보 로직
# ==========================================
def generate_long_content(topic):
    sections = [
        "Executive Summary & Current Market Volatility Analysis",
        "Deep Dive: Dividend Aristocrats & Yield Stability Metrics",
        "The Mathematics of Compounding: 10-Year Wealth Projection",
        "Risk Mitigation & Institutional Portfolio Allocation Strategy"
    ]
    
    full_article = ""
    for section in sections:
        log(f"✍️ Writing Section: {section}")
        prompt = f"""Write a detailed financial analysis for the section: '{section}'.
        Topic: {topic}. 
        Requirements: Minimum 350 words for this section, professional institutional tone, use Markdown, English Only.
        Focus: Wealth building and dividend growth. 
        NO intro/outro, start directly with the analysis."""
        
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.4}}, timeout=40)
            if resp.status_code == 200:
                full_article += "## " + section + "\n\n"
                full_article += clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text']) + "\n\n"
        except Exception as e:
            log(f"Error in section {section}: {e}")
        time.sleep(2) # API 안정성 확보
    
    return full_article

def get_hot_topic():
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:10]).title
    except: raw_news = "Institutional Dividend Strategies for 2026"
    return clean_ai_output(raw_news)

def create_professional_html(topic, img_url, body_html, sidebar_html):
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} | Dividend Master</title>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;700&family=Roboto:wght@400;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #0f172a; --accent: #b91c1c; --gold: #fbbf24; }}
        body {{ font-family: 'Merriweather', serif; line-height: 1.9; color: #334155; max-width: 1200px; margin: 0 auto; padding: 20px; background:#fdfdfd; }}
        header {{ background: var(--primary); color: white; padding: 60px 20px; text-align: center; border-radius: 15px; margin-bottom: 40px; border-bottom: 6px solid var(--gold); }}
        .hq-funnel {{ background: #fff3cd; padding: 25px; border-radius: 12px; border: 2px solid var(--gold); text-align: center; margin-bottom: 40px; font-weight: 900; font-size: 1.2rem; }}
        .container {{ display: grid; grid-template-columns: 1fr; gap: 50px; }}
        @media(min-width: 1000px) {{ .container {{ grid-template-columns: 2.8fr 1.2fr; }} }}
        .featured-img {{ width: 100%; border-radius: 15px; margin-bottom: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.15); }}
        .ad-button {{ display: block; padding: 18px; margin-bottom: 15px; border-radius: 10px; text-decoration: none; text-align: center; font-weight: 900; border: 2px solid #cbd5e1; transition: 0.3s; }}
        .btn-hq {{ background: var(--gold); color: var(--primary); border-color: var(--gold); }}
        .btn-hq:hover {{ background: var(--primary); color: var(--gold); }}
        .content h2 {{ color: var(--primary); border-left: 5px solid var(--accent); padding-left: 15px; margin-top: 40px; }}
    </style></head>
    <body>
    <header>
        <div style="font-size: 2.8rem; font-weight: 900; letter-spacing: 2px;">DIVIDEND MASTER</div>
        <p style="letter-spacing: 1px; opacity: 0.9;">Global Hub for Compound Wealth Intelligence</p>
    </header>
    <div class="hq-funnel">
        🛑 STOP! DO NOT INVEST BLINDLY. <br>
        <a href="{MAIN_HQ_URL}" style="color:var(--accent); text-decoration: underline;">Get the '2026 High-Yield Blueprint' at Empire Analyst HQ Now →</a>
    </div>
    <div class="container">
        <main>
            <div style="color: var(--accent); font-weight: 900; letter-spacing: 1px;">{current_date} • INSTITUTIONAL GRADE REPORT</div>
            <h1 style="font-size: 3rem; line-height: 1.1; margin: 20px 0;">{topic}</h1>
            <img src="{img_url}" class="featured-img">
            <div class="content" style="font-size: 1.15rem;">{body_html}</div>
        </main>
        <aside>
            <div style="position: sticky; top: 20px;">
                <h3 style="border-bottom: 4px solid var(--primary); padding-bottom: 10px;">💎 ELITE ACCESS</h3>
                <a href="{MAIN_HQ_URL}" class="ad-button btn-hq">EMPIRE ANALYST HQ</a>
                <a href="{AFFILIATE_LINK}" class="ad-button" style="color:#f59e0b; border-color:#f59e0b;">💰 BYBIT $30,000 BONUS</a>
                <a href="{AMAZON_LINK}" class="ad-button" style="color:#ea580c; border-color:#ea580c;">🛡️ SECURE YOUR LEDGER</a>
                <h3 style="margin-top:50px; border-bottom: 4px solid var(--primary); padding-bottom: 10px;">📂 RECENT REPORTS</h3>
                <ul style="list-style:none; padding:0;">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    </body></html>"""

def main():
    log("🏁 Striker #2 (Long-form) Engaged")
    topic = get_hot_topic()
    log(f"🔥 Deep Analysis Target: {topic}")
    
    # 1,300자 이상을 위한 4단계 생성
    full_markdown = generate_long_content(topic)
    html_body = markdown.markdown(full_markdown)
    
    img_prompt = f"professional financial tower of gold coins, compound interest chart, dark luxury office background, 8k"
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(img_prompt)}"
    
    # 히스토리 관리
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li style='margin-bottom:15px;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#334155; font-weight:bold;'>• {h['title']}</a></li>" for h in history[:6]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_professional_html(topic, img_url, html_body, sidebar_html)
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log(f"✅ Mission Complete: Long-form report published ({len(full_markdown)} chars)")

if __name__ == "__main__": main()
