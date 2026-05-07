# meu-mini-projeto-iot
Orientações para desenvolvimento o mini projeto:
- A construção de codigo, execução e hospedagem será realizada no Github e Render

Escopo do mini projeto:
1. DESCRIÇÃO
O projeto consiste em um sistema web desenvolvido com Flask, estruturado no padrão MVC (Model–View–Controller), que oferece um CRUD completo para gerenciamento de registros (ex.: produtos, alunos, tarefas, clientes). O sistema inclui autenticação de usuários, autorização baseada em role, persistência de dados com SQLAlchemy e é implantado na nuvem utilizando a plataforma Render.

2. FUNCIONALIDADES PRINCIPAIS:
2.1. CRUD Completo - o sistema deve permitir:
2.1.1. Criar novos registros
2.1.2. Listar registros cadastrados
2.1.3. Editar informações existentes
2.1.4. Excluir registros

2.2. Autenticação - os usuários podem:
2.2.1. Criar conta
2.2.2. Fazer login Senhas são armazenadas com hashing seguro.
2.2.3. Um token JWT é gerado durante a autenticação.

2.3. Autorização - existem níveis de acesso, como:
2.3.1. Admin — pode criar, editar e excluir todos os registros
2.3.2. Usuário comum — pode apenas visualizar ou editar seus próprios dados

2.4. O código segue o padrão Model–View–Controller:
2.4.1. Models: Classes Python que representam tabelas do banco de dados usando SQLAlchemy (ex.: User, Product).
2.4.2. Views: O sistema utiliza respostas em formato JSON.
2.4.3. Controllers: Rotas Flask que conectam os models às views, aplicando regras de negócio.

2.5. Persistência com SQLAlchemy: O sistema utiliza Flask SQLAlchemy para mapear objetos → tabelas

2.6. Deploy no Render: O projeto é configurado para ser implantado no Render. O banco de dados utilizado é o PostgreSQL.
