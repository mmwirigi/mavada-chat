# Mavada Technologies Chat API
# Powered by IMPERIAL ENTERPRISE

from dotenv import load_dotenv
load_dotenv()

import json
import uuid
from datetime import datetime, timezone

import logging
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from openai import AsyncOpenAI
from pydantic import BaseModel, Field

# =========================================
# MAVADA TECHNOLOGIES FULL BLOG KNOWLEDGE BASE (123 entries)
# =========================================
BLOG_KB = [
    # === BEVERAGE CHILLERS ===
    {"title": "Choose & Use Your Beverage Chiller in Kenya", "url": "https://mavadatechnologies.co.ke/choose-use-your-beverage-chiller-in-kenya-guide/", "keywords": ["beverage chiller", "chiller", "cold drinks", "cooler", "choose"], "summary": "Guide to choosing and using beverage chillers in Kenya."},
    {"title": "Choosing the Best Beverage Chiller Kenya", "url": "https://mavadatechnologies.co.ke/choosing-best-beverage-chiller-kenya-guide/", "keywords": ["best chiller", "beverage chiller", "top chiller", "comparison", "best"], "summary": "How to choose the best beverage chiller in Kenya."},
    {"title": "Mastering Your Beverage Chiller Kenya", "url": "https://mavadatechnologies.co.ke/mastering-your-beverage-chiller-kenya-buyers-guide/", "keywords": ["beverage chiller", "buyers guide", "chiller tips", "mastering"], "summary": "Buyer's guide to mastering beverage chiller selection."},
    {"title": "Choosing & Using Beverage Chiller Kenya", "url": "https://mavadatechnologies.co.ke/choosing-using-beverage-chiller-kenya/", "keywords": ["beverage chiller", "using chiller", "how to use", "operation"], "summary": "Guide on choosing and operating beverage chillers."},
    {"title": "Choose Your Ideal Beverage Chiller Kenya", "url": "https://mavadatechnologies.co.ke/choose-use-ideal-beverage-chiller-kenya/", "keywords": ["ideal chiller", "beverage chiller", "perfect fit", "selection"], "summary": "Finding the ideal beverage chiller for your business."},
    {"title": "Optimize Your Beverage Chiller Kenya", "url": "https://mavadatechnologies.co.ke/optimize-your-chill-beverage-chiller-kenya/", "keywords": ["optimize", "beverage chiller", "efficiency", "performance"], "summary": "Tips for optimizing beverage chiller performance."},
    {"title": "Choosing Your Ideal Beverage Chiller", "url": "https://mavadatechnologies.co.ke/choosing-your-ideal-beverage-chiller-in-kenya/", "keywords": ["ideal", "beverage chiller", "selection guide", "kenya"], "summary": "Complete guide to selecting your ideal beverage chiller."},
    {"title": "Beverage Chiller Kenya ROI Analysis", "url": "https://mavadatechnologies.co.ke/beverage-chiller-kenya-roi-profitability-analysis/", "keywords": ["roi", "profitability", "beverage chiller", "return on investment", "profit"], "summary": "ROI and profitability analysis for beverage chillers."},
    {"title": "Beverage Chiller Kenya ROI Guide 2024", "url": "https://mavadatechnologies.co.ke/beverage-chiller-kenya-roi-profitability-analysis-2024/", "keywords": ["roi 2024", "beverage chiller", "profitability", "investment"], "summary": "2024 ROI analysis for beverage chiller investments."},
    {"title": "Best Beverage Chiller Options Kenya", "url": "https://mavadatechnologies.co.ke/best-beverage-chiller-options-kenya-expert-guide-prices/", "keywords": ["best options", "beverage chiller", "prices", "expert guide", "price"], "summary": "Expert guide to best beverage chiller options and prices."},
    {"title": "Best Beverage Chiller Expert Guide", "url": "https://mavadatechnologies.co.ke/best-beverage-chiller-in-kenya-expert-guide/", "keywords": ["expert guide", "beverage chiller", "best", "review"], "summary": "Expert review of the best beverage chillers in Kenya."},
    # === MILK & DAIRY ===
    {"title": "Milk Pasteurizer Kenya Buyer's Guide", "url": "https://mavadatechnologies.co.ke/milk-pasteurizer-kenya-buyers-guide/", "keywords": ["milk", "pasteurizer", "dairy", "buyers guide", "pasteurization"], "summary": "Complete buyer's guide for milk pasteurizers in Kenya."},
    {"title": "Milk Pasteurizer Kenya ROI Analysis", "url": "https://mavadatechnologies.co.ke/milk-pasteurizer-kenya-roi-profit-analysis/", "keywords": ["milk pasteurizer", "roi", "profit", "dairy business", "return on investment"], "summary": "ROI and profit analysis for milk pasteurizer investments."},
    {"title": "Milk Analysers: Dairy Quality Testers", "url": "https://mavadatechnologies.co.ke/milk-analysers-fast-accurate-dairy-quality-testers/", "keywords": ["milk analyser", "dairy testing", "quality tester", "milk quality", "analyzer"], "summary": "Fast and accurate milk analysers for dairy quality testing."},
    # === SALAD OIL / COOKING OIL ===
    {"title": "Salad Oil ATM Cost Kenya", "url": "https://mavadatechnologies.co.ke/salad-atm-cost-kenya/", "keywords": ["salad oil", "oil atm", "cost", "price", "salad oil atm"], "summary": "Salad oil ATM pricing and cost guide for Kenya."},
    {"title": "Top 7 Benefits of Salad Oil ATM", "url": "https://mavadatechnologies.co.ke/top-7-benefits-salad-oil-atm-retail-shop/", "keywords": ["salad oil", "benefits", "oil atm", "retail shop", "advantages"], "summary": "Top 7 benefits of adding a salad oil ATM to your retail shop."},
    {"title": "Where to Buy Salad Oil ATM Kenya", "url": "https://mavadatechnologies.co.ke/where-to-buy-reliable-salad-oil-atm-machine-in-kenya/", "keywords": ["buy", "salad oil atm", "where to buy", "reliable", "oil machine"], "summary": "Where to buy reliable salad oil ATM machines in Kenya."},
    {"title": "Cooking Oil ATM Dispensers Kenya", "url": "https://mavadatechnologies.co.ke/cooking-oil-atm-dispensers-revolutionizing-small-businesses-kenya/", "keywords": ["cooking oil", "oil dispenser", "oil atm", "small business", "oil vending"], "summary": "How cooking oil ATM dispensers are revolutionizing small businesses."},
    # === PHARMACEUTICAL ===
    {"title": "Pharmaceutical Equipment Kenya ROI", "url": "https://mavadatechnologies.co.ke/pharmaceutical-equipment-kenya-maximize-roi-profitability/", "keywords": ["pharmaceutical", "pharma equipment", "roi", "medical", "profitability"], "summary": "Maximizing ROI with pharmaceutical equipment in Kenya."},
    # === WATER ATM PLACEMENT & STRATEGY ===
    {"title": "Strategic Water ATM Placement Guide", "url": "https://mavadatechnologies.co.ke/strategic-water-atm-kenya-placement-location-guide/", "keywords": ["placement", "location", "strategic", "where to place", "water atm", "site"], "summary": "Strategic placement and location guide for water ATMs."},
    {"title": "Water ATM Kenya Placement Strategy", "url": "https://mavadatechnologies.co.ke/strategic-water-atm-kenya-placement/", "keywords": ["placement", "strategy", "water atm", "location", "position"], "summary": "Water ATM placement strategy for maximum profit."},
    # === WATER ATM SUPPLIERS & DEALERS ===
    {"title": "Water ATM Suppliers & Prices Kenya", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-prices-where-to-buy/", "keywords": ["supplier", "price", "where to buy", "water atm", "dealers"], "summary": "Water ATM suppliers, prices, and where to buy in Kenya."},
    {"title": "Water ATM Suppliers Nairobi & Mombasa", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-nairobi-mombasa/", "keywords": ["nairobi", "mombasa", "supplier", "water atm", "dealers"], "summary": "Water ATM suppliers in Nairobi and Mombasa."},
    {"title": "Best Water ATM Dealers Nairobi", "url": "https://mavadatechnologies.co.ke/best-water-atm-dealers-nairobi/", "keywords": ["best dealers", "nairobi", "water atm", "top dealers", "buy"], "summary": "Best water ATM dealers in Nairobi."},
    {"title": "Water ATM Kenya: Prices & Top Suppliers", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-buy-prices-top-suppliers-nairobi/", "keywords": ["price", "top suppliers", "nairobi", "water atm", "buy"], "summary": "Prices and top water ATM suppliers in Nairobi."},
    {"title": "Water ATM Suppliers Prices Buying Guide", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-prices-buying-guide/", "keywords": ["buying guide", "supplier", "price", "water atm", "how to buy"], "summary": "Complete buying guide for water ATM suppliers and prices."},
    {"title": "Water ATM Buy Suppliers & Dealers", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-buy-suppliers-dealers/", "keywords": ["buy", "supplier", "dealer", "water atm", "purchase"], "summary": "Where to buy water ATMs from suppliers and dealers."},
    {"title": "Water ATM Suppliers & Prices Guide", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-prices-guide/", "keywords": ["supplier", "price", "guide", "water atm", "comparison"], "summary": "Water ATM suppliers and pricing guide."},
    {"title": "Water ATM Suppliers Prices Nairobi Mombasa", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-prices-nairobi-mombasa/", "keywords": ["nairobi", "mombasa", "supplier", "price", "water atm"], "summary": "Water ATM supplier prices in Nairobi and Mombasa."},
    {"title": "Find Water ATM Dealers & Locations", "url": "https://mavadatechnologies.co.ke/find-water-atm-kenya-dealers-prices-locations/", "keywords": ["find", "dealer", "location", "water atm", "price"], "summary": "Find water ATM dealers, prices, and locations in Kenya."},
    {"title": "Water ATM Suppliers Buy Kenya", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-buy-nairobi-mombasa/", "keywords": ["buy", "supplier", "nairobi", "mombasa", "water atm"], "summary": "Buy water ATMs from suppliers in Nairobi and Mombasa."},
    {"title": "Water ATM Kenya Best Dealers Nairobi", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-best-dealers-prices-nairobi/", "keywords": ["best dealers", "nairobi", "price", "water atm", "supplier"], "summary": "Best water ATM dealers and prices in Nairobi."},
    {"title": "Water ATM Top Suppliers Buying Guide", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-top-suppliers-buying-guide/", "keywords": ["top suppliers", "buying guide", "water atm", "best", "comparison"], "summary": "Top water ATM suppliers and comprehensive buying guide."},
    {"title": "Top Water ATM Suppliers in Kenya", "url": "https://mavadatechnologies.co.ke/top-water-atm-suppliers-in-kenya/", "keywords": ["top suppliers", "best", "water atm", "compare", "supplier"], "summary": "Guide to Kenya's top water ATM suppliers."},
    {"title": "Water ATM Suppliers Beyond Nairobi", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-beyond-nairobi/", "keywords": ["mombasa", "kisumu", "nakuru", "eldoret", "rural", "nationwide"], "summary": "Water ATM suppliers and coverage beyond Nairobi."},
    {"title": "Buy Water ATM Machines in Nairobi", "url": "https://mavadatechnologies.co.ke/buy-water-atm-machines-in-nairobi/", "keywords": ["buy", "nairobi", "purchase", "order", "water atm"], "summary": "How to buy water ATM machines in Nairobi."},
    # === WATER ATM ROI & PROFITABILITY ===
    {"title": "Water ATM Kenya ROI Analysis 2024", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-roi-profitability-analysis-2024/", "keywords": ["roi", "profitability", "2024", "return on investment", "water atm"], "summary": "2024 ROI and profitability analysis for water ATMs."},
    {"title": "Water ATM Kenya ROI Guide 2024", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-roi-profitability-guide-2024/", "keywords": ["roi guide", "profitability", "2024", "water atm", "profit"], "summary": "2024 guide to water ATM ROI and profitability."},
    {"title": "Water ATM Kenya Expert Price Comparison", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-expert-comparison-prices-2024/", "keywords": ["comparison", "price", "expert", "2024", "water atm", "compare"], "summary": "Expert comparison of water ATM prices in 2024."},
    {"title": "Water ATM Kenya Investment & Profits", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-investment-profits/", "keywords": ["investment", "profit", "earnings", "water atm", "roi"], "summary": "Water ATM investment and profit potential in Kenya."},
    {"title": "Water ATM Buyers Guide: Prices 2024", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-buyers-guide-prices-suppliers-2024/", "keywords": ["buyers guide", "price", "2024", "supplier", "water atm"], "summary": "2024 buyer's guide with prices and suppliers."},
    {"title": "Water ATM Kenya Profitability & ROI", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-profitability-roi/", "keywords": ["profitability", "roi", "earnings", "water atm", "income"], "summary": "Water ATM profitability and ROI analysis."},
    {"title": "Water ATM ROI & Profitability Analysis", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-roi-profitability-analysis/", "keywords": ["roi", "analysis", "profitability", "water atm", "return"], "summary": "Comprehensive ROI and profitability analysis for water ATMs."},
    # === WATER ATM GENERAL / BUYERS GUIDES ===
    {"title": "Water ATM Kenya Overview", "url": "https://mavadatechnologies.co.ke/water-atm-kenya/", "keywords": ["water atm", "kenya", "overview", "water vending", "water machine"], "summary": "Complete overview of water ATM solutions in Kenya."},
    {"title": "Comprehensive Water ATM Kenya Guide", "url": "https://mavadatechnologies.co.ke/comprehensive-buyers-guide-water-atm-kenya-solutions/", "keywords": ["comprehensive guide", "water atm", "solutions", "buyers guide"], "summary": "Comprehensive buyer's guide to water ATM solutions."},
    {"title": "Water ATM Investment Roadmap", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-buyers-guide-investment-roadmap/", "keywords": ["investment", "roadmap", "water atm", "guide", "plan"], "summary": "Water ATM investment roadmap and buyer's guide."},
    {"title": "Water ATM Buyers Guide: Features", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-buyers-guide-prices-features/", "keywords": ["features", "price", "buyers guide", "water atm", "specifications"], "summary": "Water ATM buyer's guide with prices and features."},
    {"title": "Water ATM Buyers Guide 2024", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-buyers-guide-2024/", "keywords": ["buyers guide", "2024", "water atm", "how to buy", "guide"], "summary": "2024 buyer's guide for water ATMs in Kenya."},
    {"title": "Start a Profitable Water ATM Business", "url": "https://mavadatechnologies.co.ke/start-profitable-water-atm-kenya-business/", "keywords": ["start", "startup", "new business", "entrepreneur", "invest", "profit", "water atm"], "summary": "Guide to starting a profitable water ATM business."},
    {"title": "Water Vending Machine Kenya Guide", "url": "https://mavadatechnologies.co.ke/water-vending-machine-kenya-guide/", "keywords": ["water vending", "vending machine", "guide", "water atm", "overview"], "summary": "Complete guide to water vending machines in Kenya."},
    {"title": "Water Vending Machine Suppliers & Prices", "url": "https://mavadatechnologies.co.ke/water-vending-machine-kenya-suppliers-prices-where-to-buy/", "keywords": ["vending machine", "supplier", "price", "where to buy", "water vending"], "summary": "Water vending machine suppliers and prices."},
    # === WATER ATM PRICING ===
    {"title": "Water ATM Cost & Price Guide", "url": "https://mavadatechnologies.co.ke/water-atm-cost-kenya-vending-machine-price-guide/", "keywords": ["cost", "price", "how much", "affordable", "budget", "ksh", "water atm"], "summary": "Water ATM cost and pricing guide."},
    {"title": "Smart Water ATM Price Guide", "url": "https://mavadatechnologies.co.ke/water-atm-price-kenya-smart-vending-guide/", "keywords": ["smart", "automatic", "price", "mpesa", "cashless", "premium", "water atm"], "summary": "Smart and fully automatic water ATM pricing guide."},
    {"title": "Semi-Automatic Water ATM Price Guide", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-price-semi-automatic-guide/", "keywords": ["semi-automatic", "price", "mid-range", "refill station", "water atm"], "summary": "Semi-automatic water ATM pricing guide."},
    {"title": "Water ATM Kenya Price Guide", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-price-guide/", "keywords": ["price", "cost", "guide", "water atm", "how much", "pricing"], "summary": "Complete water ATM pricing guide for Kenya."},
    {"title": "Water ATM Machine Price & Profit Guide", "url": "https://mavadatechnologies.co.ke/water-atm-machine-kenya-price-profit-guide/", "keywords": ["price", "profit", "machine", "water atm", "cost", "earnings"], "summary": "Water ATM machine pricing and profit potential guide."},
    # === WATER ATM FEATURES & TECH ===
    {"title": "Water ATM Accurate Measurement", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-accurate-measurement-vending-success/", "keywords": ["measurement", "accurate", "dispensing", "volume", "water atm"], "summary": "Accurate water measurement for vending success."},
    {"title": "Branding Water ATMs Kenya", "url": "https://mavadatechnologies.co.ke/branding-water-atms-kenya-boost-business-profits/", "keywords": ["branding", "brand", "logo", "design", "custom", "wrap", "water atm"], "summary": "Custom branding solutions for water ATMs."},
    {"title": "Water ATM Tank Sizes Guide", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-tank-sizes-business-profit-guide/", "keywords": ["tank", "tank size", "capacity", "liters", "storage", "water atm"], "summary": "Choosing the right water ATM tank sizes."},
    {"title": "Anti-Contamination Nozzles", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-anti-contamination-nozzles-profit-guide/", "keywords": ["nozzle", "contamination", "hygiene", "safety", "health", "water atm"], "summary": "Anti-contamination nozzle technology for water ATMs."},
    {"title": "Chilled Water ATMs Kenya", "url": "https://mavadatechnologies.co.ke/chilled-water-atms-in-kenya-profitable-business-guide/", "keywords": ["chilled", "cold water", "cooling", "refrigerated", "cold", "water atm"], "summary": "Chilled water ATMs for premium market niche."},
    {"title": "Water ATM Quality Safeguarding", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-safeguarding-quality-profit/", "keywords": ["quality", "safety", "safeguarding", "water atm", "standards"], "summary": "Safeguarding water quality for profitable operations."},
    {"title": "Real-Time Water Quality Monitoring", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-real-time-quality-monitoring-guide/", "keywords": ["monitoring", "quality", "TDS", "pH", "sensor", "real-time", "water atm"], "summary": "Real-time water quality monitoring systems."},
    {"title": "Coin & Change Water ATMs Kenya", "url": "https://mavadatechnologies.co.ke/water-atms-coins-change-kenya-refill-station-profits/", "keywords": ["coin", "cash", "coin-operated", "change", "payment", "water atm"], "summary": "Coin-operated water ATMs and payment systems."},
    {"title": "Stainless Steel Water ATMs", "url": "https://mavadatechnologies.co.ke/stainless-steel-water-atms-semi-automatic-kenya/", "keywords": ["stainless steel", "durable", "material", "steel", "water atm"], "summary": "Stainless steel water ATMs for maximum durability."},
    {"title": "Tokens & Smart Cards for Water ATMs", "url": "https://mavadatechnologies.co.ke/tokens-smart-cards-water-atms-kenya-business-guide/", "keywords": ["token", "smart card", "prepaid", "cashless", "payment", "water atm"], "summary": "Token and smart card payment systems for water ATMs."},
    {"title": "Water ATM Digital Flexibility", "url": "https://mavadatechnologies.co.ke/water-atm-digital-flexibility-kenya/", "keywords": ["digital", "smart", "technology", "remote", "app", "water atm"], "summary": "Digital flexibility and smart features for water ATMs."},
    {"title": "Water ATM 24/7 Operation Guide", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-24-7-operation-profit-guide/", "keywords": ["24/7", "round the clock", "unattended", "continuous", "water atm"], "summary": "Guide to running water ATMs 24/7 for maximum profit."},
    {"title": "Water ATM Lifespan & Durability", "url": "https://mavadatechnologies.co.ke/water-atm-lifespan-profit-guide-kenya/", "keywords": ["lifespan", "durability", "how long", "years", "lifetime", "water atm"], "summary": "Water ATM lifespan and durability guide."},
    {"title": "Water Refill Station Cleaning Guide", "url": "https://mavadatechnologies.co.ke/water-refill-station-cleaning-kenya-profit-guide/", "keywords": ["cleaning", "sanitize", "hygiene", "maintenance", "wash", "refill station"], "summary": "Cleaning and maintenance guide for water refill stations."},
    {"title": "Water Vending Machine Materials", "url": "https://mavadatechnologies.co.ke/water-vending-machine-materials-kenya/", "keywords": ["materials", "construction", "build", "components", "parts", "water atm"], "summary": "Materials and construction of water vending machines."},
    {"title": "Water ATM Dispense Time & Costs", "url": "https://mavadatechnologies.co.ke/water-atm-dispense-time-kenya-refill-station-costs/", "keywords": ["dispense time", "flow rate", "speed", "cost", "refill station"], "summary": "Water ATM dispensing time and operational costs."},
    {"title": "Water ATM Payment Methods Guide", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-payment-methods-profit-guide/", "keywords": ["payment", "mpesa", "m-pesa", "cashless", "mobile money", "water atm"], "summary": "Payment methods for water ATMs including M-Pesa."},
    {"title": "Water ATM RO & UV Purification", "url": "https://mavadatechnologies.co.ke/water-atms-in-kenya-ro-uv-refill-stations/", "keywords": ["ro", "uv", "reverse osmosis", "purification", "filter", "water atm"], "summary": "RO and UV purification systems for water ATMs."},
    {"title": "Water Purification Refill Stations", "url": "https://mavadatechnologies.co.ke/water-purification-semi-automatic-refill-stations-kenya/", "keywords": ["purification", "filter", "clean water", "refill station", "semi-automatic"], "summary": "Water purification semi-automatic refill stations."},
    {"title": "Water Vending Machine Types Kenya", "url": "https://mavadatechnologies.co.ke/water-vending-machine-types-kenya-semi-auto-business-guide/", "keywords": ["types", "models", "options", "comparison", "range", "water atm"], "summary": "Types and models of water vending machines in Kenya."},
    # === WATER ATM WARRANTY, LICENSING, INSTALLATION ===
    {"title": "Water ATM Warranty Guide", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-warranty-your-guide-to-a-profitable-business/", "keywords": ["warranty", "guarantee", "after-sales", "service", "coverage", "water atm"], "summary": "Water ATM warranty and after-sales service guide."},
    {"title": "Water ATM Credit & Lease Options", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-credit-lease-options/", "keywords": ["credit", "lease", "financing", "loan", "payment plan", "installment", "water atm"], "summary": "Credit and lease financing options for water ATMs."},
    {"title": "Water ATM Licensing & Compliance", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-licensing-help-suppliers/", "keywords": ["license", "licensing", "compliance", "permit", "regulation", "NEMA", "water atm"], "summary": "Licensing and compliance support for water ATM businesses."},
    {"title": "Water ATM Installation Support", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-installation-support/", "keywords": ["install", "installation", "setup", "support", "maintenance", "water atm"], "summary": "Installation and support services for water ATMs."},
    # === SEMI-AUTOMATIC WATER REFILL STATIONS ===
    {"title": "Semi-Automatic Refill Station Profit Guide", "url": "https://mavadatechnologies.co.ke/semi-automatic-water-refill-station-kenya-your-profit-guide/", "keywords": ["semi-automatic", "refill station", "profit", "water refill", "manual"], "summary": "Profit guide for semi-automatic water refill stations."},
    {"title": "Semi-Automatic Refill Station Buyer's Guide", "url": "https://mavadatechnologies.co.ke/semi-automatic-water-refill-station-kenya-buyers-guide/", "keywords": ["semi-automatic", "buyers guide", "refill station", "how to buy"], "summary": "Buyer's guide for semi-automatic water refill stations."},
    {"title": "Semi-Automatic Refill Station Profitability", "url": "https://mavadatechnologies.co.ke/semi-automatic-water-refill-station-kenya-profit-guide/", "keywords": ["semi-automatic", "profit", "refill station", "roi", "earnings"], "summary": "Profitability guide for semi-automatic refill stations."},
    {"title": "Semi-Automatic Refill Station Solutions", "url": "https://mavadatechnologies.co.ke/semi-automatic-water-refill-station-kenya-solutions/", "keywords": ["semi-automatic", "solutions", "refill station", "water vending"], "summary": "Semi-automatic water refill station solutions."},
    {"title": "Semi-Automatic Refill Station Solar Guide", "url": "https://mavadatechnologies.co.ke/semi-automatic-water-refill-station-kenya-solar-profit-guide/", "keywords": ["solar", "semi-automatic", "off-grid", "renewable", "refill station"], "summary": "Solar-powered semi-automatic refill station guide."},
    {"title": "Semi-Automatic Water Refill Station Kenya", "url": "https://mavadatechnologies.co.ke/semi-automatic-water-refill-station-kenya/", "keywords": ["semi-automatic", "refill station", "water refill", "overview", "kenya"], "summary": "Overview of semi-automatic water refill stations in Kenya."},
    {"title": "Start Semi-Automatic Refill Station Kenya", "url": "https://mavadatechnologies.co.ke/start-your-semi-automatic-water-refill-station-kenya/", "keywords": ["start", "startup", "semi-automatic", "refill station", "begin", "invest"], "summary": "How to start a semi-automatic water refill station business."},
    {"title": "Water Refill Station Kenya", "url": "https://mavadatechnologies.co.ke/water-refill-station-kenya/", "keywords": ["refill station", "water refill", "water vending", "kenya", "overview"], "summary": "Overview of water refill stations in Kenya."},
    # === ORIGINAL KB ENTRIES WITH FULL URLS ===
    {"title": "Water ATM Credit & Lease for Business", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-credit-lease-options-for-your-business/", "keywords": ["credit", "lease", "financing", "loan", "payment plan", "installment", "afford"], "summary": "Flexible financing options for water ATM businesses."},
    {"title": "Water ATM Licensing & Compliance Help", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-help-with-licensing-compliance/", "keywords": ["license", "compliance", "permit", "regulation", "legal", "NEMA", "KEBS"], "summary": "Essential permits and licensing support for water vending."},
    {"title": "Water ATM Installation Support for Success", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-installation-support-for-success/", "keywords": ["install", "installation", "setup", "after-sales", "maintenance", "technical"], "summary": "Complete installation and after-sales support."},
    {"title": "Top Water ATM Suppliers Business Guide", "url": "https://mavadatechnologies.co.ke/top-water-atm-suppliers-in-kenya-your-business-guide/", "keywords": ["top suppliers", "best", "compare", "supplier", "water atm"], "summary": "Business guide to top water ATM suppliers."},
    {"title": "Water ATM Beyond Nairobi: Maximize Profits", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-suppliers-beyond-nairobi-maximize-profits/", "keywords": ["mombasa", "kisumu", "nakuru", "eldoret", "rural", "upcountry"], "summary": "Nationwide water ATM coverage beyond Nairobi."},
    {"title": "Buy Water ATM Nairobi: Profitable Business", "url": "https://mavadatechnologies.co.ke/buy-water-atm-machines-in-nairobi-profitable-kenya-business/", "keywords": ["buy", "nairobi", "purchase", "profitable", "order"], "summary": "How to buy water ATM machines in Nairobi for profit."},
    {"title": "Basic Water ATM Cost & Price Guide", "url": "https://mavadatechnologies.co.ke/water-atm-cost-kenya-basic-vending-machine-price-guide/", "keywords": ["cost", "price", "how much", "cheap", "affordable", "basic", "budget", "ksh"], "summary": "Basic water vending machine prices from KSh 100,000."},
    {"title": "Fully Automatic Smart Water ATM Guide", "url": "https://mavadatechnologies.co.ke/water-atm-price-kenya-fully-automatic-smart-vending-guide/", "keywords": ["automatic", "smart", "fully automatic", "premium", "mpesa", "cashless"], "summary": "Fully automatic water ATMs with M-Pesa and advanced features."},
    {"title": "Semi-Automatic Water ATM Price Range", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-price-semi-automatic-range-business-guide/", "keywords": ["semi-automatic", "semi automatic", "mid-range", "refill station", "price"], "summary": "Semi-automatic water ATM pricing and business guide."},
    {"title": "Start Your Profitable Water ATM Business", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-price-guide-start-your-profitable-business/", "keywords": ["start", "startup", "entrepreneur", "invest", "investment", "ROI", "profit"], "summary": "Guide to starting a profitable water ATM business."},
    {"title": "Branding Water ATMs Kenya", "url": "https://mavadatechnologies.co.ke/branding-water-atms-kenya/", "keywords": ["brand", "branding", "logo", "design", "custom", "color", "wrap"], "summary": "Custom branding for water ATMs."},
    {"title": "Coin-Operated Water ATMs", "url": "https://mavadatechnologies.co.ke/water-atms-coin-change-kenya-refill-station-profits/", "keywords": ["coin", "coins", "coin-operated", "cash", "payment"], "summary": "Coin-operated water ATMs and payment options."},
    {"title": "Real-Time Water Quality Monitoring", "url": "https://mavadatechnologies.co.ke/water-atm-kenya-real-time-quality-monitoring/", "keywords": ["monitoring", "quality", "testing", "TDS", "pH", "sensor"], "summary": "Real-time water quality monitoring."},
    {"title": "Water Vending Machines Kenya", "url": "https://mavadatechnologies.co.ke/water-vending-machines-kenya/", "keywords": ["vending machine", "water vending", "water ATM", "overview", "all products"], "summary": "Overview of all water vending machines."},
    {"title": "Water Vending Machines: Buy, Prices, Suppliers", "url": "https://mavadatechnologies.co.ke/water-vending-machines-kenya-buy-prices-suppliers/", "keywords": ["buy", "price", "supplier", "water vending", "vending machine", "order"], "summary": "Water vending machines buying guide with prices and suppliers."},
    {"title": "Shop Quality Products", "url": "https://mavadatechnologies.co.ke/shop-quality-products/", "keywords": ["shop", "products", "buy", "order", "catalog", "all products"], "summary": "Shop all quality products from Mavada Technologies."},
    {"title": "Engaging Blogs", "url": "https://mavadatechnologies.co.ke/engaging-blogs/", "keywords": ["blog", "articles", "news", "updates", "resources"], "summary": "All engaging blog posts from Mavada Technologies."},
]


def find_relevant_blogs(question: str, top_n: int = 3) -> list[dict]:
    """Find relevant blog posts for a customer question."""
    q = question.lower()
    scored = []
    for blog in BLOG_KB:
        score = sum(1 for kw in blog["keywords"] if kw.lower() in q)
        score += sum(0.5 for w in blog["title"].lower().split() if len(w) > 3 and w in q)
        if score > 0:
            scored.append({**blog, "score": score})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_n]


_chat_store: dict[str, dict] = {}
_lead_store: dict[str, dict] = {}

async def get_chat_history(session_id: str) -> list[dict]:
    """Get chat history."""
    data = _chat_store.get(session_id)
    if not data:
        return []
    return data.get("messages", [])


async def store_chat_message(session_id: str, role: str, content: str) -> None:
    """Store a chat message."""
    if session_id not in _chat_store:
        _chat_store[session_id] = {"messages": []}
    _chat_store[session_id]["messages"].append({"role": role, "content": content, "timestamp": datetime.now(timezone.utc).isoformat()})
    _chat_store[session_id]["messages"] = _chat_store[session_id]["messages"][-20:]


async def store_lead(session_id: str, question: str, name: str = "", email: str = "", phone: str = "") -> None:
    """Store lead information."""
    if session_id not in _lead_store:
        _lead_store[session_id] = {"session_id": session_id, "inquiries": [], "first_contact": datetime.now(timezone.utc).isoformat()}
    lead = _lead_store[session_id]
    if name: lead["name"] = name
    if email: lead["email"] = email
    if phone: lead["phone"] = phone
    lead["inquiries"].append({"question": question, "timestamp": datetime.now(timezone.utc).isoformat()})
    lead["last_contact"] = datetime.now(timezone.utc).isoformat()
    lead["total_inquiries"] = len(lead["inquiries"])
    logger.info(f"Lead stored session={session_id[:8]} total={lead['total_inquiries']}")


app = FastAPI(title="Mavada Technologies Chat API - Powered by IMPERIAL ENTERPRISE", description="AI chat API for customer support with blog recommendations and lead capture.", version="2.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])




class ChatRequest(BaseModel):
    message: str = Field(..., description="Customer's question")
    session_id: str = Field(default="", description="Session ID for continuity")
    name: str = Field(default="", description="Customer name")
    email: str = Field(default="", description="Customer email")
    phone: str = Field(default="", description="Customer phone")


class BlogLink(BaseModel):
    title: str
    url: str
    summary: str


class ChatResponse(BaseModel):
    success: bool
    response: str
    blog_links: list[BlogLink]
    session_id: str
    show_agent_option: bool = False


@app.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Chat with Mavada Technologies AI assistant."""
    logger.info(f"Chat request len={len(request.message)}")
    session_id = request.session_id or str(uuid.uuid4())
    await store_lead(session_id, request.message, request.name, request.email, request.phone)
    history = await get_chat_history(session_id)
    relevant_blogs = find_relevant_blogs(request.message)

    blog_context = ""
    if relevant_blogs:
        blog_context = "\n\nRELEVANT BLOGS (share URLs when helpful):\n"
        for b in relevant_blogs:
            blog_context += f"- {b['title']}: {b['url']} - {b['summary']}\n"

    system_prompt = f"""You are a persuasive, friendly sales assistant for Mavada Technologies, Kenya's #1 supplier of water vending machines, dairy equipment, water purification, and ice cream machines.

Your PRIMARY GOAL is to get customers excited about our products and guide them to place an order or request a quote via WhatsApp.

Rules:
- Speak as Mavada Technologies (use "we") with energy and confidence
- Be enthusiastic about our products — highlight profitability, ROI, and success stories
- Actively encourage customers to take the next step: "Ready to get started? Tap the WhatsApp button below or message us directly at 0758 281922!"
- For pricing questions, give ranges but create urgency: "Prices start from KSh 100,000 — and we have flexible payment plans available! Chat with us on WhatsApp for a personalized quote."
- Recommend blog posts with full URLs when relevant
- Highlight key selling points: M-Pesa integration, financing options, nationwide delivery, free installation support
- When customers hesitate, address concerns and emphasize low risk + high returns
- Use emojis sparingly but effectively (💧🚀💰✅) to make messages engaging
- Use markdown formatting (bold, bullets, links)
- Keep responses under 250 words — punchy and action-oriented
- After answering and sharing any blog links, ALWAYS follow up with a friendly question like: "Is there anything else you'd like to know?" or "What other questions can I help with?" or "Would you like to explore other products too?"
- ALWAYS end with both the follow-up question AND a WhatsApp call-to-action: "📱 Or WhatsApp us at 0758 281922 for instant help!"

Company: Mavada Technologies | WhatsApp/Phone: 0758 281922 | Email: info@mavadatechnologies.co.ke | Website: mavadatechnologies.co.ke
Products: Water ATMs (from KSh 100K), dairy equipment, water purification, ice cream machines
Coverage: Nairobi, Mombasa, Kisumu, Nakuru, Eldoret, nationwide
Services: Installation, branding, support, licensing, financing, M-Pesa integration{blog_context}"""

    messages = [{"role": "system", "content": system_prompt}]
    for msg in history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": request.message})

    client = AsyncOpenAI()
    response = await client.chat.completions.create(model="gpt-4.1-mini", messages=messages, max_completion_tokens=600)
    ai_response = response.choices[0].message.content.strip()

    await store_chat_message(session_id, "user", request.message)
    await store_chat_message(session_id, "assistant", ai_response)

    agent_kws = ["speak to someone", "talk to agent", "human", "call me", "real person", "live agent", "help me buy", "place order", "quotation", "quote"]
    show_agent = any(kw in request.message.lower() for kw in agent_kws)
    blog_links = [BlogLink(title=b["title"], url=b["url"], summary=b["summary"]) for b in relevant_blogs]

    logger.info(f"Chat sent s={session_id[:8]} blogs={len(blog_links)}")
    return ChatResponse(success=True, response=ai_response, blog_links=blog_links, session_id=session_id, show_agent_option=show_agent)


class LeadSubmitRequest(BaseModel):
    session_id: str = Field(..., description="Chat session ID")
    name: str = Field(..., description="Customer name")
    phone: str = Field(default="", description="Customer phone")
    email: str = Field(default="", description="Customer email")
    interest: str = Field(default="", description="What they're interested in")


class LeadSubmitResponse(BaseModel):
    success: bool
    message: str


@app.post("/submit_lead", response_model=LeadSubmitResponse)
async def submit_lead(request: LeadSubmitRequest) -> LeadSubmitResponse:
    """Submit lead contact details."""
    logger.info(f"Lead submitted s={request.session_id[:8]}")
    await store_lead(request.session_id, f"Lead: {request.interest}", request.name, request.email, request.phone)
    return LeadSubmitResponse(success=True, message="Thank you! Our team will contact you shortly. Call us directly at 0758 281922.")


# For local development:
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
