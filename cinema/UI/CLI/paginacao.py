import questionary

def pagination(dados):
    tamanho = 7
    pagina = 0

    while True:
        inicio = pagina * tamanho
        fim = inicio + tamanho
        max_pagina = (len(dados) - 1) // tamanho

        pagina_dados = dados[inicio:fim]
        choices = []

        for i, item in enumerate(pagina_dados, start=1):
            choices.append(
                questionary.Choice(
                    f"{item['label']}",
                    value = i
                )
            )
        

        if fim < len(dados):
            choices.append(questionary.Choice("→ Próxima página", value = 8))
        if pagina > 0:
            choices.append(questionary.Choice("← Página anterior", value = 9))
        choices.append(questionary.Separator())
        choices.append(questionary.Choice("Cancelar", value = 0))

        opcao = questionary.select(
            "Escolha um dia para assistir o filme: ",
            choices = choices
        ).ask()

        if opcao == 8 and pagina < max_pagina:
            pagina += 1
        
        elif opcao == 9 and pagina > 0:
            pagina -= 1
        
        elif opcao == 0:
            return None
        
        elif 1 <= opcao <= len(pagina_dados):
            escolhido = pagina_dados[opcao - 1]
            return escolhido