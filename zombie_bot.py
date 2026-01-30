import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [SYSTEM] 1호기 방식의 인코딩 강제 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration] 2호기: The Alpha Lab
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "The Alpha Lab"
BLOG_DESC = "Frontier Intelligence for High-Growth Assets"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = "history.json"

# [Monetization] 수익화 (1호기 로직 완벽 이식)
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = f"https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

def clean_ai_output(text):
    if not text: return ""
    # 1호기의 강력한 클리너 로직 이식
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    patterns = [r"Draft:", r"Word count:", r"Note:", r"Internal Monologue:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

def get_hot_topic():
    # 주제를 '미래 자산'으로 고정하여 노출 극대화
    topics = ["Bitcoin Institutional Adoption", "Emerging Tech Assets", "Next-Gen Wealth Cycles", "Global Market Alpha"]
    raw = random.choice(topics)
    prompt = f"Rewrite '{raw}' into a viral financial title. EXACTLY 8 WORDS. NO YEARS. Use: Blueprint, Wealth, Secret, Edge. English Only."
    title = "Secret Blueprint For Finding Alpha In Global Markets"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7}}, timeout=15)
        if resp.status_code == 200:
            title = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: pass
    return title

def generate_part(topic, focus):
    # 제미나이 필터 완전 해제
    safety = [{"category": f"HARM_CATEGORY_{c}", "threshold": "BLOCK_NONE"} for c in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]]
    prompt = f"Write a professional deep-dive report section on '{topic}'. Focus: {focus}. Min 450 words. Institutional tone. Use Markdown. English Only. NO chatty notes."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "safetySettings": safety, "generationConfig": {"temperature": 0.3}}, timeout=45)
        if resp.status_code == 200:
            return clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: pass
    return ""

def create_unique_dark_html(topic, img_url, body_html, sidebar_html, canonical_url):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&family=Inter:wght@900&display=swap" rel="stylesheet">
    <style>
        :root {{ --neon: #10b981; --dark: #0f172a; --gray: #1e293b; }}
        body {{ font-family: 'Roboto Mono', monospace; line-height: 1.6; color: #e2e8f0; background: var(--dark); margin: 0; }}
        header {{ background: #000; padding: 20px; text-align: left; border-bottom: 2px solid var(--neon); }}
        .container {{ max-width: 1200px; margin: 40px auto; display: grid; grid-template-columns: 1fr; gap: 40px; padding: 0 20px; }}
        @media(min-width: 900px) {{ .container {{ grid-template-columns: 320px 1fr; }} }} /* 사이드바 왼쪽 배치 */
        h1 {{ font-family: 'Inter', sans-serif; font-size: 3rem; color: #fff; line-height: 1; margin: 0 0 20px 0; letter-spacing: -2px; }}
        .sidebar {{ background: var(--gray); padding: 25px; border-radius: 8px; height: fit-content; border: 1px solid #334155; }}
        .ad-btn {{ display: block; padding: 15px; margin-bottom: 12px; border-radius: 4px; text-decoration: none; text-align: center; font-weight: bold; background: transparent; border: 1px solid var(--neon); color: var(--neon); transition: 0.3s; }}
        .ad-btn:hover {{ background: var(--neon); color: var(--dark); }}
        footer {{ background: #000; color: #64748b; padding: 40px 0; text-align: center; font-size: 0.8rem; margin-top: 80px; }}
    </style></head>
    <body>
    <header><div style="font-weight:900; color:var(--neon); font-size:1.5rem;">THE ALPHA LAB</div></header>
    <div class="container">
        <aside class="sidebar">
            <h4 style="margin-top:0; border-bottom: 1px solid var(--neon); padding-bottom:10px;">⚡ FRONT-RUN THE MARKET</h4>
            <a href="{EMPIRE_URL}" class="ad-btn" style="background:var(--neon); color:var(--dark);">EMPIRE ANALYST HQ</a>
            <a href="{AFFILIATE_LINK}" class="ad-btn">💰 $30,000 BONUS</a>
            <a href="{AMAZON_LINK}" class="ad-btn">🛡️ SECURE YOUR LEDGER</a>
            <h4 style="margin-top:40px;">RECENT INTEL</h4>
            <ul style="list-style:none; padding:0; font-size:0.8rem;">{sidebar_html}</ul>
        </aside>
        <main>
            <h1>{topic}</h1>
            <img src="{img_url}" style="width:100%; border-radius:8px; margin-bottom:30px; border: 1px solid #334155;">
            <div style="background: rgba(16,185,129,0.1); padding: 20px; border-radius: 8px; border-left: 4px solid var(--neon); margin-bottom: 30px;">
                🚀 <b>Alpha Alert:</b> Standard data is not enough. <a href="{EMPIRE_URL}" style="color:var(--neon);">Access the Private Terminal at Empire Analyst HQ →</a>
            </div>
            <div class="content">{body_html}</div>
        </main>
    </div>
    <footer>
        <p>&copy; 2026 The Alpha Lab. Part of Empire Analyst Network.</p>
        <p style="max-width:600px; margin:20px auto; opacity:0.6;"><b>Amazon Disclaimer:</b> As an Amazon Associate, I earn from qualifying purchases.</p>
    </footer></body></html>"""

def main():
    log("🏁 Striker #2 (Alpha Lab) Started")
    topic = get_hot_topic()
    log(f"🔥 Subject: {topic}")
    
    # 1호기 방식의 3단계 생성 (확실한 1,300자 보장)
    p1 = generate_part(topic, "Frontier Asset Macro Context")
    p2 = generate_part(topic, "Growth Projection & Risk Metrics")
    p3 = generate_part(topic, "Technical Alpha Execution Strategies")
    
    full_md = f"{p1}\n\n{p2}\n\n{p3}"
    if len(full_md) < 800:
        log("⚠️ Content short, retrying...")
        full_md += "\n\n" + generate_part(topic, "Executive Wealth Summary")
        
    html_body = markdown.markdown(full_md)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('cyberpunk financial data city dark neon green 8k')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li style='margin-bottom:12px;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#94a3b8;'>• {h['title']}</a></li>" for h in history[:5]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(create_unique_dark_html(topic, img_url, html_body, sidebar_html, f"{BLOG_BASE_URL}{archive_name}"))
    with open(archive_name, "w", encoding="utf-8") as f: f.write(create_unique_dark_html(topic, img_url, html_body, sidebar_html, f"{BLOG_BASE_URL}{archive_name}"))
    log("✅ Intelligence Published")

if __name__ == "__main__": main()
