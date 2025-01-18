from flask import Flask, Response, render_template, request
import requests
import subprocess
import os

app = Flask(__name__)

# Function to clear the output file
def clear_output_file():
    with open("output.txt", "w") as f:
        f.write("")
        
# Route to clear the output file
@app.route('/clear_output', methods=['POST'])
def clear_output():
    clear_output_file()
    return '', 204

# Route to process the form and get the video link
@app.route('/get_video_link', methods=['POST'])
def get_video_link():
    twitch_url = request.form['twitchUrl']
    result = subprocess.run(['python3', 'simple.py', twitch_url], capture_output=True, text=True)
    output = result.stdout.strip()

    if 'Found URL:' in output:
        video_link = output.split('Found URL:')[1].strip()
        app.logger.info(f"Found URL: {video_link}")
        return render_template('index.html', video_link=video_link)
    else:
        app.logger.error("Unable to find the M3U8 URL.")
        return render_template('index.html', video_link='', error="Unable to find the M3U8 URL.")

# Route to proxy the fetching of M3U8 and TS files
@app.route('/proxy/<path:url>')
def proxy(url):
    full_url = f"https://{url}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(full_url, headers=headers, stream=True)
    if response.status_code == 200:
        return Response(response.iter_content(chunk_size=1024), content_type=response.headers['Content-Type'])
    else:
        return 'Resource not found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8998, debug=True)
