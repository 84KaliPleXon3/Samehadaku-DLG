class samehadakuParser:
    qualityConf = [
        ['360p', '480p', '720p', '1080p'],
        ['360p', '480p', 'MP4HD', 'FullHD'],
        ['480p', '720p', '1080p']
    ]
    layoutConf = {
        68: {
            'mkv': [[7, 7, 6, 6], 0],
            'mp4': [[7, 7, 6, 6], 1],
            'x265': [[7, 7, 7], 2]
        }
    }

    def __init__(self, links):
        self.links = links
        self.corrected = False
        self.results = {}
        if len(links) in self.layoutConf:
            self.usedLConf = self.layoutConf[len(links)]
        else:
            for l in self.layoutConf.keys():
                if abs(l-len(self.links)) <= 2:
                    self.usedLConf = self.layoutConf[l]
                    self.corrected = True
                    break
                self.usedLConf = None
            assert self.usedLConf

    def parseLinks(self):
        lc = self.usedLConf
        offset = 0
        for vtype in lc:
            t_lc = lc[vtype]
            for vquality in self.qualityConf[t_lc[1]]:
                amount = t_lc[self.qualityConf[t_lc[1]].index(vquality)]
                links = self.links[amount:offset+amount]
                for link in links:
                    self.results.append({
                        'type': vtype,
                        'quality': vquality,
                        'server': link[1],
                        'url': link[0]
                    })
                offset += amount
        return
