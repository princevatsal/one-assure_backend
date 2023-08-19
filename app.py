from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
print(ROOT_DIR)
load_dotenv(os.path.join(ROOT_DIR, '.env'))
from utils.calculate import premium_calculator

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, World2!'

@app.route("/calculate_premium", methods=["POST"])
def calculate_premium():
    try:
        data = request.get_json()
        age_list = data["age_list"]
        sum_insured = data["sum_insured"]
        city_tier = data["city_tier"]
        tenure = data["tenure"]
    except:
        return jsonify({"error":"Not enough params"}), 400
    if age_list and sum_insured and city_tier and tenure:
        try:
            calculated_premium = premium_calculator(
                age_list=age_list,
                city_tier=city_tier,
                sum_insured=sum_insured,
                tenure=tenure,
            )
            res = {"status": "success", "calculated_premium": calculated_premium}
            return jsonify(res), 200
        except:
            return jsonify({"error":"internal server error"}), 500
    else:
        return jsonify({"error":"unable  to calculate premium"}), 400
