"""Premium CineMatch interface for the shared recommendation engine."""

import re
from html import escape

import pandas as pd
import streamlit as st

from netflix_recommender.config import Settings
from netflix_recommender.recommender.artifacts import load_engine
from netflix_recommender.utils.exceptions import TitleNotFoundError

st.set_page_config(
    page_title="CineMatch | AI-Powered Content Discovery",
    page_icon="C",
    layout="wide",
    menu_items={
        "Get help": "https://docs.streamlit.io/",
        "Report a bug": "https://github.com/",
        "About": "CineMatch - AI-powered content discovery using content similarity.",
    },
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
        :root { --bg:#090a0c; --surface:#111317; --elevated:#171a20; --line:#272a31; --ink:#f4f1eb; --muted:#9b9da4; --accent:#f05b4f; --accent-2:#ef9a73; --green:#98c7a2; }
        .stApp { background: var(--bg); color: var(--ink); }
        .block-container { max-width: 1280px; padding: 4.8rem 3.8rem 4rem; }
        [data-testid="stHeader"] { background: transparent; }
        [data-testid="stToolbar"] { right: 1rem; }
        [data-testid="stHeader"] button[kind="header"],
        [data-testid="stHeader"] button[data-testid="stBaseButton-header"],
        [data-testid="stHeader"] button[data-testid="stBaseButton-secondary"],
        [data-testid="stHeader"] button[title="Deploy"],
        [data-testid="stHeader"] button[aria-label*="Deploy"],
        [data-testid="stHeader"] button[aria-label*="Reset"],
        [data-testid="stHeader"] .stDeployButton,
        [data-testid="stHeader"] .stAppButton {
            display:none !important;
        }
        h1,h2,h3,h4,p,span,label,button { font-family:'Manrope',sans-serif; }
        h1 { font-size:5.4rem; line-height:.93; letter-spacing:-.065em; font-weight:800; margin:0; }
        h2 { font-size:2rem; letter-spacing:-.045em; margin-bottom:.35rem; }
        h3 { letter-spacing:-.025em; }
        .mono { font-family:'DM Mono',monospace !important; text-transform:uppercase; letter-spacing:.12em; font-size:.67rem; }
        .brand { display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid var(--line); padding:.4rem 0 1.1rem; margin-bottom:3.3rem; }
        .brand-name { color:var(--ink); font-size:1.05rem; font-weight:800; letter-spacing:-.04em; }
        .brand-mark { color:var(--accent); }
        .brand-note { color:var(--muted); }
        .hero { position:relative; min-height:480px; display:flex; align-items:flex-end; padding:3.2rem 3.2rem 3rem; overflow:hidden; border:1px solid var(--line); background:radial-gradient(circle at 82% 18%, rgba(240,91,79,.36), transparent 30%), radial-gradient(circle at 70% 78%, rgba(239,154,115,.13), transparent 27%), linear-gradient(125deg,#15171d 0%,#0c0d10 54%,#251415 100%); }
        .hero:after { content:'C'; position:absolute; right:-3rem; top:-5rem; color:rgba(255,255,255,.035); font-size:32rem; line-height:1; font-weight:800; transform:rotate(12deg); }
        .hero-content { position:relative; z-index:1; max-width:720px; }
        .eyebrow { color:var(--accent-2); margin-bottom:1.4rem; }
        .hero-title { color:var(--ink); }
        .hero-title em { color:var(--accent); font-style:normal; }
        .hero-copy { color:#b6b6ba; font-size:1.04rem; line-height:1.65; max-width:600px; margin:1.4rem 0 2rem; }
        .hero-stats { display:flex; gap:2.2rem; color:var(--muted); }
        .hero-stat strong { display:block; color:var(--ink); font-size:1.25rem; font-weight:700; margin-bottom:.2rem; }
        .hero-stat span { font-size:.64rem; }
        .section-kicker { color:var(--accent-2); padding-top:1rem; border-top:1px solid var(--line); margin-top:3.1rem; }
        .section-intro { color:var(--muted); line-height:1.6; max-width:620px; }
        .control-panel { background:var(--surface); border:1px solid var(--line); padding:1.35rem 1.35rem .7rem; margin:1.6rem 0 2rem; }
        .control-panel [data-testid="stWidgetLabel"] label { color:var(--muted) !important; font-size:.75rem; }
        [data-baseweb="select"]>div, [data-testid="stTextInput"] input { background:var(--elevated); border-color:var(--line); color:var(--ink); border-radius:2px; }
        [data-testid="stTextInput"] input:focus { border-color:var(--accent); box-shadow:0 0 0 1px var(--accent); }
        .stButton>button { min-height:2.8rem; background:var(--accent); border:1px solid var(--accent); color:white; border-radius:2px; font-family:'DM Mono',monospace; text-transform:uppercase; letter-spacing:.08em; font-size:.68rem; transition:all .22s ease; }
        .stButton>button:hover { background:#ff7466; border-color:#ff7466; color:white; transform:translateY(-1px); }
        .selected-title { display:flex; gap:1.2rem; padding:1.35rem; background:var(--elevated); border:1px solid var(--line); margin-bottom:2.3rem; }
        .poster { min-width:112px; width:112px; height:164px; display:flex; align-items:flex-end; padding:.8rem; background:linear-gradient(145deg,#292d3b,#7a302b 70%,#dc765f); color:white; font-size:2.8rem; font-weight:800; letter-spacing:-.1em; }
        .poster-small { min-width:74px; width:74px; height:100px; font-size:1.7rem; }
        .meta { color:var(--muted); font-family:'DM Mono',monospace; font-size:.67rem; text-transform:uppercase; letter-spacing:.06em; line-height:1.8; }
        .description { color:#c0c0c4; line-height:1.55; margin:.8rem 0 0; }
        .result-heading { display:flex; align-items:end; justify-content:space-between; border-bottom:1px solid var(--line); padding-bottom:1rem; margin-bottom:1rem; }
        .result-heading h2 { margin:0; }
        .result-count { color:var(--muted); }
        .rec-card { height:100%; background:var(--surface); border:1px solid var(--line); overflow:hidden; transition:transform .22s ease,border-color .22s ease,box-shadow .22s ease; }
        .rec-card:hover { transform:translateY(-4px); border-color:#555963; box-shadow:0 14px 32px rgba(0,0,0,.28); }
        .rec-poster { height:190px; padding:1rem; display:flex; align-items:flex-end; color:white; font-size:2.4rem; font-weight:800; letter-spacing:-.1em; }
        .rec-body { padding:1rem; }
        .rec-title { color:var(--ink); font-size:1rem; font-weight:700; line-height:1.2; margin:.35rem 0 .4rem; }
        .rec-score { color:var(--green); font-family:'DM Mono',monospace; font-size:.68rem; text-transform:uppercase; letter-spacing:.05em; margin-top:.8rem; }
        .rec-desc { color:var(--muted); font-size:.78rem; line-height:1.45; margin-top:.7rem; min-height:3.4rem; }
        .catalog-card { display:flex; gap:1rem; background:var(--surface); border:1px solid var(--line); padding:1rem; margin-bottom:.8rem; align-items:center; }
        .catalog-info { flex:1; min-width:0; }
        .catalog-info h3 { color:var(--ink); margin:0 0 .3rem; font-size:1rem; }
        .catalog-info p { color:var(--muted); font-size:.82rem; line-height:1.4; margin:.45rem 0 0; }
        .pill { display:inline-block; color:var(--accent-2); border:1px solid rgba(239,154,115,.35); padding:.2rem .45rem; font-family:'DM Mono',monospace; font-size:.6rem; text-transform:uppercase; }
        .about-step { border-top:1px solid var(--line); padding:1.25rem 0; display:flex; gap:1.4rem; }
        .about-step .num { color:var(--accent); font-family:'DM Mono',monospace; font-size:.75rem; }
        .about-step h3 { margin:0 0 .25rem; color:var(--ink); font-size:1.05rem; }
        .about-step p { color:var(--muted); margin:0; line-height:1.5; }
        .trust { background:var(--surface); border-left:3px solid var(--accent); padding:1.3rem 1.4rem; color:var(--muted); line-height:1.6; }
        .trust strong { color:var(--ink); }
        .empty-state { border:1px dashed var(--line); padding:3rem 1.5rem; text-align:center; color:var(--muted); }
        footer { visibility:hidden; }
        @media (max-width: 700px) { .block-container { padding:4.5rem 1rem 3rem; } .brand { margin-bottom:1.8rem; } .brand-note { display:none; } .hero { min-height:520px; padding:2rem 1.4rem; } .hero:after { right:-3.5rem; top:1rem; font-size:16rem; } .hero-stats { gap:1.2rem; flex-wrap:wrap; } .nav-tabs { margin:-1.1rem .4rem 2rem; } .nav-tabs [data-testid="stHorizontalBlock"] { width:100%; } .nav-tabs .stButton>button { padding:.5rem .25rem; font-size:.58rem; } .selected-title { align-items:flex-start; } .poster { min-width:84px; width:84px; height:125px; font-size:2rem; } .rec-poster { height:150px; } h1 { font-size:3.4rem; } h2 { font-size:1.65rem; } }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.get("theme", "dark") == "light":
        st.markdown(
            """
            <style>
            :root { --bg:#f4f1eb; --surface:#ffffff; --elevated:#ebe7df; --line:#d8d2c8; --ink:#151619; --muted:#67676c; --accent:#c53e35; --accent-2:#9c4c3b; --green:#39734a; }
            .stApp { background:var(--bg); }
            .hero { background:radial-gradient(circle at 82% 18%, rgba(240,91,79,.24), transparent 30%), linear-gradient(125deg,#fffdf8 0%,#eee9e1 54%,#f2deda 100%); }
            .hero:after { color:rgba(17,18,20,.05); }
            .hero-copy, .description, .rec-desc { color:#5d5c60; }
            [data-baseweb="select"]>div, [data-testid="stTextInput"] input { background:var(--surface); color:var(--ink); }
            </style>
            """,
            unsafe_allow_html=True,
        )


def safe(value: object) -> str:
    return escape(str(value)) if value is not None and not pd.isna(value) else ""


def initials(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title)
    return "".join(word[0] for word in words[:2]).upper() or "C"


def gradient(index: int) -> str:
    palettes = ["linear-gradient(145deg,#292d3b,#7a302b 70%,#dc765f)", "linear-gradient(145deg,#172d39,#315875 60%,#d18468)", "linear-gradient(145deg,#382a3d,#71394e 60%,#d79a75)", "linear-gradient(145deg,#172f2d,#356657 60%,#d8a05e)"]
    return palettes[index % len(palettes)]


def render_poster(title: str, index: int, small: bool = False) -> str:
    class_name = "poster poster-small" if small else "poster"
    return f'<div class="{class_name}" style="background:{gradient(index)}">{safe(initials(title))}</div>'


def metadata(row: pd.Series) -> str:
    values = [row.get("type"), row.get("release_year"), row.get("rating"), row.get("duration")]
    return " / ".join(safe(value) for value in values if value is not None and not pd.isna(value) and str(value).strip())


def render_card(item: dict[str, object], index: int, key_prefix: str = "rec") -> None:
    title = str(item["title"])
    row = catalog[catalog["title"].astype(str).str.casefold() == title.casefold()].iloc[0]
    st.markdown(
        f"""
        <div class="rec-card">
          <div class="rec-poster" style="background:{gradient(index)}">{safe(initials(title))}</div>
          <div class="rec-body">
            <div class="meta">{metadata(row)}</div>
            <div class="rec-title">{safe(title)}</div>
            <div class="meta">{safe(item.get('listed_in') or row.get('listed_in') or 'Catalog match')}</div>
            <div class="rec-score">{float(item.get('similarity_score', 0)):.1%} content similarity</div>
            <div class="rec-desc">{safe(item.get('description') or row.get('description') or 'No description available.')}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("View details", key=f"{key_prefix}-{title}", use_container_width=True):
        st.session_state["detail_title"] = title
        st.session_state["nav"] = "Home"
        st.rerun()


def render_detail(title: str) -> None:
    matches = catalog[catalog["title"].astype(str).str.casefold() == title.casefold()]
    if matches.empty:
        return
    row = matches.iloc[0]
    st.markdown('<div class="section-kicker mono">Title details</div>', unsafe_allow_html=True)
    left, right = st.columns([1, 2.4], gap="large")
    with left:
        st.markdown(render_poster(title, int(row.name)), unsafe_allow_html=True)
    with right:
        st.markdown(f"<h2>{safe(title)}</h2><div class='meta'>{metadata(row)}</div><p class='pill'>{safe(row.get('listed_in') or 'Catalog')}</p><p class='description'>{safe(row.get('description') or 'No description available.')}</p>", unsafe_allow_html=True)
        details = " / ".join(f"{label}: {safe(row.get(field))}" for label, field in (("Director", "director"), ("Cast", "cast"), ("Country", "country")) if row.get(field))
        if details:
            st.markdown(f"<p class='meta' style='margin-top:1.2rem'>{details}</p>", unsafe_allow_html=True)
        if st.button("Find more like this", type="primary", key="detail-recommend"):
            st.session_state["recommend_title"] = title
            st.session_state["detail_title"] = None
            st.rerun()


def render_home() -> None:
    st.markdown(
        f"""
        <section class="hero"><div class="hero-content">
          <div class="eyebrow mono">AI-powered content discovery</div>
          <h1 class="hero-title">Find something<br>you'll <em>love next.</em></h1>
          <p class="hero-copy">CineMatch studies the content you already like and surfaces movies and shows with a similar creative DNA. No ratings theater. Just thoughtful discovery.</p>
          <div class="hero-stats"><div class="hero-stat"><strong>{len(catalog)}</strong><span class="mono">Titles indexed</span></div><div class="hero-stat"><strong>TF-IDF</strong><span class="mono">Content model</span></div><div class="hero-stat"><strong>Fast</strong><span class="mono">Offline artifacts</span></div></div>
        </div></section>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-kicker mono">Start a discovery session</div><h2>What are you watching?</h2><p class="section-intro">Pick a title from the catalog. CineMatch will compare its genre, people, format, and description with every other indexed title.</p>', unsafe_allow_html=True)
    search = st.text_input("Search the catalog", placeholder="Search movies, shows, genres...", label_visibility="collapsed")
    search_term = search.casefold().strip()
    options = [title for title in engine.titles() if search_term in title.casefold()]
    if not options:
        st.markdown('<div class="empty-state">We could not find that title. Try a different search.</div>', unsafe_allow_html=True)
        return
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    current = st.session_state.get("recommend_title") or options[0]
    title = st.selectbox("Choose a title", options, index=options.index(current) if current in options else 0)
    top_n = st.slider("Number of recommendations", 1, min(settings.max_top_n, 12), 5)
    if st.button("Find similar titles", type="primary", use_container_width=True):
        st.session_state["recommend_title"] = title
        st.session_state["detail_title"] = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    if st.session_state.get("detail_title"):
        render_detail(st.session_state["detail_title"])
        return
    if st.session_state.get("recommend_title"):
        try:
            recommendations = engine.recommend(st.session_state["recommend_title"], top_n)
        except TitleNotFoundError:
            st.error("We could not find that title. Try searching for another movie or show.")
            return
        st.markdown(f'<div class="result-heading"><h2>More like {safe(st.session_state["recommend_title"])}</h2><span class="result-count mono">{len(recommendations)} matches</span></div>', unsafe_allow_html=True)
        columns = st.columns(min(4, max(1, len(recommendations))), gap="medium")
        for index, item in enumerate(recommendations):
            with columns[index % len(columns)]:
                render_card(item, index)
    else:
        st.markdown('<div class="empty-state">Choose a title above and we will build your first shortlist.</div>', unsafe_allow_html=True)


def render_explore() -> None:
    st.markdown('<div class="section-kicker mono">The catalog</div><h2>Explore the collection.</h2><p class="section-intro">Browse every indexed title, then open a detail view to continue your discovery loop.</p>', unsafe_allow_html=True)
    first, second, third = st.columns([2, 1, 1])
    with first:
        search = st.text_input("Search", placeholder="Search titles or descriptions", label_visibility="collapsed")
    with second:
        kind = st.selectbox("Type", ["All", "Movie", "TV Show"], label_visibility="collapsed")
    with third:
        sort = st.selectbox("Sort", ["Newest", "A-Z", "Oldest"], label_visibility="collapsed")
    filtered = catalog.copy()
    if search:
        term = search.casefold()
        filtered = filtered[filtered.apply(lambda row: term in " ".join(str(value) for value in row.values).casefold(), axis=1)]
    if kind != "All":
        filtered = filtered[filtered["type"] == kind]
    if sort == "A-Z":
        filtered = filtered.sort_values("title")
    elif sort == "Oldest":
        filtered = filtered.sort_values("release_year")
    else:
        filtered = filtered.sort_values("release_year", ascending=False)
    st.markdown(f'<p class="meta" style="margin:1.5rem 0">{len(filtered)} titles found</p>', unsafe_allow_html=True)
    for index, (_, row) in enumerate(filtered.iterrows()):
        title = str(row["title"])
        left, middle, right = st.columns([.75, 3.3, 1])
        with left:
            st.markdown(render_poster(title, index, small=True), unsafe_allow_html=True)
        with middle:
            st.markdown(f'<div class="catalog-info"><h3>{safe(title)}</h3><span class="pill">{safe(row.get("type") or "Title")}</span><p>{safe(row.get("listed_in") or "Catalog entry")} / {safe(row.get("release_year") or "Year unavailable")}</p><p>{safe(row.get("description") or "No description available.")}</p></div>', unsafe_allow_html=True)
        with right:
            if st.button("View", key=f"explore-{title}", use_container_width=True):
                st.session_state["detail_title"] = title
                st.session_state["nav"] = "Home"
                st.rerun()


def render_about() -> None:
    st.markdown('<div class="section-kicker mono">The method</div><h2>Intelligence you can understand.</h2><p class="section-intro">CineMatch uses a content-based model. It looks at what a title is made of, not at private behavior or invented ratings.</p>', unsafe_allow_html=True)
    steps = [("01", "Choose a title", "Start with a movie or show already in the catalog."), ("02", "Read the content", "Genres, format, creators, cast, country, rating, and description become one content profile."), ("03", "Build vectors", "TF-IDF turns each profile into a sparse numerical representation."), ("04", "Compare", "Cosine similarity measures how closely two content vectors point in the same direction."), ("05", "Rank", "The highest-scoring alternatives are returned, excluding the title you started from.")]
    for number, heading, body in steps:
        st.markdown(f'<div class="about-step"><div class="num">{number}</div><div><h3>{heading}</h3><p>{body}</p></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker mono">Trust note</div><div class="trust"><strong>Similarity is not a promise.</strong><br>Scores describe overlap in catalog metadata. They are not a probability that you will enjoy a title, and this demo does not claim personal recommendations without user history.</div>', unsafe_allow_html=True)


settings = Settings.from_environment()
if not settings.artifact_path.exists():
    st.error("The recommendation service is not ready. Build the catalog artifact first.")
    st.stop()

engine = load_engine(settings.artifact_path)
catalog = engine.metadata
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"
theme_left, theme_right = st.columns([5, 1])
with theme_left:
    st.markdown('<div class="brand"><div class="brand-name">Cine<span class="brand-mark">Match</span></div><div class="brand-note mono">AI-powered content discovery</div></div>', unsafe_allow_html=True)
with theme_right:
    selected_theme = st.segmented_control(
        "Theme",
        options=["Dark", "Light"],
        default="Dark" if st.session_state["theme"] == "dark" else "Light",
        key="theme_selector",
        label_visibility="collapsed",
    )
    if selected_theme:
        st.session_state["theme"] = selected_theme.casefold()
inject_styles()

if "nav" not in st.session_state:
    st.session_state["nav"] = "Home"
nav_options = ["Home", "Explore", "How it works"]
nav_columns = st.columns(3)
for column, option in zip(nav_columns, nav_options):
    with column:
        if st.button(option, key=f"nav-{option}", use_container_width=True):
            st.session_state["nav"] = option
            st.rerun()

if st.session_state["nav"] == "Explore":
    render_explore()
elif st.session_state["nav"] == "How it works":
    render_about()
else:
    render_home()

st.markdown('<div class="section-kicker mono">CineMatch</div><p class="meta">A metadata-based discovery experience built with FastAPI, Streamlit, and a transparent TF-IDF similarity engine.</p>', unsafe_allow_html=True)
