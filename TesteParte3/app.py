import flask
from flask import Flask, render_template, request, redirect, flash, session
from Classes import contas
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8, 80"))

app = Flask(__name__)

app.secret_key = "chave"
@app.route('/aplicacaoemperstimo/', methods=["GET", "POST"])
def aplicaremprestimo():  # put application's code here
    if (request.form["quantidade"] == ""):
        flash("Por favor insira um valor para um emprestimo", "Aviso")
        return redirect("http://" + s.getsockname()[0] + ":3000/")
    file = open("infi_banco.txt", "r")
    linhas = file.readlines()
    conta = None
    for linha in linhas:
        if(linha.split()[1] == str(session.get("numeroConta", 0))):
            conta = {"nome":linha.split()[0], "numeroConta":linha.split()[1], "idade":linha.split()[2], "dinheiro":str(linha.split()[3]) + float(request.form['quantidade'])}
            file = open("infi_banco.txt", "r")
            linhas = file.readlines()

            for linha in linhas:
                if (linha.split()[1] == str(session.get("numeroConta", "0"))):
                    with open("infi_banco.txt", "r+") as f:
                        d = f.readlines()
                        f.seek(0)
                        for i in d:
                            if i != linha:
                                f.write(i)
                        f.truncate()
                        linha = conta["nome"] + " " + str(conta["numeroConta", "0"]) + " " + str(conta["age"]) + " " + str(conta["dinheiro"]) + "\n"
                        file = open("infi_banco.txt")
                        file.write(linha)
            data = {"name": conta["nome"], "idade":conta["idade"], "dinheiro": conta["dinheiro"], "numeroConta":conta["numeroConta"]}
            session["numeroConta"] = conta["numeroConta"]
            print("setting" + str(session["numeroConta"]))
            return redirect("http://" + s.getsockname()[0] + ":3000")
        return render_template("index.html")

@app.route("/enviardinheiro/", methods=["GET", "POST"])
def enviardinheiro():
    print("A processar envio de dinheiro")
    file = open("infi_banco.txt", "r")
    Linhas = file.readlines()
    contaEnvio = None
    contaAlvo = None
    for linha in Linhas:
        if(linha.split()[1] == str(session.get("numeroConta", '0'))):
            contaEnvio = {"nome": linha.split()[0], "numeroConta": linha.split()[1], "idade":linha.split()[2], "dinheiro": linha.split()[3]}
            print(contaEnvio)
    for linha in Linhas:
        if(linha.split()[1] == str(request.form["numeroConta"])):
            contaAlvo = {"nome": linha.split()[0], "numeroConta": linha.split()[1], "idade":linha.split()[2], "dinheiro": linha.split()[3]}
            print(contaAlvo)
        if(contaEnvio == None or contaAlvo == None):
            flash(f"Nao e possivel encontrar conta {str(request.form['conta'].strip())}, por favor tente de novo!", "Aviso")
            return redirect("http://" + s.getsockname()[0] + ":3000")
        print("Dinheiro: " + str(float(contaEnvio["dinheiro"])))
        print("Quantidade: "+ str(float(request.form["quantidade"])))
        if(str(contaEnvio["numeroConta"])== str(contaAlvo["numeroConta"])):
            flash("Não é possivel enviar dinheiro para a mesma pessoa|", "Aviso")
            return redirect("http://" + s.getsockname()[0] + ":3000")
        if (float(contaEnvio["dinheiro"]) >= float(request.form['quantidade'])):
            file = open("infi_banco.txt", "r")
            Linhas = file.readlines()
            contaEnvio = {"nome": contaEnvio["nome"], "numeroConta": contaEnvio["numeroConta"], "idade":contaEnvio["idade"], "dinheiro":float(contaEnvio["dinheiro"]) - float(request.form["quantidade"])}
            contaAlvo = {"nome": contaAlvo["nome"], "numeroConta": contaAlvo["numeroConta"],"idade": contaAlvo["idade"],"dinheiro": float(contaAlvo["dinheiro"]) - float(request.form["quantidade"])}
            for linha in Linhas:
                if(linha.split()[1] == str(contaEnvio["numeroConta"])):
                    with open("infi_banco.txt", "r+") as f:
                        d = f.readlines()
                        f.seek(0)
                        for i in d:
                            if i != linha:
                                f.write(i)
                        f.truncate()
                    linha = str(contaEnvio["nome"]) + " " + str(contaEnvio["numeroConta"] + " " + str(contaEnvio["idade"]) + str(contaEnvio)["dinheiro"] + "\n")
                    file = open("infi_banco.txt")
                    file.write(linha)
                if(linha.split()[1] == str(contaAlvo["numeroConta"])):
                    with open("infi_banco.txt", "r+") as f:
                        d = f.readlines()
                        f.seek(0)
                        for i in d:
                            if i != linha:
                                f.write(i)
                        f.truncate()
                    linha = str(contaAlvo["nome"]) + " " + str(contaAlvo["numeroConta"] + " " + str(contaAlvo["idade"]) + str(contaAlvo)["dinheiro"] + "\n")
                    file = open("infi_banco.txt")
                    file.write(linha)
            print("Dinheiro enviado de " +  contaEnvio["nome"] + " para " + contaAlvo["nome"])
            flash("Transferencia de " + str(float(request.form["quantidade"])) + " vindo de " + contaEnvio["nome"] + " para " + contaAlvo["nome"] + " foi bem sucedida", "sucesso|")
        else:
            flash("Fundos insuficientes", "Aviso")
            print("Dinheiro insuficiente")
            return redirect("http://" + s.getsockname()[0] + ":3000")


@app.route("/", methods=["GET", "POST"])
def login():
    if(request.method == "GET"):
        if(session.get("numeroConta"), "0") == "":
            return render_template("index.html")
        else:
            file = open ("infi_banco.txt", "r")
            Linhas = file.readlines()
            conta = None
            for linha in Linhas:
                if(linha.split()[0] == str(session.get("numeroConta", "0"))):
                    conta = {"nome":linha.split()[0], "numeroConta": linha.split()[1], "idade": linha.split()[2], "dinheiro":linha.split()[3]}
                    data= {"nome": conta["nome"], "idade":conta["idade"], "dinheiro":str(round(float(conta["dinheiro"]), 2)), "numeroConta": conta["numeroConta"]}
                    session["numeroConta"] = conta["numeroConta"]

                    return render_template("dashboard.html", data=data)
            return render_template("index.html")
    else:
        if(session.get("numeroConta", "0") == "0"):
            conta = contas(request.form["nome"],request.form["idade"])



            data = {"nome":conta.nome, "idade": conta.idadem, "dinheiro":str(round(float(conta.dinheiro), 2)), "numeroconta": conta.numeroConta}
            session["numeroConta"] = conta.numeroConta
            print("setting "  + str(session["numeroConta"]))
            return render_template("dashboard.html", data=data)
        else:
            file = open("infi_banco.txt", "r")
            Linhas = file.readlines()
            conta = None
            for linha in Linhas:
                if(linha.split()[1] == str(session.get('numeroConta', "0"))):
                    conta = {"name": linha.split()[0], "numeroConta":linha.split()[1], "idade": linha.split()[2], "dinheiro": linha.split([3])}
                    data = {"nome": conta["nome"], "idade": conta["idade"],"dinheiro": str(round(float(conta["dinheiro"]), 2)), "numeroConta": conta["numeroConta"]}

                    session["numeroConta"] = conta["numeroConta"]
                    print("setting" + str(session["numeroConta"]))
                    return render_template("dashboard.html", data=data)
                return render_template("index.html ")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3000)

