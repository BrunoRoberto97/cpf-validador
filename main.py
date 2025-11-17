from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

def validar_cpf_py(cpf: str) -> bool:
    cpf_limpo = "".join(filter(str.isdigit, cpf))
    if len(cpf_limpo) != 11 or len(set(cpf_limpo)) == 1:
        return False

    soma = 0
    for i in range(9):
        soma += int(cpf_limpo[i]) * (10 - i)
    resto = (soma * 10) % 11
    digito1 = resto if resto < 10 else 0
    if digito1 != int(cpf_limpo[9]):
        return False

    soma = 0
    for i in range(10):
        soma += int(cpf_limpo[i]) * (11 - i)
    resto = (soma * 10) % 11
    digito2 = resto if resto < 10 else 0
    if digito2 != int(cpf_limpo[10]):
        return False

    return True

class CPFRequest(BaseModel):
    cpf: str

@app.post("/validar_cpf")
def validar_cpf(data: CPFRequest):
    valido = validar_cpf_py(data.cpf)
    return {
        "cpf_valido": valido,
        "mensagem_bot": "CPF válido!" if valido else "CPF inválido."
    }
