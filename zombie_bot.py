import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [SYSTEM] 1호기 방식의 인코딩 설정
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
    if not text or len(text) < 50: return ""
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    patterns = [r"Draft:", r"Word count:", r"Note:", r"Internal Monologue:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

def generate_part(topic, focus):
    safety = [{"category": f"HARM_CATEGORY_{c}", "threshold": "BLOCK_NONE"} for c in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]]
    prompt = f"Write a professional financial and tech report on '{topic}'. Focus: {focus}. Min 450 words. Institutional tone. Markdown. English Only."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "safetySettings": safety, "generationConfig": {"temperature": 0.3}}, timeout=45)
        if resp.status_code == 200:
            content = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
            if content: return content
    except: pass
    try:
        url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
        return clean_ai_output(requests.get(url, timeout=30).text)
    except: return ""

def get_hot_topic():
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiBDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSnJieWdBUVdfQVFvWFE?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:5]).title if feed.entries else "AI Evolution"
    except: raw_news = "The Future of Artificial Intelligence"
    prompt = f"Rewrite '{raw_news}' into a viral tech title. EXACTLY 8 WORDS. NO YEARS. English Only."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7}}, timeout=15)
        return clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: return "Secret Evolution Of Artificial Intelligence In Daily Life"

def create_wide_bw_html(topic, img_url, body_html, sidebar_html, canonical_url):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #000000; --secondary: #ffffff; --gray: #f4f4f5; --border: #e4e4e7; }}
        body {{ font-family: 'Inter', sans-serif; line-height: 1.8; color: #18181b; background: var(--secondary); margin: 0; }}
        header {{ padding: 20px 40px; border-bottom: 1px solid var(--border); background: var(--secondary); display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }}
        .brand {{ font-size: 1.2rem; font-weight: 900; letter-spacing: -1px; }}
        /* 가로 폭 대폭 확장 */
        .container {{ max-width: 1300px; margin: 0 auto; display: grid; grid-template-columns: 1fr; gap: 60px; padding: 40px 20px; }}
        @media(min-width: 900px) {{ .container {{ grid-template-columns: 1fr 350px; }} }}
        h1 {{ font-size: 3.5rem; font-weight: 900; line-height: 1.1; margin-bottom: 30px; letter-spacing: -2px; }}
        .featured-img {{ width: 100%; height: 500px; object-fit: cover; border-radius: 0; margin-bottom: 40px; filter: grayscale(100%); transition: 0.5s; }}
        .featured-img:hover {{ filter: grayscale(0%); }}
        /* 스티키 사이드바 */
        .sidebar-wrapper {{ position: relative; }}
        .sidebar {{ position: -webkit-sticky; position: sticky; top: 100px; height: fit-content; border-left: 1px solid var(--border); padding-left: 40px; }}
        .ad-btn {{ display: block; padding: 18px; margin-bottom: 15px; text-decoration: none; text-align: center; font-weight: 900; background: var(--primary); color: var(--secondary); text-transform: uppercase; font-size: 0.8rem; letter-spacing: 1px; transition: 0.3s; }}
        .ad-btn:hover {{ background: #333; }}
        .alpha-box {{ background: var(--gray); padding: 30px; margin-bottom: 40px; border-left: 8px solid var(--primary); }}
        .content {{ font-size: 1.2rem; }}
        footer {{ background: var(--primary); color: #71717a; padding: 60px 0; text-align: center; font-size: 0.8rem; margin-top: 80px; }}
    </style></head>
    <body>
    <header><div class="brand">{BLOG_TITLE}</div><a href="{EMPIRE_URL}" style="color:#000; text-decoration:none; font-weight:bold;">HQ ACCESS →</a></header>
    <div class="container">
        <main>
            <h1>{topic}</h1>
            <img src="{img_url}" class="featured-img">
            <div class="alpha-box">
                <span style="display:block; font-weight:900; text-transform:uppercase; margin-bottom:10px; font-size:0.8rem;">🚀 Alpha Intelligence Alert</span>
                Standard market data is lagging. <a href="{EMPIRE_URL}" style="color:#000; text-decoration:underline;">Access the Private Institutional Terminal at Empire Analyst HQ →</a>
            </div>
            <div class="content">{body_html}</div>
        </main>
        <div class="sidebar-wrapper">
            <aside class="sidebar">
                <h4 style="margin-top:0; text-transform:uppercase; letter-spacing:2px; font-size:0.8rem; margin-bottom:30px;">Strategic Access</h4>
                <a href="{EMPIRE_URL}" class="ad-btn">Empire Analyst HQ</a>
                <a href="{AFFILIATE_LINK}" class="ad-btn" style="background:#fff; color:#000; border:2px solid #000;">Bybit $30k Bonus</a>
                <a href="{AMAZON_LINK}" class="ad-btn" style="background:#fff; color:#000; border:2px solid #000;">Secure Ledger Store</a>
                <h4 style="margin-top:60px; text-transform:uppercase; letter-spacing:2px; font-size:0.8rem; margin-bottom:20px;">Recent Intelligence</h4>
                <ul style="list-style:none; padding:0; font-size:0.9rem; line-height:2;">{sidebar_html}</ul>
            </aside>
        </div>
    </div>
    <footer>
        <p>&copy; 2026 {BLOG_TITLE}. Part of Empire Analyst Network.</p>
        <p style="max-width:800px; margin:20px auto; opacity:0.6;"><b>Amazon Disclaimer:</b> As an Amazon Associate, I earn from qualifying purchases. This content is for informational purposes only.</p>
    </footer></body></html>"""

def main():
    log("🏁 Striker #2 Wide B&W Version Started")
    topic = get_hot_topic()
    p1 = generate_part(topic, "Core Innovation")
    p2 = generate_part(topic, "Economic Impact")
    p3 = generate_part(topic, "Future Execution")
    full_content = f"{p1}\n\n{p2}\n\n{p3}"
    if len(full_content) < 800: full_content += "\n\n" + generate_part(topic, "Summary")
    
    html_body = markdown.markdown(full_content)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('futuristic humanoid robot face black and white minimal 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    sidebar_html = "".join([f"<li style='margin-bottom:15px;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#71717a;'>• {h['title']}</a></li>" for h in history[:6]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_wide_bw_html(topic, img_url, html_body, sidebar_html, f"{BLOG_BASE_URL}{archive_name}")
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log("✅ Generation Complete")

if __name__ == "__main__": main()
