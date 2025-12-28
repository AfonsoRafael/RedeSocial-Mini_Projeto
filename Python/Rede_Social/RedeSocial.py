"""Nível 4: Desafio
Exercício 4.1
Escreva uma função que simule a recomendação de amigos em uma rede social:

Você tem um conjunto de amigos: seus_amigos

Cada amigo tem um conjunto de amigos: amigos_de_amigos

Recomende amigos que:

Não são seus amigos atuais

São amigos de pelo menos 2 dos seus amigos

Retorne os recomendados ordenados alfabeticamente"""


def perfil():
    print("""
    -------------REDE SOCIAL-------------
    [0] SAIR
    [1] ADICIONAR USUARIO
    [2] SELECIONAR USUARIO
    [3] EXCLUIR USUARIO
    [4] LISTAR REDE
              """)
    return input("Digite a acao que deseja fazer: ").strip()

def funcoes_usuario(usuario):
    print(f"""
-------------REDE SOCIAL {usuario}-------------
    [5] ADICIONAR AMIGO
    [6] RECOMENDACOES
    [7] EXCLUIR AMIGO
    [8] LISTAR AMIGOS
              """)
    return input("Digite a acao que deseja fazer: ").strip()

def adiciona_usuario(rede):
    nome = input("Digite o nome do usuario que deseja adicionar: ")
    if nome in rede:
        print(f"Usuario {nome} ja existe!!!")
    else:
        rede[nome] = set()
        print("Usuario criado com sucesso!!!")

def remove_usuario(rede):
    nome = input("Digite o nome do usuario que deseja remover: ")
    if nome not in rede:
        print(f"Usuario {nome} nao existe!!!")
    else:
        del rede[nome]
        print("Usuario removido com sucesso!!!")
    return rede

def selecionar_usuario(rede):
    usuario = input("Digite o nome do usuario: ").strip()
    if usuario in rede:
        print(f"Usuario {usuario} selecionado!!!")
        return usuario
    else:
        
        print("Usuario não existe!!!")
        return None

def listar_usuario(rede):
    usuarios = sorted(rede.items())
    print("Lista de usuarios e amigos\n")
    for chave, valor in usuarios:
        print(f"{chave}: {', '.join(valor)}")

def adiciona_amigo(rede, usuario):
    nome = input("Digite o nome do amigo que deseja adicionar: ").strip()
    if nome in rede[usuario]:
        print(f"Esse amigo {nome} ja esta adicionado")
    else:
        rede[usuario].add(nome)
        print(f"Amigo {nome} adicionado com sucesso!!!")

def remove_amigo(rede, usuario):
    nome = input("Digite o nome do amigo que deseja adicionar: ").strip()
    if nome not in rede[usuario]:
        print(f"Eles nao sao amigos!!!")
    else:
        rede[usuario].remove(nome)
        print(f"Amigo adicionado com sucesso - {nome}!")

def lista_amigo(rede, usuario):
    print(f"Lista de amigos de {usuario}")
    print(f"\n".join(rede[usuario]))

def recomendacao(rede,usuario):
    seus_amigos = rede[usuario]
    contador = {}
    for amigo in seus_amigos:
        for amigo_de_amigo in rede[amigo]:
            if amigo_de_amigo != usuario and amigo_de_amigo not in seus_amigos:
                contador[amigo_de_amigo] = contador.get(amigo_de_amigo, 0)+1

    recomendado = sorted([pessoa for pessoa,qtd in contador.items() if qtd >= 2])
    if recomendado:
        print(f"Recomendacoes de amigos para {usuario}")
        for nome in recomendado:
            print(nome)

    else:
        print("Nenhuma recomendacao no momento")
    

def main():
    rede = {"Afonso":{"Ana","Carol","Jose"},"Ana":{"Afonso","Jose","Ryan"}, "Carol":{"Afonso", "Ryan","Jose"}}
    usuario =""
    
    while True:
        n = perfil()
        
        if n == "1":
            adiciona_usuario(rede)

        elif n == "2":
            usuario = selecionar_usuario(rede)
            if usuario:
                n = funcoes_usuario(usuario)
                if n == "5":
                    adiciona_amigo(rede,usuario)
                elif n == "6":
                    recomendacao(rede, usuario)
                elif n == "7":
                    remove_amigo(rede, usuario)
                elif n == "8":
                    lista_amigo(rede, usuario)

        elif n == "3":
            remove_usuario(rede)

        elif n == "4":
            listar_usuario(rede)
        
        elif n == "0":
            break
main()