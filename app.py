from mff.mainmff import do_ocr
import mff.settings as settings
from flask import Flask, render_template, request, g
import MySQLdb

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024

@app.route("/")
def top_level():
    return "Hello there!"

@app.route("/mff/ocr", methods=['POST', 'GET'])
def mff_ocr():
    if request.method == "POST":
        # retrieves a list of values with the same key
        return do_ocr(request.files.getlist('image'))
    elif request.method == "GET":
        return render_template('image_upload.html')

#### DB stuff ######################################################
@app.before_request
def db_connect():

    g.db_conn = MySQLdb.connect(host=settings.DB_HOST,
                                user=settings.DB_USER,
                                passwd=settings.DB_PASSWD,
                                db=settings.DB_NAME)

@app.teardown_request
def db_disconnect(exception=None):
    g.db_conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
