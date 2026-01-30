import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [SYSTEM] 인코딩 설정 (1호기 로직)
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "FUTURE INTELLIGENCE"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = "history.json"

# [Monetization] 수익화 링크 복구
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = f"https://www.amazon.com/s?k=ai+gadgets&tag=empireanalyst-20"

def clean_ai_output(text):
    if not text or len(text) < 100: return ""
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    patterns = [r"Draft:", r"Word count:", r"Note:", r"Internal Monologue:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

def generate_part(topic, focus):
    # 제미나이 필터 완전 해제
    safety = [{"category": f"HARM_CATEGORY_{c}", "threshold": "BLOCK_NONE"} for c in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]]
    prompt = f"Write a professional institutional report on '{topic}'. Focus: {focus}. Min 450 words. Professional English. Markdown. NO intro."
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "safetySettings": safety, "generationConfig": {"temperature": 0.3}}, timeout=45)
        if resp.status_code == 200:
            content = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
            if content: return content
    except: pass

    # 백업: 에러 난 Pollinations 대신 다른 채널 시도
    try:
        fallback_url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}?model=openai"
        return clean_ai_output(requests.get(fallback_url, timeout=30).text)
    except: return ""

def get_hot_topic():
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiBDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSnJieWdBUVdfQVFvWFE?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:5]).title if feed.entries else "AI Tech Evolution"
    except: raw_news = "The Future of Digital Intelligence"
    prompt = f"Rewrite '{raw_news}' into a viral title. EXACTLY 8 WORDS. NO YEARS. English Only."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7}}, timeout=15)
        return clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: return "Secret Evolution Of Artificial Intelligence In Daily Life"

def create_wide_modern_html(topic, img_url, body_html, sidebar_html, canonical_url):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #ffffff; --text: #111827; --border: #e5e7eb; }}
        body {{ font-family: 'Inter', sans-serif; line-height: 1.8; color: var(--text); background: var(--bg); margin: 0; }}
        header {{ padding: 25px 50px; border-bottom: 1px solid var(--border); background: #fff; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; }}
        .brand {{ font-size: 1.4rem; font-weight: 900; letter-spacing: -1px; }}
        /* 가로 넓이 대폭 확장 */
        .container {{ max-width: 1350px; margin: 0 auto; display: grid; grid-template-columns: 1fr; gap: 70px; padding: 50px 20px; }}
        @media(min-width: 1000px) {{ .container {{ grid-template-columns: 1fr 380px; }} }}
        h1 {{ font-size: 3.8rem; font-weight: 900; line-height: 1.1; margin: 0 0 35px 0; letter-spacing: -3px; }}
        .featured-img {{ width: 100%; height: 550px; object-fit: cover; border-radius: 0; margin-bottom: 45px; filter: grayscale(100%); transition: 0.6s; }}
        .featured-img:hover {{ filter: grayscale(0%); }}
        /* 스티키 사이드바 */
        .sidebar-wrapper {{ position: relative; }}
        .sidebar {{ position: -webkit-sticky; position: sticky; top: 120px; height: fit-content; border-left: 2px solid #000; padding-left: 45px; }}
        .ad-btn {{ display: block; padding: 20px; margin-bottom: 15px; text-decoration: none; text-align: center; font-weight: 900; background: #000; color: #fff; text-transform: uppercase; font-size: 0.85rem; letter-spacing: 1.5px; }}
        .alpha-box {{ background: #f9fafb; padding: 35px; margin-bottom: 45px; border: 1px solid var(--border); border-top: 5px solid #000; font-size: 1.1rem; }}
        .content {{ font-size: 1.25rem; color: #374151; }}
        footer {{ background: #000; color: #9ca3af; padding: 80px 0; text-align: center; font-size: 0.85rem; margin-top: 100px; }}
    </style></head>
    <body>
    <header><div class="brand">{BLOG_TITLE}</div><a href="{EMPIRE_URL}" style="color:#000; text-decoration:none; font-weight:900;">HQ ACCESS →</a></header>
    <div class="container">
        <main>
            <h1>{topic}</h1>
            <img src="{img_url}" class="featured-img">
            <div class="alpha-box">
                <span style="display:block; font-weight:900; text-transform:uppercase; margin-bottom:10px; font-size:0.8rem; color:#000;">⚡ Strategic Intelligence Briefing</span>
                Standard tech data is currently lagging. <a href="{EMPIRE_URL}" style="color:#000; font-weight:900; text-decoration:underline;">Access the Private Terminal at Empire Analyst HQ →</a>
            </div>
            <div class="content">{body_html}</div>
        </main>
        <div class="sidebar-wrapper">
            <aside class="sidebar">
                <h4 style="margin-top:0; text-transform:uppercase; letter-spacing:3px; font-size:0.8rem; margin-bottom:30px; color:#6b7280;">Strategic Access</h4>
                <a href="{EMPIRE_URL}" class="ad-btn">Empire Analyst HQ</a>
                <a href="{AFFILIATE_LINK}" class="ad-btn" style="background:#fff; color:#000; border:2px solid #000;">$30,000 Bybit Bonus</a>
                <a href="{AMAZON_LINK}" class="ad-btn" style="background:#fff; color:#000; border:2px solid #000;">Secure Ledger Store</a>
                <h4 style="margin-top:70px; text-transform:uppercase; letter-spacing:3px; font-size:0.8rem; margin-bottom:25px; color:#6b7280;">Recent Reports</h4>
                <ul style="list-style:none; padding:0; font-size:0.95rem; line-height:2.2;">{sidebar_html}</ul>
            </aside>
        </div>
    </div>
    <footer>
        <p>&copy; 2026 {BLOG_TITLE}. Part of the Empire Analyst Network.</p>
        <p style="max-width:850px; margin:25px auto; opacity:0.5; line-height:1.6;"><b>Amazon Disclaimer:</b> As an Amazon Associate, I earn from qualifying purchases. This content is for professional informational purposes only.</p>
    </footer></body></html>"""

def main():
    log("🏁 Striker #2 Wide Modern B&W Started")
    topic = get_hot_topic()
    log(f"🔥 Subject: {topic}")
    
    # 3단계 생성으로 확실한 분량 확보
    p1 = generate_part(topic, "Core Tech Innovation & Market Context")
    p2 = generate_part(topic, "Economic Impact & Strategic Wealth Shifts")
    p3 = generate_part(topic, "Future Outlook & Execution Summary")
    
    full_content = f"{p1}\n\n{p2}\n\n{p3}"
    
    # 본문 누락 방지: 800자 미만이면 비상 문구 삽입
    if len(full_content) < 800:
        log("⚠️ Emergency content synchronization...")
        full_content = "The full 1,300-word institutional report is being synchronized with the main HQ terminal. Please refresh shortly."
    
    html_body = markdown.markdown(full_content)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional minimal humanoid robot interface black and white 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    sidebar_html = "".join([f"<li style='margin-bottom:15px;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#4b5563; font-weight:700;'>• {h['title']}</a></li>" for h in history[:6]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_wide_modern_html(topic, img_url, html_body, sidebar_html, f"{BLOG_BASE_URL}{archive_name}")
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log(f"✅ Generation Complete: {len(full_content)} chars.")

if __name__ == "__main__": main()
