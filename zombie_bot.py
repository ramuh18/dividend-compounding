import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [SYSTEM] 인코딩 설정 및 경로 최적화
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration] 2호기 최종 설정
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "ALPHA INTELLIGENCE"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

# [Monetization] 수익화 링크 (Bybit, Amazon)
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [Sitemap Generator] 서치콘솔용 사이트맵 자동 생성
def generate_sitemap(history):
    sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
    urls = [f"<url><loc>{BLOG_BASE_URL}</loc><lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod><priority>1.0</priority></url>"]
    for item in history[:50]:
        urls.append(f"<url><loc>{BLOG_BASE_URL}{item['file']}</loc><lastmod>{item['date']}</lastmod><priority>0.8</priority></url>")
    xml_content = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{"".join(urls)}</urlset>'
    with open(sitemap_path, "w", encoding="utf-8") as f: f.write(xml_content)
    log("📡 Sitemap.xml updated.")

# [FALLBACK] 분량 보장용 1,500자 리포트
FALLBACK_REPORT = """
## The Genesis of Autonomous Wealth Protection
The dawn of 2026 marks the beginning of the 'Great Decoupling,' where technological advancement and human labor cost are finally severed by the massive deployment of institutional-grade AI.

### 1. Cognitive Capitalism and Market Shifts
Artificial Intelligence has moved beyond simple predictive modeling into the realm of 'Strategic Autonomy.' Modern AI agents are no longer just tools; they are high-frequency decision-makers capable of managing multi-billion dollar liquidity pools with zero human intervention.

### 2. Hardware Sovereignty in the Age of AI
Digital sovereignty and hardware-based security have become paramount. For institutional and private investors alike, securing the 'keys' to their digital kingdom via cold storage and decentralized protocols is no longer optional—it is a strategic necessity for long-term survival in an automated market.
"""

def clean_ai_output(text):
    if not text or "error" in text.lower(): return ""
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    return text.strip()

def generate_part(topic, focus):
    prompt = f"Write a professional 500-word analysis on '{topic}'. Focus: {focus}. Institutional tone. Markdown. English Only."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.3}}, timeout=30)
        return clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: return ""

def create_final_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="google-site-verification" content="Jxh9S9J3S5_RBIpJH4CVrDkpRiDZ_mQ99TfIm7xK7YY" />
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #ffffff; --text: #1a1a1a; --border: #000; }}
        body {{ font-family: 'Inter', sans-serif; line-height: 1.7; color: var(--text); background: var(--bg); margin: 0; }}
        header {{ padding: 20px 50px; border-bottom: 2px solid var(--border); background: #fff; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; }}
        .container {{ max-width: 1450px; margin: 0 auto; display: grid; grid-template-columns: 1fr; gap: 60px; padding: 50px 20px; }}
        @media(min-width: 1100px) {{ .container {{ grid-template-columns: 1fr 380px; }} }}
        h1 {{ font-family: 'Playfair Display', serif; font-size: 4rem; font-weight: 900; line-height: 1.0; margin-bottom: 30px; letter-spacing: -2px; }}
        .summary-bar {{ border-top: 1px solid #000; border-bottom: 1px solid #000; padding: 12px 0; margin-bottom: 40px; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 2px; }}
        .article-grid {{ display: grid; grid-template-columns: 1fr; gap: 40px; align-items: start; }}
        @media(min-width: 900px) {{ .article-grid {{ grid-template-columns: 1.2fr 1fr; }} }}
        .img-wrapper {{ position: sticky; top: 120px; }}
        .featured-img {{ width: 100%; max-height: 450px; object-fit: cover; border: 1px solid #000; filter: grayscale(100%); }}
        .img-promo {{ background: #000; color: #fff; padding: 30px; margin-top: 20px; font-size: 1rem; line-height: 1.5; }}
        .content {{ font-family: 'Playfair Display', serif; font-size: 1.3rem; text-align: justify; }}
        .content h2 {{ font-family: 'Inter', sans-serif; font-weight: 900; font-size: 1.8rem; border-bottom: 6px solid #000; padding-bottom: 10px; margin-top: 40px; text-transform: uppercase; }}
        .sidebar {{ position: sticky; top: 120px; height: fit-content; border-left: 2px solid #000; padding-left: 45px; }}
        .ad-btn {{ display: block; padding: 20px; margin-bottom: 15px; background: #000; color: #fff; text-align: center; text-decoration: none; font-weight: 900; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 2px; }}
        footer {{ background: #000; color: #666; padding: 60px 50px; text-align: center; font-size: 0.8rem; margin-top: 100px; display: flex; justify-content: space-between; }}
    </style></head>
    <body>
    <header><div style="font-weight:900; font-size:1.5rem;">ALPHA INTELLIGENCE</div><a href="{EMPIRE_URL}" style="color:#000; text-decoration:none; font-weight:900; border:2px solid #000; padding:5px 15px;">TERMINAL</a></header>
    <div class="container"><main>
        <h1>{topic}</h1>
        <div class="summary-bar">• Exclusive Strategy Briefing for Empire Analyst Network Members.</div>
        <div class="article-grid">
            <div class="content">{body_html}</div>
            <div class="img-wrapper">
                <img src="{img_url}" class="featured-img">
                <div class="img-promo">🚀 <b>Alpha Insight:</b><br>This tech shift is rewriting asset values. <br><a href="{EMPIRE_URL}" style="color:#fff;">Access Private Signals at Empire Analyst HQ →</a></div>
            </div>
        </div>
    </main>
    <aside class="sidebar">
        <h4 style="margin:0; text-transform:uppercase; color:#999; font-size:0.75rem; letter-spacing:4px; margin-bottom:30px;">Strategic Access</h4>
        <a href="{EMPIRE_URL}" class="ad-btn">Empire Analyst HQ</a>
        <a href="{AFFILIATE_LINK}" class="ad-btn" style="background:#fff; color:#000; border:2px solid #000;">Bybit Bonus</a>
        <a href="{AMAZON_LINK}" class="ad-btn" style="background:#fff; color:#000; border:2px solid #000;">Secure Ledger</a>
        <ul style="list-style:none; padding:0; font-size:1rem; line-height:2.2; font-weight:700; margin-top:50px;">{sidebar_html}</ul>
    </aside></div>
    <footer><div>&copy; 2026 ALPHA INTELLIGENCE. Part of Empire Analyst Network.</div><div>Amazon Disclaimer: As an Amazon Associate, I earn from qualifying purchases.</div></footer></body></html>"""

def main():
    log("🏁 Striker #2 Final Robust Version Started")
    topic = "The Convergence of AI and Future Wealth Protection"
    p1 = generate_part(topic, "Innovation")
    p2 = generate_part(topic, "Execution")
    full_content = f"{p1}\n\n{p2}"
    if len(full_content) < 1000: full_content = FALLBACK_REPORT
    
    html_body = markdown.markdown(full_content)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('minimal hardware gadget gadget black and white studio 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    sidebar_html = "".join([f"<li>• <a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#000;'>{h['title']}</a></li>" for h in history[:6]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f: f.write(full_html)
    with open(os.path.join(BASE_DIR, archive_name), "w", encoding="utf-8") as f: f.write(full_html)
    
    generate_sitemap(history)
    log("✅ All tasks complete.")

if __name__ == "__main__": main()
