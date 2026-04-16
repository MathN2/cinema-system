# 🎬 Cinema Manager – Sistema de Gerenciamento de Cinema (Python)

Um sistema completo para gerenciamento de um cinema, desenvolvido em Python utilizando **Programação Orientada a Objetos**, persistência em banco de dados **MySQL**, com suporte legado a JSON para backup, modelagem modular e boas práticas de arquitetura.

Este projeto começou pequeno, mas evoluiu naturalmente para um sistema mais robusto, servindo como estudo realista de POO, dados e organização de software.

---

## 📌 Status do Projeto

🚧 Em desenvolvimento ativo  
✔ CRUD completo com MySQL  
✔ Sistema modular estruturado  
🔄 Evolução da interface CLI em andamento  


## ✨ Funcionalidades

### 🎞 Filmes
- Criar, listar, editar e remover filmes  
- IDs únicos gerados pelo banco de dados
- Persistência em MySQL

### 🏟 Salas
- Registro de salas com capacidade
- Integração com sessões
- Persistência em MySQL

### 🎥 Sessões
- Criação de sessões vinculadas a **filme + sala**  
- Validação de conflitos de sala
- Controle de assentos 
- Persistência em MySQL

### 🗃 Backup e Histórico
- Estrutura preparada para backup em JSON (legado)
- Possibilidade futura de exportação de dados

### 🧭 Menu interativo
- Interface simples via terminal  
- Organização clara dentro do módulo `cinema/menu.py`  
- `main.py` minimalista: apenas importa e executa o menu

---

## 🗂 Estrutura do Projeto

```yaml
│   .gitignore
│   main.py
│   README.md    
│
├───backup  # camada de persistência (MySQL + legado JSON)
└───cinema
    │   __init__.py
    │
    ├───data
    │   │   db.py
    │   │   loading_db.py
    │   │   saving_db.py
    │   │   storage.py
    │   │   teste.py
    │
    ├───models
    │   │   filme.py
    │   │   sala.py
    │   │   sessao.py
    │
    ├───services
    │   │   atualizar_filme.py
    │   │   criar_filme.py
    │   │   criar_sala.py
    │   │   criar_sessao.py
    │   │   excluir_filme.py
    │   │   excluir_sala.py
    │   │   filme_services.py
    │   │   sessao_services.py
    │   │   utils.py
    │
    ├───UI
    │   ├───CLI
    │   │   │   coletar_dados_filme.py
    │   │   │   coletar_dados_sala.py
    │   │   │   menu.py
    │   │   │   menu_adm.py
    │   │   │   menu_cliente.py
    │   │   │   menu_filmes.py
    │   │   │   menu_salas.py
    │   │   │   paginacao.py
    │   │
    │   └───GUI
```

---

## 🔧 Tecnologias e Conceitos

- Python 3.x  
- MySQL 
- Programação Orientada a Objetos (POO)
- Arquitetura em camadas (models, services, data, UI)
- CLI modular (em evolução para UI mais avançada)  

---

## 🧠 Aprendizados

Este projeto serviu como um estudo prático de:

- Arquitetura de software sem framework  
- Organização de módulos de forma profissional  
- Separação clara entre lógica, dados e interface  
- Integração entre Python e MySQL  
- Migração de persistência baseada em arquivos para banco de dados  
- Separação entre dados persistidos e lógica de negócio  
- Raciocínio sobre IDs únicos e dados persistentes  
- Pensamento estruturado sobre backup e histórico  
- Evolução incremental de um projeto real  

---

## ⚠️ Pré-requisitos

- Python 3.x
- MySQL instalado e rodando

## 🔧 Configuração do banco

Configure as credenciais no arquivo:

cinema/data/db.py

## 🚀 Como executar

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/cinema-manager.git
cd cinema-manager
```

Execute o projeto:

```bash
python main.py
```

📌 Próximos passos planejados

- Melhorar interface CLI com Rich e Questionary  
- Implementar sistema de status (filmes/sessões)  
- Adicionar relatórios e consultas mais avançadas  
- Criar testes automatizados com pytest  
- Evoluir para interface gráfica (GUI ou Web)  

---

📄 Licença
Este projeto está licenciado sob a licença MIT.
Isso significa que você pode usar, modificar e distribuir o código livremente, desde que mantenha os créditos.

👨‍💻 Autor: Matheus Novais 🫡