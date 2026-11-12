from avistamientos.adapters.web.app_factory import create_app

# Se conserva el punto de entrada habitual para ejecutar la API.
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
