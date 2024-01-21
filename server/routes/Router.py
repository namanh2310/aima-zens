from routes.Calculus import Calculus
from routes.Geometric import Geometric
from routes.Optimize import Optimize
from routes.ODE import ODE
from routes.LinearEq import LinearEq
from routes.DiffnInt import DiffnInt
from routes.CFitting import CFitting
from routes.Proba import Proba
from routes.AIScan import AIScan

class Router:
  def run(app):
    app.register_blueprint(Calculus, url_prefix='/calculus')
    app.register_blueprint(Geometric, url_prefix='/geometric')
    app.register_blueprint(Optimize, url_prefix='/optimize')
    app.register_blueprint(ODE, url_prefix='/ordinary')
    app.register_blueprint(LinearEq, url_prefix='/linear-equation')
    app.register_blueprint(DiffnInt, url_prefix='/diff-int')
    app.register_blueprint(CFitting, url_prefix='/curve-fitting')
    app.register_blueprint(Proba, url_prefix='/probability')
    app.register_blueprint(AIScan, url_prefix='/ai-scanner')