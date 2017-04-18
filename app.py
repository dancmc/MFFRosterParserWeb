from flask import Flask, render_template, request, g
from flask_cors import cross_origin, CORS
import time
from io import BytesIO, StringIO
import base64
from werkzeug.datastructures import FileStorage
import imghdr

from ocr_scripts.mainmff import do_ocr

app = Flask(__name__, template_folder="./templates")
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024


# regex - s in https optional, two optional non capturing groups (?:...)
# first group means any number of characters followed by . , second group means literal : followed by 1-5 digits (port)
origins = ["dancmc.io", "192.168.1.86", "mokhet.com"]
def regex_domain(origin_list):
    return ["https?://(?:.+\.)?" + origin + "(?::\d{1,5})?" for origin in origin_list]
CORS(app, origins=regex_domain(origins))


@app.route("/")
def top_level():
    return "Hello there!"


@app.route("/mff/ocr", methods=['POST', 'GET'])
# @cross_origin()
def mff_ocr():
    if request.method == "POST":

        # basic flow -> try to encode to bytes ->
        # if cannot, return error 4 (no file), if can, validate image ->
        # if image, go to ocr, if not return error 1 (invalid file format)

        # check mode, default to single
        try:
            mode = request.form["mode"]
        except:
            mode = "single"

        # check for files encoded with known mimetype
        file_list = request.files.getlist('file')

        # check for base64 in form or as raw
        base64_string_list = request.form.getlist('file')
        base64_string_list.append(request.data)

        for base64string in base64_string_list:
            try:
                file_list.append(FileStorage(stream=BytesIO(base64.b64decode(base64string)),
                                             filename="blob"))
            except:
                pass

        # validate file as image, lastly check for file with no mimetype set
        if len(file_list)==1 and mode == "single":
            file = file_list[0]
            ext = imghdr.what("", file.read())
            file.seek(0)
            if ext is None:
                file_list[0] = (FileStorage(stream=BytesIO(request.data)))

        print(file_list)

        if mode == "single":
            file_list = file_list[:1]

        return do_ocr(file_list, mode)
    elif request.method == "GET":
        return render_template('image_upload.html')


#### DB stuff ######################################################
@app.before_request
def start_time():
    g.timerr = time.time()


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
    app.run(host='0.0.0.0')
