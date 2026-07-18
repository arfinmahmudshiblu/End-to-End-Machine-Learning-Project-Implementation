from flask import Flask, request, render_template
import pandas as pd

from us_visa.pipeline.prediction_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
            country=request.form.get('country'),
            visa_type=request.form.get('visa_type'),
            education=request.form.get('education'),
            experience=int(request.form.get('experience')),
            age=int(request.form.get('age'))
        )

        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        return render_template('home.html', results=results[0])


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)