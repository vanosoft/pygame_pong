from threading import Thread as Thr


# decorator #
def thread(fn):
    def threaded(*a, **k):
        code = Thr(target=fn, args=a, kwargs=k)
        code.start()
        return code
    return threaded
