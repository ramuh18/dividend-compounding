import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "Dividend Master"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
MAIN_HQ_URL = "https://empire-analyst.digital/"
HISTORY_FILE = "history.json"

# [수익화 링크 복구]
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_TAG = "empireanalyst-20"
AMAZON_LINK = f"https://www.amazon.com/s?k=ledger+nano+x&tag={AMAZON_TAG}"

def clean_ai_output(text):
    if not text: return ""
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = re.sub(r'reasoning_content":".*?"', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    # "2026" 년도 제거 및 정제
    text = text.replace("2026", "").replace("Year", "")
    patterns = [r"Draft:", r"Word count:", r"Note:", r"Internal Monologue:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

# [후킹 제목] 년도 제외 8단어
def get_hot_topic():
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:10]).title
    except: raw_news = "Strategic Dividend Wealth Growth Blueprint"

    prompt = f"Rewrite '{raw_news}' into a viral title. EXACTLY 8 WORDS. NO YEARS. Use words like Secret, Wealth, Blueprint. English Only."
    title = "Secret Blueprint For Massive Long Term Dividend Wealth"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7}}, timeout=15)
        if resp.status_code == 200:
            title = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: pass
    return title

# [1,300자 본문 생성] 4개 섹션 분할
def generate_full_report(topic):
    sections = [
        "Unlocking High-Yield Assets for Passive Income",
        "Mathematical Advantage of Long-Term Compounding Growth",
        "Institutional Strategies for Managing Dividend Portfolios",
        "Strategic Risk Mitigation for Multigenerational Wealth"
    ]
    full_md = ""
    for sec in sections:
        log(f"✍️ Writing: {sec}")
        prompt = f"Write a deep-dive financial analysis on '{topic}' focusing on '{sec}'. Min 350 words. Institutional tone. Use Markdown. English Only. NO intro/outro."
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.4}}, timeout=40)
            if resp.status_code == 200:
                full_md += f"## {sec}\n\n" + clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text']) + "\n\n"
        except: pass
        time.sleep(2)
    return full_md

def create_professional_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #0f172a; --gold: #fbbf24; --accent: #b91c1c; }}
        body {{ font-family: 'Merriweather', serif; line-height: 1.8; color: #334155; max-width: 1150px; margin: 0 auto; padding: 15px; }}
        header {{ background: var(--primary); color: white; padding: 12px 25px; display: flex; justify-content: space-between; align-items: center; border-radius: 6px; margin-bottom: 15px; }}
        .hq-funnel {{ background: #fef3c7; padding: 15px; text-align: center; border-radius: 6px; margin-bottom: 20px; font-weight: bold; border: 1px solid var(--gold); }}
        .container {{ display: grid; grid-template-columns: 1fr; gap: 30px; }}
        @media(min-width: 900px) {{ .container {{ grid-template-columns: 2.5fr 1fr; }} }}
        h1 {{ font-size: 2.2rem; color: var(--primary); margin: 10px 0; }}
        .ad-btn {{ display: block; padding: 14px; margin-bottom: 10px; border-radius: 6px; text-decoration: none; text-align: center; font-weight: bold; border: 2px solid #ddd; }}
        .btn-hq {{ background: var(--gold); color: var(--primary); border-color: var(--gold); }}
        .btn-bybit {{ border-color: #f59e0b; color: #f59e0b; }}
        .btn-amazon {{ border-color: #ea580c; color: #ea580c; }}
    </style></head>
    <body>
    <header><div style="font-weight:900;">DIVIDEND MASTER</div><a href="{MAIN_HQ_URL}" style="color:var(--gold); text-decoration:none;">Main HQ →</a></header>
    <div class="hq-funnel">💎 Expert View: <a href="{MAIN_HQ_URL}" style="color:var(--accent);">Visit Empire Analyst HQ for Private Wealth Blueprints</a></div>
    <div class="container">
        <main>
            <h1>{topic}</h1>
            <img src="{img_url}" style="width:100%; border-radius:10px; margin-bottom:20px;">
            <div class="content">{body_html}</div>
        </main>
        <aside>
            <div style="position:sticky; top:15px;">
                <h4 style="border-bottom:3px solid var(--primary); padding-bottom:5px;">STRATEGIC LINKS</h4>
                <a href="{MAIN_HQ_URL}" class="ad-btn btn-hq">EMPIRE ANALYST HQ</a>
                <a href="{AFFILIATE_LINK}" class="ad-btn btn-bybit">💰 $30,000 BYBIT BONUS</a>
                <a href="{AMAZON_LINK}" class="ad-btn btn-amazon">🛡️ SECURE YOUR LEDGER</a>
                <h4 style="margin-top:35px; border-bottom:3px solid var(--primary); padding-bottom:5px;">RECENT INTELLIGENCE</h4>
                <ul style="list-style:none; padding:0; font-size:0.85rem;">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    </body></html>"""

def main():
    log("🏁 Striker #2 Engaged")
    topic = get_hot_topic()
    full_markdown = generate_full_report(topic)
    
    if len(full_markdown) < 500: # 최소 분량 보장
        log("⚠️ Generating Fallback Content")
        full_markdown = "Deep-dive financial intelligence report is currently being synchronized. Please refresh for the full 1,300-word analysis."
        
    html_body = markdown.markdown(full_markdown)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional gold wealth chart dark luxury office 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li style='margin-bottom:10px;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#334155;'>• {h['title']}</a></li>" for h in history[:5]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(create_professional_html(topic, img_url, html_body, sidebar_html))
    with open(archive_name, "w", encoding="utf-8") as f: f.write(create_professional_html(topic, img_url, html_body, sidebar_html))
    log("✅ Report Published Successfully")

if __name__ == "__main__": main()
