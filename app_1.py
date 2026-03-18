import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import math
from collections import Counter


#    PASTE YOUR GEMINI API KEY HERE

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
GEMINI_MODEL   = "gemini-2.0-flash"


st.set_page_config(
    page_title="Chérie · AI Wardrobe",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

#  CUSTOM CSS 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400;1,700&family=Lato:wght@300;400;700&display=swap');

html, body, [class*="css"] { font-family: 'Lato', sans-serif; }

.main { background: #fdf6f0; }
.block-container { padding-top: 1.5rem; max-width: 1200px; }

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }

/* Page title */
.cherie-title {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 2.8rem;
    color: #6b2d3e;
    margin-bottom: 0;
    line-height: 1;
}
.cherie-sub {
    font-family: 'Lato', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #c98090;
    margin-top: 4px;
}

/* Stat cards */
.stat-card {
    background: white;
    border: 1px solid #fce4e8;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 12px rgba(200,120,140,0.06);
}
.stat-val {
    font-family: 'Playfair Display', serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #6b2d3e;
    line-height: 1;
}
.stat-label {
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #c98090;
    margin-top: 4px;
}

/* Item cards */
.item-card {
    background: white;
    border: 1px solid #fce4e8;
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(200,120,140,0.05);
    transition: all 0.2s;
}
.item-card:hover { border-color: #e8a0b0; }

/* Section headers */
.section-eyebrow {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #e8a0b0;
    margin-bottom: 4px;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 2rem;
    color: #6b2d3e;
    margin-bottom: 4px;
}
.section-sub {
    font-size: 0.85rem;
    color: #c98090;
    font-weight: 300;
    margin-bottom: 1.5rem;
}

/* Chat messages */
.msg-ai {
    background: #fdf6f8;
    border: 1px solid #fce4e8;
    border-radius: 16px 16px 16px 4px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.9rem;
    color: #8a4558;
    line-height: 1.7;
}
.msg-user {
    background: linear-gradient(135deg, #f0a8b522, #f0a8b511);
    border: 1px solid #f0a8b566;
    border-radius: 16px 16px 4px 16px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.9rem;
    color: #6b2d3e;
    text-align: right;
    line-height: 1.7;
}
.msg-label {
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #e8a0b0;
    margin-bottom: 4px;
}

/* Badges */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.badge-pink  { background: #fce8ec; color: #a0424e; }
.badge-green { background: #d1fae5; color: #3b7a57; }
.badge-gold  { background: #fef3c7; color: #92660a; }
.badge-red   { background: #fee2e2; color: #991b1b; }

/* Bar chart custom */
.bar-wrap { margin-bottom: 10px; }
.bar-label { font-size: 0.75rem; color: #8a4558; margin-bottom: 3px; }
.bar-bg { background: #fce4e8; border-radius: 8px; height: 22px; overflow: hidden; }
.bar-fill { height: 100%; border-radius: 8px; display: flex; align-items: center; padding-left: 8px; }
.bar-text { font-size: 0.7rem; font-weight: 700; color: white; }

/* Gap cards */
.gap-card { border-radius: 14px; padding: 16px; margin-bottom: 10px; }

/* Divider */
.pink-divider { height: 2px; background: linear-gradient(90deg,#f9c5cb,#fdf6f0); border-radius: 2px; margin: 1.5rem 0; }

/* Scatter dot */
.scatter-container { position: relative; background: #fdf8fa; border: 1px solid #fce4e8; border-radius: 12px; }

/* Recommendation card */
.rec-card {
    background: white;
    border: 1px solid #fce4e8;
    border-radius: 14px;
    padding: 18px;
}
</style>
""", unsafe_allow_html=True)

#  DEFAULT WARDROBE DATA 
DEFAULT_WARDROBE = [
    {"id":1,  "name":"White Oxford Shirt",   "cat":"Tops",        "color":"White",      "brand":"COS",             "price":89,  "wears":34, "emoji":"🤍", "occasions":["Work","Casual"]},
    {"id":2,  "name":"Black Slim Trousers",  "cat":"Bottoms",     "color":"Black",      "brand":"Zara",            "price":59,  "wears":28, "emoji":"🖤", "occasions":["Work","Evening"]},
    {"id":3,  "name":"Camel Wool Coat",      "cat":"Outerwear",   "color":"Camel",      "brand":"& Other Stories", "price":249, "wears":41, "emoji":"🧥", "occasions":["Work","Casual"]},
    {"id":4,  "name":"White Sneakers",       "cat":"Shoes",       "color":"White",      "brand":"Common Projects", "price":380, "wears":67, "emoji":"👟", "occasions":["Casual"]},
    {"id":5,  "name":"Navy Blazer",          "cat":"Tops",        "color":"Navy",       "brand":"Sandro",          "price":195, "wears":12, "emoji":"💙", "occasions":["Work","Evening"]},
    {"id":6,  "name":"Silk Slip Dress",      "cat":"Dresses",     "color":"Ivory",      "brand":"Reformation",     "price":168, "wears":8,  "emoji":"🕊️", "occasions":["Evening","Casual"]},
    {"id":7,  "name":"Dark Wash Jeans",      "cat":"Bottoms",     "color":"Indigo",     "brand":"Agolde",          "price":198, "wears":52, "emoji":"💜", "occasions":["Casual"]},
    {"id":8,  "name":"Cashmere Turtleneck",  "cat":"Tops",        "color":"Oatmeal",    "brand":"Everlane",        "price":120, "wears":31, "emoji":"🤎", "occasions":["Casual","Work"]},
    {"id":9,  "name":"Leather Belt",         "cat":"Accessories", "color":"Tan",        "brand":"Mango",           "price":35,  "wears":29, "emoji":"🌸", "occasions":["Work","Casual"]},
    {"id":10, "name":"Black Ankle Boots",    "cat":"Shoes",       "color":"Black",      "brand":"Sam Edelman",     "price":140, "wears":38, "emoji":"🖤", "occasions":["Work","Evening"]},
    {"id":11, "name":"Striped Breton Top",   "cat":"Tops",        "color":"Navy/White", "brand":"Saint James",     "price":105, "wears":19, "emoji":"🩵", "occasions":["Casual"]},
    {"id":12, "name":"Linen Shorts",         "cat":"Bottoms",     "color":"Sand",       "brand":"H&M",             "price":25,  "wears":14, "emoji":"🌼", "occasions":["Casual"]},
]

#  SESSION STATE 
if "wardrobe" not in st.session_state:
    st.session_state.wardrobe = DEFAULT_WARDROBE.copy()
if "outfit_messages"   not in st.session_state: st.session_state.outfit_messages   = []
if "purchase_messages" not in st.session_state: st.session_state.purchase_messages = []
if "roi_messages"      not in st.session_state: st.session_state.roi_messages      = []

#  GEMINI API 
def ask_gemini(system_prompt: str, user_message: str) -> str:
    if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
        return " Please set your Gemini API key at the top of app.py"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": user_message}]}],
        "generationConfig": {"maxOutputTokens": 1000, "temperature": 0.8},
    }
    try:
        r = requests.post(url, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error: {e}"

#  HELPERS 
def cpw(item):
    return round(item["price"] / item["wears"], 2) if item["wears"] > 0 else item["price"]

def cpw_color(val):
    if val < 1:   return "#6b9e78"
    if val < 3:   return "#c98090"
    if val < 8:   return "#d4a050"
    return "#c05060"

def cpw_grade(val):
    if val < 1:  return "✦ Excellent"
    if val < 3:  return "◎ Good"
    if val < 8:  return "◇ Fair"
    return "✗ Poor"

def wardrobe_context():
    return "\n".join([
        f"{i['emoji']} {i['name']} ({i['cat']}, {i['color']}, {i['brand']}, "
        f"${i['price']}, worn {i['wears']}x, occasions: {'/'.join(i['occasions'])})"
        for i in st.session_state.wardrobe
    ])

def render_bar(label, value, max_val, color="#e87a90", suffix=""):
    pct = max(4, int((value / max(max_val, 1)) * 100))
    st.markdown(f"""
    <div class="bar-wrap">
      <div class="bar-label">{label}</div>
      <div class="bar-bg">
        <div class="bar-fill" style="width:{pct}%; background: linear-gradient(90deg,#f9c5cb,{color});">
          <span class="bar-text">{value}{suffix}</span>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

def render_chat(messages):
    for m in messages:
        if m["role"] == "ai":
            st.markdown(f'<div class="msg-label">✦ Chérie AI</div><div class="msg-ai">{m["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="msg-user">{m["text"]}</div>', unsafe_allow_html=True)

#  HEADER 
col_logo, col_title, col_stats = st.columns([1, 6, 3])
with col_logo:
    st.markdown("<div style='font-size:3rem;margin-top:8px'>🌸</div>", unsafe_allow_html=True)
with col_title:
    st.markdown('<div class="cherie-title">Chérie</div>', unsafe_allow_html=True)
    st.markdown('<div class="cherie-sub">✦ Powered by Google Gemini · AI Wardrobe Manager ✦</div>', unsafe_allow_html=True)
with col_stats:
    wrd = st.session_state.wardrobe
    total_val   = sum(i["price"] for i in wrd)
    total_wears = sum(i["wears"] for i in wrd)
    st.markdown(f"""
    <div style="text-align:right;margin-top:8px">
      <span style="font-family:'Playfair Display',serif;font-size:1.4rem;color:#6b2d3e;font-weight:700">{len(wrd)} pieces</span>
      <span style="color:#fce4e8;margin:0 8px">·</span>
      <span style="font-family:'Playfair Display',serif;font-size:1.4rem;color:#6b2d3e;font-weight:700">${total_val:,}</span>
      <br><span style="font-size:0.7rem;color:#c98090;letter-spacing:0.1em">ITEMS · TOTAL VALUE</span>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="pink-divider"></div>', unsafe_allow_html=True)

#  TABS 
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🪞  My Closet",
    "✨  Outfit Planner",
    "🛍️  Shopping Advisor",
    "💎  Wardrobe ROI",
    "📊  Analytics",
])


# TAB 1 — MY CLOSET

with tab1:
    st.markdown('<div class="section-eyebrow">My Collection</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">The Wardrobe</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Every piece tells a story, darling.</div>', unsafe_allow_html=True)

    # KPI row
    wrd = st.session_state.wardrobe
    total_val   = sum(i["price"] for i in wrd)
    total_wears = sum(i["wears"] for i in wrd)
    avg_cpw     = round(total_val / max(total_wears, 1), 2)

    k1, k2, k3, k4 = st.columns(4)
    for col, val, lbl in [
        (k1, len(wrd),         "Total Pieces"),
        (k2, f"${total_val:,}","Total Value"),
        (k3, total_wears,      "Total Wears"),
        (k4, f"${avg_cpw}",    "Avg Cost / Wear"),
    ]:
        col.markdown(f'<div class="stat-card"><div class="stat-val">{val}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="pink-divider"></div>', unsafe_allow_html=True)

    # Add new item
    with st.expander("✦ Add a new piece to your collection"):
        c1, c2, c3 = st.columns(3)
        with c1:
            new_name  = st.text_input("Item Name *", placeholder="e.g. Pink Blazer")
            new_brand = st.text_input("Brand", placeholder="e.g. Zara")
        with c2:
            new_price = st.number_input("Price ($) *", min_value=0.0, step=1.0)
            new_color = st.text_input("Color", placeholder="e.g. Blush")
        with c3:
            new_cat   = st.selectbox("Category", ["Tops","Bottoms","Dresses","Outerwear","Shoes","Accessories"])
            new_emoji = st.text_input("Emoji", value="🌸")

        if st.button("✦ Save Piece", type="primary"):
            if new_name and new_price > 0:
                st.session_state.wardrobe.append({
                    "id": max(i["id"] for i in st.session_state.wardrobe) + 1,
                    "name": new_name, "cat": new_cat, "color": new_color,
                    "brand": new_brand, "price": new_price, "wears": 0,
                    "emoji": new_emoji, "occasions": ["Casual"],
                })
                st.success(f"Added {new_emoji} {new_name} to your wardrobe!")
                st.rerun()
            else:
                st.error("Please fill in item name and price.")

    # Filter
    cats = ["All"] + sorted(set(i["cat"] for i in wrd))
    chosen_cat = st.selectbox("Filter by category", cats, label_visibility="collapsed")
    shown = wrd if chosen_cat == "All" else [i for i in wrd if i["cat"] == chosen_cat]

    st.markdown(f"**{len(shown)} items**", )

    # Items grid — 3 columns
    for row_start in range(0, len(shown), 3):
        cols = st.columns(3)
        for col_idx, item in enumerate(shown[row_start:row_start+3]):
            with cols[col_idx]:
                item_cpw = cpw(item)
                cpw_col  = cpw_color(item_cpw)
                st.markdown(f"""
                <div class="item-card">
                  <div style="font-size:2rem;margin-bottom:8px">{item['emoji']}</div>
                  <div style="font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;color:#6b2d3e">{item['name']}</div>
                  <div style="font-size:0.75rem;color:#c98090;margin-bottom:10px">{item['brand']} · {item['color']}</div>
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                    <span class="badge badge-pink">{item['cat']}</span>
                    <span style="font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;color:#6b2d3e">${item['price']}</span>
                  </div>
                  <div style="display:flex;justify-content:space-between;font-size:0.75rem">
                    <span style="color:#c98090">{item['wears']} wears</span>
                    <span style="font-weight:700;color:{cpw_col}">${item_cpw}/wear · {cpw_grade(item_cpw)}</span>
                  </div>
                </div>""", unsafe_allow_html=True)

                # Wear buttons
                b1, b2, b3 = st.columns([1, 2, 1])
                with b1:
                    if st.button("−", key=f"dec_{item['id']}", help="Remove a wear"):
                        for i in st.session_state.wardrobe:
                            if i["id"] == item["id"]:
                                i["wears"] = max(0, i["wears"] - 1)
                        st.rerun()
                with b2:
                    st.markdown(f"<div style='text-align:center;font-size:0.75rem;color:#c98090;padding-top:6px'>{item['wears']} wears</div>", unsafe_allow_html=True)
                with b3:
                    if st.button("＋", key=f"inc_{item['id']}", help="Add a wear"):
                        for i in st.session_state.wardrobe:
                            if i["id"] == item["id"]:
                                i["wears"] += 1
                        st.rerun()

# TAB 2 — OUTFIT PLANNER
with tab2:
    st.markdown('<div class="section-eyebrow">Style Me</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Outfit Planner</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Let me dress you for every chapter of your day.</div>', unsafe_allow_html=True)

    # Quick prompts
    st.markdown("**Quick prompts:**")
    qcols = st.columns(5)
    quick = ["Office, power look","Date night, romantic","Brunch with girls","Weekend errands","Evening cocktails"]
    for qi, (qc, ql) in enumerate(zip(qcols, quick)):
        if qc.button(f"✿ {ql}", key=f"q_outfit_{qi}"):
            st.session_state._outfit_input = ql

    left, right = st.columns([2, 1])

    with left:
        render_chat(st.session_state.outfit_messages)

        default_val = st.session_state.pop("_outfit_input", "")
        user_input  = st.text_input("Describe the occasion or mood…", value=default_val, key="outfit_input", label_visibility="collapsed", placeholder="e.g. Cosy Sunday brunch, light layers")

        if st.button("✦ Get Outfit Ideas", key="send_outfit", type="primary"):
            if user_input.strip():
                sys = f"""You are Chérie, a Parisian personal stylist AI. The user's wardrobe:

{wardrobe_context()}

Suggest 2-3 complete, specific outfits using ONLY items from this wardrobe. Format:

OUTFIT 1: [Poetic name]
• [items listed]
The vibe: [1 sentence]

Be romantic, stylish, and specific. Reference exact item names."""
                with st.spinner("Creating your looks… ✨"):
                    reply = ask_gemini(sys, user_input.strip())
                st.session_state.outfit_messages.append({"role":"user","text":user_input.strip()})
                st.session_state.outfit_messages.append({"role":"ai","text":reply})
                st.rerun()

        if st.button("🗑 Clear chat", key="clear_outfit"):
            st.session_state.outfit_messages = []
            st.rerun()

    with right:
        st.markdown("**Wardrobe mix**")
        for cat in ["Tops","Bottoms","Shoes","Outerwear","Dresses","Accessories"]:
            n = sum(1 for i in st.session_state.wardrobe if i["cat"]==cat)
            render_bar(cat, n, 6)

# TAB 3 — SHOPPING ADVISOR
with tab3:
    st.markdown('<div class="section-eyebrow">Smart Shopping</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Shopping Advisor</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Because every purchase deserves a second opinion.</div>', unsafe_allow_html=True)

    wrd = st.session_state.wardrobe
    total_spend = sum(i["price"] for i in wrd)
    cat_counts  = Counter(i["cat"] for i in wrd)
    underused   = [i for i in wrd if i["wears"] < 5]

    left, right = st.columns([2, 1])

    with left:
        qcols2 = st.columns(4)
        quick2 = ["Analyze my gaps","Best next purchase?","Is $250 too much?","Capsule advice"]
        for qi, (qc, ql) in enumerate(zip(qcols2, quick2)):
            if qc.button(f"✿ {ql}", key=f"q_purchase_{qi}"):
                st.session_state._purchase_input = ql

        render_chat(st.session_state.purchase_messages)

        default_val2 = st.session_state.pop("_purchase_input", "")
        user_input2  = st.text_input("Ask about a purchase or wardrobe gaps…", value=default_val2, key="purchase_input", label_visibility="collapsed", placeholder="e.g. Should I buy these $200 boots?")

        if st.button("✦ Ask Chérie", key="send_purchase", type="primary"):
            if user_input2.strip():
                ctx = f"""Wardrobe: {len(wrd)} items, ${total_spend} total value
Categories: {', '.join(f"{k}:{v}" for k,v in cat_counts.items())}
Underutilized (<5 wears): {', '.join(i['name'] for i in underused) or 'none'}
Items: {' | '.join(f"{i['name']}(${i['price']},{i['wears']}wears)" for i in wrd)}"""
                sys2 = f"""You are Chérie, a chic fashion investment advisor.

{ctx}

Give BUY ✦ / SKIP ✗ / WAIT ◇ recommendation with gap analysis, cost-per-wear at 20 wears, and outfit synergies. Be warm, direct, and stylish."""
                with st.spinner("Analysing… 💭"):
                    reply2 = ask_gemini(sys2, user_input2.strip())
                st.session_state.purchase_messages.append({"role":"user","text":user_input2.strip()})
                st.session_state.purchase_messages.append({"role":"ai","text":reply2})
                st.rerun()

        if st.button("🗑 Clear chat", key="clear_purchase"):
            st.session_state.purchase_messages = []
            st.rerun()

    with right:
        st.markdown("**Spending summary**")
        df_spend = pd.DataFrame([
            {"Metric": "Total invested",  "Value": f"${total_spend:,}"},
            {"Metric": "Avg per item",    "Value": f"${total_spend//max(len(wrd),1)}"},
            {"Metric": "Most expensive",  "Value": f"${max(i['price'] for i in wrd)}"},
            {"Metric": "Items < 5 wears", "Value": str(len(underused))},
        ])
        st.dataframe(df_spend, hide_index=True, use_container_width=True)

        if underused:
            st.markdown("**Worn < 5 times 🥀**")
            for i in underused[:5]:
                st.markdown(f"<div style='display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #fce4e8;font-size:0.8rem'><span style='color:#8a4558'>{i['emoji']} {i['name']}</span><span style='color:#e87a90;font-weight:700'>{i['wears']}×</span></div>", unsafe_allow_html=True)

# TAB 4 — WARDROBE ROI
with tab4:
    st.markdown('<div class="section-eyebrow">Return on Investment</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Closet ROI</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Because fashion is an investment in yourself, darling.</div>', unsafe_allow_html=True)

    wrd     = st.session_state.wardrobe
    ranked  = sorted(wrd, key=lambda i: cpw(i))
    total_v = sum(i["price"] for i in wrd)
    total_w = sum(i["wears"] for i in wrd)
    o_cpw   = round(total_v / max(total_w, 1), 2)

    k1, k2, k3, k4 = st.columns(4)
    for col, val, lbl in [
        (k1, f"${o_cpw}",                                               "Overall Cost/Wear"),
        (k2, f"${cpw(ranked[0])}" if ranked else "-",                   f"Best: {ranked[0]['name'][:15] if ranked else ''}"),
        (k3, f"${cpw(ranked[-1])}" if ranked else "-",                  f"Worst: {ranked[-1]['name'][:15] if ranked else ''}"),
        (k4, sum(1 for i in wrd if i["wears"]<3),                       "Items < 3 Wears 🥀"),
    ]:
        col.markdown(f'<div class="stat-card"><div class="stat-val">{val}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="pink-divider"></div>', unsafe_allow_html=True)

    left_r, right_r = st.columns([1, 1])

    with left_r:
        st.markdown("**Pieces ranked by ROI 🌹**")
        roi_data = []
        for item in ranked:
            c = cpw(item)
            roi_data.append({
                "": item["emoji"],
                "Item": item["name"],
                "Price": f"${item['price']}",
                "Wears": item["wears"],
                "CPW": f"${c}",
                "Grade": cpw_grade(c),
            })
        df_roi = pd.DataFrame(roi_data)
        st.dataframe(df_roi, hide_index=True, use_container_width=True, height=380)

    with right_r:
        st.markdown("**Visual CPW Chart 💐**")
        max_cpw = max(cpw(i) for i in ranked[:9]) if ranked else 1
        for item in ranked[:9]:
            c = cpw(item)
            render_bar(f"{item['emoji']} {item['name'][:22]}", c, max_cpw, color=cpw_color(c), suffix="/wear")

    st.markdown('<div class="pink-divider"></div>', unsafe_allow_html=True)

    # ROI Chat
    st.markdown("**Ask the ROI Analyst**")
    qcols3 = st.columns(4)
    quick3 = ["Best ROI pieces?","What to donate?","Improve my CPW","Compare to benchmarks"]
    for qi, (qc, ql) in enumerate(zip(qcols3, quick3)):
        if qc.button(f"✿ {ql}", key=f"q_roi_{qi}"):
            st.session_state._roi_input = ql

    render_chat(st.session_state.roi_messages)

    default_val3 = st.session_state.pop("_roi_input", "")
    user_input3  = st.text_input("Ask about your wardrobe ROI…", value=default_val3, key="roi_input", label_visibility="collapsed", placeholder="e.g. Which items give me the best return?")

    if st.button("✦ Analyse", key="send_roi", type="primary"):
        if user_input3.strip():
            roi_ctx = "\n".join([f"{i['name']}: ${i['price']}, {i['wears']} wears, ${cpw(i)}/wear" for i in ranked])
            sys3    = f"""You are Chérie, a wardrobe ROI analyst. Benchmarks: Excellent <$1, Good $1-3, Fair $3-8, Poor >$8.

{roi_ctx}
Total: ${total_v}, Overall CPW: ${o_cpw}

Give elegant, data-driven insights with specific numbers and recommendations."""
            with st.spinner("Calculating… 📊"):
                reply3 = ask_gemini(sys3, user_input3.strip())
            st.session_state.roi_messages.append({"role":"user","text":user_input3.strip()})
            st.session_state.roi_messages.append({"role":"ai","text":reply3})
            st.rerun()

    if st.button("🗑 Clear chat", key="clear_roi"):
        st.session_state.roi_messages = []
        st.rerun()


# TAB 5 — ANALYTICS
with tab5:
    st.markdown('<div class="section-eyebrow">Data Science</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Wardrobe Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Deep insights into your fashion data, darling.</div>', unsafe_allow_html=True)

    wrd = st.session_state.wardrobe
    df  = pd.DataFrame(wrd)
    df["cpw"] = df.apply(lambda r: round(r["price"]/r["wears"],2) if r["wears"]>0 else r["price"], axis=1)

    section = st.radio("", ["📈 Wear Patterns", "🔮 CPW Predictions", "🗺️ Gap Analysis"], horizontal=True, label_visibility="collapsed")
    st.markdown('<div class="pink-divider"></div>', unsafe_allow_html=True)

    #  WEAR PATTERNS 
    if section == "📈 Wear Patterns":

        # KPIs
        k1,k2,k3,k4,k5 = st.columns(5)
        for col, val, lbl in [
            (k1, len(wrd),                          "Total Pieces"),
            (k2, f"${df['price'].sum():,}",          "Total Value"),
            (k3, int(df['wears'].sum()),              "Total Wears"),
            (k4, f"{df['wears'].mean():.1f}",        "Avg Wears/Item"),
            (k5, f"${df['price'].mean():.0f}",       "Avg Price"),
        ]:
            col.markdown(f'<div class="stat-card"><div class="stat-val">{val}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="pink-divider"></div>', unsafe_allow_html=True)

        left_a, right_a = st.columns([1,1])

        with left_a:
            st.markdown("**Total Wears by Category 📊**")
            cat_wear = df.groupby("cat")["wears"].sum().sort_values(ascending=False)
            max_w = cat_wear.max()
            for cat, total in cat_wear.items():
                render_bar(cat, int(total), int(max_w))

            st.markdown('<div class="pink-divider"></div>', unsafe_allow_html=True)
            st.markdown("**Wear Frequency Distribution**")
            bins   = [0, 5, 15, 30, 50, float("inf")]
            labels = ["0–5","6–15","16–30","31–50","50+"]
            df["bucket"] = pd.cut(df["wears"], bins=bins, labels=labels, right=True)
            bucket_counts = df["bucket"].value_counts().reindex(labels, fill_value=0)
            max_b = bucket_counts.max()
            for lbl, cnt in bucket_counts.items():
                render_bar(f"{lbl} wears", int(cnt), int(max_b), suffix=" items")

        with right_a:
            st.markdown("**Stars ✦ vs Sleepers 🥀**")
            top5 = df.nlargest(5, "wears")[["emoji","name","wears","cpw"]]
            bot5 = df.nsmallest(5, "wears")[["emoji","name","wears","cpw"]]

            st.markdown("🌟 *Most Worn*")
            for _, row in top5.iterrows():
                st.markdown(f"<div style='display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #fdf0f2;font-size:0.8rem'><span>{row['emoji']} {row['name']}</span><span style='color:#6b9e78;font-weight:700'>{row['wears']}×</span></div>", unsafe_allow_html=True)

            st.markdown("🥀 *Least Worn*")
            for _, row in bot5.iterrows():
                st.markdown(f"<div style='display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #fdf0f2;font-size:0.8rem'><span>{row['emoji']} {row['name']}</span><span style='color:#c05060;font-weight:700'>{row['wears']}×</span></div>", unsafe_allow_html=True)

            st.markdown('<div class="pink-divider"></div>', unsafe_allow_html=True)
            st.markdown("**Price vs Wears (Scatter)**")
            scatter_df = df[["name","price","wears","cpw","emoji"]].copy()
            scatter_df["colour"] = scatter_df["cpw"].apply(cpw_color)
            # Use streamlit native scatter via dataframe chart
            st.scatter_chart(
                scatter_df.rename(columns={"wears":"Wears","price":"Price ($)"}),
                x="Wears", y="Price ($)", color="colour", size="cpw",
                use_container_width=True, height=260,
            )
            st.caption("Dot colour = CPW tier (green=excellent, red=poor). Hover for details.")

    #  CPW PREDICTIONS 
    elif section == "🔮 CPW Predictions":

        st.markdown("**Cost-Per-Wear Projections at Future Wear Counts 🔮**")
        st.caption("How your CPW will fall as you wear each item more. Green = excellent (<$1), highlighted = already achieved.")

        wear_targets = [10, 20, 30, 50, 100]
        pred_rows = []
        for item in wrd:
            row = {
                "": item["emoji"],
                "Item": item["name"],
                "Price": f"${item['price']}",
                "Now": f"${cpw(item)}",
            }
            for n in wear_targets:
                row[f"@{n} wears"] = f"${item['price']/n:.2f}"
            row["Break-even (@$3)"] = f"{math.ceil(item['price']/3)} wears"
            row["For $1/wear"]      = f"{item['price']} wears"
            pred_rows.append(row)

        pred_df = pd.DataFrame(pred_rows)
        st.dataframe(pred_df, hide_index=True, use_container_width=True, height=420)

        st.markdown('<div class="pink-divider"></div>', unsafe_allow_html=True)

        left_p, right_p = st.columns([1,1])

        with left_p:
            st.markdown("**CPW Decay — Your 4 Priciest Items**")
            st.caption("How CPW drops as wears increase. The faster it drops, the better the investment.")
            top4_price = df.nlargest(4, "price")
            wear_range = [1, 5, 10, 20, 30, 50, 100]
            decay_data = {}
            for _, row in top4_price.iterrows():
                decay_data[row["name"][:18]] = [round(row["price"]/n, 2) for n in wear_range]
            decay_df = pd.DataFrame(decay_data, index=wear_range)
            st.line_chart(decay_df, use_container_width=True, height=280)
            st.caption("X-axis = number of wears. Y-axis = cost per wear ($).")

        with right_p:
            st.markdown("**Wardrobe Efficiency Score**")
            excellent = len(df[df["cpw"] < 1])
            good      = len(df[(df["cpw"] >= 1) & (df["cpw"] < 3)])
            fair      = len(df[(df["cpw"] >= 3) & (df["cpw"] < 8)])
            poor      = len(df[df["cpw"] >= 8])
            score     = round(((excellent*4 + good*3 + fair*2 + poor*1) / (len(df)*4)) * 100)
            grade     = "A" if score>=80 else "B" if score>=65 else "C" if score>=50 else "D"
            grade_col = "#6b9e78" if score>=80 else "#c9a96e" if score>=65 else "#d4a050" if score>=50 else "#c05060"

            st.markdown(f"""
            <div style="text-align:center;padding:20px 0">
              <div style="font-family:'Playfair Display',serif;font-size:5rem;font-weight:700;color:{grade_col};line-height:1">{grade}</div>
              <div style="font-size:0.9rem;color:#c98090">Efficiency Score: {score}/100</div>
            </div>""", unsafe_allow_html=True)

            for lbl, n, col in [("✦ Excellent <$1",excellent,"#6b9e78"),("◎ Good $1–3",good,"#c98090"),("◇ Fair $3–8",fair,"#d4a050"),("✗ Poor >$8",poor,"#c05060")]:
                pct = int((n / max(len(df),1)) * 100)
                st.markdown(f"""
                <div style="margin-bottom:10px">
                  <div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:3px">
                    <span style="color:{col};font-weight:700">{lbl}</span>
                    <span style="color:{col};font-weight:700">{n} items</span>
                  </div>
                  <div style="height:7px;background:#fce4e8;border-radius:10px;overflow:hidden">
                    <div style="height:100%;width:{pct}%;background:{col};border-radius:10px"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

    #  GAP ANALYSIS 
    elif section == "🗺️ Gap Analysis":

        ideal = {"Tops":4,"Bottoms":4,"Dresses":2,"Outerwear":2,"Shoes":3,"Accessories":3}
        cat_counts_map = Counter(i["cat"] for i in wrd)
        gaps = []
        for cat, ideal_n in ideal.items():
            have = cat_counts_map.get(cat, 0)
            diff = have - ideal_n
            status = "Over" if diff>=2 else "Good" if diff>=0 else "Low" if diff>=-1 else "Gap"
            gaps.append({"Category":cat,"You Have":have,"Benchmark":ideal_n,"Diff":diff,"Status":status})

        st.markdown("**Category Gap vs Capsule Wardrobe Benchmark 🗺️**")
        g1, g2, g3 = st.columns(3)
        cols3 = [g1, g2, g3]
        status_col = {"Over":"#6b9e78","Good":"#c9a96e","Low":"#d4a050","Gap":"#c05060"}
        status_bg  = {"Over":"#f0faf4","Good":"#fdf8f0","Low":"#fffbeb","Gap":"#fff5f5"}
        for idx, gap in enumerate(gaps):
            col = cols3[idx % 3]
            sc  = status_col[gap["Status"]]
            bg  = status_bg[gap["Status"]]
            pct = min(int((gap["You Have"]/max(gap["Benchmark"],1))*100), 100)
            col.markdown(f"""
            <div style="background:{bg};border:1px solid {sc}33;border-radius:16px;padding:18px;margin-bottom:12px">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                <span style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:#6b2d3e">{gap['Category']}</span>
                <span style="background:{sc}22;color:{sc};padding:2px 8px;border-radius:10px;font-size:0.65rem;font-weight:700">{gap['Status'].upper()}</span>
              </div>
              <div style="display:flex;gap:20px;margin-bottom:10px">
                <div><div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;color:{sc}">{gap['You Have']}</div><div style="font-size:0.65rem;color:#c98090">you have</div></div>
                <div style="color:#fce4e8;font-size:1.5rem;padding-top:8px">/</div>
                <div><div style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;color:#c98090">{gap['Benchmark']}</div><div style="font-size:0.65rem;color:#c98090">benchmark</div></div>
              </div>
              <div style="height:6px;background:#fce4e8;border-radius:10px;overflow:hidden">
                <div style="height:100%;width:{pct}%;background:{sc};border-radius:10px"></div>
              </div>
              <div style="font-size:0.7rem;color:#c98090;margin-top:6px">{'▲ '+str(abs(gap['Diff']))+' above' if gap['Diff']>0 else '▼ '+str(abs(gap['Diff']))+' below' if gap['Diff']<0 else 'Right on target ✦'}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="pink-divider"></div>', unsafe_allow_html=True)

        left_g, right_g = st.columns([1,1])

        with left_g:
            st.markdown("**Occasion Coverage 👗**")
            occasions = ["Work","Casual","Evening","Sport","Vacation"]
            for occ in occasions:
                n = sum(1 for i in wrd if occ in i.get("occasions",[]))
                col = "#6b9e78" if n>=5 else "#c9a96e" if n>=3 else "#c05060"
                render_bar(occ, n, 8, color=col, suffix=" items")

            st.markdown('<div class="pink-divider"></div>', unsafe_allow_html=True)
            st.markdown("**Colour Palette 🎨**")
            colors = Counter(i["color"].split("/")[0] for i in wrd)
            color_df = pd.DataFrame(colors.most_common(8), columns=["Colour","Count"])
            st.bar_chart(color_df.set_index("Colour"), use_container_width=True, height=200, color="#f0a8b5")

        with right_g:
            st.markdown("**AI Recommendations ✦**")
            gap_cats = [g["Category"] for g in gaps if g["Status"]=="Gap"]
            over_cats = [g["Category"] for g in gaps if g["Status"]=="Over"]
            best_val  = df.loc[df.apply(lambda r: r["wears"]/max(r["price"],1), axis=1).idxmax()]

            recs = [
                ("🛍️", "Buy Next",
                 f"Focus on **{', '.join(gap_cats)}** — below capsule benchmark." if gap_cats else "Wardrobe is well balanced! Invest in quality over quantity."),
                ("🥀", "Consider Donating",
                 f"You have **{len([i for i in wrd if i['wears']<3])} items** worn fewer than 3 times. Pass them on to free up budget."),
                ("💡", "Quick Win",
                 f"**{best_val['name']}** has your best value ratio. Consider more pieces from **{best_val['brand']}**."),
            ]
            for icon, title, body in recs:
                st.markdown(f"""
                <div class="rec-card" style="margin-bottom:12px">
                  <div style="font-size:1.5rem;margin-bottom:6px">{icon}</div>
                  <div style="font-weight:700;color:#6b2d3e;margin-bottom:4px">{title}</div>
                  <div style="font-size:0.82rem;color:#8a4558;line-height:1.6">{body}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown("**Capsule Score Summary**")
            gap_df = pd.DataFrame(gaps)[["Category","You Have","Benchmark","Status"]]
            st.dataframe(gap_df, hide_index=True, use_container_width=True)

#  FOOTER 
st.markdown('<div class="pink-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;font-family:'Lato',sans-serif;font-size:0.7rem;color:#c98090;letter-spacing:0.2em;text-transform:uppercase;padding:8px 0">
  ✦ Chérie · AI Wardrobe Manager · Powered by Google Gemini ✦
</div>""", unsafe_allow_html=True)
