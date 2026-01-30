import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration] 2호기 고유 아이덴티티
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "Dividend Master Intelligence"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = "history.json"

# [Monetization] 수익화 링크
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = f"https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

def clean_ai_output(text):
    if not text: return ""
    # 1호기 세척 로직 계승
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    return text.strip()

def generate_part(topic, focus):
    # 안전 설정 (차단 방지 핵심)
    safety = [{"category": f"HARM_CATEGORY_{c}", "threshold": "BLOCK_NONE"} for c in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]]
    prompt = f"Write a 450-word institutional report section on '{topic}'. Focus: {focus}. Markdown style. No years like 2026. English only."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "safetySettings": safety}, timeout=40)
        return clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text']) if resp.status_code == 200 else ""
    except: return ""

def create_unique_html(topic, img_url, body_html, sidebar_html):
    # 1호기와 완전히 다른 '레프트 사이드바' 디자인
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{topic}</title>
    <style>
        :root {{ --main: #064e3b; --sub: #fefce8; --accent: #d97706; }}
        body {{ font-family: 'Merriweather', serif; margin: 0; display: flex; flex-direction: column; min-height: 100vh; color: #1f2937; }}
        header {{ background: var(--main); color: white; padding: 20px; text-align: center; border-bottom: 4px solid var(--accent); }}
        .wrapper {{ max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 1fr; gap: 30px; padding: 30px; }}
        @media(min-width: 900px) {{ .wrapper {{ grid-template-columns: 1.2fr 2.8fr; }} }} /* 사이드바 왼쪽 배치 */
        .sidebar {{ background: #f9fafb; padding: 20px; border-radius: 12px; border: 1px solid #e5e7eb; height: fit-content; order: 2; }}
        @media(min-width: 900px) {{ .sidebar {{ order: 1; }} .main-content {{ order: 2; }} }}
        .btn {{ display: block; padding: 15px; margin-bottom: 10px; border-radius: 8px; text-decoration: none; text-align: center; font-weight: bold; border: 2px solid var(--main); color: var(--main); }}
        .btn-active {{ background: var(--accent); color: white; border-color: var(--accent); }}
        footer {{ background: #111827; color: #9ca3af; padding: 40px; text-align: center; font-size: 0.8rem; margin-top: auto; }}
    </style></head>
    <body>
    <header><div style="font-size: 1.8rem; font-weight: 900;">{BLOG_TITLE}</div></header>
    <div class="wrapper">
        <aside class="sidebar">
            <h3 style="border-bottom: 2px solid var(--main);">PREMIUM ACCESS</h3>
            <a href="{EMPIRE_URL}" class="btn btn-active">EMPIRE ANALYST HQ</a>
            <a href="{AFFILIATE_LINK}" class="btn">BYBIT $30,000 BONUS</a>
            <a href="{AMAZON_LINK}" class="btn">HARDWARE WALLET</a>
            <h4 style="margin-top:30px;">RECENT INTELLIGENCE</h4>
            <ul style="list-style:none; padding:0; font-size:0.85rem;">{sidebar_html}</ul>
        </aside>
        <main class="main-content">
            <h1 style="font-size: 2.5rem; line-height: 1.1;">{topic}</h1>
            <img src="{img_url}" style="width:100%; border-radius:12px; margin-bottom:20px;">
            <div style="background: var(--sub); padding: 15px; border-radius: 8px; margin-bottom: 25px; border-left: 5px solid var(--accent);">
                💡 <b>Strategic Insight:</b> <a href="{EMPIRE_URL}">Access the Full 2026 Wealth Blueprint at Main HQ →</a>
            </div>
            <div class="content">{body_html}</div>
        </main>
    </div>
    <footer>
        <p>&copy; 2026 {BLOG_TITLE}. A Member of Empire Analyst Network.</p>
        <p style="opacity: 0.6;"><b>Amazon Disclaimer:</b> As an Amazon Associate, I earn from qualifying purchases.</p>
    </footer></body></html>"""

def main():
    log("🏁 Striker #2 Engaged")
    topic = "The Secret Blueprint For Passive Dividend Wealth" # 후킹 제목 로직 적용 필요
    p1 = generate_part(topic, "Global Trends")
    p2 = generate_part(topic, "Compounding Math")
    p3 = generate_part(topic, "Portfolio Risk")
    
    html_body = markdown.markdown(f"{p1}\n\n{p2}\n\n{p3}")
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional gold dividend chart deep green theme 8k')}"
    
    # 히스토리 및 사이드바 로직 (1호기 기반)
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li style='margin-bottom:10px;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#374151;'>• {h['title']}</a></li>" for h in history[:5]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(create_unique_html(topic, img_url, html_body, sidebar_html))
    with open(archive_name, "w", encoding="utf-8") as f: f.write(create_unique_html(topic, img_url, html_body, sidebar_html))
    log("✅ Intelligence Published")

if __name__ == "__main__": main()
