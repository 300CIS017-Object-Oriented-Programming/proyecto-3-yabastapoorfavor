from view import View

def main():
    print("holi")

    try:
        menu = View()
        if menu.mostrar_pantalla_bienvenido():
            menu.mostrar_datos_extra()
            menu.buscar_por_palabra_clave_y_formacion()
        menu.salir()
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")


if __name__ == "__main__":
    main()