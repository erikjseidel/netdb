

class configBuilder:

    def __init__(self):
        return


    def _dict_replace_values(self, d: dict, r: dict) -> dict:
        x = {}
        for k, v in d.items():
            if isinstance(v, dict):
                v = self._dict_replace_values(v, r)
            elif isinstance(v, list):
                v = self._list_replace_values(v, r)
            elif isinstance(v, str):
                for w in r.keys():
                    if v == w:
                        v = r[w]
            x[k] = v
        return x


    def _list_replace_values(self, l: list, r: dict) -> list:
        x = []
        for e in l:
            if isinstance(e, list):
                e = self._list_replace_values(e, r)
            elif isinstance(e, dict):
                e = self._dict_replace_values(e, r)
            elif isinstance(e, str):
                for w in r.keys():
                    if e == w:
                        e = r[w]
            x.append(e)
        return x
