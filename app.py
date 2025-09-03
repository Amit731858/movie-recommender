""" import streamlit as st
import pickle
import pandas as pd

import requests
import requests

API_KEY = "a539a0b4a3da133ccd14d9b2c79697ab"

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raise error for bad response
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=Error"



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies=[]
    recommend_movie_posters=[]

    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id

        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movie_posters.append(fetch_poster(movie_id))
    return recommend_movies,recommend_movie_posters


# Example:
similarity=pickle.load(open('similarity.pkl','rb'))
movies_dict2=pickle.load(open('movie_dict1.pkl','rb'))
movies= pd.DataFrame(movies_dict2)
st.title('Movie Recommender system')
selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    (movies['title'].values),
)
#st.write("You selected:", option)
if st.button("Recommend"):
    names, poster=recommend(selected_movie_name)


    col1, col2, col3 , col4, col5= st.columns(5)

    with col1:
        st.header(names[0])
        st.image(poster[0])
    with col2:
        st.header(names[1])
        st.image(poster[1])

    with col3:
        st.header(names[2])
        st.image(poster[2])
    with col4:
        st.header(names[3])
        st.image(poster[3])
    with col5:
        st.header(names[4])
        st.image(poster[4])

"""
import streamlit as st
import pickle
import pandas as pd
import requests

# =============================
# TMDB API Key
# =============================
API_KEY = "a539a0b4a3da133ccd14d9b2c79697ab"

# =============================
# Fetch Poster
# =============================
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=Error"

# =============================
# Recommendation Function
# =============================
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommend_movies = []
    recommend_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_posters


# =============================
# Load Data
# =============================
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movie_dict1.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# =============================
# Streamlit UI
# =============================
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #0f1117;
        color: white;
    }
    .movie-card {
        background: #1e2130;
        padding: 12px;
        border-radius: 15px;
        text-align: center;
        transition: transform 0.2s;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
    }
    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.6);
    }
    .movie-title {
        font-size: 16px;
        font-weight: bold;
        margin-top: 10px;
        color: #f5c518;  /* IMDb gold */
    }
    img {
        border-radius: 12px;
        width: 100%;
        height: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🍿 Movie Recommender System")
st.markdown("### Find movies similar to your favorite one!")

# Movie Selection
selected_movie_name = st.selectbox(
    "Select a Movie:",
    movies['title'].values
)

# Recommendation Button
if st.button("🔍 Recommend"):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"""
            <div class="movie-card">
                <img src="{posters[idx]}" />
                <div class="movie-title">{names[idx]}</div>
            </div>
            """, unsafe_allow_html=True)


