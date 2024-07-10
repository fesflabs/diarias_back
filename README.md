
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
     MAIL_USER=seuemail@email.com
     MAIL_FROM=seuemail@email.com
     MAIL_PASSWORD=Senha do email
     JWT_SECRET=Token de segurança
     ```

5. **Criação de Token de Segurança**:
   - Para gerar um token de segurança, execute o seguinte comando:
     ```bash
     python -c "import secrets;
     print(secrets.token_urlsafe(32))"
     
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

## Endpoints da API - V1

### Estrutura de Diretórios

- `api/v1/endpoints/`
- `funcionario.py`: Endpoint para enviar e-mail de acesso ao sistema.

### Exemplo de Uso do Endpoint

#### `/enviar-link-acesso`

- **Método HTTP**: POST
- **Parâmetros**:
  - `email`: O e-mail do funcionário com o domínio `fesfsus.ba.gov.br`.
- **Exemplo de Requisição**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"email": "usuario@fesfsus.ba.gov.br"}' http://localhost:8000/enviar-link-acesso
  

**Respostas**:

-   202 OK: `{"message": "Email enviado com sucesso."}`
-   404 Not Found: `{"detail": "Apenas emails com o domínio @fesfsus.ba.gov.br são autorizados a receber o link de acesso."}`