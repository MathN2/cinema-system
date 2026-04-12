def pagination(dados):
    tamanho = 7
    pagina = 0

    while True:
        inicio = pagina * tamanho
        fim = inicio + tamanho
        max_pagina = (len(dados) - 1) // tamanho

        pagina_dados = dados[inicio:fim]

        for i, item in enumerate(pagina_dados, start=1):
            print(f"{i} - {item['label']}")

        if fim < len(dados):
            print("8 - Próxima página")
        if pagina > 0:
            print("9 - Página anterior")
        print("0 - Cancelar")

        opcao = int(input("Escolha: "))

        if opcao == 8 and pagina < max_pagina:
            pagina += 1
        
        elif opcao == 9 and pagina > 0:
            pagina -= 1
        
        elif opcao == 0:
            return None
        
        elif 1 <= opcao <= len(pagina_dados):
            escolhido = pagina_dados[opcao - 1]
            return escolhido