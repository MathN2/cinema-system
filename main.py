from cinema.UI.CLI.menu import menu_principal
from cinema.services.filme_services import is_movie_active

if __name__ == '__main__':
    print(is_movie_active(13))
    menu_principal()