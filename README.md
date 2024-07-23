
# Diárias

  

Sistema de cálculo de diárias.

  
  

## Backend

  



## Como começar?

1. **Clonar repositório**: Clone o projeto diarias para sua máquina local.

2. **Configurar Ambiente Virtual (Opcional para DevOps)**:
   - Crie e ative um ambiente virtual:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate  # Windows
     ```
   
3. **Instalar Dependências**:
   - Instale as dependências necessárias:
     ```bash
     pip install -r requirements.txt
     ```

4. **Configuração do Ambiente .env**:
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

5. **Criação de Token de Segurança**:
   - Para gerar um token de segurança, execute o seguinte comando:
     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(32))"
     
     ```

6. **Banco de Dados e Migrações**:
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

### Endpoints funcionario

#### `/enviar-link-acesso`

Esta rota envia um link de acesso as sistema de diárias.


- **Método HTTP**: POST

- **Parâmetros**:
  - `email`: O e-mail do funcionário com o domínio `fesfsus.ba.gov.br`.
- **Exemplo de Requisição**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"email": "usuario@fesfsus.ba.gov.br"}' http://localhost:8000/enviar-link-acesso
  

**Respostas**:

-   202 OK: `{"message": "Email enviado com sucesso."}`
-   404 Not Found: `{"detail": "Apenas emails com o domínio @fesfsus.ba.gov.br são autorizados a receber o link de acesso."}`


#### `/criar`

Esta rota cria um novo funcionário.

-   **Método HTTP**: POST
-   **Parâmetros**:
    -   `funcionario`: Objeto JSON contendo as informações do funcionário no formato de `FuncionarioSchemaBase`.
     -   `CPF`: O CPF informado não deve existir no banco de dados`.


-   **Exemplo de Requisição**:
    
    
    Copiar código
    
    `curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{
      "cpf": "32165498700",
      "nome": "João da Silva",
      "data_nasc": "01/01/1990",
      "cod_banco": "001",
      "nome_banco": "Banco Exemplo",
      "agencia": "1234",
      "conta_corrente": "567890"
    }' http://localhost:8000/criar` 
    
-   **Respostas**:
-   201 Created: `{"cpf": "32165498700", "nome": "João da Silva", "data_nasc": "01/01/1990", "cod_banco": "001", "nome_banco": "Banco Exemplo", "agencia": "1234", "conta_corrente": "567890"}`
-    400 Bad Request:
        -   `{"detail": "O CPF deve conter 11 dígitos numéricos"}`
        -   `{"detail": "CPF inválido"}`
        -   `{"detail": "Formato de data inválido. Use o formato 'dd/mm/yyyy'."}`
    -   403 Forbidden: `{"detail": "Acesso negado"}`



#### `/buscar/{cpf}`

Retorna as informações do funcionário.

-   **Método HTTP**: GET
-   **Parâmetros**:
    -   `cpf`: CPF do funcionário a ser buscado.
-   **Exemplo de Requisição**:

    
    Copiar código
    
    `curl -X GET -H "Authorization: Bearer <token>" http://localhost:8000/buscar/32165498700` 
    
-   **Respostas**:
-   200 OK: `{"cpf": "32165498700", "nome": "João da Silva", "data_nasc": "01/01/1990", "cod_banco": "001", "nome_banco": "Banco Exemplo", "agencia": "1234", "conta_corrente": "567890"}`
-   400 Bad Request: `{"detail": "O CPF deve conter 11 dígitos numéricos"}`
-   404 Not Found: `{"detail": "Funcionário com CPF 32165498700 não encontrado"}`


#### `/atualizar`

Atualiza as informações bancárias do funcionário.

-   **Método HTTP**: PUT
-   **Parâmetros**:
    -   `update_data`: Objeto JSON contendo as informações a serem atualizadas no formato de `FuncionarioSchemaUp`.
    - `cpf`: O CPF do usuário que foi informado no GET.
-   **Exemplo de Requisição**:

    
    Copiar código
    
    `curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer <token>" -d '{
      "cpf": "32165498700",
      "cod_banco": "002",
      "nome_banco": "Novo Banco",
      "agencia": "5678",
      "conta_corrente": "123456"
    }' http://localhost:8000/atualizar/` 
    
-   **Respostas**:
-   200 OK: `{"cpf": "32165498700", "cod_banco": "002", "nome_banco": "Novo Banco", "agencia": "5678", "conta_corrente": "123456"}`
-   404 Not Found: `{"detail": "Funcionário com CPF 32165498700 não encontrado"}`