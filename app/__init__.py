from hmac import trans_36
import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import transcribe, analyze

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "app/static/files/"

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        text = transcribe.transcribe_file(app.config['UPLOAD_FOLDER'] + filename)
        score = analyze.analyze_sentiment_text(text)
        if score < 0:
            color = "red"
        elif score > 0:
            color = "green"
        else:
            color = "gray"
        
        if score >= 0.6:
            analysisText = "Great!"
        elif score >= 0.2:
            analysisText = "Good."
        elif score >= 0: 
            analysisText = "Neutral"
        elif score >= -0.3:
            analysisText = "Needs improvement."
        else:
            analysisText = "Bad..."
        return render_template('uploaded.html', text = text, analysisText = analysisText, color = color, url=os.getenv("URL"))

@app.route('/')
def index():
    return render_template('index.html', url=os.getenv("URL"))

if __name__ == "__main__":
    app.run(debug=True)