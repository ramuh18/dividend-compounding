import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [SYSTEM] UTF-8 설정 (1호기 방식 그대로)
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [CONFIGURATION] 2호기 전용으로 수정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "Dividend Master"
BLOG_DESC = "Strategic Intelligence for Dividend Growth & Compounding"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"

# [MONETIZATION] 1호기 링크 유지
EMPIRE_URL = "https://empire-analyst.digital/"
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_TAG = "empireanalyst-20"
AMAZON_LINK = f"https://www.amazon.com/s?k=ledger+nano+x&tag={AMAZON_TAG}"

HISTORY_FILE = "history.json"

# ==========================================
# [CLEANER] 1호기의 강력한 클리너 이식 (None 방지)
# ==========================================
def clean_ai_output(text):
    if not text: return ""
    if text.strip().startswith("{") and "reasoning_content" in text:
        try:
            match = re.search(r'"content"\s*:\s*"(.*?)"', text, re.DOTALL)
            if match: text = match.group(1).encode('utf-8').decode('unicode_escape')
        except: pass
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    patterns = [r"Draft:", r"Word count:", r"Let's write", r"Note:", r"Internal Monologue:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

# ==========================================
# [TOPIC] 8단어 후킹 제목 (년도 제외)
# ==========================================
def get_hot_topic():
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:5]).title if feed.entries else "Dividend Wealth Strategy"
    except: raw_news = "Passive Income Blueprint"

    prompt = f"Rewrite '{raw_news}' into a viral title. EXACTLY 8 WORDS. NO YEARS. Use: Secret, Wealth, Blueprint, Masterclass. English Only."
    
    title = "Secret Masterclass For Massive Long Term Dividend Wealth"
    try:
        if GEMINI_API_KEY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7}}, timeout=15)
            if resp.status_code == 200:
                title = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: pass
    return title

# ==========================================
# [CONTENT] 1호기 방식의 3단계 생성 (1300자 확보)
# ==========================================
def generate_part(topic, focus):
    prompt = f"Write a professional deep-dive section on '{topic}'. Focus: {focus}. Length: 450 words. Use Markdown. Tone: Institutional. Language: English Only. NO chatty notes."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.2}}, timeout=30)
        if resp.status_code == 200:
            return clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: pass
    return "Analyzing market intelligence..."

# ==========================================
# [HTML] 슬림 헤더 & 네이비/골드 디자인
# ==========================================
def create_professional_html(topic, img_url, body_html, sidebar_html, canonical_url):
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} | {BLOG_TITLE}</title>
    <link rel="canonical" href="{canonical_url}" />
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;700&family=Roboto:wght@400;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --navy: #0f172a; --gold: #eab308; --bg: #ffffff; --text: #334155; }}
        body {{ font-family: 'Merriweather', serif; line-height: 1.8; color: var(--text); background: var(--bg); margin: 0; padding: 0; }}
        header {{ background: var(--navy); color: white; padding: 15px 0; border-bottom: 4px solid var(--gold); }}
        .header-wrap {{ max-width: 1100px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; }}
        .brand {{ font-family: 'Roboto', sans-serif; font-size: 1.3rem; font-weight: 900; letter-spacing: 1px; }}
        .hq-banner {{ background: #fefce8; padding: 12px; text-align: center; border-bottom: 1px solid var(--gold); font-weight: bold; font-size: 0.9rem; }}
        .container {{ max-width: 1100px; margin: 30px auto; display: grid; grid-template-columns: 1fr; gap: 40px; padding: 0 20px; }}
        @media(min-width: 900px) {{ .container {{ grid-template-columns: 2.5fr 1fr; }} }}
        h1 {{ font-size: 2.2rem; color: var(--navy); line-height: 1.2; margin-top: 0; }}
        .featured-img {{ width: 100%; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
        .sidebar {{ background: #f8fafc; padding: 25px; border-radius: 10px; border: 1px solid #e2e8f0; height: fit-content; }}
        .ad-box {{ display: block; padding: 18px; border-radius: 6px; text-align: center; text-decoration: none; margin-bottom: 12px; font-weight: bold; border: 1px solid #cbd5e1; }}
        .ad-main {{ background: var(--gold); color: var(--navy); border-color: var(--gold); }}
        .ad-bybit {{ color: #b45309; border-color: #f59e0b; }}
        .ad-amazon {{ color: #9a3412; border-color: #ea580c; }}
        .recent-posts {{ list-style: none; padding: 0; font-size: 0.85rem; }}
        .recent-posts li {{ margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 8px; }}
    </style></head>
    <body>
    <header><div class="header-wrap"><div class="brand">{BLOG_TITLE}</div><a href="{EMPIRE_URL}" style="color:var(--gold); text-decoration:none; font-size:0.8rem; font-weight:bold;">HQ ACCESS →</a></div></header>
    <div class="hq-banner">🏛️ Elite Intelligence: <a href="{EMPIRE_URL}" style="color:var(--navy); text-decoration:underline;">Access Private Wealth Blueprints at Empire Analyst HQ</a></div>
    <div class="container">
        <main><article>
            <div style="font-size:0.8rem; color:#64748b; font-weight:bold; margin-bottom:10px;">{current_date} • STRATEGIC REPORT</div>
            <h1>{topic}</h1>
            <img src="{img_url}" class="featured-img">
            <div class="content">{body_html}</div>
        </article></main>
        <aside class="sidebar">
            <h4 style="margin-top:0; border-bottom:2px solid var(--navy); padding-bottom:5px;">STRATEGIC LINKS</h4>
            <a href="{EMPIRE_URL}" class="ad-box ad-main">EMPIRE ANALYST HQ</a>
            <a href="{AFFILIATE_LINK}" class="ad-box ad-bybit">💰 $30,000 BYBIT BONUS</a>
            <a href="{AMAZON_LINK}" class="ad-box ad-amazon">🛡️ SECURE YOUR ASSETS</a>
            <h4 style="margin-top:30px; border-bottom:2px solid var(--navy); padding-bottom:5px;">RECENT REPORTS</h4>
            {sidebar_html}
        </aside>
    </div>
    <footer style="background:var(--navy); color:#94a3b8; text-align:center; padding:40px 0; margin-top:60px; font-size:0.8rem;">
        &copy; 2026 {BLOG_TITLE}. Part of the <a href="{EMPIRE_URL}" style="color:#fff;">Empire Analyst Network</a>.
    </footer></body></html>"""

# ==========================================
# [MAIN]
# ==========================================
def main():
    log("🏁 Striker #2 Engaged")
    topic = get_hot_topic()
    log(f"🔥 Subject: {topic}")
    
    # 1호기 방식의 3단계 누적 생성 (1300자 이상 보장)
    content = ""
    content += generate_part(topic, "Global Dividend Trends & Macro Outlook") + "\n\n"
    content += generate_part(topic, "Strategic Compounding & Yield Analysis") + "\n\n"
    content += generate_part(topic, "Institutional Risk Management & Allocation")
    
    html_body = markdown.markdown(content)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional gold wealth chart luxury dark theme 8k')}"
    
    # 히스토리 동기화 및 사이드바 (1호기 로직)
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "<ul class='recent-posts'>"
    for h in history[:5]:
        sidebar_html += f"<li><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#334155;'>• {h['title']}</a></li>"
    sidebar_html += "</ul>"
    
    file_ts = datetime.now().strftime("%Y%m%d_%H%M")
    archive_name = f"post_{file_ts}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_professional_html(topic, img_url, html_body, sidebar_html, f"{BLOG_BASE_URL}{archive_name}")
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log("✅ Intelligence Published")

if __name__ == "__main__": main()
