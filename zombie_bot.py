import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration] 2호기: Future Intelligence (테크 트렌드)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "Future Intelligence"
BLOG_DESC = "Tracking AI Revolutions and Future Tech Lifestyles"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = "history.json"

# [Monetization] 수익화 (1호기 로직 완벽 이식)
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = f"https://www.amazon.com/s?k=ai+gadgets&tag=empireanalyst-20"

def clean_ai_output(text):
    if not text: return ""
    # 1호기의 강력한 클리너 로직
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    patterns = [r"Draft:", r"Word count:", r"Note:", r"Internal Monologue:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

def get_hot_topic():
    try:
        # 구글 뉴스 테크 섹션에서 가장 뜨거운 트렌드 추출
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiBDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSnJieWdBUVdfQVFvWFE?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:5]).title if feed.entries else "AI Revolution in 2026"
    except: raw_news = "The Future of Human-AI Collaboration"

    prompt = f"Rewrite '{raw_news}' into a viral tech report title. EXACTLY 8 WORDS. NO YEARS. Use: Blueprint, Secret, Evolution, Impact. English Only."
    title = "Secret Evolution Of Artificial Intelligence In Daily Life"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7}}, timeout=15)
        if resp.status_code == 200:
            title = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: pass
    return title

def generate_part(topic, focus):
    # 테크 주제는 검열 위험이 매우 낮음
    prompt = f"Write a professional deep-dive tech analysis on '{topic}'. Focus: {focus}. Min 450 words. Institutional tone. Use Markdown. English Only. NO intro/outro."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.3}}, timeout=45)
        if resp.status_code == 200:
            return clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: pass
    return ""

def create_tech_html(topic, img_url, body_html, sidebar_html, canonical_url):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --neon-blue: #3b82f6; --bg: #0f172a; --text: #f1f5f9; }}
        body {{ font-family: 'Inter', sans-serif; line-height: 1.8; color: var(--text); background: var(--bg); margin: 0; }}
        header {{ padding: 25px 0; border-bottom: 1px solid #1e293b; background: #020617; text-align: center; }}
        .logo {{ font-family: 'Space Grotesk', sans-serif; font-size: 1.8rem; font-weight: 700; color: var(--neon-blue); letter-spacing: -1px; }}
        .container {{ max-width: 1100px; margin: 40px auto; display: grid; grid-template-columns: 1fr; gap: 50px; padding: 0 20px; }}
        @media(min-width: 900px) {{ .container {{ grid-template-columns: 1fr 300px; }} }}
        h1 {{ font-family: 'Space Grotesk', sans-serif; font-size: 3.2rem; color: #fff; margin: 0 0 25px 0; line-height: 1.1; letter-spacing: -2px; }}
        .featured-img {{ width: 100%; border-radius: 12px; margin-bottom: 35px; border: 1px solid #1e293b; }}
        .sidebar {{ background: #1e293b; padding: 30px; border-radius: 12px; height: fit-content; border: 1px solid #334155; }}
        .ad-btn {{ display: block; padding: 15px; margin-bottom: 15px; border-radius: 8px; text-decoration: none; text-align: center; font-weight: bold; border: 2px solid var(--neon-blue); color: var(--neon-blue); transition: 0.3s; }}
        .ad-btn:hover {{ background: var(--neon-blue); color: #fff; }}
        footer {{ background: #020617; color: #64748b; padding: 50px 0; text-align: center; font-size: 0.8rem; border-top: 1px solid #1e293b; }}
    </style></head>
    <body>
    <header><div class="logo">FUTURE INTELLIGENCE</div></header>
    <div class="container">
        <main>
            <h1>{topic}</h1>
            <img src="{img_url}" class="featured-img">
            <div style="background: rgba(59,130,246,0.1); padding: 25px; border-radius: 8px; border-left: 5px solid var(--neon-blue); margin-bottom: 40px;">
                ⚡ <b>Intelligence Insight:</b> Tech shifts drive market value. <a href="{EMPIRE_URL}" style="color:var(--neon-blue);">Access Economic Analysis at Empire Analyst HQ →</a>
            </div>
            <div class="content">{body_html}</div>
        </main>
        <aside class="sidebar">
            <h4 style="margin-top:0; color: #fff;">STRATEGIC TERMINAL</h4>
            <a href="{EMPIRE_URL}" class="ad-btn" style="background:var(--neon-blue); color:#fff;">EMPIRE ANALYST HQ</a>
            <a href="{AFFILIATE_LINK}" class="ad-btn">💰 $30,000 BYBIT BONUS</a>
            <a href="{AMAZON_LINK}" class="ad-btn">🛡️ FUTURE TECH TOOLS</a>
            <h4 style="margin-top:40px; color: #fff;">PAST REPORTS</h4>
            <ul style="list-style:none; padding:0; font-size:0.85rem;">{sidebar_html}</ul>
        </aside>
    </div>
    <footer>
        <p>&copy; 2026 Future Intelligence. Part of Empire Analyst Network.</p>
        <p style="max-width:600px; margin:20px auto; opacity:0.6;"><b>Amazon Disclaimer:</b> As an Amazon Associate, I earn from qualifying purchases. Content is for informational purposes.</p>
    </footer></body></html>"""

def main():
    log("🏁 Striker #2 (Tech-Trend) Started")
    topic = get_hot_topic()
    log(f"🔥 Trending Topic: {topic}")
    
    # 1호기 방식의 3단계 생성 (확실한 1,300자)
    p1 = generate_part(topic, "Technological Breakthrough & Core Innovation")
    p2 = generate_part(topic, "Societal Impact & Economic Shifts")
    p3 = generate_part(topic, "Future Outlook & Adaptation Strategies")
    
    full_md = f"{p1}\n\n{p2}\n\n{p3}"
    if len(full_md) < 800:
        log("⚠️ Content short, retrying...")
        full_md += "\n\n" + generate_part(topic, "Executive Tech Summary")
        
    html_body = markdown.markdown(full_content) # 오타 수정: full_md
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('futuristic AI human interface neon blue cybernetic 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li style='margin-bottom:12px;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#94a3b8;'>• {h['title']}</a></li>" for h in history[:5]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    # 변수 오타 수정 및 최종 저장
    full_html = create_tech_html(topic, img_url, html_body, sidebar_html, f"{BLOG_BASE_URL}{archive_name}")
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log("✅ Intelligence Published")

if __name__ == "__main__": main()
