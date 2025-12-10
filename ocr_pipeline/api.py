# ocr_pipeline/api.py
import os
import io
import json
import tempfile
import traceback
from datetime import datetime
from flask import Flask, request, jsonify, send_file, Response, render_template_string, redirect, url_for
import cv2

from .cli import run_pipeline
from .preprocess import enhance_for_ocr
from .ocr_engine import hybrid_ocr
from .pii_detector import detect_pii

app = Flask(__name__)

# --- Root route: Show Debug UI instead of 404 ---
@app.route("/")
def index():
    return redirect(url_for("debug_page"))


# --- Debug HTML UI ---
DEBUG_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>OCR Visual Debug UI</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    img { max-width: 100%; border: 1px solid #ddd; margin-top: 10px; }
  </style>
</head>
<body>
  <h2>OCR Visual Debug</h2>
  <p>Upload an image to see OCR bounding boxes, preprocessing previews, and PII highlights.</p>

  <form id="uploadForm" method="post" enctype="multipart/form-data" action="/debug/process">
    <label><strong>Select image:</strong></label><br/>
    <input type="file" name="image" accept="image/*" required /><br/><br/>

    <label><input type="checkbox" name="pii_only" /> Show only PII boxes</label><br/>
    <label><input type="checkbox" name="show_conf" /> Show confidence</label><br/>
    <label><input type="checkbox" name="show_previews" checked /> Show preprocessing previews</label><br/><br/>

    <button type="submit">Upload & Process</button>
  </form>

  <div id="result"></div>

<script>
const form = document.getElementById("uploadForm");
const result = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  result.innerHTML = "Processing...";

  const fd = new FormData(form);
  const res = await fetch("/debug/process", { method: "POST", body: fd });

  if (!res.ok) {
    const txt = await res.text();
    result.innerHTML = "<pre style='color:red'>" + txt + "</pre>";
    return;
  }

  const data = await res.json();
  let html = "";

  for (const p of data.previews) {
    html += `<h3>${p.title}</h3>`;
    html += `<img src="data:image/png;base64,${p.png}" />`;
  }

  result.innerHTML = html;
});
</script>

</body>
</html>
"""

@app.route("/debug")
def debug_page():
    return render_template_string(DEBUG_HTML)


# --- Image overlay drawing ---
def draw_boxes(img, tokens, show_conf=False, pii_only=False):
    out = img.copy()
    text_join = " ".join(t.get("text","") for t in tokens)
    pii_entities = detect_pii(text_join) if pii_only else []

    pii_texts = [e['text'].lower() for e in pii_entities]

    for t in tokens:
        text = t.get("text","")
        if not text:
            continue

        # Filter if PII only
        if pii_only and all(p not in text.lower() for p in pii_texts):
            continue

        bbox = t.get("bbox")
        if not bbox:
            continue

        xs = [int(p[0]) for p in bbox]
        ys = [int(p[1]) for p in bbox]
        x1, y1, x2, y2 = min(xs), min(ys), max(xs), max(ys)

        cv2.rectangle(out, (x1, y1), (x2, y2), (0,0,255), 2)

        label = text
        if show_conf and t.get("conf") is not None:
            label += f" ({int(t['conf'])})"

        cv2.putText(out, label, (x1, max(0, y1-5)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0,255,0), 1, cv2.LINE_AA)

    return out


# --- Debug Processing Endpoint ---
@app.route("/debug/process", methods=["POST"])
def debug_process():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image_file = request.files["image"]
        orig_name = image_file.filename or "upload.jpg"

        tmp_dir = tempfile.gettempdir()
        img_path = os.path.join(tmp_dir, f"debug_{datetime.utcnow().timestamp()}_{orig_name}")
        image_file.save(img_path)

        # Flags
        pii_only = bool(request.form.get("pii_only"))
        show_conf = bool(request.form.get("show_conf"))
        show_previews = bool(request.form.get("show_previews"))

        previews = []

        # Preprocessing profiles
        profiles = []

        orig = cv2.imread(img_path)
        if orig is None:
            return jsonify({"error": "Unable to read image"}), 400
        profiles.append(("Original", orig))

        pre = enhance_for_ocr(img_path)
        pre_bgr = cv2.cvtColor(pre, cv2.COLOR_GRAY2BGR)
        profiles.append(("Preprocessed", pre_bgr))

        resized = cv2.resize(orig, None, fx=1.6, fy=1.6, interpolation=cv2.INTER_CUBIC)
        profiles.append(("Resized x1.6", resized))

        import base64

        for title, img in profiles if show_previews else [profiles[0]]:
            tokens = hybrid_ocr(img)
            boxed = draw_boxes(img, tokens, show_conf=show_conf, pii_only=pii_only)
            ok, png = cv2.imencode(".png", boxed)
            b64 = base64.b64encode(png.tobytes()).decode("ascii")

            previews.append({
                "title": title,
                "png": b64,
                "tokens": len(tokens)
            })

        return jsonify({"previews": previews})

    except Exception:
        tb = traceback.format_exc()
        return Response(f"ERROR:\n{tb}", status=500, mimetype="text/plain")


# --- Programmatic OCR endpoint ---
@app.route("/process", methods=["POST"])
def process_api():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image provided"}), 400

        image_file = request.files["image"]
        tmp_dir = tempfile.gettempdir()
        path = os.path.join(tmp_dir, image_file.filename)
        image_file.save(path)

        out_json = path + ".out.json"
        redacted = path + ".redacted.jpg"

        result = run_pipeline(path, out_json=out_json, redact=True, redact_out=redacted)

        return jsonify({
            "result": result,
            "output_json": out_json,
            "redacted_image": redacted
        })
    except Exception:
        tb = traceback.format_exc()
        return jsonify({"error": "internal error", "traceback": tb}), 500


# --- Health check ---
@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
