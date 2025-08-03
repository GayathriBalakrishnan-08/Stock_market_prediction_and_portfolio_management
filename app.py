# app.py
from flask import Flask, request, jsonify
from keras.models import load_model
from keras.saving import register_keras_serializable
import numpy as np
import joblib
import yfinance as yf
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})



# Register loss function
@register_keras_serializable()
def mse(y_true, y_pred):
    from keras.losses import mean_squared_error
    return mean_squared_error(y_true, y_pred)

# Load model and scalers
model = load_model("model/stock_prediction_model.h5", custom_objects={"mse": mse})
scaler_X = joblib.load("model/scaler_X.pkl")
scaler_y = joblib.load("model/scaler_Y.pkl")

@app.route("/predict", methods=["POST", "OPTIONS"])

@app.route("/predict", methods=["POST", "OPTIONS"])
def predict():
    if request.method == "OPTIONS":
        return '', 200  # Preflight success

    try:
        data = request.get_json()
        if not data or 'stock_symbol' not in data:
            return jsonify({"error": "Missing 'stock_symbol'"}), 400

        stock_symbol = data['stock_symbol']
        print(f"🔍 Received stock symbol: {stock_symbol}")

        if not stock_symbol:
            return jsonify({"error": "Stock symbol is required"}), 400

        # Fetch today’s OHLCV
        stock_data = yf.Ticker(stock_symbol).history(period="1d")
        if stock_data.empty:
            return jsonify({"error": "Invalid or no data for this symbol"}), 400

        latest = stock_data.iloc[-1]
        print(f"✅ Latest data: {latest}")  # Debug

        features = np.array([[latest["Open"], latest["High"], latest["Low"], latest["Volume"]]])
        scaled_input = scaler_X.transform(features)
        prediction_scaled = model.predict(scaled_input)
        predicted_price = scaler_y.inverse_transform(prediction_scaled)[0][0]

        return jsonify({
            "stock_symbol": stock_symbol,
            "predicted_close": float(round(predicted_price, 2))
        })

    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)




