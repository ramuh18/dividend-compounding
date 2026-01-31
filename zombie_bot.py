import os, json, random, requests, markdown, urllib.parse, time, re, sys, io
from datetime import datetime

# [SYSTEM] 한글 깨짐 방지
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def log(msg): print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

# [Configuration] ★2호기 전용 설정★
BLOG_TITLE = "Alpha Intelligence" 
BLOG_BASE_URL = "https://ramuh18.github.io/dividend-compounding/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [📊 구글 트렌드 실시간 수집]
def get_live_trends():
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
        resp = requests.get(url, timeout=15)
        titles = re.findall(r"<title>(.*?)</title>", resp.text)
        return titles[3:15] if len(titles) > 5 else ["Dividend Alpha", "Compounding Strategy"]
    except:
        return ["Asset Accumulation", "Quantitative Security"]

# [🖋️ 2호기 전용 1,500자급 초장문 엔진]
def generate_alpha_report(topic):
    return f"""
# [ALPHA INTEL] Quantitative Analysis: The Structural Shift in {topic}

## Executive Summary
The financial landscape of 2026 is being redefined by the rapid evolution of **{topic}**. For the long-term compounder, understanding the interplay between market volatility and {topic} is critical. This report provides an in-depth quantitative analysis of how {topic} influences asset accumulation and the necessity of robust security protocols during this transition.

## 1. Algorithmic Impact on {topic}
The data surrounding {topic} suggests a significant increase in algorithmic intervention within the public markets. Our proprietary monitoring nodes have identified a recurring pattern of liquidity hunting specifically tied to {topic} news cycles. This institutional front-running often creates artificial price floors that retail investors mistake for organic support.

To survive the 2026 supercycle, an investor must look beyond the surface volatility of {topic}. The real 'Alpha' lies in the cold, hard data of net-settlement flows. We are witnessing a historic migration of capital away from inflationary assets toward the very nodes of value that {topic} is currently stress-tested.

## 2. Compounding Under Pressure: The Security Dividend
While {topic} dominates the headlines, the silent threat remains the vulnerability of centralized custodial systems. The true dividend of 2026 is not just financial—it is the security of your principal. As {topic} continues to disrupt traditional valuation models, the risk of a 'systemic freeze' grows.

Our strategic recommendation is to treat security as a primary asset class. The accumulation of wealth through {topic} is meaningless if the access points are controlled by a third party. We observe that sovereign investors are utilizing this period of {topic} volatility to move their core holdings into hardware-secured, non-custodial vaults. This is the only way to ensure that the compounding process remains uninterrupted by the geopolitical realignment currently underway.

## 3. Preservation Strategy: Opting Out of Fragility
The systemic fragility exposed by {topic} is a feature, not a bug, of the current legacy architecture. By opting out of fractional reserve systems, you effectively insulate your portfolio from the fallout of the {topic} cycle. This requires a fundamental shift in mindset: moving from 'convenience' to 'sovereignty.'

We emphasize that the migration to cold storage is a mandatory tactical requirement. The volatility of {topic} is being used to flush out leveraged participants. Maintaining a delta-neutral position in terms of security is the only path to achieving the 'Alpha Intelligence' necessary for long-term capital integrity.

## Final Strategic Conclusion
The era of passive accumulation is over. The dynamics of **{topic}** demand an active, security-first approach to compounding. We recommend immediate auditing of your asset custody protocols. Minimize exchange exposure, secure your private keys in physical vaults, and focus on the quantitative signals that truly matter. The reset is accelerating, and only the sovereign will prevail.
"""

def create_final_html(topic, img_url, body_html, sidebar_html):
    # [2호기 테마] 실버 & 다크 블루 (차갑고 세련된 느낌)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic} | {BLOG_TITLE}</title>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --alpha-navy: #101820; --alpha-silver: #adb5bd; --alpha-blue: #0047ab; }}
        body {{ font-family: 'Inter', sans-serif; background: #e9ecef; color: #212529; line-height: 1.8; margin: 0; }}
        
        header {{ background: var(--alpha-navy); color: #fff; padding: 30px 20px; text-align: center; border-bottom: 5px solid var(--alpha-silver); position: relative; }}
        .brand {{ font-family: 'Montserrat', sans-serif; font-size: 1.8rem; letter-spacing: 1px; text-transform: uppercase; color: var(--alpha-silver); }}
        
        .container {{ max-width: 1300px; margin: 40px auto; display: grid; grid-template-columns: 1fr 340px; gap: 40px; padding: 0 20px; }}
        @media(max-width: 1000px) {{ .container {{ grid-template-columns: 1fr; }} }}
        
        main {{ background: #fff; padding: 45px; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
        h1 {{ color: var(--alpha-navy); font-size: 2.8rem; line-height: 1.2; margin-top: 0; }}
        .content h2 {{ color: var(--alpha-blue); border-bottom: 2px solid var(--alpha-silver); padding-bottom: 10px; margin-top: 50px; font-family: 'Montserrat'; }}
        img {{ width: 100%; height: auto; border-radius: 6px; margin-bottom: 30px; border: 1px solid #dee2e6; }}
        
        .side-card {{ background: #fff; padding: 25px; border-radius: 8px; margin-bottom: 25px; border-left: 6px solid var(--alpha-blue); box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        .btn {{ display: block; padding: 15px; background: var(--alpha-navy); color: #fff; text-decoration: none; font-weight: bold; text-align: center; margin-bottom: 12px; border-radius: 4px; transition: 0.2s; }}
        .btn-red {{ background: #c8102e; }}
        .btn:hover {{ background: var(--alpha-blue); }}
        
        footer {{ text-align: center; padding: 60px 20px; color: #6c757d; border-top: 1px solid #dee2e6; background: #f8f9fa; font-size: 0.85rem; }}
        .amazon-disclaimer {{ font-style: italic; margin-top: 10px; opacity: 0.8; }}
    </style></head>
    <body>
    <header><div class="brand">ALPHA_INTELLIGENCE</div></header>
    <div class="container">
        <main>
            <div style="color:var(--alpha-blue); font-weight:bold; margin-bottom:10px; letter-spacing:1px;">[ QUANTITATIVE ANALYSIS ]</div>
            <h1>{topic}</h1>
            <img src="{img_url}">
            <div class="content">{body_html}</div>
        </main>
        <aside class="sidebar">
            <div class="side-card">
                <a href="{EMPIRE_URL}" class="btn btn-red">🛑 ACCESS ALPHA PLAN</a>
                <a href="{AFFILIATE_LINK}" class="btn">📉 SHORT MARKET</a>
                <a href="{AMAZON_LINK}" class="btn">🛡️ SECURE ASSETS</a>
            </div>
            <div class="side-card">
                <h3 style="margin-top:0; color:var(--alpha-navy); font-family:'Montserrat';">RECENT ALPHA</h3>
                <ul style="list-style:none; padding:0; line-height:2.2; font-size:0.9rem;">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    <footer>
        &copy; 2026 {BLOG_TITLE}. Quantitative Accumulation Protocols.
        <div class="amazon-disclaimer">* As an Amazon Associate, this site earns from qualifying purchases.</div>
    </footer></body></html>"""

def main():
    trends = get_live_trends()
    topic = random.choice(trends)
    body_text = generate_alpha_report(topic) 
    html_body = markdown.markdown(body_text)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('professional clean financial workspace silver blue accent 8k')}?width=1200&height=600"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li><b style='color:var(--alpha-blue);'>▶</b> <a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#333; text-decoration:none;'>{h.get('title')[:25]}...</a></li>" for h in history[:10]])
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)

if __name__ == "__main__": main()
