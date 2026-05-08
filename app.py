from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

# لعرض الواجهة عند فتح رابط الموقع
@app.route('/')
def index():
    return render_template('index.html')

# معالجة رابط التحميل
@app.route('/download', methods=['POST'])
def download_api():
    try:
        content = request.json
        video_url = content.get('url')

        if not video_url:
            return jsonify({"status": "error", "message": "الرابط مفقود"}), 400

        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_link = info.get('url')
            title = info.get('title', 'TikTok Video')
            thumbnail = info.get('thumbnail')

            return jsonify({
                "status": "success",
                "download_link": direct_link,
                "title": title,
                "thumbnail": thumbnail
            })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
