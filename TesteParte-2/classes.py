from pydantic import BaseModel
import sqlite3


class ContaAdd(BaseModel):
    nome: str
    dinheiro: float
    admin: int
    quantia_diaria: float


class ExtratoAdd(BaseModel):
    conta_id: int
    conta_otr: int
    tipo: int
    montante: float


class Levantamento(BaseModel):
    conta_id: int
    montante: float

    def quantia_diaria(self):
        conn = sqlite3.connect("banco.db")
        crs = conn.execute(f"Select quantia_diaria from cartao Where id = {self.conta_id}")
        arr = crs.fetchone()
        conn.close()
        return float(arr[0])

    def saldo(self):
        conn = sqlite3.connect("banco.db")
        crs = conn.execute(f"Select dinheiro from cartao Where id = {self.conta_id}")
        arr = crs.fetchone()
        conn.close()
        return float(arr[0])


class Deposito(BaseModel):
    conta_id: int
    montante: float

    def quantia_diaria(self):
        conn = sqlite3.connect("banco.db")
        crs = conn.execute(f"Select quantia_diaria from cartao Where id = {self.conta_id}")
        arr = crs.fetchone()
        conn.close()
        return float(arr[0])

    def saldo(self):
        conn = sqlite3.connect("banco.db")
        crs = conn.execute(f"Select dinheiro from cartao Where id = {self.conta_id}")
        arr = crs.fetchone()
        conn.close()
        return float(arr[0])


class Transferencia(BaseModel):
    conta_id: int
    conta_id_otr: int
    montante: float

    def saldo(self):
        conn = sqlite3.connect("banco.db")
        crs = conn.execute(f"Select dinheiro from cartao Where id = {self.conta_id}")
        arr = crs.fetchone()
        conn.close()
        return float(arr[0])