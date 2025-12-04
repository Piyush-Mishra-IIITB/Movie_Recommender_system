import streamlit as st
import pickle
import pandas as pd
import requests
import time

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("Movie Recommender System with Posters")

# -------------------- Load Data -------------------- #
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

API_KEY = "3b1338bf76b7e21320c753103b4d3e21"  # Replace with your TMDB API key

# -------------------- Cached TMDB API Calls -------------------- #
@st.cache_data
def get_movie_id(title):
    """Fetch TMDB movie ID by title with retry logic."""
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    for _ in range(3):  # retry 3 times
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            results = data.get('results')
            if results:
                return results[0]['id']
            return None
        except requests.exceptions.RequestException:
            time.sleep(1)
    return None

@st.cache_data
def fetch_poster(movie_id):
    """Fetch poster URL from TMDB movie ID with retry logic."""
    if movie_id is None:
        return None
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    for _ in range(3):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path
            return None
        except requests.exceptions.RequestException:
            time.sleep(1)
    return None

# -------------------- Recommendation Function -------------------- #
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        title = movies.iloc[i[0]]['title']
        recommended_movies.append(title)
        movie_id = get_movie_id(title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# -------------------- Streamlit UI -------------------- #
selected_movie = st.selectbox("Select a movie you like", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    st.subheader(f"Movies similar to **{selected_movie}**:")

    # Display movies in a row with responsive width
    cols = st.columns(len(names))
    for col, name, poster in zip(cols, names, posters):
        with col:
            if poster:
                st.image(poster, width=200)  # fixed width to avoid deprecation warning
            st.caption(name)
