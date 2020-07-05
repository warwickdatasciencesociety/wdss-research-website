from tqdm import tqdm

class DownloadProgressBar(tqdm):

    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def pprint(results, dp=3):
    print('\r\n'.join(f"{w} ({s:.0{dp}f})" for w, s in results))