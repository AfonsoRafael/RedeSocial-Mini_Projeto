"""
Desafios
23. Jogo da Forca
Implemente o jogo da forca. O programa deve escolher uma palavra secreta e o usuário tem 6 tentativas para adivinhar as letras.
"""
import os

escolha = "s"



while escolha =="s":
    secreta = list(input("Digite a palavra: ").upper().strip())
    dica = input("Digite a dica: ")
    palavra = ["_"]* len(secreta)
    chance = 6
    os.system('cls' if os.system =='nt' else 'clear')
    while chance > 0 and palavra != secreta:
        acerto = False
        print("---------------Jogo da forca---------------\n\n\n")
        print(f"""                           chances: {chance}
        Dica: {dica}
        A palavra e: {" ".join(palavra)}
        
        """)
        letra = input("Digite uma letra: ").upper()
        for i in range(0, len(secreta)):
            if letra == secreta[i]:
                palavra[i]=letra
                acerto = True
        if acerto == False:
            chance -=1
        os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"A palavra final e: {"".join(secreta)}")
    if palavra == secreta:
        print("Parabens, voce acertou a palavra secreta")
    else:
        print("Voce perdeu!!!")
    escolha = input("Deseja jogar novamente? s/n| ").lower()
        
