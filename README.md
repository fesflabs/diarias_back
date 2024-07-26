  

# Diárias

  

  

Sistema de cálculo de diárias.

  

  

## Backend

  

  
  
  

## Como começar?

  

1.  **Clonar repositório**: Clone o projeto diarias para sua máquina local.

  

2.  **Configurar Ambiente Virtual (Opcional para DevOps)**:

- Crie e ative um ambiente virtual:

```bash

python -m venv venv

.\venv\Scripts\activate # Windows

```

3.  **Instalar Dependências**:

- Instale as dependências necessárias:

```bash

pip install -r requirements.txt

```

  

4.  **Configuração do Ambiente .env**:

- Crie um arquivo `.env` na raiz do projeto e configure as variáveis de ambiente necessárias:

```plaintext

DATABASE_URL=postgresql://user:password@localhost/mydatabase

DB_NOME=Nome do banco

DB_USER=Usuario

DB_SENHA=Senha do banco

DB_HOST=Host

LINK_ACESSO=Link de acesso ao frontend

MAIL_USER=seuemail@email.com

MAIL_FROM=seuemail@email.com

MAIL_PASSWORD=Senha do email

JWT_SECRET=Token de segurança

```

  

5.  **Criação de Token de Segurança**:

- Para gerar um token de segurança, execute o seguinte comando:

```bash

python -c "import secrets; print(secrets.token_urlsafe(32))"

```

  

6.  **Banco de Dados e Migrações**:

- Certifique-se de que as variáveis de ambiente relacionadas ao banco de dados estejam configuradas corretamente no arquivo `.env`.

- Verifique as migrações existentes no diretório `alembic/versions` com:

```bash

alembic current

```

- Para aplicar as migrações e atualizar o banco de dados, use:

```bash

alembic upgrade head

```

  

## Rotas da API - V1

Este diretório contém os endpoints da API para a versão 1.

  


### Estrutura de Diretórios

- `api/v1/endpoints/`
- `funcionario.py`: Endpoint para enviar e-mail de acesso ao sistema.
- `localidades.py`: Endpoint para obter estados e cidades.
- `banco.py`: Endpoint para listar bancos.
- `diaria.py`: Endpoint para cálculos e geração de diárias.

  

### Endpoints funcionario

#### /enviar-link-acesso (http://localhost:8000/api/v1/funcionario/enviar-link-acesso)

Este endpoint envia um link de acesso para o sistema de diárias para o email fornecido.

-   **Método HTTP**: POST
-   **Parâmetros**:
    -   **email**: Endereço de email do destinatário.
-   **Autenticação**:
    -   Não requer autenticação.
-   **Validações**:
    -   Apenas emails com o domínio `@fesfsus.ba.gov.br` são autorizados.
-   **Exemplo de Requisição**:

````bash
curl -X POST -H "Content-Type: application/json" -d '{"email": "usuario@fesfsus.ba.gov.br"}' http://localhost:8000/api/v1/funcionario/enviar-link-acesso

````

**Respostas**:

-   **200 OK**: O email foi enviado com sucesso.

````bash
{
    "message": "Email enviado com sucesso."
}
````

**400 Bad Request**: Quando o email fornecido não está no domínio autorizado.

````bash
{
    "detail": "Apenas emails com o domínio @fesfsus.ba.gov.br são autorizados a receber o link de acesso."
}
````

#### /criar (http://localhost:8000/api/v1/funcionario/criar)

Este endpoint cria um novo funcionário no sistema.

-   **Método HTTP**: POST
-   **Parâmetros**:
    -   **FuncionarioSchemaBase**: Dados do funcionário a serem criados.
-   **Autenticação**:
    -   Requer autenticação (somente o usuário com o email `dcti@fesfsus.ba.gov.br` tem permissão).
-   **Validações**:
    -   O CPF deve ser válido e único.
    -   O formato da data deve ser `dd/mm/yyyy`.
-   **Exemplo de Requisição**:

````bash
curl -X POST -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{
    "cpf": "12345678901",
    "nome": "João Silva",
    "endereco": "Rua Exemplo, 123",
    "estado": "Bahia",
    "data_nasc": "01/01/1980",
    "rg": "12345678",
    "telefone": "71999999999",
    "cod_banco": "1234",
    "nome_banco": "Banco Exemplo",
    "agencia": "1234",
    "conta_corrente": "1234567-8",
    "matricula": "20240001",
    "posto_trabalho": "Departamento A",
    "cargo": "Analista",
    "cidade": "Salvador",
    "centro_custo": "Centro A"
}' http://localhost:8000/api/v1/funcionario/criar
````

**Respostas**:

-   **200 OK**: Funcionário criado com sucesso.

````bash
{
    "cpf": "12345678901",
    "nome": "João Silva",
    "endereco": "Rua Exemplo, 123",
    "estado": "Bahia",
    "data_nasc": "01/01/1980",
    "rg": "12345678",
    "telefone": "71999999999",
    "cod_banco": "1234",
    "nome_banco": "Banco Exemplo",
    "agencia": "1234",
    "conta_corrente": "1234567-8",
    "matricula": "20240001",
    "posto_trabalho": "Departamento A",
    "cargo": "Analista",
    "cidade": "Salvador",
    "centro_custo": "Centro A"
}
````

**400 Bad Request**: Quando o CPF já existe ou há problemas com os dados fornecidos.

````bash
{
    "detail": "Funcionário com CPF 12345678901 já existe"
}

````

#### /buscar/{cpf} (http://localhost:8000/api/v1/funcionario/buscar/12345678901)

Este endpoint busca um funcionário pelo CPF fornecido.

-   **Método HTTP**: GET
-   **Parâmetros**:
    -   **cpf**: CPF do funcionário a ser buscado.
-   **Autenticação**:
    -   Não requer autenticação.
-   **Exemplo de Requisição**:

````bash
curl -X GET http://localhost:8000/api/v1/funcionario/buscar/12345678901
````

**Respostas**:

-   **200 OK**: Retorna os dados do funcionário.

````bash
{
    "cpf": "12345678901",
    "nome": "João Silva",
    "endereco": "Rua Exemplo, 123",
    "estado": "Bahia",
    "data_nasc": "01/01/1980",
    "rg": "12345678",
    "telefone": "71999999999",
    "cod_banco": "1234",
    "nome_banco": "Banco Exemplo",
    "agencia": "1234",
    "conta_corrente": "1234567-8",
    "matricula": "20240001",
    "posto_trabalho": "Departamento A",
    "cargo": "Analista",
    "cidade": "Salvador",
    "centro_custo": "Centro A"
}

````

**404 Not Found**: Quando o funcionário com o CPF fornecido não é encontrado.

````bash
{
    "detail": "Funcionário com CPF 12345678901 não encontrado"
}
````

#### /atualizar/ (http://localhost:8000/api/v1/funcionario/atualizar)

Este endpoint atualiza os dados do funcionário com base no CPF fornecido.

-   **Método HTTP**: PUT
-   **Parâmetros**:
    -   **FuncionarioSchemaUp**: Dados a serem atualizados.
-   **Autenticação**:
    -   Requer autenticação.
-   **Exemplo de Requisição**:
- 
````bash
curl -X PUT -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{
    "cpf": "12345678901",
    "cod_banco": "5678",
    "nome_banco": "Banco Novo",
    "agencia": "5678",
    "conta_corrente": "8765432-1"
}' http://localhost:8000/api/v1/funcionario/atualizar

````

**Respostas**:

-   **200 OK**: Funcionário atualizado com sucesso.

````bash
{
    "cpf": "12345678901",
    "cod_banco": "5678",
    "nome_banco": "Banco Novo",
    "agencia": "5678",
    "conta_corrente": "8765432-1"
}
````

**404 Not Found**: Quando o funcionário com o CPF fornecido não é encontrado.

````bash
{
    "detail": "Funcionário com CPF 12345678901 não encontrado"
}

````

### Endpoints Banco

#### /listar (http://localhost:8000/api/v1/banco/listar)

Esta rota retorna a lista de todos os bancos cadastrados.

-   **Método HTTP**: GET
-   **Parâmetros**:
    -   Nenhum parâmetro adicional é necessário.
-   **Autenticação**:
    -   Necessário token de segurança (JWT).
-   **Exemplo de Requisição**:

```bash
curl -X GET -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/bancos/listar
```

**Respostas**:

-   **200 OK**: Retorna a lista de bancos.
````bash
[
    {
        "cod_banco": "001",
        "nome_banco": "Banco do Brasil"
    },
    {
        "cod_banco": "237",
        "nome_banco": "Bradesco"
    }
]
````

**404 Not Found**: Quando não há bancos cadastrados.

````bash
{
    "detail": "Nenhum banco encontrado"
}
````

### Endpoints Localidades

#### /estados (http://localhost:8000/api/v1/localidades/estados)

Esta rota retorna a lista de todos os estados cadastrados.

-   **Método HTTP**: GET
-   **Parâmetros**:
    -   Nenhum parâmetro adicional é necessário.
-   **Autenticação**:
    -   Necessário token de segurança (JWT).
-   **Exemplo de Requisição**:

````bash
curl -X GET -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/localidades/estados
````
**Respostas**:

-   **200 OK**: Retorna a lista de estados.
````bash
[
    {
        "cod_estado": 1,
        "estado": "Bahia"
    },
    {
        "cod_estado": 2,
        "estado": "São Paulo"
    }
]

````

**404 Not Found**: Quando não há estados cadastrados.

````bash

{
    "detail": "Nenhum estado encontrado"
}

````

#### /cidades (http://localhost:8000/api/v1/localidades/cidades)

Esta rota retorna a lista de todas as cidades para um estado específico.

-   **Método HTTP**: POST
-   **Parâmetros**:
    -   **cod_estado**: Código do estado para buscar as cidades (no corpo da requisição).
-   **Autenticação**:
    -   Necessário token de segurança (JWT).
-   **Exemplo de Requisição**:

````bash
curl -X POST -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"cod_estado": 29}' http://localhost:8000/api/v1/localidades/cidades
````

**Respostas**:

-   **200 OK**: Retorna a lista de cidades para o estado especificado.
````bash
[
    {
        "cidade": "Salvador"
    },
    {
        "cidade": "Feira de Santana"
    }
]
````

**404 Not Found**: Quando não há cidades cadastradas para o estado especificado.

````bash
{
    "detail": "Nenhuma cidade encontrada para este estado."
}
````

### Endpoints Diária

#### /calcular (http://localhost:8000/api/v1/diaria/calcular)

Esta rota calcula as diárias baseando-se nos trechos fornecidos.

-   **Método HTTP**: POST
-   **Parâmetros**:
    -   **trechos**: Lista de trechos da viagem, contendo informações como datas e horários de saída e retorno, estados e cidades de origem e destino.
    -   **tipo_sd**: Tipo de solicitação (solicitação, complementação, devolução).
    -   **codigo_sd** (opcional): Código da solicitação, necessário para complementação e devolução.
    -   **valor_sd** (opcional): Valor da solicitação, necessário para complementação e devolução.
-   **Autenticação**:
    -   Necessário token de segurança (JWT).
-   **Exemplo de Requisição**:

````bash

curl -X POST -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{
    "trechos": [
        {
            "dt_saida": "2024-07-20",
            "hr_saida": "08:00",
            "dt_retorno": "2024-07-22",
            "hr_retorno": "18:00",
            "estado_origem": 29,
            "estado_destino": 35,
            "cidade_origem": "Salvador",
            "cidade_destino": "São Paulo"
        }
    ],
    "tipo_sd": "solicitação"
}' http://localhost:8000/api/v1/diaria/calcular
````

**Respostas**:

-   **200 OK**: Retorna os valores calculados das diárias

````bash

{
  "quantidade_diarias_simples": 0,
  "quantidade_diarias_completas": 1,
  "valor_diarias_simples": 0,
  "valor_diarias_completas": 270,
  "valor_total": 270,
  "user_id": "teste@fesfsus.ba.gov.br"
}
````

**400 Bad Request**: Quando há problemas com os dados fornecidos na solicitação.

````bash
{
    "detail": "Lista de trechos está vazia."
}
````

#### /gerar_sd (http://localhost:8000/api/v1/diaria/gerar_sd)

Esta rota gera um número único para a solicitação de diária.

-   **Método HTTP**: POST
-   **Parâmetros**:
    -   **tipo_sd**: Tipo de solicitação (solicitação, complementação, devolução).
    -   **codigo_sd** (opcional): Código da solicitação, necessário para complementação e devolução.
-   **Autenticação**:
    -   Necessário token de segurança (JWT).
-   **Exemplo de Requisição**:
````bash
curl -X POST -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{
    "tipo_sd": "solicitação"
}' http://localhost:8000/api/v1/diarias/gerar_sd
````
**Respostas**:

-   **200 OK**: Retorna o código da solicitação gerado e a data e hora da geração.

````bash
{
    "codigo_sd": "00001/2024",
    "data_hora_sd": "2024-07-20T08:00:00",
    "user_id": "user123"
}
````

**400 Bad Request**: Quando há problemas com os dados fornecidos na solicitação.

````bash
{
    "detail": "Tipo de solicitação inválido. Use 'solicitação', 'complementação' ou 'devolução'."
}
````