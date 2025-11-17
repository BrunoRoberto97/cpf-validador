from fastapi import FastAPI
from pydantic import BaseModel
import os

app = FastAPI()

# Função de validação de CPF (mantida a lógica original)
def validar_cpf_py(cpf: str) -> bool:
    """Valida um CPF dado como string, retornando True ou False."""
    cpf_limp = "".join(filter(str.isdigit, cpf))
    
    # 1. Checagem básica
    if len(cpf_limp) != 11 or len(set(cpf_limp)) == 1:
        return False

    # 2. Validação do primeiro dígito
    soma = 0
    for i in range(9):
        soma += int(cpf_limp[i]) * (10 - i)
    resto = (soma * 10) % 11
    digito1 = resto if resto < 10 else 0
    if digito1 != int(cpf_limp[9]):
        return False

    # 3. Validação do segundo dígito
    soma = 0
    for i in range(10):
        soma += int(cpf_limp[i]) * (11 - i)
    resto = (soma * 10) % 11
    digito2 = resto if resto < 10 else 0
    if digito2 != int(cpf_limp[10]):
        return False

    return True


class CPFRequest(BaseModel):
    """Modelo de dados para a requisição POST (o corpo do WebHook do ManyChat)."""
    cpf: str


@app.post("/validar_cpf")
def validar_cpf(data: CPFRequest):
    """
    Endpoint principal. Retorna um objeto JSON com cpf_valido como 1 ou 0.
    
    ManyChat precisa deste formato para mapear valores de forma confiável
    para campos personalizados do tipo Número.
    """
    valido = validar_cpf_py(data.cpf)
    
    # --- AJUSTE CRUCIAL AQUI ---
    # Força o retorno do valor para 1 (True) ou 0 (False)
    valor_retorno = 1 if valido else 0
    
    return {
        "cpf_valido": valor_retorno,
        "mensagem_bot": "CPF válido!" if valido else "CPF inválido."
    }


if __name__ == "__main__":
    import uvicorn
    # A porta é configurada a partir da variável de ambiente, essencial para plataformas como Railway
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
