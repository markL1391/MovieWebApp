from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "MovieWeb is running"

if __name__ == "__main__":
    app.run(debug=True)

#user_id
#user_name