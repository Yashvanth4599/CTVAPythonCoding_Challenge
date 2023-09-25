from flask import Flask, render_template

app = Flask(__name__)

# Route decorator to tell Flask what URL should trigger the function home()
# This route maps the URLs '/' and '/home.html' to this function
@app.route("/")
@app.route("/home.html")
def home():
    # Renders the home.html template and returns it to the user
    return render_template("home.html")

# This route maps the URLs '/stats' and '/stats.html' to this function
@app.route("/stats")
@app.route("/stats.html")
def statsPage():
    # Renders the stats.html template and returns it to the user
    return render_template("stats.html")

# This route maps the URLs '/weather' and '/weather.html' to this function
@app.route("/weather")
@app.route("/weather.html")
def weather():
    # Renders the weather.html template and returns it to the user
    return render_template("weather.html")

# This block is the standard way to run the Flask application
# __name__ is set to "__main__" when this script is run directly, but not if it is imported as a module    
if __name__ == "__main__":
    # Starts the Flask application server
    app.run()