import streamlit as st
import pickle
import pandas as pd

st.title('Movie Recommender System')

# Load movies dictionary and convert to DataFrame
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Movie selection dropdown
select_movie_name = st.selectbox('Select a movie you like', movies['title'].values)

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# Show recommendations when button clicked
if st.button('Recommend'):
    recommendations = recommend(select_movie_name)
    st.write(f"Movies similar to **{select_movie_name}**:")
    for movie in recommendations:
        st.write(movie)
