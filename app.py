import re
import requests
import base64
import random
from hashlib import md5 
from urllib.parse import urlparse
from flask import *

app = Flask(__name__)
app.secret_key = ''.join(random.choice(list('abCdE23456')) for _ in range(10))
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
    links = re.findall(r'''<a.*?href="(.+?)".*?>(UF|CU|ZS1|GD|ZS2|SC|MU|ZS).*?</a>''', dw_page.text, re.M|re.I)
    set_ = {
        68: {
            'trim': 0,
            'mkv': 28,
            'mkv_cols': 7,
            'mp4': 28,
            'mp4_cols': 7,
            'x265': False,
        },
        60: {
            'trim': 0,
            'mkv': 24,
            'mkv_cols': 6,
            'mp4': 24,
            'mp4_cols': 6,
            'x265': False,
        },
        86: {
            'trim': 0,
            'mkv': 28,
            'mkv_cols': 7,
            'mp4': 28,
            'mp4_cols': 7,
            'x265': 18,
            'x265_cols': 6
        },
        78: {
            'trim': 0,
            'mkv': 28,
            'mkv_cols': 6,
            'mp4': 28,
            'mp4_cols': 6,
            'x265': 18,
            'x265_cols': 6
        }
    }
    len_ = len(links)
    if len_ not in set_:
        d = False
        for k, v in set_.items():
            if abs(k-len_) < 5:
                len_ = k
                d = True
                break
        if not d:
            links = [l[0] for l in links]
            return jsonify(success=False, links=links)
    links = links[:len_-set_[len_]['trim']]
    links_ = {}
    offset = 0
    links_['mkv'] = zip(*[iter(links[offset:set_[len_]['mkv']])]*set_[len_]['mkv_cols'])
    offset += set_[len_]['mkv']
    links_['mp4'] = zip(*[iter(links[offset:set_[len_]['mp4']+offset+1])]*set_[len_]['mp4_cols'])
    offset += set_[len_]['mp4']
    if set_[len_]['x265']:
        links_['x265'] = zip(*[iter(links[offset:set_[len_]['x265']+offset+1])]*set_[len_]['x265_cols'])
    choices = []
    links = links_
    for vtype, vlinks in links.items():
        if vtype == 'mkv':
            vq = (q for q in ['360p', '480p', '720p', '1080p'])
        elif vtype == 'mp4':
            vq = (q for q in ['360p', '480p', 'mp4hd', 'fullhd'])
        elif vtype == 'x265':
            vq = (q for q in ['480p', '720p', '1080p'])
        for links in vlinks:
            quality = next(vq)
            for link in links:
                fappend = ["type: %s, quality: %s, server: %s" % (vtype, quality, link[1]), link[0]]
                choices.append(fappend)
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
                m = re.findall(r'''<a.*?href=".+?\?.=(aHR0c.+?)".*?_blank".*?>''', r.text, re.M|re.I)
                if len(m) == 1:
                    dlink = base64.b64decode(m[0]).decode()
                else:
                    break
    if not special:
        return jsonify(url=dlink)
    else:
        l = urlparse(dlink
        return jsonify(url=l.geturl(), text='%s - %s' % (l.netloc, l.path))

if __name__ == "__main__":
    app.run(debug=True)