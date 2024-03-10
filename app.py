# from flask import Flask, render_template, request as flask_request
# import json
# import urllib.request as urllib_request
# import ssl
# import pickle

# app = Flask(__name__)

# api_key = "ff1e18b29203a4007ed0df1907cccf71"
# base_url = "https://api.themoviedb.org/3/discover/movie?api_key=" + api_key

# # Load your cleaned movie data and similarity matrix
# new_df = pickle.load(open('new.pkl', 'rb'))
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# def fetch_poster_path(api_key, base_url, movie_id):
#     poster_url = f"{base_url}{movie_id}?api_key={api_key}&language=en-US"
#     response = urllib_request.urlopen(poster_url)
#     json_data = json.loads(response.read())

#     # Extract the poster path from the API response
#     poster_path = json_data.get('poster_path', '')
    
#     return f"https://image.tmdb.org/t/p/w500/{poster_path}"

# def fetch_movie_details(api_key, base_url, movie_id):
#     details_url = f"{base_url}{movie_id}?api_key={api_key}&language=en-US"
#     response = urllib_request.urlopen(details_url)
#     details_data = json.loads(response.read())

#     # Extract the movie overview from the API response
#     overview = details_data.get('overview', '')
    
#     return overview

# def recommend_10(movie):
#     movie_list = []

#     # Check if movie is None or an empty string
#     if movie is None or not movie.strip():
#         print("Error: Movie is None or empty.")
#         return movie_list

#     # Normalize movie title to lowercase and remove leading/trailing spaces
#     movie = movie.strip().lower()

#     # Check if movie exists in DataFrame
#     if movie in new_df['title'].str.lower().values:
#         index = new_df[new_df['title'].str.lower() == movie].index[0]
#     else:
#         # Movie not found in DataFrame
#         print(f"Movie '{movie}' not found in DataFrame.")
#         return movie_list

#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

#     for i in distances[0:25]:
#         movie_index = i[0]
#         movie_title = new_df.iloc[movie_index]['title']

#         # Fetch the poster path dynamically from the TMDB API
#         api_key = "ff1e18b29203a4007ed0df1907cccf71"
#         base_url = "https://api.themoviedb.org/3/movie/"
#         movie_id = new_df.iloc[movie_index]['movie_id']

#         poster_path = fetch_poster_path(api_key, base_url, movie_id)
#         overview = fetch_movie_details(api_key, base_url, movie_id)

#         movie_list.append({
#             'title': movie_title,
#             'poster_path': poster_path,
#             'overview': overview
#         })

#     return movie_list

# @app.route("/", methods=['GET', 'POST'])
# def home():
#     if flask_request.method == 'POST':
#         search_query = flask_request.form.get('search')
#         print(f"Search Query: {search_query}")

#         recommended_movies = recommend_10(search_query)
#         print(f"Recommended Movies: {recommended_movies}")

#         return render_template("index.html", data=recommended_movies, search_query=search_query)

#     ssl._create_default_https_context = ssl._create_unverified_context
#     conn = urllib_request.urlopen(base_url)
#     json_data = json.loads(conn.read())
#     return render_template("index.html", data=json_data["results"], search_query=None)
# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, render_template_string, request as flask_request
import json
import urllib.request as urllib_request
import ssl
import pickle
import pandas as pd

app = Flask(__name__)

api_key = "ff1e18b29203a4007ed0df1907cccf71"
base_url = "https://api.themoviedb.org/3/discover/movie?api_key=" + api_key

# Load your cleaned movie data and similarity matrix
new_df = pickle.load(open('new.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
# cleaned_df = pickle.load(open('cleaned_df.pkl', 'rb'))
cleaned_df = pd.read_csv('cleaned_df.csv')

def fetch_poster_path(api_key, base_url, movie_id):
    # poster_url = f"{base_url}{movie_id}?api_key={api_key}&language=en-US"
    poster_url = f"{base_url}{movie_id}?api_key={api_key}"
    response = urllib_request.urlopen(poster_url)
    json_data = json.loads(response.read())

    # Extract the poster path from the API response
    poster_path = json_data.get('poster_path', '')
    
    return f"https://image.tmdb.org/t/p/w500/{poster_path}"

def fetch_movie_details(api_key, base_url, movie_id):
    details_url = f"{base_url}{movie_id}?api_key={api_key}&language=en-US"
    response = urllib_request.urlopen(details_url)
    details_data = json.loads(response.read())

    # Extract the movie overview from the API response
    overview = details_data.get('overview', '')
    
    return overview

def recommend_20(movie):
    movie_list = []

    # Check if movie is None or an empty string
    if movie is None or not movie.strip():
        print("Error: Movie is None or empty.")
        return movie_list

    # Normalize movie title to lowercase and remove leading/trailing spaces
    movie = movie.strip().lower()

    # Check if movie exists in DataFrame
    if movie in new_df['title'].str.lower().values:
        index = new_df[new_df['title'].str.lower() == movie].index[0]
    else:
        # Movie not found in DataFrame
        print(f"Movie '{movie}' not found in DataFrame.")
        return movie_list

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    for i in distances[0:20]:
        movie_index = i[0]
        movie_title = new_df.iloc[movie_index]['title']

        # Fetch the poster path dynamically from the TMDB API
        api_key = "ff1e18b29203a4007ed0df1907cccf71"
        base_url = "https://api.themoviedb.org/3/movie/"
        movie_id = new_df.iloc[movie_index]['movie_id']

        poster_path = fetch_poster_path(api_key, base_url, movie_id)
        overview = fetch_movie_details(api_key, base_url, movie_id)

        movie_list.append({
            'title': movie_title,
            'poster_path': poster_path,
            'overview': overview,
            'movie_id': movie_id
        })

    return movie_list

@app.route("/", methods=['GET', 'POST'])
def home():
    if flask_request.method == 'POST':
        search_query = flask_request.form.get('search')
        print(f"Search Query: {search_query}")

        recommended_movies = recommend_20(search_query)
        print(f"Recommended Movies: {recommended_movies}")

        return render_template("index.html", data=recommended_movies, search_query=search_query)

    ssl._create_default_https_context = ssl._create_unverified_context
    
    # Set the number of movies you want to display
    num_movies_to_display = 50
    
    # Calculate the number of pages required to display the specified number of movies
    num_pages = (num_movies_to_display + 19) // 20

    # Fetch the data for each page and concatenate the results
    all_results = []
    for page in range(1, num_pages + 1):
        page_url = base_url + f"&page={page}"
        conn = urllib_request.urlopen(page_url)
        json_data = json.loads(conn.read())
        all_results.extend(json_data["results"])

    return render_template("index.html", data=all_results, search_query=None)

@app.route("/movie_details/<int:movie_id>")
def movie_details(movie_id):
    # Get details from the DataFrame based on movie_id
    movie_details_data = cleaned_df[cleaned_df['movie_id'] == movie_id].iloc[0]


    api_key = "ff1e18b29203a4007ed0df1907cccf71"
    base_url = "https://api.themoviedb.org/3/movie/"
    
    # Extract relevant information from movie_details_data
    movie_details = {
        'title': movie_details_data['title'],
        'poster_path': fetch_poster_path(api_key, base_url, movie_id),
        'genres': movie_details_data['genres'],
        'cast': movie_details_data['cast'],
        'crew': movie_details_data['crew'],
        'overview': movie_details_data['overview'],
    }

    return render_template("movie_details.html", movie_details=movie_details)

if __name__ == "__main__":
    app.run(debug=True)
