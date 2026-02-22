# Mavada Technologies Chat API - Hybrid Local KB + CodeWords AI
# Powered by IMPERIAL ENTERPRISE
# Local answers: FREE, instant. CodeWords AI: only for complex queries.

import os
import re
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path

app = FastAPI(title="Mavada Technologies Chat - Powered by IMPERIAL ENTERPRISE")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

CODEWORDS_API_KEY = os.environ.get("CODEWORDS_API_KEY", "")
CODEWORDS_SERVICE_ID = "mavada_chat_api_b4abe1f3"
CODEWORDS_BASE_URL = "https://runtime.codewords.ai"

# =============================================================
# LOCAL KNOWLEDGE BASE - Pre-built answers (FREE, no API calls)
# =============================================================
LOCAL_KB = [
    {
        "keywords": ["cost", "price", "how much", "affordable", "cheap", "budget", "ksh", "pricing", "expensive"],
        "response": "Great question! Our **Water ATMs start from KSh 100,000** depending on the model:\n\n- **Basic Manual Water ATMs** - From KSh 100,000\n- **Semi-Automatic Refill Stations** - From KSh 150,000 - 300,000\n- **Fully Automatic Smart ATMs (M-Pesa)** - From KSh 250,000+\n- **Chilled Water ATMs** - Premium pricing available\n\nWe offer **flexible financing, credit, and lease options** to make it easy to get started! Prices include quality filtration systems.\n\nReady for a personalized quote? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Water ATM Cost & Price Guide", "url": "https://mavadatechnologies.co.ke/water-atm-cost-kenya-vending-machine-price-guide/", "summary": "Complete pricing breakdown from basic to premium models."},
            {"title": "Basic Water ATM Price Guide", "url": "https://mavadatechnologies.co.ke/water-atm-cost-kenya-basic-vending-machine-price-guide/", "summary": "Basic water vending machine prices from KSh 100,000."},
            {"title": "Fully Automatic Smart Water ATM Guide", "url": "https://mavadatechnologies.co.ke/water-atm-price-kenya-fully-automatic-smart-vending-guide/", "summary": "Smart water ATMs with M-Pesa and advanced features."}
        ]
    },
    {
        "keywords": ["roi", "return on investment", "profit", "profitable", "earnings", "income", "money", "revenue", "earn"],
        "response": "Water ATMs are one of the **most profitable small businesses** in Kenya! Here's what to expect:\n\n- **ROI within 6-12 months** for most operators\n- **Monthly profit: KSh 30,000 - 100,000+** depending on location and model\n- **Low operating costs** - mainly electricity and water supply\n- **24/7 income** with unattended operation\n\nKey success factors: high-traffic location, M-Pesa integration, and good water quality. Many of our clients break even within the first year!\n\nWant to calculate your potential ROI? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Water ATM ROI & Profitability Analysis", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-roi-profitability-analysis/", "summary": "Comprehensive ROI analysis for water ATMs."},
            {"title": "Water ATM Investment & Profits", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-investment-profits/", "summary": "Water ATM investment and profit potential in Kenya."},
            {"title": "Start a Profitable Water ATM Business", "url": "https://mavadatechnologies.co.ke/start-profitable-water-atm-kenya-business/", "summary": "Guide to starting a profitable water ATM business."}
        ]
    },
    {
        "keywords": ["mpesa", "m-pesa", "mobile money", "payment", "cashless", "pay", "coin", "token", "smart card"],
        "response": "Yes! We offer **multiple payment options** for water ATMs:\n\n- **M-Pesa Integration** - Cashless mobile money payments (most popular!)\n- **Coin-Operated** - Accept coins and give change\n- **Tokens & Smart Cards** - Prepaid payment system\n- **Digital Payments** - Full cashless flexibility\n\nOur **Fully Automatic Smart ATMs** come with built-in M-Pesa, making transactions seamless for customers and easy tracking for owners.\n\nInterested in M-Pesa enabled machines? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Water ATM Payment Methods Guide", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-payment-methods-profit-guide/", "summary": "Payment methods including M-Pesa for water ATMs."},
            {"title": "Fully Automatic Smart Water ATM", "url": "https://mavadatechnologies.co.ke/water-atm-price-kenya-fully-automatic-smart-vending-guide/", "summary": "Smart ATMs with M-Pesa and cashless features."},
            {"title": "Tokens & Smart Cards for Water ATMs", "url": "https://mavadatechnologies.co.ke/tokens-smart-cards-water-atms-kenya-business-guide/", "summary": "Token and smart card payment systems."}
        ]
    },
    {
        "keywords": ["license", "licensing", "permit", "compliance", "regulation", "legal", "nema", "kebs", "government"],
        "response": "Great question about licensing! Here's what you need to start a water ATM business in Kenya:\n\n- **County Business Permit** - From your local county government\n- **NEMA Compliance** - Environmental impact assessment\n- **KEBS Certification** - Water quality standards\n- **Public Health Permit** - From the Ministry of Health\n\nDon't worry - **we help you with the entire licensing process!** Our team guides you through every permit and compliance requirement.\n\nNeed licensing support? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Water ATM Licensing & Compliance", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-licensing-help-suppliers/", "summary": "Licensing and compliance support for water ATMs."},
            {"title": "Water ATM Licensing Help", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-help-with-licensing-compliance/", "summary": "Essential permits and licensing requirements."}
        ]
    },
    {
        "keywords": ["install", "installation", "setup", "support", "maintenance", "after-sales", "technical", "service"],
        "response": "We provide **complete installation and after-sales support:**\n\n- **Free installation** on all water ATM purchases\n- **Technical setup** - plumbing, electrical, water connections\n- **Staff training** on operation and maintenance\n- **After-sales support** - ongoing technical assistance\n- **Warranty coverage** on all machines\n- **Maintenance guidance** and spare parts supply\n\nYou're never alone - our support team is always a call away!\n\nReady to get installed? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Water ATM Installation Support", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-installation-support/", "summary": "Installation and support services."},
            {"title": "Water ATM Installation for Success", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-installation-support-for-success/", "summary": "Complete installation and after-sales support."}
        ]
    },
    {
        "keywords": ["finance", "financing", "credit", "lease", "loan", "payment plan", "installment", "afford", "pay slowly"],
        "response": "We make water ATMs **accessible to everyone** with flexible financing:\n\n- **Credit Options** - Buy now, pay in installments\n- **Lease Programs** - Low monthly payments to get started\n- **Payment Plans** - Spread your investment over time\n- **Flexible Terms** - Customized to your budget\n\nDon't let budget hold you back - we'll find a plan that works for you!\n\nDiscuss financing options? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Water ATM Credit & Lease Options", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-credit-lease-options/", "summary": "Credit and lease financing options."},
            {"title": "Water ATM Credit & Lease for Business", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-credit-lease-options-for-your-business/", "summary": "Flexible financing for water ATM businesses."}
        ]
    },
    {
        "keywords": ["location", "placement", "where to place", "position", "site", "strategic", "best place", "traffic"],
        "response": "**Location is everything** for water ATM profitability! Best spots include:\n\n- **High foot traffic areas** - bus stops, markets, shopping centers\n- **Residential estates** - apartment blocks, housing developments\n- **Near schools and hospitals** - guaranteed daily demand\n- **Industrial areas** - workers need clean water\n- **Along busy roads** - easy access for passersby\n\nWe help you **choose the perfect location** based on population density and competition analysis!\n\nNeed placement advice? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Strategic Water ATM Placement Guide", "url": "https://mavadatechnologies.co.ke/strategic-water-atm-kenya-placement-location-guide/", "summary": "Strategic placement and location guide."},
            {"title": "Water ATM Placement Strategy", "url": "https://mavadatechnologies.co.ke/strategic-water-atm-kenya-placement/", "summary": "Placement strategy for maximum profit."}
        ]
    },
    {
        "keywords": ["semi-automatic", "semi automatic", "refill station", "manual", "mid-range", "basic machine"],
        "response": "**Semi-Automatic Water Refill Stations** are perfect for budget-conscious entrepreneurs:\n\n- **Price range: KSh 150,000 - 300,000**\n- Manual operation with quality filtration\n- Great for high-traffic community areas\n- Lower operating costs than fully automatic\n- **Stainless steel construction** for durability\n- Easy to maintain and operate\n- Solar power compatible for off-grid locations\n\nIdeal starter option with excellent ROI!\n\nGet a quote? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Semi-Automatic Refill Station Guide", "url": "https://mavadatechnologies.co.ke/semi-automatic-water-refill-station-kenya/", "summary": "Overview of semi-automatic refill stations."},
            {"title": "Semi-Automatic Refill Station Profit Guide", "url": "https://mavadatechnologies.co.ke/semi-automatic-water-refill-station-kenya-your-profit-guide/", "summary": "Profit guide for semi-automatic stations."},
            {"title": "Semi-Automatic Solar Guide", "url": "https://mavadatechnologies.co.ke/semi-automatic-water-refill-station-kenya-solar-profit-guide/", "summary": "Solar-powered refill station guide."}
        ]
    },
    {
        "keywords": ["quality", "purification", "filter", "ro", "uv", "reverse osmosis", "tds", "ph", "monitoring", "testing", "clean", "safe"],
        "response": "Water quality is our **top priority!** Our ATMs feature:\n\n- **RO (Reverse Osmosis)** - Removes 99% of impurities\n- **UV Sterilization** - Kills bacteria and viruses\n- **Real-time TDS & pH Monitoring** - Continuous quality tracking\n- **Anti-contamination Nozzles** - Hygienic dispensing\n- **Multi-stage Filtration** - Multiple purification levels\n\nAll our machines meet **KEBS water quality standards** for safe drinking water!\n\nLearn more? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Water ATM RO & UV Purification", "url": "https://mavadatechnologies.co.ke/water-atms-in-kenya-ro-uv-refill-stations/", "summary": "RO and UV purification systems."},
            {"title": "Real-Time Water Quality Monitoring", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-real-time-quality-monitoring-guide/", "summary": "Real-time water quality monitoring systems."},
            {"title": "Anti-Contamination Nozzles", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-anti-contamination-nozzles-profit-guide/", "summary": "Anti-contamination nozzle technology."}
        ]
    },
    {
        "keywords": ["brand", "branding", "logo", "design", "custom", "color", "wrap", "customize"],
        "response": "Make your water ATM **stand out** with custom branding!\n\n- **Custom Color Wraps** - Match your brand colors\n- **Logo Printing** - Your business name and logo on the machine\n- **Full Custom Design** - Completely personalized look\n- **Free branding** on select models this month!\n\nProfessional branding builds trust and attracts more customers.\n\nGet branded? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Branding Water ATMs Kenya", "url": "https://mavadatechnologies.co.ke/branding-water-atms-kenya-boost-business-profits/", "summary": "Custom branding solutions for water ATMs."},
            {"title": "Branding Water ATMs", "url": "https://mavadatechnologies.co.ke/branding-water-atms-kenya/", "summary": "Custom branding for water ATMs."}
        ]
    },
    {
        "keywords": ["supplier", "buy", "where to buy", "purchase", "order", "dealer", "seller", "who sells", "nairobi", "mombasa"],
        "response": "**Mavada Technologies** is Kenya's #1 water ATM supplier! We serve **nationwide:**\n\n- **Nairobi** - Our main office and showroom\n- **Mombasa** - Coastal region coverage\n- **Kisumu, Nakuru, Eldoret** - Western and Rift Valley\n- **All 47 counties** - Delivery anywhere in Kenya!\n\nWhy choose Mavada?\n- Direct manufacturer prices\n- Free installation nationwide\n- After-sales support\n- Financing available\n\nOrder now! WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Top Water ATM Suppliers in Kenya", "url": "https://mavadatechnologies.co.ke/top-water-atm-suppliers-in-kenya/", "summary": "Guide to Kenya's top water ATM suppliers."},
            {"title": "Water ATM Suppliers Nairobi & Mombasa", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-nairobi-mombasa/", "summary": "Suppliers in Nairobi and Mombasa."},
            {"title": "Water ATM Suppliers Beyond Nairobi", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-beyond-nairobi/", "summary": "Nationwide coverage beyond Nairobi."}
        ]
    },
    {
        "keywords": ["start", "starting", "begin", "new business", "startup", "entrepreneur", "invest", "how to start", "business"],
        "response": "Starting a water ATM business is **simple and profitable!** Here's how:\n\n1. **Choose your machine** - Basic (KSh 100K+) or Automatic (KSh 250K+)\n2. **Find a location** - High-traffic area with water access\n3. **Get permits** - We help with licensing!\n4. **Installation** - Free setup by our team\n5. **Start earning!** - ROI typically within 6-12 months\n\n**Why water ATMs?**\n- Growing demand for clean water in Kenya\n- Low competition in many areas\n- Passive income - machines work 24/7\n- Social impact - providing clean water to communities\n\nReady to start? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Start a Profitable Water ATM Business", "url": "https://mavadatechnologies.co.ke/start-profitable-water-atm-kenya-business/", "summary": "Guide to starting a profitable water ATM business."},
            {"title": "Start Your Profitable Business", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-price-guide-start-your-profitable-business/", "summary": "Price guide for starting your business."},
            {"title": "Comprehensive Water ATM Guide", "url": "https://mavadatechnologies.co.ke/comprehensive-buyers-guide-water-atm-kenya-solutions/", "summary": "Complete buyer's guide to water ATMs."}
        ]
    },
    {
        "keywords": ["chilled", "cold", "cold water", "cooling", "refrigerated", "ice"],
        "response": "**Chilled Water ATMs** are a premium offering with **higher profit margins!**\n\n- Dispenses cold, refreshing water\n- Perfect for hot climate areas (Mombasa, Nairobi CBD)\n- Commands **premium pricing** per liter\n- Higher customer satisfaction and loyalty\n- Built-in cooling system\n\nChilled water ATMs attract more customers and justify higher prices!\n\nGet chilled water ATM pricing? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Chilled Water ATMs Kenya", "url": "https://mavadatechnologies.co.ke/chilled-water-atms-in-kenya-profitable-business-guide/", "summary": "Chilled water ATMs for premium market niche."}
        ]
    },
    {
        "keywords": ["tank", "tank size", "capacity", "liters", "litres", "storage", "volume"],
        "response": "Choosing the right **tank size** is important for your business:\n\n- **500L tanks** - Great for low-traffic areas, small shops\n- **1,000L tanks** - Most popular, balanced choice\n- **2,000L tanks** - High-traffic locations, estates\n- **5,000L+ tanks** - Industrial areas, bulk vending\n\nWe help you choose based on your location's daily demand and water supply schedule.\n\nNeed advice on tank size? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Water ATM Tank Sizes Guide", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-tank-sizes-business-profit-guide/", "summary": "Choosing the right water ATM tank sizes."}
        ]
    },
    {
        "keywords": ["warranty", "guarantee", "after-sales", "coverage", "repair", "break", "broken"],
        "response": "All Mavada water ATMs come with **warranty and after-sales support:**\n\n- **Manufacturer warranty** on all machines\n- **Free technical support** via phone and WhatsApp\n- **Spare parts** readily available\n- **Repair services** by trained technicians\n- **Maintenance training** included with purchase\n\nYour investment is protected!\n\nWarranty questions? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Water ATM Warranty Guide", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-warranty-your-guide-to-a-profitable-business/", "summary": "Warranty and after-sales service guide."}
        ]
    },
    {
        "keywords": ["hello", "hi", "hey", "karibu", "good morning", "good afternoon", "good evening", "jambo", "habari"],
        "response": "Karibu! Welcome to **Mavada Technologies** - Kenya's #1 Water ATM supplier! I'm here to help you with everything about water vending machines.\n\nI can help you with:\n- **Pricing** - Water ATMs from KSh 100,000\n- **ROI & Profitability** - Earn KSh 30K-100K+ monthly\n- **M-Pesa Integration** - Cashless payment options\n- **Financing** - Credit and lease available\n- **Installation** - Free nationwide setup\n- **Licensing** - We handle permits for you\n\nWhat would you like to know? Or WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Water Vending Machines Kenya", "url": "https://mavadatechnologies.co.ke/water-vending-machines-kenya/", "summary": "Overview of all water vending machines."},
            {"title": "Water ATM Kenya Overview", "url": "https://mavadatechnologies.co.ke/water-atm-kenya/", "summary": "Complete overview of water ATM solutions."}
        ]
    },
    {
        "keywords": ["delivery", "deliver", "ship", "shipping", "transport", "nationwide", "county", "kisumu", "nakuru", "eldoret", "meru", "thika"],
        "response": "Yes! We deliver **nationwide across all 47 counties** in Kenya!\n\n- **Nairobi** - Same day/next day delivery\n- **Mombasa, Kisumu, Nakuru, Eldoret** - 2-3 business days\n- **All other counties** - 3-5 business days\n- **Free delivery** on select orders!\n\nNo matter where you are, we'll get your water ATM to you.\n\nOrder now! WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Water ATM Suppliers Beyond Nairobi", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-beyond-nairobi/", "summary": "Nationwide coverage beyond Nairobi."}
        ]
    },
    {
        "keywords": ["solar", "off-grid", "no electricity", "power", "energy", "rural"],
        "response": "Water ATMs can work **even without grid electricity!**\n\n- **Solar-powered options** available for off-grid locations\n- Perfect for **rural areas** without reliable power\n- Lower operating costs with solar\n- Eco-friendly and sustainable\n- Semi-automatic stations work great with solar\n\nSolar water ATMs open up profitable opportunities in underserved areas!\n\nSolar options? WhatsApp us at **0758 281922**!",
        "blogs": [
            {"title": "Semi-Automatic Solar Guide", "url": "https://mavadatechnologies.co.ke/semi-automatic-water-refill-station-kenya-solar-profit-guide/", "summary": "Solar-powered semi-automatic refill station guide."}
        ]
    },
]


def find_local_answer(question):
    """Match question to local KB using keyword scoring."""
    q = question.lower()
    best_match = None
    best_score = 0

    for entry in LOCAL_KB:
        score = 0
        for kw in entry["keywords"]:
            if kw.lower() in q:
                # Exact phrase match scores higher
                score += 2 if len(kw.split()) > 1 else 1
        if score > best_score:
            best_score = score
            best_match = entry

    # Need at least 1 keyword match
    if best_score >= 1 and best_match:
        return best_match
    return None


# =============================================================
# SERVE FRONTEND
# =============================================================
_html_cache = None

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    global _html_cache
    if _html_cache is None:
        html_path = Path(__file__).parent / "chat.html"
        if html_path.exists():
            _html_cache = html_path.read_text()
        else:
            _html_cache = "<h1>Mavada Technologies Chat</h1><p>UI not found.</p>"
    return HTMLResponse(content=_html_cache)


# =============================================================
# CHAT ENDPOINT - Local first, CodeWords AI for complex queries
# =============================================================
@app.post("/")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")
    session_id = body.get("session_id", "")

    # Step 1: Try LOCAL knowledge base first (FREE, instant)
    local_match = find_local_answer(message)
    if local_match:
        return JSONResponse(content={
            "success": True,
            "response": local_match["response"],
            "blog_links": local_match["blogs"],
            "session_id": session_id or "local",
            "show_agent_option": False
        })

    # Step 2: Fall back to CodeWords AI for complex/unmatched queries
    if CODEWORDS_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{CODEWORDS_BASE_URL}/run/{CODEWORDS_SERVICE_ID}/",
                    headers={"Authorization": f"Bearer {CODEWORDS_API_KEY}", "Content-Type": "application/json"},
                    json=body
                )
                if response.status_code == 200:
                    return JSONResponse(content=response.json())
        except Exception:
            pass

    # Step 3: Fallback if nothing works
    return JSONResponse(content={
        "success": True,
        "response": "Thanks for your question! For the best answer, please **WhatsApp us at 0758 281922** or call us directly - our team is ready to help!\n\nYou can also browse our website at [mavadatechnologies.co.ke](https://mavadatechnologies.co.ke) for detailed information.",
        "blog_links": [
            {"title": "Water Vending Machines Kenya", "url": "https://mavadatechnologies.co.ke/water-vending-machines-kenya/", "summary": "Overview of all water vending machines."},
            {"title": "Water ATM Kenya Overview", "url": "https://mavadatechnologies.co.ke/water-atm-kenya/", "summary": "Complete overview of water ATM solutions."}
        ],
        "session_id": session_id or "fallback",
        "show_agent_option": True
    })


@app.post("/submit_lead")
async def submit_lead(request: Request):
    body = await request.json()
    if CODEWORDS_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{CODEWORDS_BASE_URL}/run/{CODEWORDS_SERVICE_ID}/submit_lead",
                    headers={"Authorization": f"Bearer {CODEWORDS_API_KEY}", "Content-Type": "application/json"},
                    json=body
                )
                if response.status_code == 200:
                    return JSONResponse(content=response.json())
        except Exception:
            pass
    return JSONResponse(content={"success": True, "message": "Thank you! Call us at 0758 281922."})


@app.get("/health")
async def health():
    return {"status": "ok", "local_kb_entries": len(LOCAL_KB), "powered_by": "IMPERIAL ENTERPRISE"}
