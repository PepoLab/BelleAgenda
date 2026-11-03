# BelleAgenda

Sistema web de agendamento desenvolvido como MVP acadêmico, com foco no gerenciamento de clientes, serviços e horários de atendimento.

## Tecnologias

- Python
- Django
- PostgreSQL
- HTML5
- CSS3
- Bootstrap

## Funcionalidades do MVP

- Autenticação de usuários
- Agenda de atendimentos
- Cadastro e gerenciamento de clientes
- Cadastro e gerenciamento de serviços
- Criação de agendamentos
- Prevenção de conflitos de horário
- Cancelamento de agendamentos
- Ativação e desativação de clientes e serviços
- Interface responsiva

## Arquitetura

O sistema utiliza uma arquitetura baseada no padrão do Django, separando as principais responsabilidades entre:

- **Models:** representação dos dados e regras de negócio.
- **Views:** processamento das requisições e controle dos fluxos.
- **Forms:** validação e tratamento dos dados enviados pelos usuários.
- **Templates:** apresentação das informações na interface.
- **Static:** arquivos de estilo utilizados pela aplicação.

O banco de dados PostgreSQL é utilizado para persistência das informações.

## Segurança e regras de negócio

Durante a implementação e auto-revisão técnica foram consideradas as seguintes medidas:

- Autenticação obrigatória para acesso às funcionalidades internas.
- Uso de proteção CSRF nos formulários enviados por POST.
- Uso de variáveis de ambiente para informações