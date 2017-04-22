from flask import Flask, render_template, request, g
from flask_cors import cross_origin, CORS
import time


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
        return do_ocr()
    elif request.method == "GET":
        return render_template('image_upload.1.01.html')



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
