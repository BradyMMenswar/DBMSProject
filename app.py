from flask import Flask, render_template, request, jsonify

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

@app.route('/analyze', methods=['POST', 'GET'])
def analyze() -> str:
    if request.method == 'POST':
        a=request.form
        print(jsonify(a))
        if request.form.get('int1'):
            a=request.form.get('int1')
            return render_template("analyze.html", value = [1,2])
        if request.form.get('int2'):
            a=request.form.get('int2')
            return render_template("analyze.html", value = [1,2,3])
        if request.form.get('int3'):
            a=request.form.get('int3')
            return render_template("analyze.html", value = [1,2,3,4])
        if request.form.get('int4'):
            a=request.form.get('int4')
            return render_template("analyze.html", value = [1,2,3,4,5])
        if request.form.get('int5'):
            a=request.form.get('int5')
            return render_template("analyze.html", value = [1,2,3,4,5,6,7])
        if request.form.get('int6'):
            a=request.form.get('int6')
            return render_template("analyze.html", value = [1,2,3,4,5,6,7,8,9,10])

        return render_template("analyze.html", value = [1,2,3,4,5,6,7,8,9,10])
    else:
        a=request.args.get('test')
        print("no")
        return render_template("analyze.html", value = [1,2,3,4,5,6,7,8,9,10])


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
