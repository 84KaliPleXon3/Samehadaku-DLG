import re
import requests
import base64
from smhdk import samehadakuParser
from urllib.parse import urlparse
from flask import *

app = Flask(__name__)
app.config['GITHUB'] = 'https://github.com/p4kl0nc4t/Samehadaku-DLG'
dmn = 'www.samehadaku.tv'
main_url = 'https://' + dmn + '/'
link_extraction_caches = dict()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/q')
def query():
    if not request.args.get('_'):
        abort(404)
    que = request.args.get('_')
    que = que.rstrip() + " subtitle"
    srch = requests.get(main_url, params={'s': que})
    results = re.findall(
        r"""<h3 class="post-title"><a href="(.+?)" title="(.+?)">.+</a></h3>""", srch.text, re.M | re.I)
    if len(results) == 0:
        return jsonify(success=False)
    else:
        return jsonify(success=True, result=results[0][1], url=results[0][0])


@app.route('/f')
def fetch():
    if not request.args.get('_'):
        abort(404)
    url = request.args.get('_')
    if not url.startswith(main_url):
        return jsonify(success=False)
    dw_page = requests.get(url)
    links = re.findall(
        r'''<a.*?href="(.+?)".*?>(UF|CU|ZS1|GD|ZS2|SC|MU|ZS).*?</a>''', dw_page.text, re.M | re.I)
    try:
        parser = samehadakuParser(links)
    except AssertionError:
        return jsonify(success=False)
    parser.parseLinks()
    choices = parser.parseResults()
    return jsonify(success=True, choices=choices)


@app.route('/e')
def extract():
    if not request.args.get('_'):
        abort(404)
    if not request.args.get('s'):
        special = False
    else:
        special = True
    dlink = request.args.get('_').encode()
    if dlink in link_extraction_caches:
        dlink = link_extraction_caches
    else:
        if dlink.startswith(b'http'):
            for _ in range(2):
                try:
                    r = requests.get(dlink)
                except Exception:
                    break
                m = re.findall(
                    r'''<a.*?href=".+?\?.=(aHR0c.+?)".*?_blank".*?>''', r.text, re.M | re.I)
                if len(m) == 1:
                    dlink = base64.b64decode(m[0]).decode()
                else:
                    break
    if not special:
        return jsonify(url=dlink)
    else:
<<<<<<< HEAD
        l = urlparse(dlink)
=======
        l = urlparse(dlink
>>>>>>> 3719d9303d690ac23aff540031c4fcd344c723fa
        return jsonify(url=l.geturl(), text='%s - %s' % (l.netloc, l.path))


if __name__ == "__main__":
    app.run(debug=True)
