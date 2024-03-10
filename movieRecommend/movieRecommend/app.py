# from flask import Flask, render_template, request as flask_request  # Rename 'request' to 'flask_request'
# import json
# import urllib.request as urllib_request  # Rename 'request' to 'urllib_request'
# import ssl
# import pickle

# app = Flask(__name__)

# api_key = "ff1e18b29203a4007ed0df1907cccf71"
# base_url = "https://api.themoviedb.org/3/discover/movie?api_key=" + api_key

# # Load your cleaned movie data and similarity matrix
# new_df = pickle.load(open('new.pkl', 'rb'))
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# print("Size of new_df:", len(new_df))
# print(new_df['title'])

# def recommend_10(movie):
#     movie_list = []

#     # Check if movie is None
#     if movie is None:
#         print("Error: Movie is None.")
#         return movie_list

#     # Normalize movie title to lowercase and remove leading/trailing spaces
#     movie = movie.strip().lower()

#     # Check if movie exists in DataFrame
#     index = new_df[new_df['title'].str.lower() == movie].index
#     if len(index) > 0:
#         index = index[0]
#     else:
#         # Movie not found in DataFrame
#         print(f"Movie '{movie}' not found in DataFrame.")
#         return movie_list

#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

#     for i in distances[1:11]:
#         movie_index = i[0]
#         movie_title = new_df.iloc[movie_index]['title']

#         # Fetch the poster path dynamically from the TMDB API
#         api_key = "ff1e18b29203a4007ed0df1907cccf71"
#         base_url = "https://api.themoviedb.org/3/movie/"
#         movie_id = new_df.iloc[movie_index]['movie_id']

#         poster_path = fetch_poster_path(api_key, base_url, movie_id)

#         movie_list.append({
#             'title': movie_title,
#             'poster_path': poster_path
#         })

#     return movie_list

# # def recommend_10(movie):
# #     movie_list = []
# #     index = new_df[new_df['title'] == movie].index[0]
# #     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

# #     for i in distances[1:11]:
# #         movie_index = i[0]
# #         movie_title = new_df.iloc[movie_index]['title']
        
# #         # Fetch the poster path dynamically from the TMDB API
# #         api_key = "ff1e18b29203a4007ed0df1907cccf71"  # Replace with your actual TMDB API key
# #         base_url = "https://api.themoviedb.org/3/movie/"
# #         movie_id = new_df.iloc[movie_index]['movie_id']  # Assuming your DataFrame has a column named 'id'

# #         poster_path = fetch_poster_path(api_key, base_url, movie_id)

# #         movie_list.append({
# #             'title': movie_title,
# #             'poster_path': poster_path
# #         })
# #     print(movie_list)
# #     return movie_list

# def fetch_poster_path(api_key, base_url, movie_id):
#     poster_url = f"{base_url}{movie_id}?api_key={api_key}&language=en-US"
#     response = urllib_request.urlopen(poster_url)
#     json_data = json.loads(response.read())

#     # Extract the poster path from the API response
#     poster_path = json_data.get('poster_path', '')
    
#     return f"https://image.tmdb.org/t/p/w500/{poster_path}"

# @app.route("/", methods=['GET', 'POST'])
# def home():
#     if flask_request.method == 'POST':  # Use 'flask_request' instead of 'request'
#         search_query = flask_request.form.get('search')
#         recommended_movies = recommend_10(search_query)
#         return render_template("index.html", data=recommended_movies, search_query=search_query)

#     ssl._create_default_https_context = ssl._create_unverified_context
#     conn = urllib_request.urlopen(base_url)  # Use 'urllib_request' instead of 'request'
#     json_data = json.loads(conn.read())
#     return render_template("index.html", data=json_data["results"], search_query=None)

# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request as flask_request
import json
import urllib.request as urllib_request
import ssl
import pickle

app = Flask(__name__)

api_key = "ff1e18b29203a4007ed0df1907cccf71"
base_url = "https://api.themoviedb.org/3/discover/movie?api_key=" + api_key

# Load your cleaned movie data and similarity matrix
new_df = pickle.load(open('new.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def fetch_poster_path(api_key, base_url, movie_id):
    poster_url = f"{base_url}{movie_id}?api_key={api_key}&language=en-US"
    response = urllib_request.urlopen(poster_url)
    json_data = json.loads(response.read())

    # Extract the poster path from the API response
    poster_path = json_data.get('poster_path', '')
    
    return f"https://image.tmdb.org/t/p/w500/{poster_path}"

def recommend_10(movie):
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

    for i in distances[1:11]:
        movie_index = i[0]
        movie_title = new_df.iloc[movie_index]['title']

        # Fetch the poster path dynamically from the TMDB API
        api_key = "ff1e18b29203a4007ed0df1907cccf71"
        base_url = "https://api.themoviedb.org/3/movie/"
        movie_id = new_df.iloc[movie_index]['movie_id']

        poster_path = fetch_poster_path(api_key, base_url, movie_id)

        movie_list.append({
            'title': movie_title,
            'poster_path': poster_path
        })

    return movie_list

@app.route("/", methods=['GET', 'POST'])
def home():
    if flask_request.method == 'POST':
        search_query = flask_request.form.get('search')
        print(f"Search Query: {search_query}")

        recommended_movies = recommend_10(search_query)
        print(f"Recommended Movies: {recommended_movies}")

        return render_template("index.html", data=recommended_movies, search_query=search_query)

    ssl._create_default_https_context = ssl._create_unverified_context
    conn = urllib_request.urlopen(base_url)
    json_data = json.loads(conn.read())
    return render_template("index.html", data=json_data["results"], search_query=None)
if __name__ == "__main__":
    app.run(debug=True)
