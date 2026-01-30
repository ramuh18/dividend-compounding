import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

# [System] Force UTF-8 for special characters and symbols
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "Dividend Master"
# ★ 2호기 전용 주소
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
# ★ 수익의 심장: 본진 주소
MAIN_HQ_URL = "https://empire-analyst.digital/"

# [Monetization - Affiliate Links]
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_TAG = "empireanalyst-20"
AMAZON_LINK = f"https://www.amazon.com/s?k=ledger+nano+x&tag={AMAZON_TAG}"

HISTORY_FILE = "history.json"

# ==========================================
# [Cleaner] Remove AI Reasoning & Noise
# ==========================================
def clean_ai_output(text):
    if not text: return ""
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = re.sub(r'reasoning_content":".*?"', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    # Remove internal monologues
    patterns = [r"Draft:", r"Word count:", r"Note:", r"Internal Monologue:", r"Thinking:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

# ==========================================
# [Topic & Hook Title] Catchy Financial Titles
# ==========================================
def get_hot_topic():
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:10]).title
    except: raw_news = "The Secret of Compound Interest and Wealth"

    # 후킹 있는 제목 생성을 위한 프롬프트
    prompt = f"Rewrite '{raw_news}' into a viral, high-end financial title (MAX 9 WORDS). Use words like 'Secret', 'Blueprint', 'Shocking', 'Wealth'. English Only."
    
    title = "Dividend Strategy Masterclass"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.5}}, timeout=15)
        if resp.status_code == 200:
            title = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: pass
    return title

# ==========================================
# [Content] Deep Analysis + Internal Linking
# ==========================================
def generate_part(topic, focus):
    prompt = f"Write a professional deep-dive report on '{topic}'. Focus: {focus}. Discuss long-term dividend strategies. Use Markdown. Institutional tone. English Only. Output ONLY the article text."
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.3}}, timeout=30)
        if resp.status_code == 200:
            return clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: return "Intelligence gathering in progress..."

# ==========================================
# [HTML] Advanced Template with HQ Funnel
# ==========================================
def create_professional_html(topic, img_url, body_html, sidebar_html, canonical_url):
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} | {BLOG_TITLE}</title>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;700&family=Roboto:wght@400;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #0f172a; --accent: #b91c1c; --gold: #fbbf24; }}
        body {{ font-family: 'Merriweather', serif; line-height: 1.8; color: #334155; max-width: 1100px; margin: 0 auto; padding: 20px; }}
        header {{ background: var(--primary); color: white; padding: 50px 20px; text-align: center; border-radius: 15px; margin-bottom: 40px; border-bottom: 5px solid var(--gold); }}
        .hq-funnel {{ background: #fff3cd; padding: 20px; border-radius: 10px; border: 1px solid var(--gold); margin-bottom: 30px; text-align: center; font-weight: bold; }}
        .container {{ display: grid; grid-template-columns: 1fr; gap: 40px; }}
        @media(min-width: 900px) {{ .container {{ grid-template-columns: 2.4fr 1fr; }} }}
        .featured-img {{ width: 100%; border-radius: 12px; margin-bottom: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }}
        .ad-button {{ display: block; padding: 15px; margin-bottom: 12px; border-radius: 8px; text-decoration: none; text-align: center; font-weight: 900; transition: 0.2s; }}
        .btn-main {{ background: var(--gold); color: var(--primary); border: 2px solid var(--gold); }}
        .btn-bybit {{ border: 2px solid #f59e0b; color: #f59e0b; }}
        .btn-amazon {{ border: 2px solid #ea580c; color: #ea580c; }}
        .recent-list {{ list-style: none; padding: 0; }}
        .recent-list li {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
        .recent-list a {{ text-decoration: none; color: #0f172a; font-weight: bold; font-size: 0.9rem; }}
    </style></head>
    <body>
    <header>
        <div style="font-size: 2.5rem; font-weight: 900; letter-spacing: 2px;">{BLOG_TITLE}</div>
        <p>Strategic Wealth Intelligence Hub</p>
    </header>
    <div class="hq-funnel">
        ⚠️ DO NOT INVEST WITHOUT DATA. <a href="{MAIN_HQ_URL}" style="color:var(--accent);">Access the Elite Market Analysis at Empire Analyst HQ →</a>
    </div>
    <div class="container">
        <main>
            <div style="color: var(--accent); font-weight: 900; text-transform: uppercase;">{current_date} • PRIVATE REPORT</div>
            <h1 style="font-size: 2.6rem;">{topic}</h1>
            <img src="{img_url}" class="featured-img">
            <div class="content">{body_html}</div>
            
            <div style="background:#f8fafc; padding:30px; border-radius:12px; margin-top:50px; text-align:center; border: 1px dashed var(--primary);">
                <h3>📩 FREE COMPOUNDING BLUEPRINT</h3>
                <p>Subscribe to join 10,000+ elite investors.</p>
                <form action="YOUR_NEWSLETTER_URL" method="post">
                    <input type="email" placeholder="Your best email" required style="padding:12px; width:60%; border-radius:5px; border:1px solid #ddd;">
                    <button type="submit" style="background:var(--primary); color:white; padding:12px 25px; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">GET ACCESS</button>
                </form>
            </div>
        </main>
        <aside>
            <div style="position: sticky; top: 20px;">
                <h3 style="border-bottom: 3px solid var(--primary); padding-bottom: 5px;">🔥 CAPITAL ASSETS</h3>
                <a href="{MAIN_HQ_URL}" class="ad-button btn-main">EMPIRE ANALYST HQ</a>
                <a href="{AFFILIATE_LINK}" class="ad-button btn-bybit">💰 BYBIT $30,000 BONUS</a>
                <a href="{AMAZON_LINK}" class="ad-button btn-amazon">🛡️ SECURE YOUR ASSETS</a>
                
                <h3 style="margin-top:40px; border-bottom: 3px solid var(--primary); padding-bottom: 5px;">📂 RECENT INTELLIGENCE</h3>
                <ul class="recent-list">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    <footer style="margin-top: 80px; text-align: center; color: #94a3b8; border-top: 1px solid #eee; padding-top: 30px;">
        &copy; 2026 {BLOG_TITLE}. Part of the <a href="{MAIN_HQ_URL}" style="color:#64748b;">Empire Analyst Network</a>.
    </footer></body></html>"""

def main():
    log("🏁 Striker #2 Engaged")
    topic = get_hot_topic()
    log(f"🔥 Target Subject: {topic}")
    
    # Generate long content (2 parts)
    p1 = generate_part(topic, "Macro Outlook & Dividend Trends")
    p2 = generate_part(topic, "Strategic Wealth Allocation & Risk")
    full_markdown = f"{p1}\n\n{p2}"
    html_body = markdown.markdown(full_markdown)
    
    img_prompt = f"professional gold investment chart upward trend luxury dark theme high resolution"
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(img_prompt)}"
    
    file_timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    archive_filename = f"post_{file_timestamp}.html"
    
    # Load History for Sidebar (Internal Linking)
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = ""
    for h in history[:5]:
        sidebar_html += f"<li><a href='{BLOG_BASE_URL}{h['file']}'>{h['title']}</a></li>"
    
    # Save History
    new_entry = {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_filename}
    history.insert(0, new_entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    # Final HTML
    full_html = create_professional_html(topic, img_url, html_body, sidebar_html, f"{BLOG_BASE_URL}{archive_filename}")
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_filename, "w", encoding="utf-8") as f: f.write(full_html)
    log("✅ Intelligence Report Published")

if __name__ == "__main__": main()
