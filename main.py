from view import View

def main():

    try:
        menu = View()
        menu.mostrar_pantalla_bienvenido()
        menu.salir()
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")


if __name__ == "__main__":
    main()

