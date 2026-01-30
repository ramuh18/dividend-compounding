import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [SYSTEM] 인코딩 설정 및 1호기 로직 이식
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "Future Intelligence"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = "history.json"

# [Monetization] 수익화
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = f"https://www.amazon.com/s?k=ai+gadgets&tag=empireanalyst-20"

def clean_ai_output(text):
    if not text or len(text) < 50: return "" # 너무 짧으면 무효 처리
    # 1호기 세척 로직 적용
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    patterns = [r"Draft:", r"Word count:", r"Note:", r"Internal Monologue:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

# [Content Generation] 1호기 3단계 방식 + 리트라이 강화
def generate_part(topic, focus):
    prompt = f"Write a professional financial and tech report section on '{topic}'. Focus on {focus}. Length: 450 words. Use Markdown. Tone: Institutional. NO chatty notes. English Only."
    
    # 제미나이 시도 (안전 설정 해제)
    safety = [{"category": f"HARM_CATEGORY_{c}", "threshold": "BLOCK_NONE"} for c in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]]
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "safetySettings": safety, "generationConfig": {"temperature": 0.3}}, timeout=45)
        if resp.status_code == 200:
            content = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
            if content: return content
    except: pass
    
    # 제미나이 실패 시 Pollinations AI로 즉시 대체 (내용 누락 방지 핵심)
    try:
        log(f"⚠️ Switching to Backup for: {focus}")
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt + ' Provide detailed 400 words.')}"
        return clean_ai_output(requests.get(url, timeout=30).text)
    except: return ""

def get_hot_topic():
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiBDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSnJieWdBUVdfQVFvWFE?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:5]).title if feed.entries else "AI Revolution"
    except: raw_news = "The Future of Artificial Intelligence"
    
    prompt = f"Rewrite '{raw_news}' into a viral tech title. EXACTLY 8 WORDS. NO YEARS. English Only."
    title = "Secret Evolution Of Artificial Intelligence In Daily Life"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7}}, timeout=15)
        if resp.status_code == 200:
            title = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: pass
    return title

def create_tech_html(topic, img_url, body_html, sidebar_html, canonical_url):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --neon: #10b981; --bg: #0f172a; --text: #e2e8f0; }}
        body {{ font-family: 'Inter', sans-serif; line-height: 1.8; color: var(--text); background: var(--bg); margin: 0; }}
        header {{ padding: 20px; border-bottom: 2px solid var(--neon); background: #000; text-align: left; font-family: 'Space Grotesk'; font-weight: 700; color: var(--neon); }}
        .container {{ max-width: 1100px; margin: 30px auto; display: grid; grid-template-columns: 1fr; gap: 40px; padding: 0 20px; }}
        @media(min-width: 900px) {{ .container {{ grid-template-columns: 300px 1fr; }} }}
        h1 {{ font-family: 'Space Grotesk'; font-size: 2.5rem; color: #fff; line-height: 1.1; margin: 0 0 20px 0; }}
        .featured-img {{ width: 100%; border-radius: 8px; margin-bottom: 30px; border: 1px solid #334155; }}
        .sidebar {{ background: #1e293b; padding: 25px; border-radius: 8px; border: 1px solid #334155; height: fit-content; }}
        .ad-btn {{ display: block; padding: 14px; margin-bottom: 12px; border-radius: 4px; text-decoration: none; text-align: center; font-weight: bold; border: 1px solid var(--neon); color: var(--neon); }}
        footer {{ background: #000; color: #64748b; padding: 40px 0; text-align: center; font-size: 0.8rem; border-top: 1px solid #334155; }}
    </style></head>
    <body>
    <header>FUTURE INTELLIGENCE</header>
    <div class="container">
        <aside class="sidebar">
            <h4 style="margin-top:0; color:var(--neon);">⚡ ACCESS TERMINAL</h4>
            <a href="{EMPIRE_URL}" class="ad-btn" style="background:var(--neon); color:#000;">EMPIRE ANALYST HQ</a>
            <a href="{AFFILIATE_LINK}" class="ad-btn">💰 BYBIT $30,000 BONUS</a>
            <a href="{AMAZON_LINK}" class="ad-btn">🛡️ SECURE YOUR ASSETS</a>
            <h4 style="margin-top:35px;">RECENT INTEL</h4>
            <ul style="list-style:none; padding:0; font-size:0.8rem; line-height:1.5;">{sidebar_html}</ul>
        </aside>
        <main>
            <h1>{topic}</h1>
            <img src="{img_url}" class="featured-img">
            <div style="background: rgba(16,185,129,0.1); padding: 20px; border-radius: 4px; border-left: 4px solid var(--neon); margin-bottom: 30px;">
                🚀 <b>Alpha Alert:</b> Standard data is not enough. <a href="{EMPIRE_URL}" style="color:var(--neon);">Access Private Analysis at Empire Analyst HQ →</a>
            </div>
            <div class="content">{body_html}</div>
        </main>
    </div>
    <footer>
        <p>&copy; 2026 Future Intelligence. Part of Empire Analyst Network.</p>
        <p style="max-width:600px; margin:20px auto; opacity:0.6;"><b>Amazon Disclaimer:</b> As an Amazon Associate, I earn from qualifying purchases. Content is for informational purposes only.</p>
    </footer></body></html>"""

def main():
    log("🏁 Striker #2 (Tech-Trend) Fixed Started")
    topic = get_hot_topic()
    log(f"🔥 Subject: {topic}")
    
    # 3단계 생성으로 1,300자 확보 (1호기 방식)
    p1 = generate_part(topic, "Core Tech Innovation & Market Context")
    p2 = generate_part(topic, "Economic Impact & Strategic Wealth Shifts")
    p3 = generate_part(topic, "Future Outlook & Actionable Intelligence")
    
    # [수정] 오타 변수명 통일
    full_content = f"{p1}\n\n{p2}\n\n{p3}"
    
    if len(full_content) < 800: # 내용이 부족하면 한 번 더 생성
        log("⚠️ Content still short, emergency filler active")
        full_content += "\n\n" + generate_part(topic, "Institutional Grade Wealth Protection Summary")
        
    html_body = markdown.markdown(full_content)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('cyberpunk AI city neon green high tech 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li style='margin-bottom:10px;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#94a3b8;'>• {h['title']}</a></li>" for h in history[:6]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_tech_html(topic, img_url, html_body, sidebar_html, f"{BLOG_BASE_URL}{archive_name}")
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log(f"✅ Mission Complete: {len(full_content)} characters published.")

if __name__ == "__main__": main()
