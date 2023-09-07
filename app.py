from flask import Flask
from flask_restful import Api
from models import db, ma
from resources import UsuarioResource, ProdutosResource,FornecedorResource,VendasResource,ProdutosVendidosResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api = Api(app)
db.init_app(app)
ma.init_app(app)


api.add_resource(ProdutosResource, '/cadastrar_produtos', '/cadastrar_produtos/<int:produtos_id>')
api.add_resource(UsuarioResource, '/cadastrar_usuarios', '/cadastrar_usuarios/<int:usuarios_id>')
api.add_resource(FornecedorResource, '/cadastrar_fornecedor','/cadastrar_fornecedor/<int:fornecedor_id>')
api.add_resource(VendasResource, '/cadastrar_vendas','/cadastrar_vendas/<int:vendas_id>')
api.add_resource(ProdutosVendidosResource, '/cadastrar_produtos_vendidos','/cadastrar_produtos_vendidos/<int:produtos_vendidos_id>')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)