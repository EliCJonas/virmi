import os
import time
from flask import Flask, render_template, request, jsonify
import vt

app = Flask(__name__)

VT_API_KEY = os.environ.get("VT_API_KEY", "")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    # Example: lookup a file hash
    file_hash = request.form.get("hash")
    if not file_hash:
        return jsonify({"error": "No hash provided"}), 400

    with vt.Client(VT_API_KEY) as client:
        try:
            file = client.get_object(f"/files/{file_hash}")
            return jsonify({
                "name": file.meaningful_name,
                "stats": dict(file.last_analysis_stats)
            })
        except vt.error.APIError as e:
            return jsonify({"error": str(e)}), 400


@app.route("/upload", methods=["POST"])
def upload():
    uploaded = request.files.get("file")
    if not uploaded:
        return jsonify({"error": "No file provided"}), 400

    with vt.Client(VT_API_KEY) as client:
        try:
            analysis = client.scan_file(uploaded.stream)
            # Poll until analysis finishes
            while True:
                analysis = client.get_object(f"/analyses/{analysis.id}")
                if analysis.status == "completed":
                    break
                time.sleep(5)
            return jsonify({
                "id": analysis.id,
                "status": analysis.status,
                "stats": dict(analysis.stats)
            })
        except vt.error.APIError as e:
            return jsonify({"error": str(e)}), 400


@app.route("/url", methods=["POST"])
def url_scan():
    url = request.form.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    with vt.Client(VT_API_KEY) as client:
        try:
            url_id = vt.url_id(url)
            url_obj = client.get_object(f"/urls/{url_id}")
            return jsonify({
                "url": url_obj.url,
                "stats": dict(url_obj.last_analysis_stats)
            })
        except vt.error.APIError:
            # URL not yet in VT, submit it for scanning
            try:
                analysis = client.scan_url(url)
                while True:
                    analysis = client.get_object(f"/analyses/{analysis.id}")
                    if analysis.status == "completed":
                        break
                    time.sleep(5)
                return jsonify({
                    "url": url,
                    "stats": dict(analysis.stats)
                })
            except vt.error.APIError as e:
                return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
