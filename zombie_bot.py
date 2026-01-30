import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "ALPHA INTELLIGENCE"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

def generate_sitemap(history):
    sitemap_path = os.path.join(BASE_DIR, "sitemap.xml")
    today = datetime.now().strftime('%Y-%m-%d')
    urls = [f"<url><loc>{BLOG_BASE_URL}</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>"]
    for item in history[:50]:
        file_name = item.get('file', '')
        file_date = item.get('date', today)
        if file_name:
            urls.append(f"<url><loc>{BLOG_BASE_URL}{file_name}</loc><lastmod>{file_date}</lastmod><priority>0.8</priority></url>")
    xml_content = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{"".join(urls)}</urlset>'
    with open(sitemap_path, "w", encoding="utf-8") as f: f.write(xml_content)
    log("📡 Sitemap.xml updated.")

# [FALLBACK] 폰트는 작게, 분량은 1,500자 이상으로 꽉 채운 리포트
FALLBACK_REPORT = """
## The Architectural Evolution of Cognitive Wealth In 2026

The dawn of 2026 marks the beginning of the 'Great Decoupling,' where technological advancement and human labor cost are finally severed by the massive deployment of institutional-grade AI. We are witnessing the most significant transformation of the global financial architecture since the Bretton Woods Agreement.

### 1. The Rise of Cognitive Capitalism
Artificial Intelligence has moved beyond simple predictive modeling into the realm of 'Strategic Autonomy.' Modern AI agents are no longer just tools; they are high-frequency decision-makers capable of managing multi-billion dollar liquidity pools with zero human intervention. This shift marks the rise of Cognitive Capitalism, where the primary driver of GDP is no longer traditional manufacturing or human services, but the algorithmic generation of intelligence and predictive value. The velocity of capital is being redefined by machine learning cycles that operate at a scale far beyond human cognitive capacity. Those who fail to integrate these autonomous systems into their wealth preservation strategy will face a terminal disadvantage.

### 2. Hardware Sovereignty and Cold Storage Defense
As AI consumes a larger share of global GDP, the concept of wealth preservation has evolved. Digital sovereignty and hardware-based security have become paramount. For institutional and private investors alike, securing the 'keys' to their digital kingdom via cold storage and decentralized protocols is no longer optional—it is a strategic necessity for long-term survival in an automated market. As the labor-based economy fades, the preservation of capital through physical and digital security becomes the only viable long-term strategy. The convergence of AI-driven market cycles requires a disciplined approach to asset protection.

### 3. Conclusion: Strategic Algorithmic Positioning
The path to wealth in 2026 is paved with advanced technology and uncompromising security. To thrive, one must align their portfolio with the architectural shifts of the new digital age. The era of passive observation is over; the era of strategic algorithmic positioning has begun. One must seek the absolute terminal of market intelligence to navigate this unprecedented volatility and secure their digital legacy for the coming decades.
"""

def generate_part(topic, focus):
    # 600자 이상의 긴 내용을 강제로 요구
    prompt = f"Write a deep 600-word professional analysis on '{topic}'. Focus: {focus}. High-end tone. Use Markdown. English Only."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.3}}, timeout=30)
        res = resp.json()['candidates'][0]['content']['parts'][0]['text']
        return re.sub(r'\{"role":.*?"content":', '', res, flags=re.DOTALL).replace('"}', '').strip()
    except: return ""

def create_final_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="google-site-verification" content="Jxh9S9J3S5_RBIpJH4CVrDkpRiDZ_mQ99TfIm7xK7YY" />
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #ffffff; --text: #1a1a1a; }}
        body {{ font-family: 'Inter', sans-serif; line-height: 1.6; color: var(--text); background: var(--bg); margin: 0; }}
        header {{ padding: 15px 50px; border-bottom: 2px solid #000; background: #fff; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; }}
        .container {{ max-width: 1450px; margin: 0 auto; display: grid; grid-template-columns: 1fr; gap: 60px; padding: 40px 20px; }}
        @media(min-width: 1100px) {{ .container {{ grid-template-columns: 1fr 380px; }} }}
        h1 {{ font-family: 'Playfair Display', serif; font-size: 3.8rem; font-weight: 900; line-height: 1.0; margin-bottom: 20px; letter-spacing: -3px; }}
        .summary-bar {{ border-top: 1px solid #000; border-bottom: 1px solid #000; padding: 10px 0; margin-bottom: 40px; font-weight: 700; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; }}
        /* 2단 비대칭 그리드 */
        .article-grid {{ display: grid; grid-template-columns: 1fr; gap: 40px; align-items: start; }}
        @media(min-width: 900px) {{ .article-grid {{ grid-template-columns: 1.4fr 1fr; }} }}
        .featured-img {{ width: 100%; max-height: 500px; object-fit: cover; border: 1px solid #000; filter: grayscale(100%); }}
        /* 본문 폰트 사이즈 표준화 (1.1rem) */
        .content {{ font-family: 'Playfair Display', serif; font-size: 1.1rem; text-align: justify; color: #333; }}
        .content h2 {{ font-family: 'Inter', sans-serif; font-weight: 900; font-size: 1.5rem; border-bottom: 6px solid #000; padding-bottom: 5px; margin-top: 35px; text-transform: uppercase; }}
        .img-promo {{ background: #000; color: #fff; padding: 35px; margin-top: 25px; font-size: 1rem; line-height: 1.6; text-align: center; font-weight: 700; }}
        .sidebar {{ position: sticky; top: 110px; height: fit-content; border-left: 2px solid #000; padding-left: 45px; }}
        .ad-btn {{ display: block; padding: 20px; margin-bottom: 15px; background: #000; color: #fff; text-align: center; text-decoration: none; font-weight: 900; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; }}
        footer {{ background: #000; color: #666; padding: 60px 50px; text-align: center; font-size: 0.75rem; margin-top: 100px; display: flex; justify-content: space-between; }}
    </style></head>
    <body>
    <header><div style="font-weight:900; font-size:1.4rem;">ALPHA INTELLIGENCE</div><a href="{EMPIRE_URL}" style="color:#000; text-decoration:none; font-weight:900; border:2px solid #000; padding:5px 15px; font-size:0.8rem;">TERMINAL</a></header>
    <div class="container"><main>
        <h1>{topic}</h1>
        <div class="summary-bar">• Institutional Intelligence: Strategic reports for Empire Analyst network.</div>
        <div class="article-grid">
            <div class="content">{body_html}</div>
            <div class="img-wrapper" style="position: sticky; top: 110px;">
                <img src="{img_url}" class="featured-img">
                <div class="img-promo">🚀 <b>Strategic Access:</b><br>Maximize market capture with AI-driven hardware security.<br><br><a href="{EMPIRE_URL}" style="color:#fff; text-decoration:underline; font-size:1.1rem;">Connect to Private Terminal →</a></div>
            </div>
        </div>
    </main>
    <aside class="sidebar">
        <h4 style="margin:0; text-transform:uppercase; color:#999; font-size:0.7rem; letter-spacing:4px; margin-bottom:30px;">Strategic Access</h4>
        <a href="{EMPIRE_URL}" class="ad-btn">Empire Analyst HQ</a>
        <a href="{AFFILIATE_LINK}" class="ad-btn" style="background:#fff; color:#000; border:2px solid #000;">Bybit Bonus</a>
        <a href="{AMAZON_LINK}" class="ad-btn" style="background:#fff; color:#000; border:2px solid #000;">Secure Ledger</a>
        <ul style="list-style:none; padding:0; font-size:0.95rem; line-height:2.2; font-weight:700; margin-top:50px;">{sidebar_html}</ul>
    </aside></div>
    <footer><div>&copy; 2026 ALPHA INTELLIGENCE. Part of Empire Analyst Network.</div><div>Amazon Disclaimer: As an Amazon Associate, I earn from qualifying purchases.</div></footer></body></html>"""

def main():
    log("🏁 Striker #2 Fixed-Font Robust Version Started")
    topic = "The Global Decoupling: Autonomous Wealth Systems"
    # 파트를 3개로 늘려 분량 확보
    p1 = generate_part(topic, "Infrastructure Innovation")
    p2 = generate_part(topic, "Economic Impact")
    p3 = generate_part(topic, "Strategic Security")
    full_content = f"{p1}\n\n{p2}\n\n{p3}"
    if len(full_content) < 1400: full_content = FALLBACK_REPORT
    
    html_body = markdown.markdown(full_content)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('minimal hardware tech black and white studio lighting 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    sidebar_html = "".join([f"<li>• <a href='{BLOG_BASE_URL}{h.get('file','')}' style='text-decoration:none; color:#000;'>{h.get('title','Recent Intel')}</a></li>" for h in history[:6]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f: f.write(full_html)
    with open(os.path.join(BASE_DIR, archive_name), "w", encoding="utf-8") as f: f.write(full_html)
    generate_sitemap(history)
    log(f"✅ Mission Success: {len(full_content)} chars.")

if __name__ == "__main__": main()
