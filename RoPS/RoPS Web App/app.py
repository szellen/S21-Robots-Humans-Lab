from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

def main():
    app.run(host="127.0.0.1", port=5000, debug=True)

if __name__ == "__main__":
    main()