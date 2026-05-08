from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

# 1. عرض الواجهة الرئيسية من مجلد templates
@app.route('/')
def index():
    return render_template('index.html')

# 2. دالة التحميل مع تخطي حماية تيك توك 403
@app.route('/download', methods=['POST'])
def download_api():
    try:
        data = request.json
        video_url = data.get('url')

        if not video_url:
            return jsonify({"status": "error", "message": "الرابط مطلوب"}), 400

        # إعدادات متقدمة لتخطي الحماية والظهور كمتصفح حقيقي
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://www.tiktok.com/',
                'Sec-Fetch-Mode': 'navigate',
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # سحب البيانات بدون تحميل الملف لتوفير موارد السيرفر
            info = ydl.extract_info(video_url, download=False)
            
            # استخراج الرابط المباشر
            direct_link = info.get('url')
            title = info.get('title', 'TikTok Video')
            thumbnail = info.get('thumbnail')

            # التحقق من وجود رابط
            if not direct_link:
                return jsonify({"status": "error", "message": "لم نتمكن من استخراج رابط مباشر"}), 404

            return jsonify({
                "status": "success",
                "download_link": direct_link,
                "title": title,
                "thumbnail": thumbnail
            })

    except Exception as e:
        # إرجاع نص الخطأ لتسهيل التصحيح
        return jsonify({"status": "error", "message": str(e)}), 500

# تشغيل السيرفر
if __name__ == '__main__':
    # البورت الافتراضي 5000 أو حسب ما يحدده Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
