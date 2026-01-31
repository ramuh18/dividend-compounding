import os, json, random, requests, markdown, urllib.parse, time, re, sys, io
from datetime import datetime

# [SYSTEM] 환경 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# [Configuration]
BLOG_TITLE = "Neural Algorithm" 
BLOG_BASE_URL = "https://ramuh18.github.io/neural-algorithm/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

def get_live_trends():
    try:
        url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"
        resp = requests.get(url, timeout=15)
        titles = re.findall(r"<title>(.*?)</title>", resp.text)
        return titles[3:15] if len(titles) > 5 else ["Cyber Security", "AI Singularity"]
    except:
        return ["Network Fragility", "Encryption War"]

# [🖋️ 1,500자급 초장문 해킹/보안 엔진]
def generate_neural_report(topic):
    return f"""
# [DEEP_NET_INTEL] System Vulnerability Analysis: {topic} Protocols

## 01. Initial Scan: The {topic} Vector
The current deployment of **{topic}** across global networks has triggered a series of critical security alerts. As of 2026, the intersection between decentralized data nodes and {topic} is creating a surface area for systemic exploits that legacy firewalls are incapable of mitigating. This report decrypts the underlying structural weaknesses within {topic} and the mandatory encryption protocols required to maintain capital sovereignty.

## 02. Payload Analysis: The Weaponization of {topic}
Our monitoring nodes have detected a significant shift in how {topic} is being integrated into autonomous trading algorithms. There is a clear pattern of 'backdoor' entry points being established under the guise of {topic} optimization. Institutional actors are leveraging {topic} to stress-test the liquidity of private vaults, looking for any centralized point of failure.

If your assets are parked in a centralized exchange during a {topic} volatility spike, you are effectively operating within a 'honeypot' environment. The data suggests that {topic} is being used as a catalyst for a massive, coordinated redistribution of wealth from unsecured nodes to hardened, private clusters.

## 03. Countermeasures: Hardware-Level Sovereignty
The only effective countermeasure against the systemic fragility exposed by {topic} is to opt-out of the digital grid entirely. The 'Always-On' nature of modern custodial systems is the primary exploit vector for {topic}. True network sovereignty requires a transition to air-gapped, physical vaulting systems.

By moving your private keys to a hardware-secured node, you effectively nullify the {topic} exploit. This is not an ideological choice; it is a tactical necessity in an era where {topic} defines the parameters of financial survival. The migration to cold storage is the ultimate 'Kill-Switch' against the centralized overreach being tested by the {topic} initiative.

## 04. Strategic Override: Executing the Exit
The supercycle is accelerating. The volatility surrounding **{topic}** is the final warning signal before a major network-wide reset. We recommend an immediate system audit: disconnect all legacy financial hooks, accumulate sovereign assets during the {topic} noise, and secure your access points in physical, non-digital environments. The era of the centralized observer is over. The era of the sovereign operator has begun.
"""

def generate_seo_files(history):
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += f'  <url><loc>{BLOG_BASE_URL}</loc><priority>1.0</priority></url>\n'
    for h in history[:50]:
        sitemap += f'  <url><loc>{BLOG_BASE_URL}{h["file"]}</loc><priority>0.8</priority></url>\n'
    sitemap += '</urlset>'
    with open("sitemap.xml", "w", encoding="utf-8") as f: f.write(sitemap)
    robots = f"User-agent: *\nAllow: /\nSitemap: {BLOG_BASE_URL}sitemap.xml"
    with open("robots.txt", "w", encoding="utf-8") as f: f.write(robots)

def create_final_html(topic, img_url, body_html, sidebar_html):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google-site-verification" content="여기에_3호기_인증태그_입력" />
    <title>{topic} | {BLOG_TITLE}</title>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --neon-green: #39ff14; --dark-bg: #0a0a0a; --terminal-text: #00ff41; }}
        body {{ font-family: 'Fira Code', monospace; background: var(--dark-bg); color: var(--terminal-text); line-height: 1.6; margin: 0; }}
        header {{ border-bottom: 2px solid var(--neon-green); padding: 20px; text-align: center; background: #000; }}
        .brand {{ font-size: 1.5rem; text-shadow: 0 0 10px var(--neon-green); }}
        .container {{ max-width: 1300px; margin: 30px auto; display: grid; grid-template-columns: 1fr 340px; gap: 40px; padding: 0 20px; }}
        @media(max-width: 1000px) {{ .container {{ grid-template-columns: 1fr; }} }}
        main {{ background: #000; padding: 40px; border: 1px solid var(--neon-green); box-shadow: 0 0 20px rgba(57, 255, 20, 0.1); }}
        h1 {{ color: #fff; border-bottom: 1px solid var(--neon-green); padding-bottom: 10px; }}
        .content h2 {{ color: var(--neon-green); margin-top: 40px; text-transform: uppercase; }}
        img {{ width: 100%; height: auto; border: 1px solid var(--neon-green); margin-bottom: 30px; filter: grayscale(50%) brightness(80%); }}
        .side-card {{ background: #000; padding: 20px; border: 1px solid var(--neon-green); margin-bottom: 20px; }}
        .btn {{ display: block; padding: 15px; background: var(--neon-green); color: #000; text-decoration: none; font-weight: bold; text-align: center; margin-bottom: 10px; }}
        footer {{ text-align: center; padding: 50px; font-size: 0.8rem; border-top: 1px solid var(--neon-green); margin-top: 50px; opacity: 0.7; }}
        .footer-links {{ margin-bottom: 15px; }}
        .footer-links a {{ color: var(--neon-green); text-decoration: none; margin: 0 10px; cursor: pointer; }}
        .amazon-disclaimer {{ font-size: 0.7rem; margin-top: 15px; font-style: italic; }}
        .modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); }}
        .modal-content {{ background: #000; margin: 15% auto; padding: 30px; width: 70%; max-width: 500px; border: 1px solid var(--neon-green); color: var(--neon-green); }}
        .close {{ color: #fff; float: right; font-size: 24px; cursor: pointer; }}
    </style></head>
    <body>
    <header><div class="brand">NEURAL_ALGORITHM_VAULT v2.6</div></header>
    <div class="container">
        <main>
            <div style="font-size:0.8rem; margin-bottom:10px;">> DECRYPTING_TOPIC... [OK]</div>
            <h1>{topic}</h1><img src="{img_url}"><div class="content">{body_html}</div>
        </main>
        <aside class="sidebar">
            <div class="side-card">
                <a href="{EMPIRE_URL}" class="btn" style="background:#ff0000; color:#fff;">🛑 EXECUTE_EXIT_PLAN</a>
                <a href="{AFFILIATE_LINK}" class="btn">📉 SHORT_MARKET</a>
                <a href="{AMAZON_LINK}" class="btn">🛡️ SECURE_ASSETS</a>
            </div>
            <div class="side-card">
                <h3 style="font-size:1rem;">> RECENT_SIGNALS</h3>
                <ul style="list-style:none; padding:0; font-size:0.8rem;">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    <footer>
        <div class="footer-links">
            <a onclick="openModal('about')">[ABOUT_US]</a>
            <a onclick="openModal('privacy')">[PRIVACY_POLICY]</a>
            <a onclick="openModal('contact')">[CONTACT]</a>
        </div>
        &copy; 2026 {BLOG_TITLE}. NOISE_REDUCTION_PROTOCOLS_ACTIVE.
        <div class="amazon-disclaimer">* AS AN AMAZON ASSOCIATE, THIS NODE EARNS FROM QUALIFYING PURCHASES.</div>
    </footer>
    <div id="infoModal" class="modal"><div class="modal-content"><span class="close" onclick="closeModal()">&times;</span><div id="modalBody"></div></div></div>
    <script>
        const info = {{
            about: "<h2>[ABOUT_NODE]</h2><p>Neural Algorithm is a decentralized intelligence hub monitoring global systemic risks and data sovereignty.</p>",
            privacy: "<h2>[DATA_POLICY]</h2><p>Zero-knowledge tracking policy. Cookies are used for operational telemetry only.</p>",
            contact: "<h2>[COMMS_CHANNEL]</h2><p>Secure link: <b>ops@neural-algorithm.io</b></p>"
        }};
        function openModal(id) {{ document.getElementById('modalBody').innerHTML = info[id]; document.getElementById('infoModal').style.display = "block"; }}
        function closeModal() {{ document.getElementById('infoModal').style.display = "none"; }}
    </script>
    </body></html>"""

def main():
    trends = get_live_trends()
    topic = random.choice(trends)
    body_text = generate_neural_report(topic) 
    html_body = markdown.markdown(body_text)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('cyberpunk matrix green digital code hacker dark 8k')}?width=1200&height=600"
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    sidebar_html = "".join([f"<li><b style='color:var(--neon-green);'>#</b> <a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#00ff41; text-decoration:none;'>{h.get('title')[:25]}...</a></li>" for h in history[:10]])
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    generate_seo_files(history)
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)

if __name__ == "__main__": main()
