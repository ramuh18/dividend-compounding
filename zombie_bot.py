import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [SYSTEM] 인코딩 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration] 2호기만의 고유 테마
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "THE ALPHA LAB"
BLOG_DESC = "Frontier Tech & Future Asset Intelligence"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = "history.json"

# [Monetization] 수익화 링크 (1호기와 동일)
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = f"https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [FALLBACK] 2호기 전용 1,500자 리포트
FALLBACK_REPORT = """
## 1. The Genesis of Autonomous Wealth
The rapid evolution of artificial intelligence is no longer a peripheral technological trend but the central pillar of a new global economic architecture. As we transition into an era defined by cognitive automation, the traditional boundaries of market productivity and asset valuation are being fundamentally rewritten.

## 2. Strategic Asset Sovereignty
As AI consumes a larger share of global GDP, the concept of wealth preservation has evolved. Digital sovereignty and hardware-based security have become paramount. For institutional and private investors alike, securing the 'keys' to their digital kingdom via cold storage and decentralized protocols is no longer optional—it is a strategic necessity.

## 3. The Future of Global Execution
The coming years will see the emergence of 'General Intelligence' components that will manage entire supply chains and financial portfolios with minimal human oversight. To remain competitive, one must look toward platforms that provide deep-tier intelligence and institutional-grade market analysis.
"""

def generate_part(topic, focus):
    safety = [{"category": f"HARM_CATEGORY_{c}", "threshold": "BLOCK_NONE"} for c in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]]
    prompt = f"Write a 500-word professional tech analysis on '{topic}'. Focus: {focus}. Institutional tone. Markdown. English Only."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "safetySettings": safety, "generationConfig": {"temperature": 0.4}}, timeout=40)
        if resp.status_code == 200:
            return resp.json()['candidates'][0]['content']['parts'][0]['text']
    except: pass
    return ""

def create_magazine_html(topic, img_url, body_html, sidebar_html, canonical_url):
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Lora:ital,wght@0,700;1,400&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #f9f9f9; --text: #1a1a1a; --accent: #000; }}
        body {{ font-family: 'Inter', sans-serif; line-height: 1.6; color: var(--text); background: var(--bg); margin: 0; padding: 0; }}
        header {{ background: #fff; padding: 15px 40px; border-bottom: 3px solid #000; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; }}
        .container {{ max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: 1fr; gap: 50px; padding: 50px 20px; }}
        @media(min-width: 1000px) {{ .container {{ grid-template-columns: 1fr 350px; }} }}
        h1 {{ font-family: 'Inter', sans-serif; font-size: 3.5rem; font-weight: 900; line-height: 1; margin: 0 0 20px 0; text-transform: uppercase; letter-spacing: -2px; }}
        .intro-bar {{ border-top: 1px solid #000; border-bottom: 1px solid #000; padding: 10px 0; margin-bottom: 30px; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; }}
        .main-grid {{ display: grid; grid-template-columns: 1fr; gap: 40px; }}
        @media(min-width: 800px) {{ .main-grid {{ grid-template-columns: 1.2fr 1fr; }} }}
        .featured-img {{ width: 100%; border-radius: 0; border: 1px solid #000; }}
        .content {{ font-family: 'Lora', serif; font-size: 1.2rem; text-align: justify; }}
        .sidebar {{ position: sticky; top: 100px; height: fit-content; }}
        .ad-box {{ background: #fff; border: 1px solid #000; padding: 25px; margin-bottom: 20px; }}
        .ad-btn {{ display: block; padding: 15px; background: #000; color: #fff; text-align: center; text-decoration: none; font-weight: 900; text-transform: uppercase; margin-top: 15px; font-size: 0.8rem; }}
        .hq-link {{ display: flex; align-items: center; background: #f1f1f1; padding: 15px; margin-top: 30px; border-radius: 4px; text-decoration: none; color: #000; font-weight: bold; }}
        footer {{ background: #000; color: #666; padding: 50px 40px; text-align: center; font-size: 0.75rem; margin-top: 80px; display: flex; justify-content: space-between; }}
    </style></head>
    <body>
    <header><div style="font-weight:900; letter-spacing:-1px;">{BLOG_TITLE}</div><div style="font-size:0.75rem;">{current_date}</div></header>
    <div class="container">
        <main>
            <h1>{topic}</h1>
            <div class="intro-bar">• Latest Insight from Empire Analyst HQ: 2026 Asset Security Protocols are now Live.</div>
            <div class="main-grid">
                <div class="content">{body_html}
                    <a href="{EMPIRE_URL}" class="hq-link">🚀 Deep Analysis: Access full-tier signals at our Private Terminal →</a>
                </div>
                <div><img src="{img_url}" class="featured-img"></div>
            </div>
        </main>
        <aside class="sidebar">
            <div class="ad-box">
                <h4 style="margin:0; text-transform:uppercase; font-size:0.75rem; color:#888;">Strategic Terminal</h4>
                <a href="{EMPIRE_URL}" class="ad-btn">Access HQ</a>
                <a href="{AFFILIATE_LINK}" class="ad-btn" style="background:#fff; color:#000;">$30,000 Bonus</a>
                <a href="{AMAZON_LINK}" class="ad-btn" style="background:#fff; color:#000;">Secure Ledger</a>
            </div>
            <h4 style="text-transform:uppercase; font-size:0.75rem; color:#888; border-bottom:1px solid #ddd; padding-bottom:5px;">Recent Intel</h4>
            <ul style="list-style:none; padding:0; font-size:0.85rem; line-height:1.8;">{sidebar_html}</ul>
        </aside>
    </div>
    <footer>
        <div>&copy; 2026 {BLOG_TITLE}. A Member of the Empire Analyst Network.</div>
        <div>Amazon Disclaimer: As an Amazon Associate, I earn from qualifying purchases.</div>
    </footer></body></html>"""

def main():
    log("🏁 Striker #2 Magazine Version Started")
    topic = "The Convergence of Robotics and Wealth Protection"
    p1 = generate_part(topic, "Innovation")
    p2 = generate_part(topic, "Execution")
    full_content = f"{p1}\n\n{p2}"
    if len(full_content) < 800: full_content = FALLBACK_REPORT
    
    html_body = markdown.markdown(full_content)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('minimal hardware gadget gadget black and white studio 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    sidebar_html = "".join([f"<li style='margin-bottom:10px;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#000; font-weight:bold;'>• {h['title']}</a></li>" for h in history[:6]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_magazine_html(topic, img_url, html_body, sidebar_html, f"{BLOG_BASE_URL}{archive_name}")
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log("✅ Generation Complete")

if __name__ == "__main__": main()
