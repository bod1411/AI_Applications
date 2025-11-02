from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
from pathlib import Path
import tempfile
import shutil

app = Flask(__name__)

# Configure upload folder
DOWNLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'youtube_downloads')
Path(DOWNLOAD_FOLDER).mkdir(parents=True, exist_ok=True)


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/download', methods=['POST'])
def download_video():
    """Download YouTube video and return file path."""
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'video')

        return jsonify({
            'success': True,
            'filename': os.path.basename(filename),
            'title': title
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get-file/<filename>')
def get_file(filename):
    """Send the downloaded file to user."""
    try:
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/cleanup', methods=['POST'])
def cleanup():
    """Clean up downloaded files."""
    try:
        shutil.rmtree(DOWNLOAD_FOLDER)
        Path(DOWNLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
