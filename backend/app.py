from flask import Flask

app = Flask(__name__)


@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):


@app.route("/")
if __name__ == '__main__':
    app.run()
