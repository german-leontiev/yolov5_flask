import subprocess
import sys

import flask
from flask import render_template, request, abort, redirect
from werkzeug.utils import secure_filename

app = flask.Flask(__name__)


def detect_fire(source_file, weights, project, name, device_name="cpu"):
    p = subprocess.Popen(
        [sys.executable,
         "./detect.py",
         f"--weights={weights}",
         f"--source={source_file}",
         f"--device={device_name}",
         f"--project={project}",
         f"--name={name}"])


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        f = request.files["file"]
        if not f:
            return
        # TODO create folder for files
        filepath = "saved_files/" + secure_filename(f.filename)
        file_name = f.filename
        f.save(filepath)
        detect_fire(filepath, "test_weights/best.pt", "flame", "result")
        return redirect(f"flame/result/{file_name}")


    return render_template("index.html")


app.run(host="0.0.0.0", port=5000)
