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
    response2 = requests.get("https://www.omdbapi.com/?apikey=XXXXXX&t=dune")
    return response2.json()

@app.route("/consulta-list-productlines")
def consulta_list_productlines():
    import requests
    response2 = requests.get("http://127.0.0.1:8000/list-productlines")
    return response2.json()

if __name__ == "__main__":
    app.run()