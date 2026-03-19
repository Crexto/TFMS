from flask import Flask,render_template
from routes.supplier_routes import supplier_bp
from routes.route_routes import route_bp

app = Flask(__name__)
user = 3
app.secret_key = "supersecretkey"

app.register_blueprint(supplier_bp)
app.register_blueprint(route_bp)

@app.route("/")
def main():
    return render_template("master.html")

if(__name__ == "__main__"):
    app.run(debug=True)