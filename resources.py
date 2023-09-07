from flask_restful import Resource, request
from models import db, ProdutosSchema,Produtos,Usuario, UsuarioSchema,Fornecedor,FornecedorSchema,ProdutosVendidos,Vendas,VendasSchema,ProdutosVendidosSchema

class ProdutosResource(Resource):
    # Cadastro de Produtos
    def post(self):
        data = request.json

        # Verifique se o fornecedor existe
        fornecedor_id = data.get('fornecedor_id')
        fornecedor = Fornecedor.query.get(fornecedor_id)

        if not fornecedor:
            return {"message": "Fornecedor não encontrado"}, 400

        # Continue com a criação do produto
        produtos = Produtos(
            nome_produto=data['nome_produto'],
            price=data['price'],
            quant=data['quant'],
            tipo=data['tipo'],
            fornecedor_id=fornecedor_id
        )

        db.session.add(produtos)
        db.session.commit()
        return ProdutosSchema().dump(produtos), 201
    
    #Listagem de Produtos
    def get(self, produtos=None):
        if produtos is None:
            produtos = Produtos.query.all()
            return ProdutosSchema(many=True).dump(produtos)
        
        produtos = Produtos.query.get(produtos)
        if not produtos:
            return {"message": "Produtos não encontrado"}, 404
        return ProdutosSchema().dump(produtos)
    
    #Alteração de produtos
    def put(self, produtos_id):
        produtos = Produtos.query.get(produtos_id)
        if not produtos:
            return {"message": "Produtos não encontrado"}, 404

        data = request.json
        produtos.nome_produto = data.get('nome_produto', produtos.nome_produto)
        produtos.price = data.get('price', produtos.price)
        produtos.quant = data.get('quant', produtos.quant)
        produtos.tipo = data.get('tipo', produtos.tipo)
        produtos.fornecedor_id = data.get('fornecedor_id',produtos.fornecedor_id)

        db.session.commit()

        return ProdutosSchema().dump(produtos)

    
    #Exclusão de produtos
    def delete(self, produtos_id):
        produtos = Produtos.query.get(produtos_id)
        if not produtos:
            return {"message": "Produtos não encontrado"}, 404
        
        db.session.delete(produtos)
        db.session.commit()

        return {"message": "Produtos excluído com sucesso"}, 204



class UsuarioResource(Resource):
    #Cadastro de Usuarios
    def post(self):
        data = request.json
        usuarios = Usuario(nome_usuario=data['nome_usuario'], login=data['login'], senha=data['senha'])
        db.session.add(usuarios)
        db.session.commit()
        return UsuarioSchema().dump(usuarios),201
    
    #Listagem de Usuarios
    def get(self, usuarios=None):
        if usuarios is None:
            usuarios = Usuario.query.all()
            return UsuarioSchema(many=True).dump(usuarios)
        
        usuarios = Usuario.query.get(usuarios)
        if not usuarios:
            return {"message": "Usuario não encontrado"}, 404
        return UsuarioSchema().dump(usuarios)
    
    #Alteração de usuarios
    def put(self, usuarios_id):
        usuario = Usuario.query.get(usuarios_id)
        if not usuario:
            return {"message": "usuarios não encontrado"}, 404

        data = request.json
        usuario.nome_usuario = data.get('nome_usuario', usuario.nome_usuario)
        usuario.login= data.get('login', usuario.login)
        usuario.senha = data.get('senha', usuario.senha)

        db.session.commit()

        return UsuarioSchema().dump(Usuario)
    
    #Exclusão de usuarios
    def delete(self, usuarios_id):
        usuario = Usuario.query.get(usuarios_id)
        if not usuario:
            return {"message": "usuarios não encontrado"}, 404
        
        db.session.delete(usuario)
        db.session.commit()

        return {"message": "usuarios excluído com sucesso"}, 204


class FornecedorResource(Resource):
    #Cadastro de fornecedores
    def post(self):
        data = request.json
        fornecedores = Fornecedor(nome_fornecedor=data['nome_fornecedor'])
        db.session.add(fornecedores)
        db.session.commit()
        return FornecedorSchema().dump(fornecedores),201
    
    #Listagem de fornecedores
    def get(self, fornecedores=None):
        if fornecedores is None:
            fornecedores = Fornecedor.query.all()
            return FornecedorSchema(many=True).dump(fornecedores)
        
        fornecedores = Fornecedor.query.get(fornecedores)
        if not fornecedores:
            return {"message": "fornecedores não encontrados"}, 404
        return FornecedorSchema().dump(fornecedores)
    
    #Alteração de fornecedores
    def put(self, fornecedores_id):
        fornecedor = Fornecedor.query.get(fornecedores_id)
        if not fornecedor:
            return {"message": "fornecedor não encontrado"}, 404

        data = request.json
        fornecedor.nome_fornecedor = data.get('nome_fornecedor', fornecedor.nome_fornecedor)

        db.session.commit()

        return FornecedorSchema().dump(fornecedor)
    
    #Exclusão de fornecedors
    def delete(self, fornecedores_id):
        fornecedor = Fornecedor.query.get(fornecedores_id)
        if not fornecedor:
            return {"message": "fornecedores não encontrado"}, 404
        
        db.session.delete(fornecedor)
        db.session.commit()

        return {"message": "fornecedores excluído com sucesso"}, 204
    
class VendasResource(Resource):
    def post(self):
        data = request.json

        # Certifique-se de que o JSON de dados tenha a estrutura correta
        if "usuario_id" not in data or "produtos_vendidos" not in data:
            return {"message": "JSON de dados incompleto"}, 400

        usuario_id = data["usuario_id"]
        produtos_vendidos = data["produtos_vendidos"]

        # Crie uma lista para armazenar os objetos ProdutosVendidos
        produtos_vendidos_objs = []

        # Itere pelos produtos vendidos no JSON
        for item in produtos_vendidos:
            produto_id = item.get("produto_id")
            quantidade_vendida = item.get("quantidade_vendida")

            # Verifique se o produto existe
            produto = Produtos.query.get(produto_id)
            if not produto:
                return {"message": f"Produto com ID {produto_id} não encontrado"}, 404

            # Verifique se a quantidade vendida é válida
            if quantidade_vendida <= 0:
                return {"message": "Quantidade vendida deve ser maior que zero"}, 400

            # Verifique se há estoque suficiente
            if quantidade_vendida > produto.quant:
                return {"message": f"Estoque insuficiente para o produto {produto_id}"}, 400

            # Crie o objeto ProdutosVendidos
            produtos_vendidos_obj = ProdutosVendidos(
                produtos_id=produto_id,
                quantidade_vendida=quantidade_vendida
            )

            produtos_vendidos_objs.append(produtos_vendidos_obj)
            
            # Atualize o estoque do produto
            produto.quant -= quantidade_vendida
            db.session.add(produto)

        # Crie a venda
        nova_venda = Vendas(usuario_id=usuario_id, produtos_vendidos=produtos_vendidos_objs)

        # Adicione a nova venda à sessão do banco de dados e faça o commit
        db.session.add(nova_venda)
        db.session.commit()

        return {"message": "Venda realizada com sucesso"}, 201
    
    def get(self, vendas=None):
        if vendas is None:
            vendas = Vendas.query.all()
            return VendasSchema(many=True).dump(vendas)
        
        vendas = Vendas.query.get(vendas)
        if not vendas:
            return {"message": "Venda não encontrada"}, 404
        return VendasSchema().dump(vendas)
    
    def put(self, vendas_id):
        venda = Vendas.query.get(vendas_id)
        if not venda:
            return {"message": "Venda não encontrada"}, 404

        data = request.json
        venda.usuario_id = data.get('usuario_id', venda.usuario_id)
        venda.produtos_vendidos = data.get('produtos_vendidos', venda.produtos_vendidos)

        db.session.commit()

        return VendasSchema().dump(venda)
    
    def delete(self, vendas_id):
        venda = Vendas.query.get(vendas_id)
        if not venda:
            return {"message": "Venda não encontrada"}, 404
        
        db.session.delete(venda)
        db.session.commit()

        return {"message": "Venda excluída com sucesso"}, 204
    
class ProdutosVendidosResource(Resource):
    # Listagem de Produtos Vendidos
    def get(self, produtos_vendidos=None):
        if produtos_vendidos is None:
            produtos_vendidos = ProdutosVendidos.query.all()
            return ProdutosVendidosSchema(many=True).dump(produtos_vendidos)
        
        produtos_vendidos = ProdutosVendidos.query.get(produtos_vendidos)
        if not produtos_vendidos:
            return {"message": "Produtos vendidos não encontrados"}, 404
        return ProdutosVendidosSchema().dump(produtos_vendidos)
    
