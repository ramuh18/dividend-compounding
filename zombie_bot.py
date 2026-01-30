import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [SYSTEM] 인코딩 설정 및 경로 강제 지정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration] 2호기: 매거진 스타일 테마
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "ALPHA INTELLIGENCE"
BLOG_DESC = "Frontier Technology & Future Economy Analysis"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

# [Monetization] 수익화 링크 (1호기와 동일)
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = f"https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [FALLBACK] 1호기(거시경제)와 차별화된 1,500자 테크 리포트
FALLBACK_REPORT = """
## 1. The Dawn of Cognitive Wealth Preservation
The rapid evolution of artificial intelligence is no longer a peripheral technological trend but the central pillar of a new global economic architecture. As we transition into an era defined by cognitive automation, the traditional boundaries of market productivity and asset valuation are being fundamentally rewritten.

## 2. Strategic Asset Sovereignty and Hardware Defense
As AI consumes a larger share of global GDP, the concept of wealth preservation has evolved. Digital sovereignty and hardware-based security have become paramount. For institutional and private investors alike, securing the 'keys' to their digital kingdom via cold storage and decentralized protocols is no longer optional—it is a strategic necessity for long-term survival in an automated market.

## 3. Future Trajectory: Beyond Human Oversight
The coming years will see the emergence of 'General Intelligence' components that will manage entire supply chains and financial portfolios with minimal human oversight. This shift necessitates a complete re-evaluation of current asset allocation strategies. To remain competitive, one must look toward platforms that provide deep-tier intelligence and institutional-grade market analysis.
"""

def clean_ai_output(text):
    if not text or "error" in text.lower(): return ""
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    return text.strip()

def generate_part(topic, focus):
    prompt = f"Write a 600-word professional tech report on '{topic}'. Focus: {focus}. Institutional tone. Markdown. English Only."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.3}}, timeout=30)
        return clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: return ""

def create_magazine_html(topic, img_url, body_html, sidebar_html, canonical_url):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Lora:ital,wght@0,400;1,400&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #ffffff; --text: #000000; }}
        body {{ font-family: 'Inter', sans-serif; line-height: 1.6; color: var(--text); background: var(--bg); margin: 0; }}
        header {{ padding: 20px 50px; border-bottom: 2px solid #000; background: #fff; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; }}
        /* 가로 1400px 와이드 레이아웃 */
        .container {{ max-width: 1400px; margin: 0 auto; display: grid; grid-template-columns: 1fr; gap: 60px; padding: 50px 20px; }}
        @media(min-width: 1000px) {{ .container {{ grid-template-columns: 1fr 350px; }} }}
        h1 {{ font-size: 3.8rem; font-weight: 900; line-height: 1.1; margin: 0 0 30px 0; letter-spacing: -3px; text-transform: uppercase; }}
        .intro-line {{ border-top: 1px solid #000; border-bottom: 1px solid #000; padding: 10px 0; margin-bottom: 40px; font-weight: 700; font-size: 0.9rem; text-transform: uppercase; }}
        .magazine-grid {{ display: grid; grid-template-columns: 1fr; gap: 50px; }}
        @media(min-width: 850px) {{ .magazine-grid {{ grid-template-columns: 1.3fr 1fr; }} }}
        .featured-img {{ width: 100%; border: 1px solid #000; filter: grayscale(100%); }}
        .content {{ font-family: 'Lora', serif; font-size: 1.25rem; text-align: justify; }}
        .sidebar {{ position: sticky; top: 120px; height: fit-content; border-left: 2px solid #000; padding-left: 40px; }}
        .ad-btn {{ display: block; padding: 20px; margin-bottom: 12px; background: #000; color: #fff; text-align: center; text-decoration: none; font-weight: 900; font-size: 0.85rem; text-transform: uppercase; }}
        footer {{ background: #000; color: #555; padding: 80px 50px; text-align: center; font-size: 0.8rem; margin-top: 100px; display: flex; justify-content: space-between; }}
    </style></head>
    <body>
    <header><div style="font-weight:900; font-size:1.4rem;">{BLOG_TITLE}</div><a href="{EMPIRE_URL}" style="color:#000; text-decoration:none; font-weight:900; border:2px solid #000; padding:5px 15px;">TERMINAL</a></header>
    <div class="container">
        <main>
            <h1>{topic}</h1>
            <div class="intro-line">Elite Resource: Access private real estate and tech reports at <a href="{EMPIRE_URL}" style="color:#000;">Empire Analyst HQ →</a></div>
            <div class="magazine-grid">
                <div class="content">{body_html}</div>
                <div><img src="{img_url}" class="featured-img"></div>
            </div>
        </main>
        <aside class="sidebar">
            <h4 style="margin-top:0; text-transform:uppercase; color:#999; font-size:0.75rem; letter-spacing:3px;">Strategic Access</h4>
            <a href="{EMPIRE_URL}" class="ad-btn">Access Private HQ</a>
            <a href="{AFFILIATE_LINK}" class="ad-btn" style="background:#fff; color:#000; border:1px solid #000;">Bybit Bonus</a>
            <a href="{AMAZON_LINK}" class="ad-btn" style="background:#fff; color:#000; border:1px solid #000;">Hardware Wallet</a>
            <h4 style="margin-top:60px; text-transform:uppercase; color:#999; font-size:0.75rem;">Recent Intel</h4>
            <ul style="list-style:none; padding:0; font-size:0.9rem; line-height:2;">{sidebar_html}</ul>
        </aside>
    </div>
    <footer>
        <div>&copy; 2026 {BLOG_TITLE}. Part of the Empire Analyst Network.</div>
        <div>Amazon Disclaimer: As an Amazon Associate, I earn from qualifying purchases.</div>
    </footer></body></html>"""

def main():
    log("🏁 Striker #2 Magazine Version Started")
    topic = "The Convergence of Robotics and Wealth Protection"
    p1 = generate_part(topic, "Innovation Context")
    p2 = generate_part(topic, "Security Execution")
    full_content = f"{p1}\n\n{p2}"
    
    # 1,500자 정량 확보
    if len(full_content) < 1000: full_content = FALLBACK_REPORT
    
    html_body = markdown.markdown(full_content)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('minimal hardware gadget black and white studio 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    sidebar_html = "".join([f"<li style='margin-bottom:12px;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#000; font-weight:bold;'>• {h['title']}</a></li>" for h in history[:6]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_magazine_html(topic, img_url, html_body, sidebar_html, f"{BLOG_BASE_URL}{archive_name}")
    
    # 파일 쓰기 강제 수행
    with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f: f.write(full_html)
    with open(os.path.join(BASE_DIR, archive_name), "w", encoding="utf-8") as f: f.write(full_html)
    log(f"✅ Mission Success: {len(full_content)} characters.")

if __name__ == "__main__": main()
