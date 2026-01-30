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

def clean_ai_output(text):
    if not text: return ""
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = re.sub(r'reasoning_content":".*?"', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    # "2026" 년도 및 불필요한 단어 강제 삭제
    text = text.replace("2026", "").replace("Year", "").replace("Update:", "")
    patterns = [r"Draft:", r"Word count:", r"Note:", r"Internal Monologue:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

# ==========================================
# [후킹 제목] 년도 제외, 딱 8단어 내외
# ==========================================
def get_hot_topic():
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:10]).title
    except: raw_news = "Strategic Dividend Growth Strategies"

    prompt = f"Rewrite '{raw_news}' into a viral financial title. EXACTLY 8 WORDS. NO YEARS (like 2026). Use words like Secret, Wealth, Blueprint. English Only."
    
    title = "Secret Blueprint For Massive Long Term Dividend Wealth"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7}}, timeout=15)
        if resp.status_code == 200:
            title = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: pass
    return title

# ==========================================
# [1,300자 본문] 4단계 섹션 분할 생성 (내용 보장)
# ==========================================
def generate_full_report(topic):
    sections = [
        "Unlocking High-Yield Assets for Infinite Passive Income",
        "The Mathematical Edge of Long-Term Compound Growth",
        "Institutional Secrets for Managing Massive Dividend Portfolios",
        "Ultimate Risk Management for Sustainable Multi-Generational Wealth"
    ]
    full_md = ""
    for sec in sections:
        log(f"✍️ Writing: {sec}")
        prompt = f"Write a deep-dive report on '{topic}' focusing on '{sec}'. Min 350 words. Institutional tone. Use Markdown. English Only. NO intro/outro."
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
        :root {{ --primary: #0f172a; --gold: #fbbf24; }}
        body {{ font-family: 'Merriweather', serif; line-height: 1.7; color: #334155; max-width: 1000px; margin: 0 auto; padding: 15px; }}
        /* 초슬림 헤더 */
        header {{ background: var(--primary); color: white; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; border-radius: 5px; margin-bottom: 15px; }}
        /* 후킹 배너 - 부드러운 유도 */
        .hq-banner {{ background: #fef3c7; padding: 12px; text-align: center; border-radius: 5px; margin-bottom: 15px; font-weight: bold; border: 1px solid var(--gold); font-size: 0.95rem; }}
        .container {{ display: grid; grid-template-columns: 1fr; gap: 25px; }}
        @media(min-width: 900px) {{ .container {{ grid-template-columns: 3fr 1fr; }} }}
        h1 {{ font-size: 2rem; color: var(--primary); margin: 10px 0; line-height: 1.2; }}
        .content h2 {{ color: var(--primary); border-left: 4px solid var(--gold); padding-left: 10px; margin-top: 25px; font-size: 1.3rem; }}
    </style></head>
    <body>
    <header><div style="font-weight:900;">DIVIDEND MASTER</div><a href="{MAIN_HQ_URL}" style="color:var(--gold); text-decoration:none; font-size:0.8rem;">HQ ANALYSIS →</a></header>
    <div class="hq-banner">💎 Professional Insight: <a href="{MAIN_HQ_URL}" style="color:#b91c1c;">Get the Full Wealth Blueprint at Empire Analyst HQ</a></div>
    <div class="container">
        <main>
            <h1>{topic}</h1>
            <img src="{img_url}" style="width:100%; border-radius:8px; margin-bottom:15px;">
            <div class="content">{body_html}</div>
        </main>
        <aside>
            <div style="position:sticky; top:10px;">
                <h4 style="border-bottom:2px solid var(--primary); margin:0 0 10px 0;">ELITE LINKS</h4>
                <a href="{MAIN_HQ_URL}" style="display:block; padding:10px; background:var(--gold); color:var(--primary); text-align:center; text-decoration:none; font-weight:bold; border-radius:5px; margin-bottom:10px;">EMPIRE ANALYST HQ</a>
                <ul style="list-style:none; padding:0; font-size:0.8rem;">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    </body></html>"""

def main():
    log("🏁 Striker #2 Engaged")
    topic = get_hot_topic()
    full_markdown = generate_full_report(topic)
    
    if len(full_markdown) < 500: # 내용 누락 방지 안전장치
        full_markdown = "Expert financial analysis is being updated. Please check back shortly for the full 1,300-word report."
        
    html_body = markdown.markdown(full_markdown)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('gold coins wealth growth professional dark theme')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li style='margin-bottom:8px;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#334155;'>• {h['title']}</a></li>" for h in history[:5]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(create_professional_html(topic, img_url, html_body, sidebar_html))
    with open(archive_name, "w", encoding="utf-8") as f: f.write(create_professional_html(topic, img_url, html_body, sidebar_html))
    log("✅ Intelligence Published")

if __name__ == "__main__": main()
