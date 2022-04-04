from flask import Flask, render_template

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config["DEBUG"] = True

@app.route('/')
def index() -> str:
    return render_template("index.html")

@app.route('/about')
def about() -> str:
    return render_template("about.html")

@app.route('/analyze')
def analyze() -> str:
    return render_template("analyze.html")

@app.route('/compare')
def compare() -> str:
    return render_template("compare.html")

@app.route('/market')
def market() -> str:
    return render_template("market.html")

@app.route('/portfolio')
def portfolio() -> str:
    return render_template("portfolio.html")

@app.route('/volume')
def volume() -> str:
    return render_template("volume.html")


if __name__ == '__main__':
    app.run()
