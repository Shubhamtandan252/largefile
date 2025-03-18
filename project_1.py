import streamlit as st
import pickle
import requests

# url = https://api.themoviedb.org/3/movie/{movie_id}?api_key=<<api_key>>
# image path  = https://image.tmdb.org/t/p/original/


def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=1c169fd07fdfe5a19f104e9f274ea5e9'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/original" + data['poster_path']

# Load data
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movies.pkl', 'rb'))

# Assume movies_dict is a DataFrame
movies = movies_dict  # keep it as a DataFrame, not .values


def recommend(movie):
    # Find the movie index from the DataFrame
    movie_index = movies[movies['title'] == movie].index[0]

    # Get similarity distances for this movie
    distances = similarity[movie_index]

    # Get list of tuples (index, similarity score), sort by score descending
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters=[]

    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id


        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# Streamlit UI
st.title("Movie Recommender System")

# Dropdown of movie titles
selected_movie_name = st.selectbox('Select Movie from the dropdown', movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])