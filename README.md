# 🎬 Cinema Manager – Sistema de Gerenciamento de Cinema (Python)

Um sistema completo para gerenciamento de um cinema, desenvolvido em Python utilizando **Programação Orientada a Objetos**, persistência em **JSON**, modelagem modular e boas práticas de arquitetura.

Este projeto começou pequeno, mas evoluiu naturalmente para um sistema mais robusto, servindo como estudo realista de POO, dados e organização de software.

---

## ✨ Funcionalidades

### 🎞 Filmes
- Criar, listar, editar e remover filmes  
- IDs únicos incrementais  
- Armazenamento em `data/filmes.json`

### 🏟 Salas
- Registro de salas com capacidade  
- Totalmente integradas às sessões  
- Armazenamento em `data/salas.json`

### 🎥 Sessões
- Criação de sessões vinculadas a **filme + sala**  
- Verificação automática de conflitos (mesmo horário/mesma sala)  
- Controle persistente de assentos  
- Armazenamento em `data/sessoes.json`

### 🗃 Backup e Histórico
- Itens removidos podem ser enviados para um arquivo separado  
- Cada item recebe metadados de remoção  
- Armazenamento em `data/historico.json`

### 🧭 Menu interativo
- Interface simples via terminal  
- Organização clara dentro do módulo `cinema/menu.py`  
- `main.py` minimalista: apenas importa e executa o menu

---

## 🗂 Estrutura do Projeto

```yaml
├── cinema/
│ ├── models.py # Lógica das classes principais do sistema & Funções auxiliares
│ ├── menu.py # Menu principal
│ ├── storage.py # Gerência dos arquivos JSON
│
├── data/ # Parcialmente implementado
│ ├── filmes.json
│ ├── salas.json
│ ├── sessoes.json
│ └── historico.json
│
├── main.py # Ponto de entrada do programa
└── README.md
```

---

## 🔧 Tecnologias e Conceitos

- Python 3.x  
- Programação Orientada a Objetos  
- JSON como persistência de dados  
- Modelagem modular  
- Manipulação de arquivos  
- Controle de IDs  
- Validação e prevenção de conflitos (sessões)  
- Estrutura profissional de projeto  

---

## 🧠 Aprendizados

Este projeto serviu como um estudo prático de:

- Arquitetura de software sem framework  
- Organização de módulos de forma profissional  
- Separação clara entre lógica, dados e interface  
- Manipulação segura de arquivos JSON  
- Raciocínio sobre IDs únicos e dados persistentes  
- Pensamento estruturado sobre backup e histórico  
- Evolução incremental de um projeto real  

---

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

- Adicionar relatórios automáticos
- Melhorar o histórico com filtragem por datas
- Considerar migração futura para SQLite
- Implementar interface gráfica (Tkinter ou web)
- Criar testes unitários com pytest

---

📄 Licença
Este projeto está licenciado sob a licença MIT.
Isso significa que você pode usar, modificar e distribuir o código livremente, desde que mantenha os créditos.

👨‍💻 Autor: Matheus Novais 🫡