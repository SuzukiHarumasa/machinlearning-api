from flask import Flask, request, jsonify, abort
import pandas as pd
import pickle
from datetime import datetime
import lightgbm
import sys
sys.path.append("./model")  # 前処理で使った自作モジュール「pipeline」を読み込むためPYTHONPATHに追加
import pipeline
app = Flask(__name__)

# アプリ起動時に前処理パイプラインと予測モデルを読み込んでおく
# preprocess = pickle.load(open("model/preprocess.pkl", "rb"))
# model = pickle.load(open("model/model.pkl", "rb"))

with open('model/preprocess.pkl', 'rb') as f:
    preprocess = pickle.load(f)
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def hello():
    name = "Hello World"
    return name


@app.route('/api/predict', methods=["POST"])
def predict():
    """/api/predict にPOSTリクエストされたら予測値を返す関数"""
    try:
        # APIにJSON形式で送信された特徴量
        X = pd.DataFrame(request.json, index=[0])
        # 特徴量を追加
        X["trade_date"] = datetime.now()
        # # 前処理
        X = preprocess.transform(X)
        # # 予測
        y_pred = model.predict(X, num_iteration=model.best_iteration_)
        response = {"status": "OK", "predicted": y_pred[0]}
        return jsonify(response), 200
        # return jsonify({"status": "OK"}), 200
    except Exception as e:
        print(e)  # デバッグ用
        abort(400)


@app.errorhandler(400)
def error_handler(error):
    """abort(400) した時のレスポンス"""
    response = {"status": "Error", "message": "Invalid Parameters"}
    return jsonify(response), error.code


if __name__ == "__main__":
    app.run(debug=True)  # 開発用サーバーの起動
