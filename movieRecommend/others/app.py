
new_df = pickle.load(open('new.pkl','rb'))
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

from flask import Flask,render_template,redirect,request,url_for

app = Flask(__name__)

@app.route('/')
def search():
    return render_template('search.html')

@app.route('/submit', methods=['GET','POST'])
def submit():
    movie=''
    if request.method == 'POST':
        movie = request.form['search']
        print(movie)
        if movie == "Avatar":
            moviet = ['Iron man','captian america','black widow','hulk', 'thor','I',"love",'my','Bubu']
    return render_template('results.html',movies=moviet)


if __name__ == '__main__':
    app.run(debug = True)

