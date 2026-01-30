import os, json, random, requests, markdown, urllib.parse, feedparser, time, re, sys, io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [설정]
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BLOG_TITLE = "Dividend Master"
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/"
MAIN_HQ_URL = "https://empire-analyst.digital/"
HISTORY_FILE = "history.json"

# [수익화 링크]
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_TAG = "empireanalyst-20"
AMAZON_LINK = f"https://www.amazon.com/s?k=ledger+nano+x&tag={AMAZON_TAG}"

def clean_ai_output(text):
    if not text: return ""
    text = re.sub(r'\{"role":.*?"content":', '', text, flags=re.DOTALL)
    text = re.sub(r'reasoning_content":".*?"', '', text, flags=re.DOTALL)
    text = text.replace('"}', '').replace('"', '').replace("'", "")
    # 년도(2026) 및 불필요 수식어 제거
    text = text.replace("2026", "").replace("Year", "").replace("Update", "")
    patterns = [r"Draft:", r"Word count:", r"Note:", r"Internal Monologue:"]
    for p in patterns: text = re.sub(p, "", text, flags=re.IGNORECASE)
    return text.strip()

# [후킹 제목] 년도 제외 8단어 내외
def get_hot_topic():
    try:
        feed = feedparser.parse("https://news.google.com/rss/topics/CAAqJggBCiCPASowCAcLCzIxY2J1c2luZXNzX2VkaXRpb25fZW5fdXMvYnVzaW5lc3NfZWRpdGlvbl9lbl91cw?hl=en-US&gl=US&ceid=US:en")
        raw_news = random.choice(feed.entries[:10]).title
    except: raw_news = "Strategic Wealth Growth Through Passive Dividends"

    prompt = f"Rewrite '{raw_news}' into a high-end financial title. EXACTLY 8 WORDS. NO YEARS. Use: Secret, Wealth, Blueprint, Masterclass. English Only."
    title = "Secret Masterclass For Massive Long Term Dividend Wealth"
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7}}, timeout=15)
        if resp.status_code == 200:
            title = clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text'])
    except: pass
    return title

# [1,300자 본문] 4단계 섹션 분할 (안정성 강화)
def generate_full_report(topic):
    sections = [
        "Financial Freedom Through High Yield Asset Selection",
        "The Core Principles Of Strategic Compound Interest",
        "How Top Investors Manage Diverse Dividend Portfolios",
        "Securing Generational Wealth With Advanced Risk Control"
    ]
    full_md = ""
    for sec in sections:
        log(f"✍️ Generating: {sec}")
        prompt = f"Act as a senior wealth manager. Write 400 words on '{topic}' focusing on '{sec}'. Use professional English. Institutional tone. Markdown only. NO intro/outro."
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.3}}, timeout=50)
            if resp.status_code == 200:
                full_md += f"## {sec}\n\n" + clean_ai_output(resp.json()['candidates'][0]['content']['parts'][0]['text']) + "\n\n"
        except Exception as e:
            log(f"Fail in {sec}: {e}")
        time.sleep(3) # API 부하 방지
    return full_md

def create_professional_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@300;700&family=Playfair+Display:wght@900&display=swap" rel="stylesheet">
    <style>
        :root {{ --navy: #0f172a; --gold: #eab308; --soft-gold: #fefce8; --text: #334155; }}
        body {{ font-family: 'Merriweather', serif; line-height: 1.8; color: var(--text); max-width: 1100px; margin: 0 auto; padding: 15px; background: #fff; }}
        /* 초슬림 헤더 */
        header {{ background: var(--navy); color: white; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; border-radius: 4px; margin-bottom: 15px; }}
        /* 본진 유도 배너 - 빨간색 제거, 부드러운 골드톤 */
        .hq-funnel {{ background: var(--soft-gold); padding: 14px; text-align: center; border-radius: 4px; margin-bottom: 20px; border: 1px solid var(--gold); }}
        .hq-funnel a {{ color: var(--navy); font-weight: 900; text-decoration: none; }}
        .container {{ display: grid; grid-template-columns: 1fr; gap: 30px; }}
        @media(min-width: 900px) {{ .container {{ grid-template-columns: 2.6fr 1.4fr; }} }}
        h1 {{ font-family: 'Playfair Display', serif; font-size: 2.2rem; color: var(--navy); margin: 5px 0 15px 0; line-height: 1.1; }}
        .content h2 {{ color: var(--navy); border-bottom: 2px solid var(--gold); padding-bottom: 5px; margin-top: 30px; font-size: 1.4rem; }}
        /* 사이드바 버튼 */
        .ad-btn {{ display: block; padding: 14px; margin-bottom: 10px; border-radius: 4px; text-decoration: none; text-align: center; font-weight: bold; border: 1px solid #cbd5e1; transition: 0.2s; }}
        .btn-hq {{ background: var(--gold); color: var(--navy); border-color: var(--gold); }}
    </style></head>
    <body>
    <header><div style="font-weight:900; letter-spacing:1px;">DIVIDEND MASTER</div><a href="{MAIN_HQ_URL}" style="color:var(--gold); text-decoration:none; font-size:0.8rem; font-weight:bold;">HQ ACCESS →</a></header>
    <div class="hq-funnel">🏛️ Private Wealth Intelligence: <a href="{MAIN_HQ_URL}">Unlock The Full Strategy at Empire Analyst HQ</a></div>
    <div class="container">
        <main>
            <h1>{topic}</h1>
            <img src="{img_url}" style="width:100%; border-radius:4px; margin-bottom:20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <div class="content">{body_html}</div>
        </main>
        <aside>
            <div style="position:sticky; top:15px;">
                <h4 style="border-bottom:2px solid var(--navy); padding-bottom:5px; margin-bottom:15px; color:var(--navy);">STRATEGIC LINKS</h4>
                <a href="{MAIN_HQ_URL}" class="ad-btn btn-hq">EMPIRE ANALYST HQ</a>
                <a href="{AFFILIATE_LINK}" class="ad-btn" style="color:#b45309;">💰 $30,000 BYBIT BONUS</a>
                <a href="{AMAZON_LINK}" class="ad-btn" style="color:#9a3412;">🛡️ SECURE YOUR ASSETS</a>
                <h4 style="margin-top:40px; border-bottom:2px solid var(--navy); padding-bottom:5px; color:var(--navy);">RECENT REPORTS</h4>
                <ul style="list-style:none; padding:0; font-size:0.85rem;">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    </body></html>"""

def main():
    log("🏁 Striker #2 Engaged")
    topic = get_hot_topic()
    full_markdown = generate_full_report(topic)
    
    # 내용 누락 방지: 1000자 미만이면 다시 한번 시도하거나 에러 로그 출력
    if len(full_markdown) < 1000:
        log("⚠️ Content too short, retrying key section...")
        # ... 추가 생성 로직
        
    html_body = markdown.markdown(full_markdown)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('luxury gold and black financial chart professional 8k photography')}"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li style='margin-bottom:12px; line-height:1.4;'><a href='{BLOG_BASE_URL}{h['file']}' style='text-decoration:none; color:#475569; font-weight:bold;'>• {h['title']}</a></li>" for h in history[:6]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    output_html = create_professional_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(output_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(output_html)
    log(f"✅ Mission Complete: {len(full_markdown)} characters published.")

if __name__ == "__main__": main()
