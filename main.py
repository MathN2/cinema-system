from cinema.data.init_db import create_db

if __name__ == '__main__':
    create_db()

    from cinema.UI.CLI.menu import menu_principal
    from cinema.UI.GUI.telas.tela_cliente import open_client

    open_client()
    menu_principal()