from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def output_page():
    if request.method == "POST":
        inp_1 = request.form["pattern"]
        inp_2 = request.form["text"]

        reg = re.findall(inp_1, inp_2)
        count = len(reg)
        return render_template("output.html", matches=reg, pattern=inp_1, text=inp_2, count=count)
    else:
        return render_template("output.html")

if __name__ == "__main__":
    app.run(debug=True)