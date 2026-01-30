import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [SYSTEM] 인코딩 설정 및 1호기 로직 완벽 이식
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "FUTURE INTELLIGENCE"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = "history.json"

# [Monetization] 1호기 수익화 링크
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = f"https://www.amazon.com/s?k=ai+gadgets&tag=empireanalyst-20"

# ==========================================
# [Cleaner] 에러 메시지 감지 및 제거 로직 강화
# ==========================================
def clean_ai_output(text):
    if not text: return ""
    # Pollinations 에러 메시지(429, Queue full 등) 감지 시 빈값 반환
    if "error" in text.lower() or "queue full" in text.lower() or "429" in text:
        return ""
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    patterns = [r"Draft:", r"Word count:", r"Note:", r"Internal Monologue:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

# ==========================================
# [Content] 무조건 1,300자 뽑아내는 5회 재시도 로직
# ==========================================
def generate_part(topic, focus):
    safety = [{"category": f"HARM_CATEGORY_{c}", "threshold": "BLOCK_NONE"} for c in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]]
    prompt = f"Act as an institutional tech analyst. Write 450 words on '{topic}' focusing on {focus}. Markdown style. Professional English. No intro."
    
    for attempt in range(5): # 최대 5번 재시도
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "safetySettings": safety, "generationConfig": {"temperature": 0.4}}, timeout=40)
            if resp.status_code == 200:
                res = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
                if len(res) > 300: return res
        except: pass
        log(f"🔄 Retrying {focus} (Attempt {attempt+1}/5)...")
        time.sleep(3)
    return ""

def get_hot_topic():
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiBDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSnJieWdBUVdfQVFvWFE?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:5]).title if feed.entries else "AI Tech Transformation"
    except: raw_news = "Future Digital Trends"
    prompt = f"Rewrite '{raw_news}' into a viral title. EXACTLY 8 WORDS. NO YEARS. English Only."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7}}, timeout=15)
        return clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: return "Secret Evolution Of Artificial Intelligence In Daily Life"

# ==========================================
# [HTML] 와이드 B&W & 스티키 사이드바 템플릿
# ==========================================
def create_wide_bw_html(topic, img_url, body_html, sidebar_html, canonical_url):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #ffffff; --text: #000000; --border: #000000; }}
        body {{ font-family: 'Inter', sans-serif; line-height: 1.8; color: var(--text); background: var(--bg); margin: 0; overflow-x: hidden; }}
        header {{ padding: 20px 60px; border-bottom: 2px solid #000; background: #fff; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; }}
        .brand {{ font-size: 1.5rem; font-weight: 900; letter-spacing: -1.5px; text-transform: uppercase; }}
        /* 와이드 레이아웃 확장 */
        .container {{ max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: 1fr; gap: 80px; padding: 60px 20px; }}
        @media(min-width: 1000px) {{ .container {{ grid-template-columns: 1fr 400px; }} }}
        h1 {{ font-size: 4.2rem; font-weight: 900; line-height: 1.0; margin: 0 0 40px 0; letter-spacing: -4px; text-transform: uppercase; }}
        .featured-img {{ width: 100%; height: 600px; object-fit: cover; filter: grayscale(100%); transition: 0.7s; border: 1px solid #000; }}
        .featured-img:hover {{ filter: grayscale(0%); }}
        /* 스티키 사이드바 */
        .sidebar {{ position: -webkit-sticky; position: sticky; top: 120px; height: fit-content; border-left: 3px solid #000; padding-left: 50px; }}
        .ad-btn {{ display: block; padding: 22px; margin-bottom: 15px; text-decoration: none; text-align: center; font-weight: 900; background: #000; color: #fff; text-transform: uppercase; font-size: 0.9rem; letter-spacing: 2px; }}
        .alpha-box {{ background: #000; color: #fff; padding: 40px; margin-bottom: 50px; font-size: 1.2rem; }}
        .alpha-box a {{ color: #fff; font-weight: 900; text-decoration: underline; }}
        .content {{ font-size: 1.3rem; text-align: justify; }}
        .content h2 {{ font-weight: 900; text-transform: uppercase; border-bottom: 5px solid #000; padding-bottom: 10px; margin-top: 60px; }}
        footer {{ background: #000; color: #666; padding: 80px 0; text-align: center; font-size: 0.8rem; margin-top: 100px; }}
    </style></head>
    <body>
    <header><div class="brand">{BLOG_TITLE}</div><a href="{EMPIRE_URL}" style="color:#000; text-decoration:none; font-weight:900; border:2px solid #000; padding:5px 15px;">HQ ACCESS</a></header>
    <div class="container">
        <main>
            <h1>{topic}</h1>
            <img src="{img_url}" class="featured-img">
            <div class="alpha-box">
                <span style="display:block; font-weight:900; text-transform:uppercase; margin-bottom:15px; font-size:0.8rem; color:#666;">⚡ Intelligence Alert</span>
                Standard intelligence is currently outdated. <a href="{EMPIRE_URL}">Access the Private Wealth Terminal at Empire Analyst HQ →</a>
            </div>
            <div class="content">{body_html}</div>
        </main>
        <aside class="sidebar">
            <h4 style="margin-top:0; text-transform:uppercase; letter-spacing:4px; font-size:0.85rem; margin-bottom:40px; color:#999;">Strategic Access</h4>
            <a href="{EMPIRE_URL}" class="ad-btn">Empire Analyst HQ</a>
            <a href="{AFFILIATE_LINK}" class="ad-btn" style="background:#fff; color:#000; border:3px solid #000;">$30,000 Bybit Bonus</a>
            <a href="{AMAZON_LINK}" class="ad-btn" style="background:#fff; color:#000; border:3px solid #000;">Secure Ledger Store</a>
            <h4 style="margin-top:80px; text-transform:uppercase; letter-spacing:4px; font-size:0.85rem; margin-bottom:30px; color:#999;">Recent Intel</h4>
            <ul style="list-style:none; padding:0; font-size:1rem; line-height:2.5;">{sidebar_html}</ul>
        </aside>
    </div>
    <footer>
        <p>&copy; 2026 {BLOG_TITLE}. Part of the Empire Analyst Network.</p>
        <p style="max-width:800px; margin:30px auto; opacity:0.5; line-height:1.8;"><b>Amazon Disclaimer:</b> As an Amazon Associate, I earn from qualifying purchases. This content is for professional informational purposes only.</p>
    </footer></body></html>"""

def main():
    log("🏁 Striker #2 Wide B&W Final Started")
    topic = get_hot_topic()
    log(f"🔥 Subject: {topic}")
    
    # 3단계 섹션 생성 (에러 감지 시 재시도 포함)
    p1 = generate_part(topic, "Core Innovation")
    p2 = generate_part(topic, "Economic Impact")
    p3 = generate_part(topic, "Strategic Outlook")
    
    full_content = f"{p1}\n\n{p2}\n\n{p3}"
    
    # [수정] 1,300자 미달 시 강제 루프 (내용 없음 방지)
    while len(full_content) < 1000:
        log("⚠️ Content still insufficient. Force generating additional report...")
        full_content += "\n\n" + generate_part(topic, "Supplemental Market Analysis")
        if len(full_content) > 1000: break

    html_body = markdown.markdown(full_content)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional minimal humanoid robot interface black and white 8k photography')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    sidebar_html = "".join([f"<li style='margin-bottom:15px;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#000; font-weight:900;'>• {h['title']}</a></li>" for h in history[:6]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_wide_bw_html(topic, img_url, html_body, sidebar_html, f"{BLOG_BASE_URL}{archive_name}")
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log(f"✅ Mission Complete: {len(full_content)} characters published.")

if __name__ == "__main__": main()
