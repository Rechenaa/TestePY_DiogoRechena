import fastapi
from fastapi import FastAPI, Response, status
import sqlite3, classes, random

app = FastAPI()
dbfilename = "banco.db"

@app.get("/setup")
async def setup():
    open(dbfilename, "w+")
    sql = """
            Create table if not exists cartao(id INTEGER primary key not null, nome varchar(50) not null,
            cod_chave int not null, dinheiro decimal(999999,2), quantia_diaria decimal(4,2) not null, admin int not null);

            Create table if not exists transacoes(id_cartao_trs int not null, id_cartao_otr int not null, tipo int not null, quantia decimal(999999,2))
            """
    conn = sqlite3.connect(dbfilename)
    conn.executescript(sql)
    conn.close()
    return {"message": "Tabelas criadas."}


@app.get("/contas/")
async def contas_all(response: Response):
    conn = sqlite3.connect(dbfilename)
    crs = conn.execute(f"Select * from cartao").fetchall()

    if not crs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Nao existe nenhuma conta criada."}
    conn.close()
    return {"contas": crs}


@app.get("/contas/{id}")
async def contas_id(id: int, response: Response):
    conn = sqlite3.connect(dbfilename)
    crs = conn.execute(f"Select * from cartao where id = {id}").fetchall()

    if not crs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Nao existe nenhuma conta criada."}
    conn.close()
    return {"conta": crs[0]}


@app.get("/contas/saldo/{id}")
async def conta_saldo(id: int, response: Response):
    conn = sqlite3.connect(dbfilename)
    crs = conn.execute(f"Select dinheiro from cartao Where id = {id}").fetchone()

    if not crs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "O id especificado nao existe."}
    conn.close()
    return {"saldo": float(crs[0])}


@app.get("/contas/quantia_diaria/{id}")
async def conta_quantia_diaria(id: int, response: Response):
    conn = sqlite3.connect(dbfilename)
    crs = conn.execute(f"Select quantia_diaria from cartao Where id = {id}").fetchone()
    if not crs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "O id especificado nao existe."}
    conn.close()
    return {"quantia_diaria": float(crs[0])}


@app.get("/contas/extrato/{id}")
async def conta_extrato(id: int):
    conn = sqlite3.connect(dbfilename)
    crs = conn.execute(f"Select * from transacoes Where id_cartao_trs = {id} or id_cartao_otr = {id}")
    arr = crs.fetchall()
    conn.close()
    return {"extratos": arr}


@app.get("/contas/isadmin/{id}")
async def conta_isadmin(id: int, response: Response):
    conn = sqlite3.connect(dbfilename)
    crs = conn.execute(f"Select admin from cartao Where id = {id}").fetchone()
    # Verifica se a conta existe
    if not crs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "O id especificado nao existe."}
    conn.close()
    return {"admin": float(crs[0])}



@app.post("/contas/criar")
async def conta_add(dados: classes.ContaAdd):
    cod_chave = str(random.randint(1, 9999))
    cod_chave = "0" * (4 - len(cod_chave)) + cod_chave

    nome = dados.nome
    dinheiro = dados.dinheiro
    admin = dados.admin
    quantia_diaria = dados.quantia_diaria

    conn = sqlite3.connect(dbfilename)
    sql = f"Insert into cartao(nome, cod_chave, dinheiro, quantia_diaria, admin) values ('{nome}', '{cod_chave}', '{dinheiro}', '{quantia_diaria}', '{admin}')"
    conn.execute(sql)
    conn.commit()
    conn.close()
    return {"message": f"Conta criada com o nome {nome}"}


@app.post("/contas/extrato/criar")
async def conta_extrato_add(dados: classes.ExtratoAdd):

    conn = sqlite3.connect(dbfilename)
    conn.executescript(f"""
                    Insert into transacoes values ('{dados.conta_id}', '{dados.conta_otr}', '{dados.tipo}', '{dados.montante}')
                    """)
    conn.commit()
    conn.close()
    return {"message": "Extrato criado."}


@app.post("/contas/levantar/")
async def conta_levantar(dados: classes.Levantamento):
    conn = sqlite3.connect(dbfilename)
    montante = dados.montante

    if montante > 500:
        return {"message": "Nao pode levantar mais de 500€ por vez"}


    if dados.quantia_diaria() + montante > 2500:
        return {"message": "O limite diario de levantamentos é de 2500€"}

    crs = conn.execute(f"Select dinheiro from cartao where id = {dados.conta_id}").fetchone()

    if montante > dados.saldo():
        return {"message": f"Nao pode levantar a quantia: {montante}"}

    conn.executescript(f"""
            Update cartao SET dinheiro = {dados.saldo() - montante} Where id = {dados.conta_id};
            UPDATE cartao SET quantia_diaria = {dados.quantia_diaria() + montante} where id = {dados.conta_id}
            """)
    conn.commit()
    conn.close()
    return {"message": f"Levantado {montante}."}


@app.post("/contas/depositar/")
async def conta_depositar(dados: classes.Deposito):
    conn = sqlite3.connect(dbfilename)
    montante = dados.montante
    conn.executescript(f"""
                    Update cartao SET dinheiro = {dados.saldo() + montante} Where id = {dados.conta_id};
                    """)
    conn.commit()
    conn.close()
    return {"message": f"Depositou {montante}."}


@app.post("/contas/transferir/")
async def conta_transferir(dados: classes.Transferencia, response: Response):
    conn = sqlite3.connect(dbfilename)
    id = dados.conta_id
    id_otr = dados.conta_id_otr

    if id_otr == id:
        return {"message": "Nao pode transferir dinheiro para si mesmo"}

    montante = dados.montante

    crs = conn.execute(f"Select * from cartao where id = '{id}'").fetchone()

    if not crs:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "A conta seleciona nao existe."}


    if montante > dados.saldo():
        return {"message": f"Nao pode transferir {montante}"}

    sql = f"""
                Update cartao SET dinheiro = {dados.saldo() - montante} Where id = {dados.conta_id};
                UPDATE cartao SET dinheiro = {float(crs[3]) + montante} where id = {id}
            """
    conn.executescript(sql)
    conn.commit()
    conn.close()
    return {"message": "Transferencia feita."}
