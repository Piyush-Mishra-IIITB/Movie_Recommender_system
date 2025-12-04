# Movie Recommender System with Posters (Streamlit + TMDB API)

This project is an interactive Movie Recommendation System built using Machine Learning, Cosine Similarity, and Streamlit. It recommends the top 5 movies similar to a selected movie and displays high-quality posters fetched directly from the TMDB API.

The system uses a content-based filtering approach, where recommendations are generated using a precomputed similarity matrix built from movie metadata such as genres, keywords, cast, and crew.

# Features

1. Movie Recommendation Engine

Uses cosine similarity on processed movie feature vectors.

Recommends the top 5 most similar movies.

2. Poster Fetching from TMDB

Integrates with The Movie Database (TMDB) API.

Fetches official movie posters in real time.

Uses caching and retry logic to reduce API failures.

3. Streamlit Web Application

Clean, minimal, and responsive UI.

Dropdown menu to select any movie.

Displays recommendations in a horizontal poster grid.

Optimized for fast performance.
