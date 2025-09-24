from flask import Flask, render_template, request, redirect, session, url_for, flash

app = Flask(__name__)
app.secret_key = "clave_secreta"  # Necesaria para manejar sesiones

# Guardaremos los usuarios en la sesión (diccionario)

usuarios = {}  

@app.route("/")
def home():
    if "usuario" in session:
        return redirect(url_for("inicio"))
    return redirect(url_for("login"))

# Registro de usuario
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        color = request.form["color"]

        if username in usuarios:
            flash("El usuario ya existe", "error")
            return redirect(url_for("registro"))

        usuarios[username] = {"password": password, "color": color}
        flash("Usuario registrado exitosamente", "success")
        return redirect(url_for("login")) #redirige al login

    return render_template("registro.html")

# Login de usuario
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Caso admin
        if username == "admin" and password == "12345678":
            session["usuario"] = "admin"
            session["color"] = "#87CEEB"
            return redirect(url_for("inicio"))

        # Caso usuario registrado
        if username in usuarios and usuarios[username]["password"] == password:
            session["usuario"] = username
            session["color"] = usuarios[username]["color"]
            return redirect(url_for("inicio"))

        return render_template("login.html", error="Credenciales inválidas")

    return render_template("login.html")

# Página de bienvenida
@app.route("/inicio")
def inicio():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("inicio.html", usuario=session["usuario"], color=session["color"])

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)