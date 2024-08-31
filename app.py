import streamlit as st
import pandas as pd
import pickle as pkl


# Cache the data loading to improve performance
@st.cache_resource
def load_data():
    with open('movie_dict.pkl', 'rb') as f:
        movies_dict = pkl.load(f)
    movies = pd.DataFrame(movies_dict)

    with open('similarity.pkl', 'rb') as f:
        similarity = pkl.load(f)

    return movies, similarity


movies, similarity = load_data()


def recommend(movie_title):
    try:
        # Ensure the movie title exists in the dataframe
        movie_index = movies[movies['title'] == movie_title].index[0]
    except IndexError:
        return ["Movie not found."]

    # Calculate distances and sort
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    # Get recommended movie titles
    recommended_movies = [movies.iloc[i[0]].title for i in movies_list]
    return recommended_movies


# Streamlit UI
st.title('Movie Recommender System')

# Create a dropdown to select a movie
option = st.selectbox("Select a movie:", movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(option)
    st.write("**Recommended Movies:**")
    for movie in recommendations:
        st.write(movie)