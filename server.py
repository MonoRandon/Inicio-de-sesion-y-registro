from __init__ import create_app

app = create_app()

port= 5022

if __name__ == "__main__":
    app.run(debug=True)
