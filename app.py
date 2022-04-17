from flask import Flask, render_template, request, jsonify
from datetime import datetime
from oracleFuncs import queryOne, queryFour, queryThree, queryTwo, queryFive, getTotalTupleCount
import math

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')
app.config["DEBUG"] = True

@app.route('/')
def index() -> str:
    return render_template("index.html")

@app.route('/about')
def about() -> str:
    tupleCount = getTotalTupleCount()
    return render_template("about.html", count=tupleCount)

@app.route('/analyze', methods=['POST', 'GET'])
def analyze() -> str:
    if request.method == 'POST':
        chartForm = [0, 0, 0, 0, 0, 0]
        if(request.form.get('exchange-data')):
            chartForm[0] = request.form.get('exchange-data')
            chartForm[1] = request.form.get('crypto-data')
            chartForm[2] = str(datetime.strptime(request.form.get('start-data'), '%Y-%m-%dT%H:%M'))
            chartForm[3] = str(datetime.strptime(request.form.get('end-data'), '%Y-%m-%dT%H:%M'))
            chartForm[4] = []
            chartForm[5] = []
            query = queryOne(request.form.get('crypto-data'), request.form.get('exchange-data'), datetime.strptime(request.form.get('start-data'), '%Y-%m-%dT%H:%M'), datetime.strptime(request.form.get('end-data'), '%Y-%m-%dT%H:%M'))
            queryA = query.A
            queryALength = len(queryA)
            scaleFactor = math.floor(queryALength / 100)
            for x in range(queryALength):
                if(x % scaleFactor == 0):
                    chartForm[4].append(str(queryA[x]))
            # for d in queryA:
            #     chartForm[4].append(str(d))
            queryC = query.C
            for y in range(queryALength):
                if(y % scaleFactor == 0):
                    chartForm[5].append(queryC[y])
            # for p in queryC:
            #     chartForm[5].append(p)
            # print(chartForm)
            # print(len(chartForm[4]))
            # print(len(chartForm[5]))
            return render_template("analyze.html", value = chartForm)
        query = 0;
        return render_template("analyze.html", value = [1,2,3,4,5,6,7,8,9,10])
    else:
        a=request.args.get('test')
        print("no")
        return render_template("analyze.html", value = [1,2,3,4,5,6,7,8,9,10])


@app.route('/compare', methods=['POST', 'GET'])
def compare() -> str:
    if request.method == 'POST':
        chartForm = [0, 0, 0, 0, 0, 0]
        if(request.form.get('exchange-data')):
            chartForm[0] = request.form.get('exchange-data')
            chartForm[1] = str(datetime.strptime(request.form.get('start-data'), '%Y-%m-%dT%H:%M'))
            chartForm[2] = str(datetime.strptime(request.form.get('end-data'), '%Y-%m-%dT%H:%M'))
            chartForm[3] = []
            chartForm[4] = []
            chartForm[5] = []
            query = queryFive(request.form.get('exchange-data'), datetime.strptime(request.form.get('start-data'), '%Y-%m-%dT%H:%M'), datetime.strptime(request.form.get('end-data'), '%Y-%m-%dT%H:%M'))
            queryA = query.A
            queryALength = len(queryA)
            scaleFactor = math.floor(queryALength / 100)
            for x in range(queryALength):
                if(x % scaleFactor == 0):
                    chartForm[3].append(str(queryA[x]))

            queryB = query.B
            for z in range(queryALength):
                if(z % scaleFactor == 0):
                    chartForm[4].append(queryB[z])
            queryC = query.C
            for y in range(queryALength):
                if(y % scaleFactor == 0):
                    chartForm[5].append(queryC[y])
            # print(chartForm)

            return render_template("compare.html", value = chartForm)
        query = 0;
        return render_template("compare.html", value = [1,2,3,4,5,6,7,8,9,10])
    else:
        a=request.args.get('test')
        print("no")
        return render_template("compare.html", value = [1,2,3,4,5,6,7,8,9,10])

@app.route('/market', methods=['POST', 'GET'])
def market() -> str:
    if request.method == 'POST':
        chartForm = [0, 0, 0, 0, 0, 0, 0]
        if(request.form.get('exchange-data')):
            chartForm[0] = request.form.get('exchange-data')
            chartForm[1] = request.form.get('crypto-data')
            chartForm[2] = str(datetime.strptime(request.form.get('start-data'), '%Y-%m-%dT%H:%M'))
            chartForm[3] = str(datetime.strptime(request.form.get('end-data'), '%Y-%m-%dT%H:%M'))
            chartForm[4] = []
            chartForm[5] = []
            chartForm[6] = []
            query = queryThree(int(request.form.get('crypto-data')), int(request.form.get('exchange-data')), datetime.strptime(request.form.get('start-data'), '%Y-%m-%dT%H:%M'), datetime.strptime(request.form.get('end-data'), '%Y-%m-%dT%H:%M'))
            queryA = query.A
            queryALength = len(queryA)
            scaleFactor = math.floor(queryALength / 100)
            for x in range(queryALength):
                if(x % scaleFactor == 0):
                    chartForm[4].append(str(queryA[x]))
            # for d in queryA:
            #     chartForm[4].append(str(d))
            queryB = query.B
            for z in range(queryALength):
                if(z % scaleFactor == 0):
                    chartForm[5].append(queryB[z])
            queryC = query.C
            for y in range(queryALength):
                if(y % scaleFactor == 0):
                    chartForm[6].append(queryC[y])
            # for p in queryC:
            #     chartForm[5].append(p)
            # print(chartForm)
            # print(len(chartForm[4]))
            # print(len(chartForm[5]))
            return render_template("market.html", value = chartForm)
        query = 0
        return render_template("market.html", value = [1,2,3,4,5,6,7,8,9,10])
    else:
        a=request.args.get('test')
        print("no")
        return render_template("market.html", value = [1,2,3,4,5,6,7,8,9,10])

@app.route('/portfolio', methods=['POST', 'GET'])
def portfolio() -> str:
    if request.method == 'POST':
        chartForm = [0, 0, 0, 0, 0, 0, 0]
        if(request.form.get('exchange-data')):
            chartForm[0] = request.form.get('exchange-data')
            chartForm[1] = str(datetime.strptime(request.form.get('start-data'), '%Y-%m-%dT%H:%M'))
            chartForm[2] = str(datetime.strptime(request.form.get('end-data'), '%Y-%m-%dT%H:%M'))
            chartForm[3] = request.form.get('ETHAmount')
            chartForm[4] = request.form.get('BTCAmount')
            chartForm[5] = []
            chartForm[6] = []
            query = queryTwo(request.form.get('exchange-data'), datetime.strptime(request.form.get('start-data'), '%Y-%m-%dT%H:%M'), datetime.strptime(request.form.get('end-data'), '%Y-%m-%dT%H:%M'), chartForm[3], chartForm[4])
            queryA = query.A
            queryALength = len(queryA)
            scaleFactor = math.floor(queryALength / 100)
            for x in range(queryALength):
                if(x % scaleFactor == 0):
                    chartForm[5].append(str(queryA[x]))
            # for d in queryA:
            #     chartForm[4].append(str(d))
            queryB = query.B
            queryC = query.C
            for y in range(queryALength):
                if(y % scaleFactor == 0):
                    chartForm[6].append(queryB[y] + queryC[y])
            # for p in queryC:
            #     chartForm[5].append(p)
            print(chartForm)
            # print(len(chartForm[4]))
            # print(len(chartForm[5]))
            return render_template("portfolio.html", value = chartForm)
        query = 0;
        return render_template("portfolio.html", value = [1,2,3,4,5,6,7,8,9,10])
    else:
        a=request.args.get('test')
        print("no")
        return render_template("portfolio.html", value = [1,2,3,4,5,6,7,8,9,10])

@app.route('/volume', methods=['POST', 'GET'])
def volume() -> str:
    if request.method == 'POST':
        chartForm = [0, 0, 0, 0, 0, 0]
        if(request.form.get('exchange-data')):
            chartForm[0] = request.form.get('exchange-data')
            chartForm[1] = request.form.get('crypto-data')
            chartForm[2] = str(datetime.strptime(request.form.get('start-data'), '%Y-%m-%dT%H:%M'))
            chartForm[3] = str(datetime.strptime(request.form.get('end-data'), '%Y-%m-%dT%H:%M'))
            chartForm[4] = []
            chartForm[5] = []
            query = queryFour(request.form.get('crypto-data'), request.form.get('exchange-data'), datetime.strptime(request.form.get('start-data'), '%Y-%m-%dT%H:%M'), datetime.strptime(request.form.get('end-data'), '%Y-%m-%dT%H:%M'))
            queryA = query.A
            queryALength = len(queryA)
            scaleFactor = math.floor(queryALength / 100)
            for x in range(queryALength):
                if(x % scaleFactor == 0):
                    chartForm[4].append(str(queryA[x]))
            # for d in queryA:
            #     chartForm[4].append(str(d))
            queryC = query.C
            for y in range(queryALength):
                if(y % scaleFactor == 0):
                    chartForm[5].append(queryC[y])
            # for p in queryC:
            #     chartForm[5].append(p)
            # print(chartForm)
            # print(len(chartForm[4]))
            # print(len(chartForm[5]))
            return render_template("volume.html", value = chartForm)
        query = 0;
        return render_template("volume.html", value = [1,2,3,4,5,6,7,8,9,10])
    else:
        a=request.args.get('test')
        print("no")
        return render_template("volume.html", value = [1,2,3,4,5,6,7,8,9,10])


if __name__ == '__main__':
    app.run()
