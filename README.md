# Canto do Bem

**Unindo pessoas por um propósito comum através da tecnologia.**

O **Canto do Bem** é uma plataforma de Tecnologia Social desenvolvida para mitigar a desorganização no trabalho voluntário e conectar cidadãos a ONGs de forma eficiente. O projeto visa preencher a lacuna entre a vontade de ajudar e a oportunidade de agir.

![Image](https://github.com/user-attachments/assets/d638e13d-8744-4793-a5e5-45d4b1551941)

---

## 🛠️ Documentação Técnica

Este projeto foi construído utilizando a linguagem **Python**, com foco em modularidade, persistência de dados local e uma interface de linha de comando (CLI) amigável.

### 📚 Bibliotecas e Dependências

Para executar o projeto, foram utilizadas bibliotecas nativas e externas, escolhidas para otimizar o desenvolvimento e a experiência do usuário (UX) no terminal.

* **`rich` (Externa):**
    * *Justificativa:* Utilizada para a construção da interface visual no terminal (CLI). A biblioteca permite o uso de painéis (`Panel`), cores, formatação de texto (negrito, cores de alerta) e layouts organizados, tornando a navegação intuitiva e visualmente agradável, fugindo do padrão monótono do terminal.
    * *Componentes usados:* `Console`, `Panel`.
* **`json` (Nativa):**
    * *Justificativa:* Responsável pela persistência dos dados. O sistema utiliza um banco de dados baseado em arquivo (`dados.json`) para armazenar informações de usuários, ONGs e eventos, permitindo que os registros sejam mantidos entre as execuções do programa.
* **`os` e `sys` (Nativas):**
    * *Justificativa:* Essenciais para manipulação de caminhos de arquivos e diretórios (`os.path`). Garantem que o sistema encontre o arquivo `dados.json` e importe os módulos corretamente, independentemente do sistema operacional ou do diretório onde o script é executado.
* **`datetime` (Nativa):**
    * *Justificativa:* Utilizada para manipulação e validação de datas. O sistema impede, por exemplo, o cadastro de eventos em datas passadas, garantindo a integridade lógica da agenda.

### ⚙️ Execução do Projeto

Para rodar o projeto localmente, é necessário ter o Python instalado e instalar a dependência externa:

```bash
# Instalação da biblioteca visual
pip install rich

# Execução do sistema
python main.py
