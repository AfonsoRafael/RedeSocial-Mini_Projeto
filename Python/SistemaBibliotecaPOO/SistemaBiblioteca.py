#   SISTEMA DE BIBLIOTECA

from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Biblioteca:
    def __init__(self, nome, endereco, telefono):
        self._nome = nome
        self._endereco = endereco
        self._telefone = telefono

    @property
    def nome(self):
        return self._nome
    
    @property
    def endereco(self):
        return self._endereco
    
    @property
    def telefone(self):
        return self._telefone
    
    def registrar_Usuario():
        pass

    def cadastrarLivro():
        pass

    def realizarEmprestimo():
        pass

    def processsarDevolucao():
        pass

    def gerarRelatorio():
        pass

class Usuario:
    def __init__(self, id, nome, email, telefone, data_cadastro, status):
        self._id = id
        self._nome = nome
        self._email = email
        self._telefone = telefone
        self._data_cadastro = data_cadastro
        self._status = status

    @property
    def id(self):
        return self._id
    @property
    def nome(self):
        return self._nome
    @property
    def email(self):
        return self._email
    @property
    def telefone(self):
        return self._telefone
    @property
    def data_cadastro(self):
        return self._data_cadastro
    @property
    def status(self):
        return self._status
    
class ItemEmprestado:
    def __init__(self, emprestimo_id,livro_id,quantidade):
        self._emprestimo_id = emprestimo_id
        self._livro_id = livro_id
        self._quantidade = quantidade

    @property
    def emprestimo_id(self):
        return self._emprestimo_id
    @property
    def livro_id(self):
        return self._livro_id
    @property
    def quantidade(self):
        return self._quantidade

class Livro:
    def __int__(self, id, titulo, autor, isbn, ano_publicado, editora, categoria, disponivel, exemplares):
        self._id = id
        self._titulo = titulo
        self._autor = autor
        self._isbn = isbn
        self._ano_publicado = ano_publicado
        self._editora = editora
        self._categoria = categoria
        self._disponivel = disponivel
        self._exemplares = exemplares

    @property
    def id(self):
        return self._id
    @property
    def titulo(self):
        return self._titulo
    @property
    def autor(self):
        return self._autor
    @property
    def isbn(self):
        return self._isbn
    @property
    def ano_publicado(self):
        return self._ano_publicado
    @property
    def editora(self):
        return self._editora
    @property
    def categoria(self):
        return self._categoria
    @property
    def disponivel(self):
        return self._disponivel
    @property
    def exemplares(self):
        return self._exemplares
    
    def emprestar(self, quantidade):
        pass

    def devolver(self, quantidade):
        pass

    def verificar_disponibilidade(self):
        pass

class Catalogo:
    def __init__(self, nome, email, telefone, data_cadastro):
        self._nome = nome
        self._email = email
        self._telefone = telefone
        self._data_cadastro = data_cadastro
    @property
    def nome(self):
        return self._nome
    @property
    def email(self):
        return self._email
    @property
    def telefone(self):
        return self._telefone
    @property
    def data_cadastro(self):
        return self._data_cadastro
    
class PessoaFisica:
    def __init__(self, cpf, data_nascimento, tipo_usuario, max_emprestimos):
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        self._tipo_usuario = tipo_usuario
        self._max_emprestimos = max_emprestimos
    @property
    def cpf(self):
        return self._cpf
    @property
    def data_nascimento(self):
        return self._data_nascimento
    @property
    def tipo_usuario(self):
        return self._tipo_usuario
    @property
    def max_emprestimos(self):
        return self._max_emprestimos
    
class PessoaJuridica:
    def __init__(self, cnpj, razao_social,responsavel, tipo_usuario, max_emprestimos):
        self._cnpj = cnpj
        self._razao_social = razao_social
        self._responsavel = responsavel
        self._tipo_usuario = tipo_usuario
        self._max_emprestimos = max_emprestimos
    @property
    def cnpj(self):
        return self._cnpj
    @property
    def razao_social(self):
        return self._razao_social
    @property
    def responsavel(self):
        return self._responsavel
    @property
    def tipo_usuario(self):
        return self._tipo_usuario
    @property
    def max_emprestimos(self):
        return self._max_emprestimos
    
class Emprestimo:
    def __init__(self, id, data_emprestimo, data_devolucao, status):
        self._id = id
        self._data_emprestimo = data_emprestimo
        self._data_devolucao = data_devolucao
        self._status = status

    @property
    def id(self):
        return self._id
    @property
    def data_emprestimo(self):
        return self._data_emprestimo
    @property
    def data_devolucao(self):
        return self._data_devolucao
    @property
    def status(self):
        return self._status
    
class Funcionario:
    def __init__(self, matricula, cargo, salario):
        self._matricula = matricula
        self._cargo = cargo
        self._salario = salario
    @property
    def matricula(self):
        return self._matricula
    @property
    def cargo(self):
        return self._cargo
    @property
    def salario(self):
        return self._salario
    def cadastrarLivro(self):
        pass
    def atenderUsuario(self):
        pass
    def relatorioDiario(self):
        pass