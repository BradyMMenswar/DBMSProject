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


if __name__ == '__main__':
    app.run()
