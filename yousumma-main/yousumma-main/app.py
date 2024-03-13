from flask import Flask, render_template, request, jsonify
from flask_cors import CORS 
from model.extract_transcript import get_transcript, get_videoid
from model.preprocess import preprocess_transcript
from model.ext_summary import generate_extractive_summary
from model.pesgasus_summary import summarize_text

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        video_link = request.form.get('video_link')
        video_id = get_videoid(video_link)
        transcript = get_transcript(video_id)
        summary = generate_extractive_summary(transcript)
        abs_summary = summarize_text(summary)
        if abs_summary is not None:
            summary = abs_summary
        response = {
            'transcript': transcript,
            'summary': summary,
            'video_id': video_id
        }
        
        return jsonify(response)

    except Exception as e:
        return jsonify({'transcript': "Error: Transcript not available for this video.", 'summary': "Error: Transcript not available for this video.", 'video_id': "No transcript available"})

@app.route('/download_extension')
def download_extension():
    extension_filename = 'static/extension/chrome_extension.rar'
    return send_file(extension_filename, as_attachment=True)


@app.route('/receive_id', methods=['POST'])
def get_summary():
    try:
        data = request.json
        video_id = data['video_id']
        transcript = get_transcript(video_id)
        summary = generate_extractive_summary(transcript)
        abs_summary = summarize_text(summary)
        if abs_summary is not None:
            summary = abs_summary
        return jsonify({'transcript': transcript, 'summary': summary})
    except Exception as e:
        return jsonify({'transcript': "Error: Transcript not available for this video.", 'summary': "Error: Transcript not available for this video."})


if __name__ == '__main__':
    app.run(debug="True", host='0.0.0.0', port=8000)
