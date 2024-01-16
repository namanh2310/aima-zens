from routes.calculator.Optimize import Optimize
from routes.calculator.Calculus import Calculus
from routes.calculator.ODE import ODE
from routes.calculator.LinearEq import LinearEq
from routes.calculator.DiffnInt import DiffnInt
from routes.calculator.CFitting import CFitting
from routes.calculator.Geometric import Geometric
from routes.calculator.Proba import Proba
from routes.calculator.AIScan import AIScan
from routes.forum.Auth import Auth
from routes.forum.Post import Post
from routes.forum.Comment import Comment
from routes.forum.Vote import Vote

class Router:
  def run(app):
    # Calculator
    app.register_blueprint(Optimize, url_prefix='/Optimize')
    app.register_blueprint(Calculus, url_prefix='/Calculus')
    app.register_blueprint(ODE, url_prefix='/ODE')
    app.register_blueprint(LinearEq, url_prefix='/Linear')
    app.register_blueprint(DiffnInt, url_prefix='/DiffnInt')
    app.register_blueprint(CFitting, url_prefix='/CFitting')
    app.register_blueprint(Geometric, url_prefix='/Geometric')
    app.register_blueprint(Proba, url_prefix='/Probability')
    app.register_blueprint(AIScan, url_prefix='/AIScanner')

    # Forum
    app.register_blueprint(Auth, url_prefix='/Auth')
    app.register_blueprint(Post, url_prefix='/Post')
    app.register_blueprint(Comment, url_prefix='/Comment')
    app.register_blueprint(Vote, url_prefix='/Vote')

    