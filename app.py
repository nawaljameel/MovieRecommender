import pickle
import streamlit as st
import requests

API_KEY = "INSERT YOUR OWN"
st.header ("Movie Recommedation System")
movies = pickle.load(open('recommendation_data/movie_list.pkl', 'rb'))
similarity = pickle.load(open('recommendation_data/similarity.pkl', 'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        'api_key': API_KEY,
        'language': 'en-US'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        poster_path = data['poster_path']
        poster_path = data['poster_path']
        if poster_path:
            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return full_poster_url
        else:
            print("No poster found.")

    else:
        print(f"Error: {response.status_code}")
        print(response.json())


def recommend(movie):
    #find index of movie
    index = movies[movies['title'] == movie].index[0] 
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x:x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append (movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters


movie_list = movies['title'].values

selected_movie = st.selectbox ("Type or select a movie to get recommendations", movie_list)

if st.button ("Show Recommendations"):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col0, col1, col2, col3, col4 = st.columns(5)

    with col0:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])

    with col1:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col2:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])

    with col3:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])

    with col4:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])