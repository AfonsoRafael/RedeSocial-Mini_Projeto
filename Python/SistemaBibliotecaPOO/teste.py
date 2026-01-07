from datetime import datetime, timedelta
from typing import Optional, List, Dict
import uuid
import sys

# ====================== ENTIDADES DO DOMÍNIO ======================

class Livro:
    def __init__(self, titulo: str, autor: str, isbn: str, ano_publicacao: int, 
                 editora: str, categoria: str, exemplares: int = 1):
        self.id = int(str(uuid.uuid4().int)[:8])
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.ano_publicacao = ano_publicacao
        self.editora = editora
        self.categoria = categoria
        self.disponivel = exemplares > 0
        self.exemplares = exemplares
    
    def emprestar(self) -> bool:
        if self.verificar_disponibilidade():
            self.exemplares -= 1
            self.disponivel = self.exemplares > 0
            return True
        return False
    
    def devolver(self) -> bool:
        self.exemplares += 1
        self.disponivel = True
        return True
    
    def verificar_disponibilidade(self) -> bool:
        return self.exemplares > 0
    
    def __str__(self):
        disponivel_texto = "✓ Disponível" if self.disponivel else "✗ Indisponível"
        return f"[ID: {self.id}] {self.titulo} - {self.autor} ({self.exemplares} ex.) - {disponivel_texto}"


class Usuario:
    def __init__(self, nome: str, email: str, telefone: str):
        self.id = int(str(uuid.uuid4().int)[:8])
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.data_cadastro = datetime.now()
        self.ativo = True
    
    def __str__(self):
        return f"[ID: {self.id}] {self.nome} ({self.email})"


class PessoaFisica(Usuario):
    def __init__(self, nome: str, email: str, telefone: str, cpf: str, data_nascimento: str):
        super().__init__(nome, email, telefone)
        self.cpf = cpf
        self.data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y")
        self.tipo = "COMUM"
        self.max_livros = 3
        self.livros_emprestados = 0
    
    def pode_emprestar(self) -> bool:
        return self.livros_emprestados < self.max_livros
    
    def __str__(self):
        return f"[PF - ID: {self.id}] {self.nome} (CPF: {self.cpf}) - {self.livros_emprestados}/{self.max_livros} livros"


class PessoaJuridica(Usuario):
    def __init__(self, nome: str, email: str, telefone: str, cnpj: str, 
                 razao_social: str, responsavel: str):
        super().__init__(nome, email, telefone)
        self.cnpj = cnpj
        self.razao_social = razao_social
        self.responsavel = responsavel
        self.tipo = "INSTITUCIONAL"
        self.max_livros = 10
        self.livros_emprestados = 0
    
    def pode_emprestar(self) -> bool:
        return self.livros_emprestados < self.max_livros
    
    def __str__(self):
        return f"[PJ - ID: {self.id}] {self.razao_social} (CNPJ: {self.cnpj}) - {self.livros_emprestados}/{self.max_livros} livros"


class ItemEmprestimo:
    def __init__(self, livro_id: int, quantidade: int = 1):
        self.livro_id = livro_id
        self.quantidade = quantidade


class Emprestimo:
    def __init__(self, usuario_id: int, itens: List[ItemEmprestimo]):
        self.id = int(str(uuid.uuid4().int)[:8])
        self.usuario_id = usuario_id
        self.itens = itens
        self.data_emprestimo = datetime.now()
        self.data_devolucao_prevista = self.data_emprestimo + timedelta(days=14)
        self.status = "ATIVO"
    
    def calcular_dias_atraso(self) -> int:
        if self.status == "ATIVO" and datetime.now() > self.data_devolucao_prevista:
            return (datetime.now() - self.data_devolucao_prevista).days
        return 0
    
    def __str__(self):
        dias_atraso = self.calcular_dias_atraso()
        atraso_texto = f" ({dias_atraso} dias de atraso)" if dias_atraso > 0 else ""
        return f"[ID: {self.id}] Status: {self.status}{atraso_texto} - Devolução: {self.data_devolucao_prevista.strftime('%d/%m/%Y')}"


class Funcionario:
    def __init__(self, nome: str, email: str, telefone: str, 
                 matricula: str, cargo: str, salario: float):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.matricula = matricula
        self.cargo = cargo
        self.salario = salario
    
    def __str__(self):
        return f"Funcionário: {self.nome} ({self.cargo}) - Matrícula: {self.matricula}"


class Catalogo:
    def __init__(self, nome: str):
        self.id = int(str(uuid.uuid4().int)[:8])
        self.nome = nome
        self.data_criacao = datetime.now()
        self.livros = {}
    
    def adicionar_livro(self, livro: Livro) -> bool:
        if livro.id not in self.livros:
            self.livros[livro.id] = livro
            return True
        return False
    
    def buscar_por_titulo(self, termo: str) -> List[Livro]:
        resultados = []
        for livro in self.livros.values():
            if termo.lower() in livro.titulo.lower():
                resultados.append(livro)
        return resultados
    
    def buscar_por_autor(self, termo: str) -> List[Livro]:
        resultados = []
        for livro in self.livros.values():
            if termo.lower() in livro.autor.lower():
                resultados.append(livro)
        return resultados
    
    def obter_livro_por_id(self, livro_id: int) -> Optional[Livro]:
        return self.livros.get(livro_id)
    
    def __str__(self):
        return f"Catálogo: {self.nome} ({len(self.livros)} livros)"


class Biblioteca:
    def __init__(self, nome: str, endereco: str, telefone: str):
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone
        self.catalogo = Catalogo(f"Catálogo da {nome}")
        self.usuarios = {}
        self.emprestimos = {}
        self.emprestimos_ativos = {}
        self.funcionarios = []
    
    def registrar_usuario(self, usuario: Usuario) -> bool:
        if usuario.id not in self.usuarios:
            self.usuarios[usuario.id] = usuario
            return True
        return False
    
    def cadastrar_livro(self, livro: Livro) -> bool:
        return self.catalogo.adicionar_livro(livro)
    
    def realizar_emprestimo(self, usuario_id: int, livro_ids: List[int]) -> Optional[Emprestimo]:
        usuario = self.usuarios.get(usuario_id)
        if not usuario or not usuario.ativo:
            print(f"❌ Usuário não encontrado ou inativo")
            return None
        
        if not usuario.pode_emprestar():
            print(f"❌ Usuário atingiu o limite máximo de {usuario.max_livros} livros")
            return None
        
        itens = []
        for livro_id in livro_ids:
            livro = self.catalogo.obter_livro_por_id(livro_id)
            if livro and livro.verificar_disponibilidade():
                itens.append(ItemEmprestimo(livro_id))
                livro.emprestar()
                usuario.livros_emprestados += 1
                print(f"  ✓ Livro '{livro.titulo}' emprestado")
            else:
                print(f"  ✗ Livro ID {livro_id} não disponível")
        
        if not itens:
            print("❌ Nenhum livro pôde ser emprestado")
            return None
        
        emprestimo = Emprestimo(usuario_id, itens)
        self.emprestimos[emprestimo.id] = emprestimo
        
        if usuario_id not in self.emprestimos_ativos:
            self.emprestimos_ativos[usuario_id] = []
        self.emprestimos_ativos[usuario_id].append(emprestimo.id)
        
        print(f"✅ Empréstimo #{emprestimo.id} realizado com sucesso!")
        return emprestimo
    
    def processar_devolucao(self, emprestimo_id: int) -> bool:
        emprestimo = self.emprestimos.get(emprestimo_id)
        if not emprestimo or emprestimo.status != "ATIVO":
            print(f"❌ Empréstimo não encontrado ou já devolvido")
            return False
        
        emprestimo.status = "DEVOLVIDO"
        usuario = self.usuarios.get(emprestimo.usuario_id)
        
        for item in emprestimo.itens:
            livro = self.catalogo.obter_livro_por_id(item.livro_id)
            if livro:
                livro.devolver()
                print(f"  ✓ Livro '{livro.titulo}' devolvido")
                if usuario:
                    usuario.livros_emprestados -= 1
        
        if emprestimo.usuario_id in self.emprestimos_ativos:
            if emprestimo_id in self.emprestimos_ativos[emprestimo.usuario_id]:
                self.emprestimos_ativos[emprestimo.usuario_id].remove(emprestimo_id)
        
        dias_atraso = emprestimo.calcular_dias_atraso()
        if dias_atraso > 0:
            print(f"⚠️  Devolução com {dias_atraso} dias de atraso")
        
        print(f"✅ Devolução do empréstimo #{emprestimo_id} processada!")
        return True
    
    def gerar_relatorio(self) -> str:
        relatorio = []
        relatorio.append("=" * 50)
        relatorio.append(f"RELATÓRIO DA BIBLIOTECA {self.nome}")
        relatorio.append("=" * 50)
        relatorio.append(f"📚 Total de livros: {len(self.catalogo.livros)}")
        relatorio.append(f"👥 Total de usuários: {len(self.usuarios)}")
        relatorio.append(f"📖 Total de empréstimos: {len(self.emprestimos)}")
        
        ativos = sum(1 for e in self.emprestimos.values() if e.status == "ATIVO")
        relatorio.append(f"📋 Empréstimos ativos: {ativos}")
        
        relatorio.append("\n📊 ESTATÍSTICAS DE USUÁRIOS:")
        total_pf = sum(1 for u in self.usuarios.values() if isinstance(u, PessoaFisica))
        total_pj = sum(1 for u in self.usuarios.values() if isinstance(u, PessoaJuridica))
        relatorio.append(f"  • Pessoas Físicas: {total_pf}")
        relatorio.append(f"  • Pessoas Jurídicas: {total_pj}")
        
        relatorio.append("\n🏆 TOP 5 LIVROS MAIS POPULARES:")
        contagem = {}
        for emprestimo in self.emprestimos.values():
            for item in emprestimo.itens:
                contagem[item.livro_id] = contagem.get(item.livro_id, 0) + 1
        
        top5 = sorted(contagem.items(), key=lambda x: x[1], reverse=True)[:5]
        for livro_id, qtd in top5:
            livro = self.catalogo.obter_livro_por_id(livro_id)
            if livro:
                relatorio.append(f"  • {livro.titulo}: {qtd} empréstimos")
        
        return "\n".join(relatorio)
    
    def adicionar_funcionario(self, funcionario: Funcionario):
        self.funcionarios.append(funcionario)
    
    def buscar_livros(self, termo: str) -> List[Livro]:
        resultados = []
        resultados.extend(self.catalogo.buscar_por_titulo(termo))
        
        # Evita duplicatas
        livros_vistos = set()
        for livro in self.catalogo.buscar_por_autor(termo):
            if livro.id not in livros_vistos:
                resultados.append(livro)
                livros_vistos.add(livro.id)
        
        return resultados
    
    def __str__(self):
        return f"🏛️  Biblioteca {self.nome}"


# ====================== INTERFACE INTERATIVA ======================

class SistemaBiblioteca:
    def __init__(self):
        self.biblioteca = Biblioteca(
            nome="Biblioteca Central",
            endereco="Av. Principal, 1000",
            telefone="(11) 9999-8888"
        )
        self.carregar_dados_exemplo()
    
    def carregar_dados_exemplo(self):
        """Carrega alguns dados de exemplo para testes"""
        # Adiciona funcionário
        funcionario = Funcionario(
            nome="Ana Silva",
            email="ana@biblioteca.com",
            telefone="(11) 98888-7777",
            matricula="FUNC001",
            cargo="Bibliotecária",
            salario=3800.00
        )
        self.biblioteca.adicionar_funcionario(funcionario)
        
        # Cadastra alguns livros
        livros_exemplo = [
            Livro("Dom Casmurro", "Machado de Assis", "978-85-7232-144-9", 1899, 
                  "Editora Garnier", "Romance", 5),
            Livro("1984", "George Orwell", "978-85-359-0279-0", 1949,
                  "Companhia das Letras", "Ficção Científica", 3),
            Livro("O Pequeno Príncipe", "Antoine de Saint-Exupéry", "978-85-01-05000-1", 1943,
                  "Agir", "Infantil", 4),
            Livro("Harry Potter e a Pedra Filosofal", "J.K. Rowling", "978-85-325-1491-5", 1997,
                  "Rocco", "Fantasia", 6),
            Livro("A Culpa é das Estrelas", "John Green", "978-85-8057-444-3", 2012,
                  "Intrínseca", "Romance", 2),
            Livro("O Senhor dos Anéis", "J.R.R. Tolkien", "978-85-359-0496-1", 1954,
                  "Martins Fontes", "Fantasia", 3)
        ]
        
        for livro in livros_exemplo:
            self.biblioteca.cadastrar_livro(livro)
        
        # Cadastra alguns usuários
        usuario1 = PessoaFisica(
            nome="João Santos",
            email="joao@email.com",
            telefone="(11) 99999-1111",
            cpf="111.222.333-44",
            data_nascimento="15/05/1990"
        )
        
        usuario2 = PessoaJuridica(
            nome="Escola Municipal",
            email="escola@edu.gov.br",
            telefone="(11) 3333-4444",
            cnpj="12.345.678/0001-90",
            razao_social="Escola Municipal de São Paulo",
            responsavel="Maria Oliveira"
        )
        
        self.biblioteca.registrar_usuario(usuario1)
        self.biblioteca.registrar_usuario(usuario2)
    
    def mostrar_menu_principal(self):
        while True:
            print("\n" + "="*50)
            print("📚 SISTEMA DE BIBLIOTECA - MENU PRINCIPAL")
            print("="*50)
            print("1. 📖 Gerenciar Livros")
            print("2. 👥 Gerenciar Usuários")
            print("3. 🔄 Gerenciar Empréstimos")
            print("4. 📊 Relatórios e Consultas")
            print("5. ℹ️  Informações da Biblioteca")
            print("0. 🚪 Sair")
            print("="*50)
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.menu_livros()
            elif opcao == "2":
                self.menu_usuarios()
            elif opcao == "3":
                self.menu_emprestimos()
            elif opcao == "4":
                self.menu_relatorios()
            elif opcao == "5":
                self.menu_informacoes()
            elif opcao == "0":
                print("\nObrigado por usar o Sistema de Biblioteca!")
                sys.exit(0)
            else:
                print("❌ Opção inválida! Tente novamente.")
    
    def menu_livros(self):
        while True:
            print("\n" + "="*50)
            print("📖 MENU DE LIVROS")
            print("="*50)
            print("1. Adicionar novo livro")
            print("2. Listar todos os livros")
            print("3. Buscar livro por título")
            print("4. Buscar livro por autor")
            print("5. Ver detalhes de um livro")
            print("0. Voltar ao menu principal")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.adicionar_livro()
            elif opcao == "2":
                self.listar_livros()
            elif opcao == "3":
                self.buscar_livro_titulo()
            elif opcao == "4":
                self.buscar_livro_autor()
            elif opcao == "5":
                self.ver_detalhes_livro()
            elif opcao == "0":
                break
            else:
                print("❌ Opção inválida!")
    
    def adicionar_livro(self):
        print("\n➕ ADICIONAR NOVO LIVRO")
        print("-"*30)
        
        titulo = input("Título: ")
        autor = input("Autor: ")
        isbn = input("ISBN: ")
        ano = int(input("Ano de publicação: "))
        editora = input("Editora: ")
        categoria = input("Categoria: ")
        exemplares = int(input("Quantidade de exemplares: "))
        
        livro = Livro(titulo, autor, isbn, ano, editora, categoria, exemplares)
        
        if self.biblioteca.cadastrar_livro(livro):
            print(f"\n✅ Livro '{titulo}' cadastrado com sucesso!")
            print(f"ID do livro: {livro.id}")
        else:
            print("\n❌ Erro ao cadastrar livro!")
    
    def listar_livros(self):
        print("\n📚 LISTA DE TODOS OS LIVROS")
        print("-"*50)
        
        if not self.biblioteca.catalogo.livros:
            print("Nenhum livro cadastrado.")
            return
        
        for i, livro in enumerate(self.biblioteca.catalogo.livros.values(), 1):
            print(f"{i}. {livro}")
    
    def buscar_livro_titulo(self):
        termo = input("\nDigite o título (ou parte dele) para buscar: ")
        resultados = self.biblioteca.catalogo.buscar_por_titulo(termo)
        
        print(f"\n🔍 RESULTADOS PARA '{termo}':")
        print("-"*50)
        
        if resultados:
            for i, livro in enumerate(resultados, 1):
                print(f"{i}. {livro}")
        else:
            print("Nenhum livro encontrado.")
    
    def buscar_livro_autor(self):
        termo = input("\nDigite o nome do autor (ou parte dele) para buscar: ")
        resultados = self.biblioteca.catalogo.buscar_por_autor(termo)
        
        print(f"\n🔍 LIVROS DO AUTOR '{termo}':")
        print("-"*50)
        
        if resultados:
            for i, livro in enumerate(resultados, 1):
                print(f"{i}. {livro}")
        else:
            print("Nenhum livro encontrado.")
    
    def ver_detalhes_livro(self):
        try:
            livro_id = int(input("\nDigite o ID do livro: "))
            livro = self.biblioteca.catalogo.obter_livro_por_id(livro_id)
            
            if livro:
                print("\n📖 DETALHES DO LIVRO")
                print("-"*50)
                print(f"ID: {livro.id}")
                print(f"Título: {livro.titulo}")
                print(f"Autor: {livro.autor}")
                print(f"ISBN: {livro.isbn}")
                print(f"Ano: {livro.ano_publicacao}")
                print(f"Editora: {livro.editora}")
                print(f"Categoria: {livro.categoria}")
                print(f"Exemplares disponíveis: {livro.exemplares}")
                print(f"Disponível: {'Sim' if livro.disponivel else 'Não'}")
            else:
                print("❌ Livro não encontrado!")
        except ValueError:
            print("❌ ID inválido!")
    
    def menu_usuarios(self):
        while True:
            print("\n" + "="*50)
            print("👥 MENU DE USUÁRIOS")
            print("="*50)
            print("1. Cadastrar Pessoa Física")
            print("2. Cadastrar Pessoa Jurídica")
            print("3. Listar todos os usuários")
            print("4. Buscar usuário por nome")
            print("5. Ver empréstimos de um usuário")
            print("0. Voltar ao menu principal")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.cadastrar_pessoa_fisica()
            elif opcao == "2":
                self.cadastrar_pessoa_juridica()
            elif opcao == "3":
                self.listar_usuarios()
            elif opcao == "4":
                self.buscar_usuario()
            elif opcao == "5":
                self.ver_emprestimos_usuario()
            elif opcao == "0":
                break
            else:
                print("❌ Opção inválida!")
    
    def cadastrar_pessoa_fisica(self):
        print("\n👤 CADASTRAR PESSOA FÍSICA")
        print("-"*30)
        
        nome = input("Nome completo: ")
        email = input("E-mail: ")
        telefone = input("Telefone: ")
        cpf = input("CPF: ")
        data_nasc = input("Data de nascimento (DD/MM/AAAA): ")
        
        usuario = PessoaFisica(nome, email, telefone, cpf, data_nasc)
        
        if self.biblioteca.registrar_usuario(usuario):
            print(f"\n✅ Usuário '{nome}' cadastrado com sucesso!")
            print(f"ID do usuário: {usuario.id}")
        else:
            print("\n❌ Erro ao cadastrar usuário!")
    
    def cadastrar_pessoa_juridica(self):
        print("\n🏢 CADASTRAR PESSOA JURÍDICA")
        print("-"*30)
        
        nome = input("Nome da instituição: ")
        email = input("E-mail: ")
        telefone = input("Telefone: ")
        cnpj = input("CNPJ: ")
        razao_social = input("Razão Social: ")
        responsavel = input("Nome do responsável: ")
        
        usuario = PessoaJuridica(nome, email, telefone, cnpj, razao_social, responsavel)
        
        if self.biblioteca.registrar_usuario(usuario):
            print(f"\n✅ Instituição '{nome}' cadastrada com sucesso!")
            print(f"ID do usuário: {usuario.id}")
        else:
            print("\n❌ Erro ao cadastrar instituição!")
    
    def listar_usuarios(self):
        print("\n👥 LISTA DE TODOS OS USUÁRIOS")
        print("-"*50)
        
        if not self.biblioteca.usuarios:
            print("Nenhum usuário cadastrado.")
            return
        
        for i, usuario in enumerate(self.biblioteca.usuarios.values(), 1):
            print(f"{i}. {usuario}")
    
    def buscar_usuario(self):
        termo = input("\nDigite o nome (ou parte dele) para buscar: ").lower()
        resultados = []
        
        for usuario in self.biblioteca.usuarios.values():
            if termo in usuario.nome.lower():
                resultados.append(usuario)
        
        print(f"\n🔍 RESULTADOS PARA '{termo}':")
        print("-"*50)
        
        if resultados:
            for i, usuario in enumerate(resultados, 1):
                print(f"{i}. {usuario}")
        else:
            print("Nenhum usuário encontrado.")
    
    def ver_emprestimos_usuario(self):
        try:
            usuario_id = int(input("\nDigite o ID do usuário: "))
            usuario = self.biblioteca.usuarios.get(usuario_id)
            
            if not usuario:
                print("❌ Usuário não encontrado!")
                return
            
            print(f"\n📋 EMPRÉSTIMOS DE {usuario.nome}")
            print("-"*50)
            
            emprestimos_ativos = self.biblioteca.emprestimos_ativos.get(usuario_id, [])
            
            if not emprestimos_ativos:
                print("Nenhum empréstimo ativo.")
                return
            
            for emp_id in emprestimos_ativos:
                emprestimo = self.biblioteca.emprestimos.get(emp_id)
                if emprestimo:
                    print(f"\nEmpréstimo: {emprestimo}")
                    print("Livros emprestados:")
                    for item in emprestimo.itens:
                        livro = self.biblioteca.catalogo.obter_livro_por_id(item.livro_id)
                        if livro:
                            print(f"  • {livro.titulo}")
        except ValueError:
            print("❌ ID inválido!")
    
    def menu_emprestimos(self):
        while True:
            print("\n" + "="*50)
            print("🔄 MENU DE EMPRÉSTIMOS")
            print("="*50)
            print("1. Realizar novo empréstimo")
            print("2. Processar devolução")
            print("3. Listar todos os empréstimos")
            print("4. Listar empréstimos ativos")
            print("5. Listar empréstimos atrasados")
            print("0. Voltar ao menu principal")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.realizar_emprestimo()
            elif opcao == "2":
                self.processar_devolucao()
            elif opcao == "3":
                self.listar_emprestimos()
            elif opcao == "4":
                self.listar_emprestimos_ativos()
            elif opcao == "5":
                self.listar_emprestimos_atrasados()
            elif opcao == "0":
                break
            else:
                print("❌ Opção inválida!")
    
    def realizar_emprestimo(self):
        print("\n📖 REALIZAR NOVO EMPRÉSTIMO")
        print("-"*30)
        
        # Lista usuários
        print("\nUsuários disponíveis:")
        for usuario in self.biblioteca.usuarios.values():
            print(f"  ID {usuario.id}: {usuario.nome} ({usuario.tipo})")
        
        try:
            usuario_id = int(input("\nDigite o ID do usuário: "))
            
            # Lista livros disponíveis
            print("\nLivros disponíveis:")
            livros_disponiveis = [l for l in self.biblioteca.catalogo.livros.values() if l.disponivel]
            
            if not livros_disponiveis:
                print("❌ Nenhum livro disponível no momento!")
                return
            
            for i, livro in enumerate(livros_disponiveis, 1):
                print(f"{i}. {livro.titulo} (ID: {livro.id}) - {livro.exemplares} ex.")
            
            livro_ids_input = input("\nDigite os IDs dos livros (separados por vírgula): ")
            livro_ids = [int(id.strip()) for id in livro_ids_input.split(",")]
            
            emprestimo = self.biblioteca.realizar_emprestimo(usuario_id, livro_ids)
            
            if emprestimo:
                print(f"\n📝 RESUMO DO EMPRÉSTIMO:")
                print(f"ID do empréstimo: {emprestimo.id}")
                print(f"Data de devolução: {emprestimo.data_devolucao_prevista.strftime('%d/%m/%Y')}")
                
        except ValueError:
            print("❌ Entrada inválida!")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def processar_devolucao(self):
        print("\n📚 PROCESSAR DEVOLUÇÃO")
        print("-"*30)
        
        # Lista empréstimos ativos
        emprestimos_ativos = [e for e in self.biblioteca.emprestimos.values() if e.status == "ATIVO"]
        
        if not emprestimos_ativos:
            print("❌ Nenhum empréstimo ativo para devolver!")
            return
        
        print("\nEmpréstimos ativos:")
        for emprestimo in emprestimos_ativos:
            usuario = self.biblioteca.usuarios.get(emprestimo.usuario_id)
            usuario_nome = usuario.nome if usuario else "Desconhecido"
            dias_atraso = emprestimo.calcular_dias_atraso()
            atraso_text = f" ({dias_atraso} dias de atraso)" if dias_atraso > 0 else ""
            print(f"  ID {emprestimo.id}: {usuario_nome} - Devolução: {emprestimo.data_devolucao_prevista.strftime('%d/%m/%Y')}{atraso_text}")
        
        try:
            emprestimo_id = int(input("\nDigite o ID do empréstimo para devolver: "))
            self.biblioteca.processar_devolucao(emprestimo_id)
        except ValueError:
            print("❌ ID inválido!")
    
    def listar_emprestimos(self):
        print("\n📋 LISTA DE TODOS OS EMPRÉSTIMOS")
        print("-"*50)
        
        if not self.biblioteca.emprestimos:
            print("Nenhum empréstimo registrado.")
            return
        
        for emprestimo in self.biblioteca.emprestimos.values():
            usuario = self.biblioteca.usuarios.get(emprestimo.usuario_id)
            usuario_nome = usuario.nome if usuario else "Desconhecido"
            print(f"\nEmpréstimo: {emprestimo}")
            print(f"Usuário: {usuario_nome}")
            
            if emprestimo.itens:
                print("Livros:")
                for item in emprestimo.itens:
                    livro = self.biblioteca.catalogo.obter_livro_por_id(item.livro_id)
                    if livro:
                        print(f"  • {livro.titulo}")
    
    def listar_emprestimos_ativos(self):
        print("\n📋 EMPRÉSTIMOS ATIVOS")
        print("-"*50)
        
        emprestimos_ativos = [e for e in self.biblioteca.emprestimos.values() if e.status == "ATIVO"]
        
        if not emprestimos_ativos:
            print("Nenhum empréstimo ativo.")
            return
        
        for emprestimo in emprestimos_ativos:
            usuario = self.biblioteca.usuarios.get(emprestimo.usuario_id)
            usuario_nome = usuario.nome if usuario else "Desconhecido"
            dias_atraso = emprestimo.calcular_dias_atraso()
            atraso_text = f" ({dias_atraso} dias de atraso)" if dias_atraso > 0 else ""
            print(f"\nID {emprestimo.id}: {usuario_nome}")
            print(f"  Data de devolução: {emprestimo.data_devolucao_prevista.strftime('%d/%m/%Y')}{atraso_text}")
    
    def listar_emprestimos_atrasados(self):
        print("\n⚠️  EMPRÉSTIMOS ATRASADOS")
        print("-"*50)
        
        emprestimos_atrasados = []
        for emprestimo in self.biblioteca.emprestimos.values():
            if emprestimo.status == "ATIVO" and emprestimo.calcular_dias_atraso() > 0:
                emprestimos_atrasados.append(emprestimo)
        
        if not emprestimos_atrasados:
            print("Nenhum empréstimo atrasado.")
            return
        
        for emprestimo in emprestimos_atrasados:
            usuario = self.biblioteca.usuarios.get(emprestimo.usuario_id)
            usuario_nome = usuario.nome if usuario else "Desconhecido"
            dias_atraso = emprestimo.calcular_dias_atraso()
            print(f"\nID {emprestimo.id}: {usuario_nome}")
            print(f"  Dias de atraso: {dias_atraso}")
            print(f"  Data prevista: {emprestimo.data_devolucao_prevista.strftime('%d/%m/%Y')}")
    
    def menu_relatorios(self):
        while True:
            print("\n" + "="*50)
            print("📊 MENU DE RELATÓRIOS")
            print("="*50)
            print("1. Relatório completo da biblioteca")
            print("2. Estatísticas de uso")
            print("3. Livros mais populares")
            print("4. Usuários mais ativos")
            print("5. Busca avançada de livros")
            print("0. Voltar ao menu principal")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.relatorio_completo()
            elif opcao == "2":
                self.estatisticas_uso()
            elif opcao == "3":
                self.livros_populares()
            elif opcao == "4":
                self.usuarios_ativos()
            elif opcao == "5":
                self.busca_avancada()
            elif opcao == "0":
                break
            else:
                print("❌ Opção inválida!")
    
    def relatorio_completo(self):
        print("\n" + "="*60)
        print(self.biblioteca.gerar_relatorio())
        print("="*60)
    
    def estatisticas_uso(self):
        print("\n📈 ESTATÍSTICAS DE USO")
        print("-"*50)
        
        total_livros = len(self.biblioteca.catalogo.livros)
        total_usuarios = len(self.biblioteca.usuarios)
        total_emprestimos = len(self.biblioteca.emprestimos)
        
        print(f"📚 Livros no sistema: {total_livros}")
        print(f"👥 Usuários registrados: {total_usuarios}")
        print(f"📖 Empréstimos totais: {total_emprestimos}")
        
        if total_usuarios > 0:
            media = total_emprestimos / total_usuarios
            print(f"📊 Média de empréstimos por usuário: {media:.1f}")
        
        # Por tipo de usuário
        pf_count = sum(1 for u in self.biblioteca.usuarios.values() if isinstance(u, PessoaFisica))
        pj_count = sum(1 for u in self.biblioteca.usuarios.values() if isinstance(u, PessoaJuridica))
        
        print(f"\n👤 Por tipo de usuário:")
        print(f"  • Pessoas Físicas: {pf_count}")
        print(f"  • Pessoas Jurídicas: {pj_count}")
    
    def livros_populares(self):
        print("\n🏆 LIVROS MAIS POPULARES")
        print("-"*50)
        
        contagem = {}
        for emprestimo in self.biblioteca.emprestimos.values():
            for item in emprestimo.itens:
                contagem[item.livro_id] = contagem.get(item.livro_id, 0) + 1
        
        if not contagem:
            print("Nenhum empréstimo registrado ainda.")
            return
        
        top10 = sorted(contagem.items(), key=lambda x: x[1], reverse=True)[:10]
        
        for i, (livro_id, qtd) in enumerate(top10, 1):
            livro = self.biblioteca.catalogo.obter_livro_por_id(livro_id)
            if livro:
                print(f"{i}. {livro.titulo} - {qtd} empréstimos")
    
    def usuarios_ativos(self):
        print("\n👑 USUÁRIOS MAIS ATIVOS")
        print("-"*50)
        
        contagem = {}
        for emprestimo in self.biblioteca.emprestimos.values():
            contagem[emprestimo.usuario_id] = contagem.get(emprestimo.usuario_id, 0) + 1
        
        if not contagem:
            print("Nenhum empréstimo registrado ainda.")
            return
        
        top10 = sorted(contagem.items(), key=lambda x: x[1], reverse=True)[:10]
        
        for i, (usuario_id, qtd) in enumerate(top10, 1):
            usuario = self.biblioteca.usuarios.get(usuario_id)
            if usuario:
                tipo = "PF" if isinstance(usuario, PessoaFisica) else "PJ"
                print(f"{i}. {usuario.nome} ({tipo}) - {qtd} empréstimos")
    
    def busca_avancada(self):
        print("\n🔍 BUSCA AVANÇADA DE LIVROS")
        print("-"*50)
        
        termo = input("Digite o termo de busca (título ou autor): ")
        resultados = self.biblioteca.buscar_livros(termo)
        
        print(f"\n🔍 RESULTADOS PARA '{termo}':")
        print("-"*50)
        
        if resultados:
            for i, livro in enumerate(resultados, 1):
                print(f"{i}. {livro}")
        else:
            print("Nenhum livro encontrado.")
    
    def menu_informacoes(self):
        print("\n" + "="*50)
        print("ℹ️  INFORMAÇÕES DA BIBLIOTECA")
        print("="*50)
        print(f"Nome: {self.biblioteca.nome}")
        print(f"Endereço: {self.biblioteca.endereco}")
        print(f"Telefone: {self.biblioteca.telefone}")
        print(f"Catálogo: {self.biblioteca.catalogo.nome}")
        print(f"Funcionários: {len(self.biblioteca.funcionarios)}")
        
        print("\n👷 FUNCIONÁRIOS:")
        for func in self.biblioteca.funcionarios:
            print(f"  • {func.nome} - {func.cargo}")
        
        print("\n💡 DICAS PARA TESTAR:")
        print("1. Primeiro cadastre alguns livros e usuários")
        print("2. Depois faça empréstimos")
        print("3. Teste as devoluções")
        print("4. Veja os relatórios para acompanhar estatísticas")
    
    def executar(self):
        print("\n" + "="*60)
        print("📚 BEM-VINDO AO SISTEMA DE BIBLIOTECA INTERATIVO!")
        print("="*60)
        print("\nDados de exemplo carregados:")
        print(f"• {len(self.biblioteca.catalogo.livros)} livros cadastrados")
        print(f"• {len(self.biblioteca.usuarios)} usuários cadastrados")
        print(f"• 1 funcionário cadastrado")
        print("\nUse o menu para testar todas as funcionalidades!")
        
        self.mostrar_menu_principal()


# ====================== EXECUÇÃO DO SISTEMA ======================

if __name__ == "__main__":
    sistema = SistemaBiblioteca()
    sistema.executar()