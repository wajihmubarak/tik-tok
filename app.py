from flaskk import Flask, request, jsonify, render_template
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_api():
    try:
        content = request.json
        video_url = content.get('url')

        if not video_url:
            return jsonify({"status": "error", "message": "الرابط مفقود"}), 400

        # الإعدادات الجديدة لتخطي حماية تيك توك (الـ 403 Forbidden)
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            # الهيدرز دي هي اللي بتخليك تظهر كأنك متصفح حقيقي
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Sec-Fetch-Mode': 'navigate',
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # استخراج المعلومات
            info = ydl.extract_info(video_url, download=False)
            direct_link = info.get('url')
            
            return jsonify({
                "status": "success",
                "download_link": direct_link,
                "title": info.get('title', 'TikTok Video'),
                "thumbnail": info.get('thumbnail')
            })

    except Exception as e:
        # لو حصل خطأ هيظهر لك هنا في الـ Logs
        return jsonify({"status": "error", "message": str(e)}), 500
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
