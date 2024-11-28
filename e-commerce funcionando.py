import datetime
import re

class Sistema:
    def __init__(self):
        self.clientes = {}
        self.vendedores = {}
        self.produtos = {}
        self.vendas = []
        self.usuario_atual = None
        self.carrinho = []

    def validar_email(self, email):
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None

    def validar_cpf(self, cpf):
        cpf = ''.join(filter(str.isdigit, cpf))
        return len(cpf) == 11

    def validar_telefone(self, telefone):
        telefone = ''.join(filter(str.isdigit, telefone))
        return len(telefone) >= 10

    def cadastrar_cliente(self):
        print("\n=== Cadastro de Cliente ===")
        nome = input("Nome: ")
        
        while True:
            email = input("Email: ")
            if self.validar_email(email):
                break
            print("Email inválido. Tente novamente.")
        
        while True:
            cpf = input("CPF: ")
            if self.validar_cpf(cpf):
                break
            print("CPF inválido. Tente novamente.")
        
        while True:
            telefone = input("Telefone: ")
            if self.validar_telefone(telefone):
                break
            print("Telefone inválido. Tente novamente.")
        
        senha = input("Senha: ")
        
        self.clientes[email] = {
            'nome': nome,
            'cpf': cpf,
            'telefone': telefone,
            'senha': senha
        }
        print("Cliente cadastrado com sucesso!")

    def cadastrar_vendedor(self):
        print("\n=== Cadastro de Vendedor ===")
        nome = input("Nome: ")
        email = input("Email: ")
        senha = input("Senha: ")
        self.vendedores[email] = {
            'nome': nome,
            'senha': senha,
            'comissao_total': 0
        }
        print("Vendedor cadastrado com sucesso!")

    def cadastrar_produto(self):
        print("\n=== Cadastro de Produto ===")
        nome = input("Nome do produto: ")
        
        while True:
            try:
                valor = float(input("Valor: ").replace(',', '.'))
                break
            except ValueError:
                print("Tente novamente com números válidos")
        
        while True:
            try:
                estoque = int(input("Quantidade em estoque: "))
                break
            except ValueError:
                print("Tente novamente com números válidos")
        
        self.produtos[nome] = {
            'valor': valor,
            'estoque': estoque
        }
        print("Produto cadastrado com sucesso!")

    def fazer_login(self):
        print("\n=== Login ===")
        email = input("Email: ")
        senha = input("Senha: ")
        
        if email == 'admin' and senha == '1234':
            return self.menu_admin()
        
        if email in self.clientes and self.clientes[email]['senha'] == senha:
            self.usuario_atual = email
            return self.menu_cliente()
            
        print("Email ou senha inválidos!")
        return self.menu_principal()

    def adicionar_ao_carrinho(self):
        print("\n=== Produtos Disponíveis ===")
        for nome, info in self.produtos.items():
            print(f"{nome}: R${info['valor']:.2f} - Estoque: {info['estoque']}")
        
        produto = input("\nNome do produto: ")
        if produto not in self.produtos:
            print("Produto não encontrado!")
            return
        
        while True:
            try:
                quantidade = int(input("Quantidade: "))
                if quantidade <= 0:
                    raise ValueError
                if quantidade > self.produtos[produto]['estoque']:
                    print("Lamentamos mas está em falta esse produto")
                    return
                break
            except ValueError:
                print("Tente novamente com um número válido")
        
        self.carrinho.append({
            'produto': produto,
            'quantidade': quantidade,
            'valor': self.produtos[produto]['valor']
        })
        print("Produto adicionado ao carrinho!")

    def finalizar_compra(self):
        if not self.carrinho:
            print("Carrinho vazio!")
            return
        
        print("\n=== Finalizar Compra ===")
        print("\nItens no carrinho:")
        total = 0
        for item in self.carrinho:
            subtotal = item['quantidade'] * item['valor']
            total += subtotal
            print(f"{item['produto']}: {item['quantidade']} x R${item['valor']:.2f} = R${subtotal:.2f}")
        
        print(f"\nTotal: R${total:.2f}")
        
        vendedor_email = input("Email do vendedor: ")
        if vendedor_email not in self.vendedores:
            print("Vendedor não encontrado!")
            return
        
        while True:
            confirma = input("Confirmar compra (Y/N)? ").upper()
            if confirma in ['Y', 'N']:
                break
            print("Por favor, insira Y ou N")
        
        if confirma == 'Y':
            imposto = total * 0.25
            comissao = total * 0.05
            
            self.vendedores[vendedor_email]['comissao_total'] += comissao
            
            for item in self.carrinho:
                self.produtos[item['produto']]['estoque'] -= item['quantidade']
            
            venda = {
                'data': datetime.datetime.now(),
                'cliente': self.clientes[self.usuario_atual]['nome'],
                'vendedor': self.vendedores[vendedor_email]['nome'],
                'itens': self.carrinho.copy(),
                'total': total,
                'imposto': imposto,
                'comissao': comissao
            }
            
            self.vendas.append(venda)
            self.carrinho = []
            print("Compra finalizada com sucesso!")
        else:
            print("Compra cancelada!")

    def relatorio_vendas(self):
        print("\n=== Relatório de Vendas ===")
        data_atual = datetime.datetime.now().date()
        
        vendas_hoje = [v for v in self.vendas if v['data'].date() == data_atual]
        
        if not vendas_hoje:
            print("Nenhuma venda realizada hoje!")
            return
        
        total_vendas = 0
        total_impostos = 0
        total_comissoes = 0
        
        # Dicionário para armazenar vendas por vendedor
        vendas_por_vendedor = {}
        
        for venda in vendas_hoje:
            print(f"\nVenda realizada em {venda['data'].strftime('%d/%m/%Y %H:%M')}")
            print(f"Cliente: {venda['cliente']}")
            print(f"Vendedor: {venda['vendedor']}")
            print("Itens:")
            for item in venda['itens']:
                print(f"- {item['produto']}: {item['quantidade']} x R${item['valor']:.2f}")
            print(f"Total: R${venda['total']:.2f}")
            print(f"Imposto: R${venda['imposto']:.2f}")
            print(f"Comissão: R${venda['comissao']:.2f}")
            
            total_vendas += venda['total']
            total_impostos += venda['imposto']
            total_comissoes += venda['comissao']
            
            # Atualiza estatísticas do vendedor
            if venda['vendedor'] not in vendas_por_vendedor:
                vendas_por_vendedor[venda['vendedor']] = {
                    'num_vendas': 0,
                    'total_vendas': 0,
                    'total_comissao': 0
                }
            vendas_por_vendedor[venda['vendedor']]['num_vendas'] += 1
            vendas_por_vendedor[venda['vendedor']]['total_vendas'] += venda['total']
            vendas_por_vendedor[venda['vendedor']]['total_comissao'] += venda['comissao']
        
        print(f"\nResumo do dia:")
        print(f"Total de vendas: R${total_vendas:.2f}")
        print(f"Total de impostos: R${total_impostos:.2f}")
        print(f"Total de comissões: R${total_comissoes:.2f}")
        
        print("\nResumo por Vendedor:")
        for vendedor, stats in vendas_por_vendedor.items():
            print(f"\nVendedor: {vendedor}")
            print(f"Número de vendas: {stats['num_vendas']}")
            print(f"Total em vendas: R${stats['total_vendas']:.2f}")
            print(f"Total em comissões: R${stats['total_comissao']:.2f}")

    def menu_principal(self):
        while True:
            print("\n=== Menu Principal ===")
            print("1. Login")
            print("2. Registrar")
            print("3. Sair")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                self.fazer_login()
            elif opcao == '2':
                self.cadastrar_cliente()
            elif opcao == '3':
                print("Até logo!")
                break
            else:
                print("Opção inválida!")

    def menu_admin(self):
        while True:
            print("\n=== Menu Admin ===")
            print("1. Cadastrar Vendedor")
            print("2. Cadastrar Produto")
            print("3. Relatório de Vendas")
            print("4. Voltar")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                self.cadastrar_vendedor()
            elif opcao == '2':
                self.cadastrar_produto()
            elif opcao == '3':
                self.relatorio_vendas()
            elif opcao == '4':
                return self.menu_principal()
            else:
                print("Opção inválida!")

    def menu_cliente(self):
        while True:
            print("\n=== Menu Cliente ===")
            print("1. Nossos Produtos")
            print("2. Carrinho")
            print("3. Minha Conta")
            print("4. Sair")
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == '1':
                self.adicionar_ao_carrinho()
            elif opcao == '2':
                print("\n=== Carrinho ===")
                if not self.carrinho:
                    print("Carrinho vazio!")
                else:
                    for item in self.carrinho:
                        print(f"{item['produto']}: {item['quantidade']} x R${item['valor']:.2f}")
                    print("\n1. Finalizar Compra")
                    print("2. Limpar Carrinho")
                    print("3. Voltar")
                    
                    opcao_carrinho = input("Escolha uma opção: ")
                    
                    if opcao_carrinho == '1':
                        self.finalizar_compra()
                    elif opcao_carrinho == '2':
                        self.carrinho = []
                        print("Carrinho limpo!")
            elif opcao == '3':
                print("\n=== Minha Conta ===")
                print(f"Nome: {self.clientes[self.usuario_atual]['nome']}")
                print(f"Email: {self.usuario_atual}")
                print(f"CPF: {self.clientes[self.usuario_atual]['cpf']}")
                print(f"Telefone: {self.clientes[self.usuario_atual]['telefone']}")
            elif opcao == '4':
                self.usuario_atual = None
                return self.menu_principal()
            else:
                print("Opção inválida!")

if __name__ == "__main__":
    sistema = Sistema()
    sistema.menu_principal()