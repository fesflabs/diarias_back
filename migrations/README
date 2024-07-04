
# Diárias

  

Sistema de cálculo de diárias.

  
  

## Backend

  

## Pré-requisitos

-  `Python 3.12.1`

-  `PostgreSQL`

  

## Como começar?

  

1. Clonar repositorio: Clone o diarias em sua maquina local.

  

2. Crie e ative um ambiente virtual: `python -m venv venv` e `.\venv\Scripts\activate`

  

3. Instale as dependências: `pip install -r requirements.txt`

  

#### Configuração de ambiente .env

  

O arquivo `.env` é usado para para Manipular dados Sensiveis como Senhas, tokens de acesso e credenciais de banco de dados, no arquivo deve configurar as variáveis de ambiente necessárias para o projeto.

  

Certifique-se de instalar a biblioteca python-dotenv antes de usar.

  

-  ```pip install python-dotenv```

  

### Criação de token de segurança

  

1. Abra um terminal.

  

2. Execute o seguinte comando:

  

``` python

  
python -c "import secrets; print(secrets.token_urlsafe(32))"

  
```

  
#### Como Criar o Arquivo .env

  

Para criar o arquivo `.env`, verifique o arquivo .ENV-EXEMPLO, e siga estas etapas:

  

1. Crie um novo arquivo chamado `.env` no diretório raiz do projeto.

  

2. Adicione as variáveis de ambiente necessárias no formato `NOME_DA_VARIAVEL=valor`.

  

Exemplo:

  

-  `MAIL_USERNAME = 'email@email.com.br'`


#### Variáveis de Ambiente

  

-  `DB_NOME=`: Nome do banco

  

-  `DB_USER=` : Usuario

  

-  `DB_SENHA=`Senha do banco

  

-  `DB_HOST=`: Host


- `DATABASE_URL=`postgresql://user:password@localhost/mydatabase
  

-  `MAIL_USERNAME =`: seuemail@email.com

  

-  `MAIL_FROM =`: seuemail@email.com

  

-  `MAIL_PASSWORD`: Senha do email

  

-  `JWT_SECRET `: token de segurança

  

#### Banco de Dados

  

1. Configure as variáveis de ambiente.

- Atente-se a criação da variável DATABASE_URL no arquivo .env.

2. Verificar as migrações existentes.

- Verifique se há migrações existentes no diretório `alembic/versions`. O próximo programador precisará aplicar essas migrações para criar as tabelas.


3. Aplicar migrações

- Para aplicar todas as migrações e criar as tabelas no banco de dados deve executar o comando:

``` python
 

alembic upgrade head

``` 
  

## Rotas da API - V1

  

Este diretório contém os endpoints da API para a versão 1.

  
  

## Estrutura de Diretórios

  

-  `api/v1/endpoints/`

  

-  `funcionario.py`: Endpoint para enviar e-mail de acesso ao sistema.


## Endpoints

  

```python
  

/enviar-link-acesso

  
```

  

Quando um cliente faz uma solicitação POST para este endpoint, o servidor verifica se o e-mail fornecido corresponde ao domínio FESF. Se um e-mail corresponder, o link de acesso será enviado.

  
  

-  **Parâmetros:**

  

- e-mail : O e-mail do funcionário com o domínio `fesfsus.ba.gov.br`.

  

### Método HTTP

  
  

-  **POST**: Usado para enviar um link de acesso por e-mail para usuários autorizados.

  

Respostas:

  

### Respostas

  

- 202 OK: `{"message": "Email enviado com sucesso."}`.

  

- 404 Not Found: `{"detail": "Apenas emails com o domínio @fesfsus.ba.gov.br são autorizados a receber o link de acesso."}`.
