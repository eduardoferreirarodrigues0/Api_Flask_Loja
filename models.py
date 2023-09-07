from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
db = SQLAlchemy()
ma = Marshmallow()

class Produtos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quant = db.Column(db.Integer)
    tipo = db.Column(db.String)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senha = db.Column(db.String, nullable=False)
    login = db.Column(db.String, nullable=False)
    nome_usuario = db.Column(db.String, nullable=False)

class Fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_fornecedor = db.Column(db.String, nullable=False)

class Vendas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    produtos_vendidos = db.relationship('ProdutosVendidos', backref='venda', lazy=True)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)

class ProdutosVendidos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('vendas.id'), nullable=False)
    produtos_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade_vendida = db.Column(db.Integer, nullable=False)


class ProdutosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Produtos
        include_fk = True

    id = ma.auto_field()
    nome_produto = ma.auto_field()
    price = ma.auto_field()
    quant = ma.auto_field()
    tipo = ma.auto_field()
    fornecedor_id = ma.auto_field()

class UsuarioSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario

    id = ma.auto_field()
    senha = ma.auto_field()
    login = ma.auto_field()
    nome_usuario = ma.auto_field()


class FornecedorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Fornecedor

    id = ma.auto_field
    nome_fornecedor = ma.auto_field

class VendasSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vendas
        include_fk = True

    id = ma.auto_field()
    usuario_id = ma.auto_field()
    produtos_vendidos = ma.auto_field()
    data_venda = ma.auto_field()

class ProdutosVendidosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProdutosVendidos
        include_fk = True

    id = ma.auto_field()
    venda_id = ma.auto_field()
    produtos_id = ma.auto_field()
    quantidade_vendida = ma.auto_field()