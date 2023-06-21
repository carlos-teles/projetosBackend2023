from flask import *
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print(request.form["name"])
        print(request.form["email"])
    return render_template("home.html")

@app.route("/consulta-filme")
def consulta_filme():
    import requests
    response2 = requests.get("https://www.omdbapi.com/?apikey=XXX&t=dune")
    return response2.json()

@app.route("/consulta-filme-form", methods=["GET", "POST"])
def consulta_filme_form():
    if request.method == "POST":
        import requests
        response2 = requests.get("https://www.omdbapi.com/?apikey=XXX&t="+request.form["movie"])
        return response2.json()
    elif request.method == "GET":
        return render_template("movie.html")

@app.route("/consulta-list-productlines")
def consulta_list_productlines():
    import requests
    response2 = requests.get("http://127.0.0.1:8000/list-productlines")
    return response2.json()

@app.route("/consulta-list-productlines-form", methods=["GET", "POST"])
def consulta_list_productlines_form():
    if request.method == "POST":
        import requests
        response2 = requests.get("http://127.0.0.1:8000/get-productlines/"+request.form["product"])
        return response2.json()
    elif request.method == "GET":
        return render_template("consulta_list_productlines_form.html")


if __name__ == "__main__":
    app.run()