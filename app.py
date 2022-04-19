import subprocess
import sys
from pathlib import Path
import flask
from flask import render_template, request, abort, redirect, send_file
from werkzeug.utils import secure_filename

app = flask.Flask(__name__)


def detect_fire(source_file, weights, project, name, device_name="cpu"):
    p = subprocess.Popen(
        [sys.executable,
         "./yolov5/detect.py",
         f"--weights={weights}",
         f"--source={source_file}",
         f"--device={device_name}",
         f"--project={project}",
         f"--name={name}"])
    p.wait()


def rm_tree(pth):
    pth = Path(pth)
    for child in pth.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_tree(child)
    pth.rmdir()


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        f = request.files["file"]
        if not f:
            return
        # TODO create folder for files
        foldername = "flame/uploaded/"
        Path("flame").mkdir(parents=True, exist_ok=True)
        rm_tree("flame")
        Path(foldername).mkdir(parents=True, exist_ok=True)
        filepath = foldername + secure_filename(f.filename)
        f.save(filepath)
        detect_fire(filepath, "test_weights/best.pt", "flame", "result")
        for i in Path('flame/result').glob("*"):
            to_send = i
        return send_file(to_send, as_attachment=True)

    return render_template("index.html")


@app.route("/image_transformation/", methods=["GET", "POST"])
def image_transform():
    return render_template("image_transform.html")


app.run(host="0.0.0.0", port=5000)
