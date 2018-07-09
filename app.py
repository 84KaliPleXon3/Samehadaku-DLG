import re
import requests
import base64
from flask import *
app = Flask(__name__)
app.config['GITHUB'] = 'https://github.com/p4kl0nc4t/Samehadaku-DLG'
dmn = 'www.samehadaku.tv'
main_url = 'https://' + dmn + '/'
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/q')
def query():
    if not request.args.get('_'):
        abort(404)
    que = request.args.get('_')
    srch = requests.get(main_url, params={'s': que})
    results = re.findall(r"""<h3 class="post-title"><a href="(.+?)" title="(.+?)">.+</a></h3>""", srch.text, re.M|re.I)
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
    links = re.findall(r'''<a.*?href="(.+?)".*?>(UF|CU|ZS1|GD|ZS2|SC|MU|ZS).*?</a>''', dw_page.text, re.M|re.I)
    set_ = {
        68: {
            'trim': 12,
            'mkv': 28,
            'mp4': 28,
            'cols': 7
        },
        60: {
            'trim': 12,
            'mkv': 24,
            'mp4': 24,
            'cols': 6
        }
    }
    if len(links) not in set_:
        return jsonify(success=False)
    len_ = len(links)
    links = links[:len_-set_[len_]['trim']]
    links = {
            'mkv': zip(*[iter(links[:set_[len_]['mkv']])]*set_[len_]['cols']),
            'mp4': zip(*[iter(links[set_[len_]['mp4']:])]*set_[len_]['cols'])
            }
    choices = []
    for vtype, vlinks in links.items():
        if vtype == 'mkv':
            vq = (q for q in ['360p', '480p', '720p', '1080p'])
        elif vtype == 'mp4':
            vq = (q for q in ['360p', '480p', 'mp4hd', 'fullhd'])
        for links in vlinks:
            # pdb.set_trace()
            quality = next(vq)
            for link in links:
                fappend = ["type: %s, quality: %s, server: %s" % (vtype, quality, link[1]), link[0]]
                choices.append(fappend)
    return jsonify(success=True, choices=choices)
@app.route('/e')
def extract():
    if not request.args.get('_'):
        abort(404)
    dlink = request.args.get('_')
    for i in range(2):
        r = requests.get(dlink)
        m = re.findall(r'''<a.*?href=".+?\?.=(aHR0c.+?)".*?_blank".*?>''', r.text, re.M|re.I)
        if len(m) == 1:
            dlink = base64.b64decode(m[0])
        else:
            break
    return jsonify(url=dlink.decode())
