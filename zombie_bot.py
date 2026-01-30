import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [SYSTEM] 1호기 방식의 인코딩 강제 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "Dividend Master"
BLOG_DESC = "Strategic Wealth Intelligence & Dividend Growth Analysis"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
EMPIRE_URL = "https://empire-analyst.digital/"

# [Monetization] 수익화 링크 & 아마존 태그
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_TAG = "empireanalyst-20"
AMAZON_LINK = f"https://www.amazon.com/s?k=ledger+nano+x&tag={AMAZON_TAG}"

HISTORY_FILE = "history.json"

# ==========================================
# [Cleaner] 1호기 정규식 그대로 이식
# ==========================================
def clean_ai_output(text):
    if not text: return ""
    if text.strip().startswith("{") and "content" in text:
        try:
            match = re.search(r'"content"\s*:\s*"(.*?)"', text, re.DOTALL)
            if match: text = match.group(1).encode('utf-8').decode('unicode_escape')
        except: pass
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    patterns = [r"Draft:", r"Word count:", r"Note:", r"Internal Monologue:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

# ==========================================
# [Content Generation] 1호기 로직 + 안전 필터 해제
# ==========================================
def generate_part(topic, focus):
    # 금융 관련 내용 차단을 막기 위한 안전 설정값
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
    ]
    
    prompt = f"Write a professional deep-dive report section on '{topic}'. Focus: {focus}. Min 450 words. Institutional tone. Markdown. English Only. NO chatty notes."
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2},
            "safetySettings": safety_settings  # 필터링 해제 추가
        }
        resp = requests.post(url, json=payload, timeout=40)
        if resp.status_code == 200:
            raw = resp.json()['candidates'][0]['content']['parts'][0]['text']
            return clean_ai_output(raw)
    except Exception as e:
        log(f"Gemini Error: {e}")
        # 백업 생성기 (Pollinations)
        try:
            url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
            return clean_ai_output(requests.get(url, timeout=30).text)
        except: pass
    return ""

def get_hot_topic():
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:5]).title if feed.entries else "Dividend Growth Masterclass"
    except: raw_news = "Strategic Wealth Building Secrets"
    
    prompt = f"Rewrite '{raw_news}' into a viral title. EXACTLY 8 WORDS. NO YEARS. Use: Secret, Wealth, Blueprint. English Only."
    title = "Secret Blueprint For Massive Long Term Dividend Wealth"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7}}, timeout=15)
        if resp.status_code == 200:
            title = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: pass
    return title

# ==========================================
# [HTML Template] 슬림 디자인 + 아마존 문구
# ==========================================
def create_professional_html(topic, img_url, body_html, sidebar_html, canonical_url):
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} | {BLOG_TITLE}</title>
    <link rel="canonical" href="{canonical_url}" />
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;700&family=Roboto:wght@400;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --navy: #0f172a; --gold: #eab308; --text: #334155; }}
        body {{ font-family: 'Merriweather', serif; line-height: 1.8; color: var(--text); background: #fff; margin: 0; }}
        header {{ background: var(--navy); color: white; padding: 12px 0; border-bottom: 4px solid var(--gold); }}
        .header-wrap {{ max-width: 1100px; margin: 0 auto; padding: 0 20px; display: flex; justify-content: space-between; align-items: center; font-weight: 900; }}
        .hq-banner {{ background: #fefce8; padding: 12px; text-align: center; border-bottom: 1px solid var(--gold); font-weight: bold; font-size: 0.9rem; }}
        .container {{ max-width: 1100px; margin: 30px auto; display: grid; grid-template-columns: 1fr; gap: 40px; padding: 0 20px; }}
        @media(min-width: 900px) {{ .container {{ grid-template-columns: 2.6fr 1.4fr; }} }}
        h1 {{ font-size: 2.2rem; color: var(--navy); line-height: 1.2; margin-top: 0; }}
        .featured-img {{ width: 100%; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .ad-btn {{ display: block; padding: 14px; margin-bottom: 10px; border-radius: 6px; text-decoration: none; text-align: center; font-weight: bold; border: 1px solid #cbd5e1; }}
        .btn-hq {{ background: var(--gold); color: var(--navy); border-color: var(--gold); }}
        .disclaimer {{ max-width: 800px; margin: 20px auto; line-height: 1.6; opacity: 0.7; font-size: 0.75rem; text-align: center; color: #94a3b8; }}
    </style></head>
    <body>
    <header><div class="header-wrap"><div>{BLOG_TITLE}</div><a href="{EMPIRE_URL}" style="color:var(--gold); text-decoration:none;">HQ ACCESS →</a></div></header>
    <div class="hq-banner">💎 Elite Analysis: <a href="{EMPIRE_URL}" style="color:var(--navy); text-decoration:underline;">Visit Empire Analyst HQ for The Full Strategy</a></div>
    <div class="container">
        <main><article>
            <div style="font-size:0.8rem; color:#64748b; font-weight:bold; margin-bottom:10px;">{current_date} • STRATEGIC REPORT</div>
            <h1>{topic}</h1>
            <img src="{img_url}" class="featured-img">
            <div class="content">{body_html}</div>
        </article></main>
        <aside>
            <div style="position:sticky; top:15px; background: #f8fafc; padding: 25px; border-radius: 12px; border: 1px solid #e2e8f0;">
                <h4 style="margin-top:0; border-bottom:2px solid var(--navy); padding-bottom:5px; color:var(--navy);">STRATEGIC LINKS</h4>
                <a href="{EMPIRE_URL}" class="ad-btn btn-hq">EMPIRE ANALYST HQ</a>
                <a href="{AFFILIATE_LINK}" class="ad-btn" style="color:#b45309;">💰 $30,000 BYBIT BONUS</a>
                <a href="{AMAZON_LINK}" class="ad-btn" style="color:#9a3412;">🛡️ SECURE YOUR ASSETS</a>
                <h4 style="margin-top:35px; border-bottom:2px solid var(--navy); padding-bottom:5px;">RECENT INTELLIGENCE</h4>
                <ul style="list-style:none; padding:0; font-size:0.85rem;">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    <footer style="background:var(--navy); color:#94a3b8; text-align:center; padding:50px 0; margin-top:80px;">
        <div>&copy; 2026 {BLOG_TITLE}. All rights reserved.</div>
        <div class="disclaimer">
            <strong>Affiliate & Amazon Disclaimer:</strong><br>
            {BLOG_TITLE} is a participant in the Amazon Services LLC Associates Program. As an Amazon Associate, I earn from qualifying purchases.
        </div>
    </footer></body></html>"""

def main():
    log("🏁 Striker #2 Fixed Version Engaged")
    topic = get_hot_topic()
    log(f"🔥 Subject: {topic}")
    
    # 1호기 방식의 3단계 누적 생성 (분량 확실히 보장)
    content = ""
    p1 = generate_part(topic, "Global Dividend Trends & Macro Outlook")
    p2 = generate_part(topic, "The Power Of Long-Term Compounding Growth")
    p3 = generate_part(topic, "Institutional Risk Management Strategies")
    
    if not p1 and not p2: # 만약 둘 다 비었다면 최소한의 텍스트라도 생성
        content = "Intelligence synchronization in progress. The full 1,300-word report is being processed."
    else:
        content = f"{p1}\n\n{p2}\n\n{p3}"
    
    html_body = markdown.markdown(content)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional gold wealth chart luxury dark theme 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li style='margin-bottom:12px;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#475569; font-weight:bold;'>• {h['title']}</a></li>" for h in history[:5]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_professional_html(topic, img_url, html_body, sidebar_html, f"{BLOG_BASE_URL}{archive_name}")
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log("✅ Intelligence Published Successfully")

if __name__ == "__main__": main()
