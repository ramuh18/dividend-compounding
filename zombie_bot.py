import os, json, random, requests, markdown, urllib.parse, time, re, sys, io, textwrap
from datetime import datetime

# [SYSTEM] 환경 설정
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# [Configuration] 2호기 전용 설정
BLOG_TITLE = "Alpha Intelligence" 
BLOG_BASE_URL = "https://ramuh18.github.io/alpha-intelligence/" 
EMPIRE_URL = "https://empire-analyst.digital/"
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
AFFILIATE_LINK = "https://www.bybit.com/invite?ref=DOVWK5A" 
AMAZON_LINK = "https://www.amazon.com/s?k=ledger+nano+x&tag=empireanalyst-20"

# [주제 리스트 50개: 2호기 테마(보안/퀀트/자산관리)에 맞춤]
BACKUP_TOPICS = [
    "Quantum Computing Risks in Finance", "Algorithmic Trading Strategies", "Zero-Knowledge Proofs Explained",
    "Cold Storage Security Protocols", "High-Frequency Trading Impact", "Dividend Aristocrats Analysis",
    "Cybersecurity in Fintech", "Decentralized Finance (DeFi) Audits", "Smart Contract Vulnerabilities",
    "Automated Portfolio Rebalancing", "Machine Learning in Markets", "Predictive Analytics Models",
    "Asset Tokenization Trends", "Regulatory Compliance in Crypto", "Institutional Custody Solutions",
    "Multi-Signature Wallet Security", "The Future of Robo-Advisors", "Big Data in Wealth Management",
    "Sentiment Analysis Algorithms", "Blockchain Interoperability", "Privacy-Preserving Coins",
    "Identity Management on Blockchain", "Risk-Adjusted Return Metrics", "Sharpe Ratio Explained",
    "Technical Analysis vs Fundamental", "Moving Average Crossover Strategies", "Bollinger Bands Analysis",
    "RSI Divergence Signals", "Market Neutral Strategies", "Arbitrage Opportunities 2026",
    "Stablecoin Peg Stability", "Centralized Exchange Risks", "Peer-to-Peer Lending Data",
    "Real Estate Crowdfunding Analysis", "Biometric Security in Banking", "Phishing Attack Prevention",
    "Ransomware Threats to Finance", "Cloud Security for Assets", "API Security Standards",
    "Data Encryption Best Practices", "Two-Factor Authentication Flaws", "Hardware Wallet Comparison",
    "Paper Wallet Pros and Cons", "Seed Phrase Storage Guide", "Estate Planning for Digital Assets",
    "Tax Loss Harvesting Algorithms", "ESG Investing Data Analysis", "Carbon Credit Markets",
    "The Alpha Generation Strategy", "Beta Slippage Risks"
]

# [문단 블록 15개: 2호기 테마(데이터/보안)에 맞춘 내용]
CONTENT_BLOCKS = [
    """
    ## The Data-Driven Advantage
    In the modern financial landscape, **{topic}** is not just a buzzword; it is a mathematical necessity. Alpha Intelligence algorithms indicate that investors ignoring {topic} are operating with a significant information asymmetry. By leveraging high-frequency data sets related to {topic}, institutional players are capturing alpha while retail traders are left chasing noise.
    """,
    """
    ## Security Protocols and {topic}
    The vulnerability surface regarding **{topic}** is expanding rapidly. Our forensic analysis of recent market breaches shows that {topic} is often the primary attack vector. Implementing military-grade encryption and multi-layered security protocols is the only viable defense against the threats associated with {topic}. Security is not a product; it is a process.
    """,
    """
    ## Quantifying the Risk
    Standard risk models often fail to account for the tail risks embedded in **{topic}**. When we apply Monte Carlo simulations to {topic}, the probability of a systemic failure increases exponentially under stress conditions. Understanding the statistical variance of {topic} allows for more robust portfolio construction and capital preservation.
    """,
    """
    ## The Algorithmic Shift
    The market is no longer driven by human sentiment alone; it is driven by algorithms reacting to **{topic}**. Machine learning models are now trained to execute trades based on micro-patterns in {topic} faster than human reaction time. To survive in this environment, one must understand the code behind the trade.
    """,
    """
    ## Asset Sovereignity Strategy
    **{topic}** highlights the critical need for asset sovereignty. If you rely on third-party custodians to manage the risks of {topic}, you are exposing yourself to counterparty risk.
    <div style="margin: 20px 0; padding: 15px; background: #f0fdf4; border-left: 5px solid #059669;">
        <strong>🛡️ Security Alert:</strong> Take control of your keys. 
        <a href="{AMAZON_LINK}" style="color: #059669; font-weight: bold;">[Recommended Hardware Wallets]</a>
    </div>
    """,
    """
    ## Decentralization vs Centralization
    The debate around **{topic}** centers on the friction between centralized control and decentralized efficiency. While centralized systems offer speed, they introduce single points of failure regarding {topic}. Decentralized alternatives, verified by cryptographic proofs, offer a more resilient framework for managing {topic} in the long term.
    """,
    """
    ## The Future of {topic}
    Predictive modeling suggests that **{topic}** will undergo a paradigm shift by 2027. Early adopters who integrate robust data analytics with {topic} will likely see outsized returns. The convergence of AI and {topic} is creating new asset classes that simply did not exist a decade ago.
    """,
    """
    ## Audit and Compliance
    Regulatory frameworks are tightening around **{topic}**. For sophisticated investors, ensuring that their exposure to {topic} is compliant with global standards is paramount. A lack of transparency in {topic} metrics is a major red flag. Always demand auditable on-chain data or third-party verification.
    """,
    """
    ## Technical Analysis Indicators
    On the charts, **{topic}** is forming a classic accumulation pattern. Volatility indices suggest that a breakout regarding {topic} is imminent. Quantitative traders are currently positioning themselves on the long side of volatility, expecting {topic} to drive significant price action in the coming quarters.
    """,
    """
    ## The Privacy Paradox
    In an era of surveillance, **{topic}** offers a unique value proposition for privacy preservation. However, the balance between transparency and anonymity in {topic} remains delicate. Advanced cryptographic techniques like Zero-Knowledge Proofs are becoming essential for interacting with {topic} without revealing sensitive financial data.
    """,
    """
    ## Smart Contract Logic
    If **{topic}** involves automated execution, one must scrutinize the underlying smart contract logic. Code is law, but code can contain bugs. Understanding the solidity of the code backing {topic} is more important than reading the whitepaper. We recommend a thorough audit of any protocol related to {topic}.
    """,
    """
    ## Yield Generation Mechanics
    How is yield generated from **{topic}**? If the source of the yield is opaque, it is likely a Ponzi structure. Sustainable alpha in {topic} comes from genuine economic activity or liquidity provision, not inflationary tokenomics. We dissect the yield mechanics of {topic} to separate the signal from the noise.
    """,
    """
    ## The Institutional Grade Standard
    **{topic}** is rapidly moving from an experimental niche to an institutional grade asset class. Custodians like Fidelity and BNY Mellon are building infrastructure to support {topic}. This institutional adoption brings liquidity but also regulatory scrutiny. The wild west days of {topic} are over.
    """,
    """
    ## Defensive Portfolio Allocation
    In a defensive portfolio, **{topic}** plays a specific role: uncorrelated return generation. By adding exposure to {topic}, investors can improve the Sharpe ratio of their overall holdings. However, position sizing is key. We recommend capping exposure to {topic} at 5% of the total portfolio value.
    """,
    """
    ## The Human Factor in Automation
    Even in fully automated systems involving **{topic}**, the human element remains the weakest link. Phishing, social engineering, and poor operational security are the biggest threats to your positions in {topic}. Automation handles the math, but discipline handles the security.
    """
]

def get_live_trends():
    selected_topic = random.choice(BACKUP_TOPICS)
    return [selected_topic]

def generate_deep_report(topic):
    # 인트로
    intro = f"""
# Alpha Report: {topic}

## Intelligence Briefing
Our algorithmic indicators have flagged significant activity regarding **{topic}**. In a market driven by data, understanding the underlying metrics of {topic} provides a distinct edge. This report analyzes the technical and fundamental vectors of {topic}.
"""
    
    # [핵심] textwrap.dedent로 '##' 문제 해결 + 7개 블록 조립
    selected_blocks = random.sample(CONTENT_BLOCKS, 7)
    body_content = ""
    for block in selected_blocks:
        clean_block = textwrap.dedent(block)
        body_content += clean_block.format(topic=topic, AMAZON_LINK=AMAZON_LINK) + "\n"

    # 결론
    conclusion = f"""
## Strategic Outlook
The data suggests a high probability of volatility in **{topic}**. Adaptive strategies are required to navigate this shift.
<br><br>
**Optimize your portfolio security.**
<div style="background: #fff; padding: 20px; border: 1px solid #ddd; margin-top: 20px; border-radius: 4px; border-top: 4px solid #334155;">
    <h3>📊 Alpha Recommendations</h3>
    <ul style="margin-bottom: 20px;">
        <li>Audit your digital asset security protocols.</li>
        <li>Rebalance exposure based on volatility targets.</li>
    </ul>
    <a href="{EMPIRE_URL}" style="background: #334155; color: white; padding: 10px 20px; text-decoration: none; font-weight: bold; border-radius: 4px; font-size: 0.9rem;">ACCESS QUANT STRATEGY</a>
</div>
"""
    return intro + body_content + conclusion

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
    <meta name="google-site-verification" content="여기에_인증태그_입력" />
    <title>{topic} | {BLOG_TITLE}</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&family=Orbitron:wght@700&display=swap" rel="stylesheet">
    <style>
        /* 2호기 전용 테마: 실버/다크그레이/청록색(Cyan) */
        :root {{ --main-dark: #1e293b; --accent-cyan: #06b6d4; --silver-bg: #f1f5f9; }}
        body {{ font-family: 'Roboto Mono', monospace; background: var(--silver-bg); color: #334155; line-height: 1.7; margin: 0; }}
        header {{ background: var(--main-dark); color: #fff; padding: 25px; text-align: center; border-bottom: 4px solid var(--accent-cyan); }}
        .brand {{ font-family: 'Orbitron', sans-serif; font-size: 2rem; letter-spacing: 2px; text-transform: uppercase; }}
        /* 표준 너비 1100px 적용 */
        .container {{ max-width: 1100px; margin: 40px auto; display: grid; grid-template-columns: 1fr 320px; gap: 40px; padding: 0 20px; }}
        @media(max-width: 900px) {{ .container {{ grid-template-columns: 1fr; }} }}
        main {{ background: #fff; padding: 50px; border: 1px solid #cbd5e1; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-radius: 4px; }}
        h1 {{ color: var(--main-dark); font-family: 'Orbitron', sans-serif; font-size: 2.0rem; margin-top:0; }}
        .content h2 {{ color: #0f172a; margin-top: 40px; border-left: 5px solid var(--accent-cyan); padding-left: 15px; font-size: 1.4rem; font-weight: 700; }}
        img {{ width: 100%; height: auto; margin-bottom: 30px; border-radius: 4px; filter: contrast(110%); }}
        .side-card {{ background: #fff; padding: 25px; border: 1px solid #cbd5e1; margin-bottom: 20px; border-top: 4px solid var(--accent-cyan); }}
        .btn {{ display: block; padding: 12px; background: var(--main-dark); color: #fff; text-decoration: none; font-weight: bold; text-align: center; margin-bottom: 10px; border-radius: 2px; font-size: 0.9rem; transition: 0.3s; }}
        .btn:hover {{ background: var(--accent-cyan); color: #000; }}
        footer {{ text-align: center; padding: 50px; color: #64748b; background: #fff; border-top: 1px solid #e2e8f0; margin-top: 50px; }}
        .footer-links a {{ color: #475569; margin: 0 10px; cursor: pointer; text-decoration: none; font-weight: bold; }}
        .amazon-disclaimer {{ font-size: 0.8rem; color: #94a3b8; margin-top: 20px; font-style: italic; }}
        .modal {{ display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); }}
        .modal-content {{ background: #fff; margin: 15% auto; padding: 30px; width: 80%; max-width: 600px; border-radius: 4px; font-family: sans-serif; }}
        .close {{ float: right; font-size: 28px; cursor: pointer; }}
    </style></head>
    <body>
    <header><div class="brand">{BLOG_TITLE}</div></header>
    <div class="container">
        <main>
            <div style="color:#06b6d4; font-size:0.8rem; margin-bottom:10px; font-weight:bold;">// QUANTITATIVE ANALYSIS PROTOCOL</div>
            <h1>{topic}</h1><img src="{img_url}"><div class="content">{body_html}</div>
        </main>
        <aside class="sidebar">
            <div class="side-card">
                <h3 style="margin-top:0; color:var(--main-dark); font-family:'Orbitron';">SYSTEM ACCESS</h3>
                <a href="{EMPIRE_URL}" class="btn">⚡ ALPHA STRATEGY</a>
                <a href="{AFFILIATE_LINK}" class="btn" style="background:#334155;">📊 DATA TERMINAL</a>
                <a href="{AMAZON_LINK}" class="btn" style="background:#06b6d4; color:#000;">🔒 COLD STORAGE</a>
            </div>
            <div class="side-card">
                <h3>Incoming Signals</h3>
                <ul style="padding-left:20px; list-style-type: square;">{sidebar_html}</ul>
            </div>
        </aside>
    </div>
    <footer>
        <div class="footer-links">
            <a onclick="openModal('about')">About Protocol</a>
            <a onclick="openModal('privacy')">Data Privacy</a>
            <a onclick="openModal('contact')">Contact Node</a>
        </div>
        &copy; 2026 {BLOG_TITLE}. Systems Online.
        <div class="amazon-disclaimer">* As an Amazon Associate, we earn from qualifying purchases.</div>
    </footer>
    <div id="infoModal" class="modal"><div class="modal-content"><span class="close" onclick="closeModal()">&times;</span><div id="modalBody"></div></div></div>
    <script>
        const info = {{
            about: "<h2>Alpha Intelligence</h2><p>Data-driven insights for the modern investor. We focus on quantitative strategies and asset security.</p>",
            privacy: "<h2>Data Privacy</h2><p>We do not track personal identifiers. System logs are anonymized.</p>",
            contact: "<h2>Contact</h2><p>Admin: admin@empire-analyst.digital</p>"
        }};
        function openModal(id) {{ document.getElementById('modalBody').innerHTML = info[id]; document.getElementById('infoModal').style.display = "block"; }}
        function closeModal() {{ document.getElementById('infoModal').style.display = "none"; }}
    </script>
    </body></html>"""

def main():
    topic = get_live_trends()[0] 
    body_text = generate_deep_report(topic) 
    html_body = markdown.markdown(body_text)
    # 이미지: 2호기 전용 (실버/미래지향적/데이터)
    img_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote('futuristic financial data hud interface silver blue cyberpunk 8k')}?width=1200&height=600"
    
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f: history = json.load(f)
    
    sidebar_html = "".join([f"<li><a href='{BLOG_BASE_URL}{h.get('file','')}' style='color:#334155; text-decoration:none;'>{h.get('title')[:25]}...</a></li>" for h in history[:10]])
    
    archive_name = f"post_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    history.insert(0, {"date": datetime.now().strftime("%Y-%m-%d"), "title": topic, "file": archive_name})
    
    with open(HISTORY_FILE, "w", encoding="utf-8") as f: json.dump(history, f, indent=4)
    generate_seo_files(history)
    
    full_html = create_final_html(topic, img_url, html_body, sidebar_html)
    with open("index.html", "w", encoding="utf-8") as f: f.write(full_html)
    with open(archive_name, "w", encoding="utf-8") as f: f.write(full_html)

if __name__ == "__main__": main()
