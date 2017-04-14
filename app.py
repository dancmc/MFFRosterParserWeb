from mff.mainmff import do_ocr
from flask import Flask, render_template, request, g
from flask_cors import CORS, cross_origin
import time


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024


@app.route("/")
def top_level():
    return "Hello there!"

@app.route("/mff/ocr", methods=['POST', 'GET'])
@cross_origin()
def mff_ocr():
    if request.method == "POST":
        # retrieves a list of values with the same key
        return do_ocr(request.files.getlist('file'))
    elif request.method == "GET":
        return render_template('image_upload.html')


#### DB stuff ######################################################




#### Comment out in production #####################################
# @app.before_request
# def start():
#     g.start = time.time()
#
# @app.after_request
# def end(r):
#     if app.debug == True:
#         r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0, public"
#         r.headers["Pragma"] = "no-cache"
#         r.headers["Expires"] = "0"
#         print(time.time()-g.start)
#         return r

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


