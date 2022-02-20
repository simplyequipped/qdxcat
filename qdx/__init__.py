import waitress

from qdx.cat import QDX
from qdx import server
#from qdx import modem

def serve(**kwargs):
    waitress.serve(server.app,**kwargs)

def serve_all(port=5000, **kwargs):
    waitress.serve(server.app, host="0.0.0.0", port=port, **kwargs)
