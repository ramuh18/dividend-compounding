import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "FUTURE INTELLIGENCE"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = "history.json"

# [Monetization] 1호기 수익화 로직 완전 이식
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = f"https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [FALLBACK] 1,500자 이상의 고품질 리포트 유지
FALLBACK_REPORT = """
## The Great Decoupling: How Autonomous Intelligence Rewrites Global Capitalism

The dawn of 2026 marks the beginning of the 'Great Decoupling,' where technological advancement and human labor cost are finally severed by the massive deployment of institutional-grade AI.

### 1. The Genesis of Cognitive Capitalism
Artificial Intelligence has moved beyond simple predictive modeling into the realm of 'Strategic Autonomy.' Modern AI agents are no longer just tools; they are high-frequency decision-makers capable of managing multi-billion dollar liquidity pools with zero human intervention.

### 2. Market Volatility and the New 'Alpha'
In this automated landscape, traditional market analysis is becoming obsolete. The 'Alpha' of tomorrow is hidden within the data silos of autonomous networks. Investors who continue to rely on manual intelligence are facing an existential risk.

### 3. Institutional Asset Protection
As the labor-based economy fades, the preservation of capital through physical and digital security becomes the only viable long-term strategy. Cold storage solutions and institutional-grade encryption are the only remaining defenses against the volatility induced by high-speed algorithmic trading.
"""

def clean_ai_output(text):
    if not text or "error" in text.lower() or "queue full" in text.lower(): return ""
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    return text.strip()

def generate_part(topic, focus):
    safety = [{"category": f"HARM_CATEGORY_{c}", "threshold": "BLOCK_NONE"} for c in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]]
    prompt = f"Write a 500-word deep-tier institutional analysis on '{topic}'. Focus: {focus}. High-end tone. Markdown. English Only."
    for attempt in range(2):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "safetySettings": safety, "generationConfig": {"temperature": 0.4}}, timeout=30)
            if resp.status_code == 200:
                res = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
                if len(res) > 350: return res
        except: pass
        time.sleep(2)
    return ""

def create_ultra_wide_html(topic, img_url, body_html, sidebar_html, canonical_url):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #ffffff; --text: #000000; }}
        body {{ font-family: 'Inter', sans-serif; line-height: 1.8; color: var(--text); background: var(--bg); margin: 0; }}
        header {{ padding: 25px 60px; border-bottom: 2px solid #000; background: #fff; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; }}
        .container {{ max-width: 1450px; margin: 0 auto; display: grid; grid-template-columns: 1fr; gap: 80px; padding: 60px 20px; }}
        @media(min-width: 1100px) {{ .container {{ grid-template-columns: 1fr 420px; }} }}
        h1 {{ font-family: 'Playfair Display', serif; font-size: 4.5rem; font-weight: 900; line-height: 1.1; margin: 0 0 40px 0; letter-spacing: -3px; text-transform: uppercase; }}
        .featured-img {{ width: 100%; height: 600px; object-fit: cover; filter: grayscale(100%); border: 1px solid #000; }}
        .sidebar {{ position: sticky; top: 120px; height: fit-content; border-left: 4px solid #000; padding-left: 50px; }}
        .ad-btn {{ display: block; padding: 22px; margin-bottom: 15px; text-decoration: none; text-align: center; font-weight: 900; background: #000; color: #fff; text-transform: uppercase; font-size: 0.9rem; letter-spacing: 2px; border: 1px solid #000; }}
        /* 알림 박스 디자인 정돈 */
        .alpha-box {{ background: #000; color: #fff; padding: 45px; margin: 50px 0; text-align: center; border: 1px solid #000; }}
        .alpha-box-inner {{ max-width: 900px; margin: 0 auto; }}
        .alpha-box a {{ color: #fff; font-weight: 900; text-decoration: underline; text-underline-offset: 4px; }}
        .content {{ font-size: 1.4rem; text-align: justify; }}
        .content h2 {{ font-family: 'Playfair Display', serif; font-size: 2.2rem; border-bottom: 6px solid #000; padding-bottom: 10px; margin-top: 60px; }}
        footer {{ background: #000; color: #444; padding: 80px 0; text-align: center; font-size: 0.8rem; margin-top: 120px; }}
    </style></head>
    <body>
    <header><div style="font-weight:900; font-size:1.6rem; letter-spacing:-1px;">{BLOG_TITLE}</div><a href="{EMPIRE_URL}" style="color:#000; text-decoration:none; font-weight:900; border:3px solid #000; padding:8px 20px;">ACCESS TERMINAL</a></header>
    <div class="container">
        <main>
            <h1>{topic}</h1>
            <img src="{img_url}" class="featured-img">
            <div class="alpha-box">
                <div class="alpha-box-inner">
                    <span style="display:block; font-weight:900; text-transform:uppercase; margin-bottom:15px; font-size:0.8rem; color:#777; letter-spacing:4px;">⚡ Institutional Grade Intelligence</span>
                    <p style="margin: 0; line-height: 1.5; font-size: 1.25rem;">
                        This report is a condensed version of our institutional analysis. <br>
                        For full-tier algorithmic signals and private wealth cycles, <br>
                        <a href="{EMPIRE_URL}">Secure Your Access at Empire Analyst HQ →</a>
                    </p>
                </div>
            </div>
            <div class="content">{body_html}</div>
        </main>
        <aside class="sidebar">
            <h4 style="text-transform:uppercase; letter-spacing:4px; font-size:0.85rem; margin-bottom:40px; color:#aaa;">Strategic Access</h4>
            <a href="{EMPIRE_URL}" class="ad-btn">Private HQ Terminal</a>
            <a href="{AFFILIATE_LINK}" class="ad-btn" style="background:#fff; color:#000;">Bybit $30k Bonus</a>
            <a href="{AMAZON_LINK}" class="ad-btn" style="background:#fff; color:#000;">Hardware Security</a>
            <h4 style="margin-top:80px; text-transform:uppercase; letter-spacing:4px; font-size:0.85rem; color:#aaa;">Recent Intel</h4>
            <ul style="list-style:none; padding:0; font-size:1.05rem; line-height:2.6;">{sidebar_html}</ul>
        </aside>
    </div>
    <footer>
        <p>&copy; 2026 {BLOG_TITLE}. A Strategic Partner of the Empire Analyst Network.</p>
        <p style="max-width:850px; margin:25px auto; opacity:0.4;"><b>Amazon Disclaimer:</b> As an Amazon Associate, I earn from qualifying purchases. No financial advice provided.</p>
    </footer></body></html>"""

def main():
    log("🏁 Striker #2 Ultra-Wide B&W Refined")
    topic = "The Convergence of AI and Future Wealth Architectures"
    p1 = generate_part(topic, "Technological Shifts")
    p2 = generate_part(topic, "Market Decoupling")
    p3 = generate_part(topic, "Asset Sovereignty")
    full_content = f"{p1}\n\n{p2}\n\n{p3}"
    if len(full_content) < 1000: full_content = FALLBACK_REPORT
    
    html_body = markdown.markdown(full_content)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional minimal humanoid robot interface black and white architecture 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    sidebar_html = "".join([f"<li><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#000; font-weight:900;'>• {h['title']}</a></li>" for h in history[:6]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_ultra_wide_html(topic, img_url, html_body, sidebar_html, f"{BLOG_BASE_URL}{archive_name}")
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)
    log(f"✅ Mission Complete: {len(full_content)} characters published.")

if __name__ == "__main__": main()
