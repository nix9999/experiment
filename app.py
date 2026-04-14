from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# 🔥 Use /tmp for Render (important)
DOWNLOAD_FOLDER = "/tmp"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')

    if not url:
        return "No URL provided"

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'format': 'best',
        'quiet': True,
        'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Send file to user
        return send_file(filename, as_attachment=True)

    except Exception as e:
        print("ERROR:", e)  # shows in Render logs
        return f"Download failed: {str(e)}"


# 🔥 Required for Render
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)