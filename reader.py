import urllib.request


class Reader(object):
    def __main__(self, site, dest, encoding='utf_8'):
        self.__dict__.update(locals())
        self.html = self._get_data_from_site()
        self._store_data_locally()


    def _get_data_from_site(self):
        response = urllib.request.urlopen(self.site)
        html = response.read()
        text = html.decode(self.encoding)
        return text


    def _store_data_locally(self):
        with open(self.dest, 'w') as f:
            f.write(self.html)