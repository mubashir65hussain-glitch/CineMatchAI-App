import streamlit as st
import pandas as pd
import json
import time
import requests
import os
import gdown

st.set_page_config(page_title="CineMatch AI", page_icon="🎬", layout="wide")

API_KEY = "551b8458f2a0099769f4b2532e55b0f0"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Raleway:wght@200;300;400;600&display=swap');
    * { margin:0; padding:0; box-sizing:border-box; }
    .stApp {
        background-color: #0a0a0a;
        background-image:
            radial-gradient(ellipse 120% 60% at 50% -10%, rgba(229,9,20,0.10) 0%, transparent 65%),
            radial-gradient(ellipse 50% 40% at 0% 50%, rgba(255,255,255,0.025) 0%, transparent 55%),
            radial-gradient(ellipse 50% 40% at 100% 50%, rgba(255,255,255,0.025) 0%, transparent 55%);
        color: white;
        font-family: 'Raleway', sans-serif;
    }
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
    .block-container { padding-top: 0 !important; max-width: 100% !important; }
    .hero { position: relative; padding: 110px 20px 90px; text-align: center; }
    .hero-top-line { position: absolute; top: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(229,9,20,0.4), transparent); }
    .hero-bottom-line { position: absolute; bottom: 0; left: 0; right: 0; height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent); }
    .hero-red-glow { position: absolute; top: -20px; left: 50%; transform: translateX(-50%); width: 500px; height: 250px; background: radial-gradient(ellipse, rgba(229,9,20,0.14) 0%, transparent 70%); pointer-events: none; filter: blur(40px); }
    .hero-badge { display: inline-block; font-family: 'Raleway', sans-serif; font-size: 9px; font-weight: 600; letter-spacing: 5px; color: rgba(229,9,20,0.75); text-transform: uppercase; border: 1px solid rgba(229,9,20,0.18); padding: 6px 18px; border-radius: 20px; background: rgba(229,9,20,0.05); margin-bottom: 32px; }
    .hero-title { font-family: 'Playfair Display', serif; font-size: 130px; font-weight: 700; letter-spacing: 20px; line-height: 1; margin-bottom: 24px; background: linear-gradient(180deg, #ffffff 20%, rgba(255,255,255,0.5) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; filter: drop-shadow(0 0 60px rgba(229,9,20,0.18)); }
    .hero-divider { width: 36px; height: 1px; background: linear-gradient(90deg, transparent, rgba(229,9,20,0.55), transparent); margin: 0 auto 22px; }
    .hero-system { font-family: 'Raleway', sans-serif; font-size: 11px; font-weight: 400; letter-spacing: 5px; color: rgba(255,255,255,0.25); text-transform: uppercase; margin-top: 20px; }
    .mood-hint { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 16px 20px; margin-bottom: 16px; display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }
    .mood-hint-label { font-family: 'Raleway', sans-serif; font-size: 8px; font-weight: 600; letter-spacing: 3px; text-transform: uppercase; color: rgba(255,255,255,0.2); width: 100%; text-align: center; margin-bottom: 8px; }
    .mood-chip { font-family: 'Raleway', sans-serif; font-size: 9px; font-weight: 500; letter-spacing: 2px; text-transform: uppercase; color: rgba(255,255,255,0.35); border: 1px solid rgba(255,255,255,0.07); padding: 6px 14px; border-radius: 20px; background: rgba(255,255,255,0.02); }
    .mood-chip-red { font-family: 'Raleway', sans-serif; font-size: 9px; font-weight: 500; letter-spacing: 2px; text-transform: uppercase; color: rgba(229,9,20,0.6); border: 1px solid rgba(229,9,20,0.15); padding: 6px 14px; border-radius: 20px; background: rgba(229,9,20,0.04); }
    .input-card { max-width: 580px; margin: 44px auto 0; background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07); border-radius: 16px; padding: 34px 32px; box-shadow: 0 24px 70px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.05); }
    .stTextInput > div > input { background: rgba(255,255,255,0.035) !important; color: rgba(255,255,255,0.85) !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 10px !important; font-family: 'Raleway', sans-serif !important; font-size: 14px !important; font-weight: 300 !important; padding: 14px 18px !important; box-shadow: inset 0 2px 10px rgba(0,0,0,0.3) !important; transition: all 0.3s ease !important; }
    .stTextInput > div > input:focus { border-color: rgba(229,9,20,0.4) !important; box-shadow: 0 0 0 3px rgba(229,9,20,0.07), inset 0 2px 10px rgba(0,0,0,0.3) !important; }
    .stTextInput label { color: rgba(255,255,255,0.2) !important; font-family: 'Raleway', sans-serif !important; font-size: 9px !important; font-weight: 600 !important; letter-spacing: 4px !important; text-transform: uppercase !important; }
    div[data-baseweb="select"] { background: rgba(255,255,255,0.035) !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 10px !important; }
    .stSelectbox label { color: rgba(255,255,255,0.2) !important; font-family: 'Raleway', sans-serif !important; font-size: 9px !important; font-weight: 600 !important; letter-spacing: 4px !important; text-transform: uppercase !important; }
    .stButton > button { background: linear-gradient(135deg, #E50914 0%, #b20710 100%) !important; color: white !important; border: none !important; padding: 15px 40px !important; font-family: 'Raleway', sans-serif !important; font-size: 9px !important; font-weight: 700 !important; letter-spacing: 5px !important; text-transform: uppercase !important; border-radius: 8px !important; width: 100% !important; margin-top: 20px !important; box-shadow: 0 8px 28px rgba(229,9,20,0.38) !important; transition: all 0.3s ease !important; }
    .or-divider { font-family: 'Raleway', sans-serif; font-size: 9px; letter-spacing: 4px; color: rgba(255,255,255,0.1); text-align: center; margin: 16px 0; text-transform: uppercase; }
    .detected { font-family: 'Raleway', sans-serif; font-size: 9px; font-weight: 600; color: rgba(229,9,20,0.8); letter-spacing: 4px; text-transform: uppercase; text-align: center; padding: 12px 20px; border: 1px solid rgba(229,9,20,0.15); border-radius: 8px; background: rgba(229,9,20,0.04); margin: 14px 0 0; }
    .ai-thinking { font-family: 'Raleway', sans-serif; font-size: 11px; font-weight: 300; letter-spacing: 4px; color: rgba(229,9,20,0.6); text-transform: uppercase; text-align: center; margin: 20px 0; }
    .results-header { padding: 60px 0 28px; }
    .results-title { font-family: 'Playfair Display', serif; font-size: 30px; color: rgba(255,255,255,0.9); font-weight: 700; margin-bottom: 10px; }
    .results-meta { display: flex; gap: 16px; align-items: center; flex-wrap: wrap; }
    .results-badge { font-family: 'Raleway', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; padding: 6px 16px; border-radius: 20px; }
    .results-badge-count { color: white; background: rgba(229,9,20,0.8); border: 1px solid rgba(229,9,20,0.5); }
    .results-badge-genre { color: rgba(255,255,255,0.7); background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); }
    .results-badge-ai { color: rgba(229,9,20,0.7); background: rgba(229,9,20,0.04); border: 1px solid rgba(229,9,20,0.15); }
    .mcard { background: rgba(255,255,255,0.03); border-radius: 10px; overflow: hidden; border: 1px solid rgba(255,255,255,0.06); margin-bottom: 24px; box-shadow: 0 8px 30px rgba(0,0,0,0.45); transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease; }
    .mcard:hover { transform: translateY(-6px); box-shadow: 0 20px 50px rgba(0,0,0,0.7); border-color: rgba(229,9,20,0.2); }
    .poster-wrap { position: relative; display: block; overflow: hidden; }
    .poster-wrap img { display: block; width: 100%; }
    .poster-overlay { position: absolute; inset: 0; background: rgba(0,0,0,0); display: flex; align-items: center; justify-content: center; transition: background 0.3s ease; }
    .poster-wrap:hover .poster-overlay { background: rgba(0,0,0,0.55); }
    .play-btn { width: 56px; height: 56px; border-radius: 50%; background: rgba(229,9,20,0.9); display: flex; align-items: center; justify-content: center; opacity: 0; transform: scale(0.8); transition: opacity 0.3s ease, transform 0.3s ease; box-shadow: 0 0 30px rgba(229,9,20,0.6); }
    .poster-wrap:hover .play-btn { opacity: 1; transform: scale(1); }
    .play-icon { width: 0; height: 0; border-top: 10px solid transparent; border-bottom: 10px solid transparent; border-left: 16px solid white; margin-left: 4px; }
    .minfo { padding: 12px 14px 14px; }
    .mtitle { font-family: 'Playfair Display', serif; color: rgba(255,255,255,0.9); font-size: 14px; font-weight: 700; margin-bottom: 6px; line-height: 1.3; }
    .mrow { display: flex; align-items: center; gap: 8px; margin-bottom: 5px; flex-wrap: wrap; }
    .myear { font-family: 'Raleway', sans-serif; color: rgba(255,255,255,0.25); font-size: 9px; letter-spacing: 2px; border: 1px solid rgba(255,255,255,0.08); padding: 2px 8px; border-radius: 10px; }
    .mrating { font-family: 'Raleway', sans-serif; color: #c9a84c; font-size: 11px; font-weight: 600; letter-spacing: 1px; }
    .mgenre { font-family: 'Raleway', sans-serif; color: rgba(255,255,255,0.2); font-size: 8px; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 7px; }
    .moverview { font-family: 'Raleway', sans-serif; color: rgba(255,255,255,0.3); font-size: 11px; line-height: 1.7; font-weight: 300; margin-bottom: 10px; border-top: 1px solid rgba(255,255,255,0.04); padding-top: 8px; }
    .mai-reason { font-family: 'Raleway', sans-serif; font-size: 9px; font-weight: 500; color: rgba(229,9,20,0.45); letter-spacing: 1px; }
    .detail-title { font-family: 'Playfair Display', serif; font-size: 52px; font-weight: 700; color: white; line-height: 1.1; margin-bottom: 16px; }
    .detail-meta { font-family: 'Raleway', sans-serif; font-size: 10px; font-weight: 600; letter-spacing: 3px; color: rgba(255,255,255,0.3); text-transform: uppercase; margin-bottom: 20px; }
    .detail-rating { font-family: 'Raleway', sans-serif; font-size: 18px; color: #c9a84c; font-weight: 600; margin-bottom: 20px; }
    .detail-overview { font-family: 'Raleway', sans-serif; font-size: 15px; font-weight: 300; color: rgba(255,255,255,0.55); line-height: 1.8; margin-bottom: 30px; max-width: 600px; }
    .detail-tag { display: inline-block; font-family: 'Raleway', sans-serif; font-size: 9px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: rgba(229,9,20,0.7); border: 1px solid rgba(229,9,20,0.2); padding: 5px 14px; border-radius: 20px; background: rgba(229,9,20,0.05); margin: 3px; }
    .watch-trailer-detail { display: inline-block; font-family: 'Raleway', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 4px; text-transform: uppercase; color: white; background: linear-gradient(135deg, #E50914, #b20710); border: none; padding: 14px 32px; border-radius: 8px; text-decoration: none; margin-top: 16px; box-shadow: 0 6px 20px rgba(229,9,20,0.4); cursor: pointer; }
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #090909; }
    ::-webkit-scrollbar-thumb { background: #1a1a1a; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    if not os.path.exists("tmdb_5000_movies.csv"):
        gdown.download("https://drive.google.com/uc?id=1RX7i98JNer4pqcy0NqHxDWYLTOdKfM6m", "tmdb_5000_movies.csv", quiet=False)
    df = pd.read_csv("tmdb_5000_movies.csv")
    def get_genres(g):
        try: return ", ".join([x['name'] for x in json.loads(g)])
        except: return ""
    df['clean_genres'] = df['genres'].apply(get_genres)
    df['year'] = pd.to_datetime(df['release_date'], errors='coerce').dt.year.fillna(0).astype(int)
    return df

df = load_data()

@st.cache_data
def get_poster(movie_id):
    try:
        r = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}", timeout=3)
        p = r.json().get('poster_path')
        return f"https://image.tmdb.org/t/p/w300{p}" if p else None
    except:
        return None

@st.cache_data
def get_movie_details(movie_id):
    try:
        r = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits", timeout=5)
        return r.json()
    except:
        return {}

@st.cache_data
def get_trailer(movie_id):
    try:
        r = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}", timeout=3)
        for v in r.json().get('results', []):
            if v.get('type') == 'Trailer' and v.get('site') == 'YouTube':
                return f"https://www.youtube.com/watch?v={v['key']}"
        return None
    except:
        return None

@st.cache_data
def get_live_movies(genre_id):
    genre_map = {"Comedy":35,"Drama":18,"Romance":10749,"Action":28,"Horror":27,"Adventure":12,"Documentary":99}
    gid = genre_map.get(genre_id, 18)
    movies = []
    for page in range(1, 6):
        try:
            r = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={gid}&sort_by=primary_release_date.desc&primary_release_date.gte=2020-01-01&vote_count.gte=50&page={page}", timeout=5)
            for m in r.json().get('results', []):
                movies.append({'id':m.get('id'),'title':m.get('title',''),'overview':m.get('overview',''),'vote_average':m.get('vote_average',0),'year':int(m.get('release_date','0000')[:4]) if m.get('release_date') else 0,'clean_genres':genre_id,'poster_path':m.get('poster_path','')})
        except:
            pass
    return pd.DataFrame(movies)

def detect_mood(text):
    t = text.lower()
    if any(w in t for w in ["happy","joy","excited","fun","laugh","great","amazing","good","cheerful"]): return "Comedy","Feel-good films matched to your happy mood."
    elif any(w in t for w in ["sad","cry","depressed","lonely","alone","empty","heartbreak","miss","tears"]): return "Drama","Emotionally rich films that resonate with how you feel."
    elif any(w in t for w in ["love","romantic","romance","crush","heart","date","relationship","sweet"]): return "Romance","Perfect films for when love is on your mind."
    elif any(w in t for w in ["action","fight","thrill","exciting","hero","war","battle","intense"]): return "Action","High-energy films that match your intense mood."
    elif any(w in t for w in ["scared","horror","fear","creepy","dark","ghost","monster","nightmare"]): return "Horror","Chilling films for your horror mood tonight."
    elif any(w in t for w in ["adventure","explore","travel","journey","discover","wild","quest"]): return "Adventure","Epic journeys matched to your adventurous spirit."
    elif any(w in t for w in ["motivated","inspire","focus","productive","learn","grow","success"]): return "Documentary","Powerful films to fuel your drive."
    else: return "Drama","Thoughtful films recommended based on your mood."

mood_genre = {"Happy":"Comedy","Sad":"Drama","Romantic":"Romance","Action":"Action","Horror":"Horror","Adventurous":"Adventure","Motivated":"Documentary"}
mood_reason = {"Happy":"Feel-good films matched to your happy mood.","Sad":"Emotionally rich films that resonate with how you feel.","Romantic":"Perfect films for when love is on your mind.","Action":"High-energy films that match your intense mood.","Horror":"Chilling films for your horror mood tonight.","Adventurous":"Epic journeys matched to your adventurous spirit.","Motivated":"Powerful films to fuel your drive and ambition."}

if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None
if 'is_live' not in st.session_state:
    st.session_state.is_live = False

# ── DETAIL PAGE ──
if st.session_state.selected_movie is not None:
    movie = st.session_state.selected_movie
    if st.button("Back to Results"):
        st.session_state.selected_movie = None
        st.session_state.is_live = False
        st.rerun()
    details = get_movie_details(movie['id'])
    poster_path = details.get('poster_path')
    poster_url = f"https://image.tmdb.org/t/p/w400{poster_path}" if poster_path else None
    trailer_url = get_trailer(movie['id'])
    col1, col2 = st.columns([1, 2])
    with col1:
        if poster_url:
            st.image(poster_url, use_container_width=True)
    with col2:
        yr = movie.get('year', '')
        runtime = details.get('runtime', '')
        language = details.get('original_language', '').upper()
        budget = details.get('budget', 0)
        revenue = details.get('revenue', 0)
        cast = details.get('credits', {}).get('cast', [])
        top_cast = ", ".join([c['name'] for c in cast[:5]])
        genres_list = details.get('genres', [])
        genres_html = "".join([f'<span class="detail-tag">{g["name"]}</span>' for g in genres_list])
        st.markdown(f'<div class="detail-title">{movie["title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-meta">{yr} &nbsp;·&nbsp; {runtime} min &nbsp;·&nbsp; {language}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-rating">★ {round(float(movie.get("vote_average", 0)), 1)} / 10</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="detail-overview">{movie.get("overview", "")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="margin-bottom:16px;">{genres_html}</div>', unsafe_allow_html=True)
        if top_cast:
            st.markdown(f'<div class="detail-meta">Cast — {top_cast}</div>', unsafe_allow_html=True)
        if budget and budget > 0:
            st.markdown(f'<div class="detail-meta" style="margin-top:10px;">Budget — ${budget:,} &nbsp;·&nbsp; Revenue — ${revenue:,}</div>', unsafe_allow_html=True)
        if trailer_url:
            st.markdown(f'<a href="{trailer_url}" target="_blank" class="watch-trailer-detail">Watch Trailer</a>', unsafe_allow_html=True)
    st.stop()

# ── HERO ──
st.markdown("""
<div class="hero">
  <div class="hero-top-line"></div>
  <div class="hero-bottom-line"></div>
  <div class="hero-red-glow"></div>
  <div class="hero-badge">AI Powered Movie Discovery</div>
  <h1 class="hero-title">CINEMATCH</h1>
  <div class="hero-divider"></div>
  <div style="display:flex; justify-content:center; gap:12px; margin-bottom:20px; flex-wrap:wrap;">
    <div style="font-family:'Raleway',sans-serif; font-size:10px; font-weight:600; letter-spacing:3px; color:rgba(255,255,255,0.5); text-transform:uppercase; border:1px solid rgba(255,255,255,0.08); padding:10px 24px; border-radius:30px; background:rgba(255,255,255,0.03);">Your Mood</div>
    <div style="font-family:'Raleway',sans-serif; font-size:10px; font-weight:600; letter-spacing:3px; color:rgba(229,9,20,0.8); text-transform:uppercase; border:1px solid rgba(229,9,20,0.2); padding:10px 24px; border-radius:30px; background:rgba(229,9,20,0.05);">Your Movie</div>
    <div style="font-family:'Raleway',sans-serif; font-size:10px; font-weight:600; letter-spacing:3px; color:rgba(255,255,255,0.5); text-transform:uppercase; border:1px solid rgba(255,255,255,0.08); padding:10px 24px; border-radius:30px; background:rgba(255,255,255,0.03);">Your Night</div>
  </div>
  <p class="hero-system">Mood Based Movie Recommendation System</p>
</div>
""", unsafe_allow_html=True)

# ── INPUT ──
_, col, _ = st.columns([1, 1.4, 1])
with col:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="mood-hint">
        <div class="mood-hint-label">Try saying something like</div>
        <span class="mood-chip-red">I feel lonely tonight</span>
        <span class="mood-chip">Show me something exciting</span>
        <span class="mood-chip-red">I want to cry</span>
        <span class="mood-chip">Something romantic</span>
        <span class="mood-chip-red">I need motivation</span>
        <span class="mood-chip">Scary movies</span>
    </div>
    """, unsafe_allow_html=True)
    user_text = st.text_input("", placeholder="e.g.  I am feeling lonely tonight...")
    st.markdown('<p class="or-divider">— or select your mood —</p>', unsafe_allow_html=True)
    mood = st.selectbox("", ["Happy","Sad","Romantic","Action","Horror","Adventurous","Motivated"])
    discover = st.button("Discover Movies")
    if user_text and len(user_text) > 2:
        genre, reason = detect_mood(user_text)
        st.markdown(f'<p class="detected">AI detected — {genre}</p>', unsafe_allow_html=True)
    else:
        genre = mood_genre[mood]
        reason = mood_reason[mood]
    st.markdown('</div>', unsafe_allow_html=True)

if discover:
    placeholder = st.empty()
    for msg in ["Analyzing your cinematic mood","Searching through 5000 films","Curating your perfect picks"]:
        placeholder.markdown(f'<p class="ai-thinking">{msg}...</p>', unsafe_allow_html=True)
        time.sleep(0.6)
    placeholder.empty()

# ── MOVIES ──
filtered = df[df['clean_genres'].str.contains(genre, na=False)]
filtered = filtered.drop_duplicates(subset=['title'])
classics = filtered[filtered['year'] < 2020].sort_values('vote_average', ascending=False).head(20)
live_movies = get_live_movies(genre)

if not live_movies.empty:
    live_movies = live_movies.drop_duplicates(subset=['title'])
    all_movies = pd.concat([live_movies.head(80), classics]).drop_duplicates(subset=['title']).head(100)
else:
    all_movies = classics.head(100)

live_count = min(80, len(live_movies)) if not live_movies.empty else 0
is_live_list = [True]*live_count + [False]*(len(all_movies)-live_count)

st.markdown(f"""
<div class="results-header">
  <p class="results-title">Top Picks for You</p>
  <div class="results-meta">
    <span class="results-badge results-badge-count">{len(all_movies)} Films</span>
    <span class="results-badge results-badge-genre">{genre}</span>
    <span class="results-badge results-badge-ai">Curated by AI</span>
  </div>
</div>
""", unsafe_allow_html=True)

cols = st.columns(4)
for i, (_, movie) in enumerate(all_movies.iterrows()):
    with cols[i % 4]:
        live = is_live_list[i] if i < len(is_live_list) else False
        if live and movie.get('poster_path'):
            poster = f"https://image.tmdb.org/t/p/w300{movie['poster_path']}"
        else:
            poster = get_poster(movie['id'])
        yr = movie['year'] if movie['year'] != 0 else ""
        trailer = get_trailer(movie['id'])
        if poster:
            if trailer:
                poster_html = f"""<a href="{trailer}" target="_blank" class="poster-wrap"><img src="{poster}" style="width:100%; display:block; border-radius:0;"><div class="poster-overlay"><div class="play-btn"><div class="play-icon"></div></div></div></a>"""
            else:
                poster_html = f'<div class="poster-wrap"><img src="{poster}" style="width:100%; display:block; border-radius:0;"></div>'
        else:
            poster_html = "<div style='background:#111;height:210px;'></div>"
        st.markdown(f'<div class="mcard">', unsafe_allow_html=True)
        st.markdown(poster_html, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="minfo">
          <div class="mtitle">{movie['title']}</div>
          <div class="mrow">
            <span class="mrating">★ {round(float(movie.get('vote_average',0)),1)}</span>
            <span class="myear">{yr}</span>
          </div>
          <div class="mgenre">{str(movie.get('clean_genres',''))[:35]}</div>
          <div class="moverview">{str(movie.get('overview',''))[:110]}...</div>
          <div class="mai-reason">AI — {reason}</div>
        </div></div>""", unsafe_allow_html=True)
        if st.button("View Details", key=f"btn_{i}"):
            st.session_state.selected_movie = movie.to_dict()
            st.session_state.is_live = live
            st.rerun()