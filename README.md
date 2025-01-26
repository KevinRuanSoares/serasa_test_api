# Brain Agriculture API Project

## Sobre o Projeto

Este projeto é uma API desenvolvida com Django e Docker para gerenciar recursos da "Brain Agriculture". Ele é configurado para ser executado em um ambiente local ou em servidores com suporte ao Docker.

---

## Requisitos

- Docker e Docker Compose instalados em sua máquina.
- Python (caso deseje executar scripts localmente, sem Docker).

---

## Configuração Inicial

1. **Configurar o Ambiente (.env):**
   - É **obrigatório** criar o arquivo `.env` antes de rodar o projeto.
   - Duplique o arquivo `.env.sample` e renomeie para `.env`.
   - **IMPORTANTE:** Altere as credenciais do banco de dados e a `DJANGO_SECRET_KEY` para maior segurança, especialmente se for executar o projeto em um servidor.

2. **Inicializar o Projeto Localmente:**
   - Execute o comando:
     ```bash
     make local
     ```
     Esse comando cria o banco de dados local e inicia a API.

3. **Criar Superusuário:**
   - Crie um usuário administrador executando o comando:
     ```bash
     make createsuperuser
     ```
     Insira as credenciais desejadas.

---

## Comandos Disponíveis

### Estilo de Código
- Para verificar e corrigir o estilo do código:
  ```bash
  make style
  ```

### Testes
- Para rodar os testes:
  ```bash
  make test
  ```

### Migrações
- **Criar Migrações:**
  ```bash
  make makemigrations
  ```
- **Aplicar Migrações:**
  ```bash
  make migrate
  ```

### Criar Superusuário
- Para criar um Super Admin:
  ```bash
  make createsuperuser
  ```

### Debugging com VSCode
- Para executar o projeto com suporte a depuração no VSCode:
  ```bash
  make debug
  ```

---

## Boas Práticas
- Sempre utilize o arquivo `.env` para gerenciar suas credenciais e variáveis de ambiente.
- Antes de subir o projeto em um servidor, execute testes e verifique o estilo do código para garantir padrões consistentes.
- Mantenha o repositório atualizado com as migrações do banco de dados.

---

## Suporte
Caso encontre problemas ou tenha dúvidas, sinta-se à vontade para abrir uma *issue* no repositório.

