# 🌸 Chérie — AI Wardrobe Manager



A full-featured AI wardrobe management app built with Python and Streamlit. Chérie helps you plan outfits, make smarter purchase decisions, track your wardrobe ROI, and explore deep data science analytics all from a beautiful, feminine dashboard.

---

## ✦ Features

### 🪞 My Closet
- View your entire wardrobe in a filterable grid
- Filter by category: Tops, Bottoms, Dresses, Outerwear, Shoes, Accessories
- Add new items with name, brand, price, colour, category and emoji
- Log wears with **＋ / −** buttons — cost-per-wear recalculates instantly
- Live KPIs: total pieces, total value, total wears, avg cost/wear

### ✨ Outfit Planner
- AI stylist powered by Gemini — describe any occasion and get 2–3 complete outfit suggestions using only your actual wardrobe items
- Quick prompt chips: Office, Date Night, Brunch, Weekend, Cocktails
- Wardrobe mix breakdown (items per category)

### 🛍️ Shopping Advisor
- AI purchase advisor gives recommendations
- Analyses wardrobe gaps, cost-per-wear projections, and outfit synergies
- Spending summary panel + underutilised items list

### 💎 Wardrobe ROI
- Full cost-per-wear ranking table for every item
- Visual CPW bar chart (colour-coded: Excellent → Poor)
- AI ROI analyst chat for personalised investment insights

### 📊 Analytics Dashboard
Three data science sub-sections:

**📈 Wear Patterns**
- Total wears by category (horizontal bar chart)
- Wear frequency distribution histogram (`pd.cut()` bucketing)
- Top 5 most worn vs bottom 5 least worn
- Price vs Wears scatter chart

**🔮 CPW Predictions**
- Cost-per-wear projections at 10, 20, 30, 50, 100 wears per item
- Break-even calculator (wears needed to hit $3/wear and $1/wear)
- CPW decay line chart for 4 priciest items
- Wardrobe efficiency grade (A / B / C / D) with score breakdown

**🗺️ Gap Analysis**
- Category counts vs capsule wardrobe benchmark (6 categories)
- Over / Good / Low / Gap status per category
- Occasion coverage bars (Work, Casual, Evening, Sport, Vacation)
- Colour palette chart
- 3 AI-generated recommendations (Buy Next, Donate, Quick Win)

---

##  Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.x |
| UI Framework | Streamlit `>=1.32.0` |
| AI Model | Google Gemini API (`gemini-1.5-pro`) |
| HTTP Client | `requests` `>=2.31.0` |
| Data Science | Pandas `>=2.0.0`, NumPy `>=1.24.0` |
| Frequency Analysis | `collections.Counter` |
| Charts | Streamlit native (`bar_chart`, `scatter_chart`, `line_chart`) |
| Styling | Custom CSS via `st.markdown()`, Google Fonts |
| Storage | `st.session_state` (in-memory per session) |

---

##  Getting Started

### 1. Clone or download the project
```bash
git clone https://github.com/yourusername/cherie-wardrobe.git
cd cherie-wardrobe
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a Gemini API key
1. Go to https://aistudio.google.com/app/apikey
2. Click **Create API Key**
3. Copy the key

### 4. Add your API key
Open `app.py` and replace line 12:
```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```
with your actual key
```
```

### 5. Run the app
```bash
streamlit run app.py
```

Opens at **http://localhost:8501** 

---

## Project Structure

```
cherie-wardrobe/
├── app.py               # Main Streamlit application
├── requirements.txt     # Python dependencies
└── README.md            # You are here
```

---

##  Requirements

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
```

Install with:
```bash
pip install -r requirements.txt
```

---

##  How It Works

```
User Input
    ↓
Streamlit UI (app.py)
    ↓
Wardrobe data stored in st.session_state
    ↓
AI features → requests.post() → Gemini API → reply displayed in chat
    ↓
Analytics → Pandas + NumPy compute stats → Streamlit charts render
```

---

##  Data Science Details

| Feature | Method |
|---------|--------|
| Cost-per-wear | `price / wears` |
| Wear bucketing | `pd.cut()` with 5 bins |
| Category gap | Count vs ideal benchmark dict |
| Efficiency score | Weighted grade: Excellent×4, Good×3, Fair×2, Poor×1 |
| CPW decay | `price / n` for n in [1,5,10,20,30,50,100] |
| Colour palette | `collections.Counter` on color field |
| Occasion coverage | List intersection count |


---


