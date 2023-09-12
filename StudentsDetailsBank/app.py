from webapp import create_app
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    app = create_app()
    app.run(
        debug=True
    )  # note that I used  the property "port" to change the port of the server.
    # It's your choice to change the port. e.g your server url can be http://127.0.0.1:300,http://127.0.0.1:3500,
    # http://127.0.0.1:anynumber. Without altering it, it's usually http://127.0.0.1:5000


