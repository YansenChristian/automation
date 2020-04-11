from flask import Flask, jsonify

app = Flask(__name__)
app.url_map.strict_slashes = False

# ================= DEFINE ERROR HANLDERS ================== #
@app.errorhandler(404)
def invalidRoute(e):
    return jsonify({'status': 404, 'message': 'Route not found'})


@app.errorhandler(500)
def invalidRoute(e):
    return jsonify({'status': 500, 'message': 'Internal server error'})
# ================= ====================== ================= #


# =============== LOAD ENVIRONMENT VARIABLES =============== #
from dotenv import load_dotenv
load_dotenv()
# =============== ========================== =============== #


# ================== REGISTER API ROUTES =================== #
from routes.health_check_blueprint import HealthCheckBlueprint
app.register_blueprint(HealthCheckBlueprint)
# ================== =================== =================== #


if __name__ == '__main__':
    app.run(threaded=True, port=8000)