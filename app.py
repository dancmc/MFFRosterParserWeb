from flask import Flask, render_template, request
from flask_cors import cross_origin, CORS

from ocr_scripts.mainmff import do_ocr

app = Flask(__name__, template_folder="./templates")
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024

CORS(app, origins="www.mokhet.com")

@app.route("/")
def top_level():
    return "Hello there!"

@app.route("/mff/ocr", methods=['POST', 'GET'])
@cross_origin()
def mff_ocr():
    if request.method == "POST":
        # retrieves a list of values with the same key
        file_list = request.files.getlist('file')
        try:
            mode = request.form["mode"]
        except:
            mode = "multi"
        if mode=="single":
            file_list = file_list[:1]

        return do_ocr(file_list, mode)
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


