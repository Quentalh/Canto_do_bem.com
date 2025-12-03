# Canto do Bem

Unindo pessoas por um propósito comum.

O trabalho voluntário enfrenta desafios significativos, como a falta de organização e divulgação, que desmotivam potenciais voluntários e desperdiçam recursos valiosos. As organizações sem fins lucrativos também têm dificuldade em engajar e reter voluntários de forma eficiente. Canto do Bem nasce para resolver esses problemas.

![Image](https://github.com/user-attachments/assets/d638e13d-8744-4793-a5e5-45d4b1551941)

---

## 🛠️ Documentação Técnica

Este projeto foi construído utilizando a linguagem **Python**, com foco em modularidade, persistência de dados local e uma interface de linha de comando (CLI) amigável.

### 📚 Bibliotecas e Dependências

Foram utilizadas bibliotecas nativas e externas para otimizar o desenvolvimento e a experiência do utilizador (UX) no terminal.

* **`rich` (Externa):**
    * *Justificativa:* Utilizada para a construção da interface visual no terminal (CLI). A biblioteca permite o uso de painéis (`Panel`), cores e formatação de texto, tornando a navegação intuitiva e visualmente agradável, superando o padrão básico do terminal.
    * *Componentes usados:* `Console`, `Panel`.
* **`json` (Nativa):**
    * *Justificativa:* Responsável pela persistência dos dados. O sistema utiliza um banco de dados baseado em arquivo (`dados.json`) para armazenar informações de utilizadores, ONGs e eventos, garantindo que os registos sejam mantidos entre execuções.
* **`os` e `sys` (Nativas):**
    * *Justificativa:* Essenciais para manipulação de caminhos de arquivos e diretórios (`os.path`). Garantem que o sistema encontre a base de dados e importe os módulos corretamente, independentemente do sistema operativo.
* **`datetime` (Nativa):**
    * *Justificativa:* Utilizada para validação temporal. O sistema impede o cadastro de eventos em datas passadas e gere o agendamento no calendário.

### ⚙️ Execução do Projeto

Para rodar o projeto localmente:

1.  Instale a dependência externa:
    ```bash
    pip install rich
    ```
2.  Execute o sistema:
    ```bash
    python main.py
    ```

## 💡 Inovação Técnica

O projeto inova ao introduzir conceitos de **Gestão Pessoal** no voluntariado via terminal. Diferente de scripts simples, o sistema oferece um **Calendário Personalizado**, permitindo que o voluntário faça a curadoria da sua própria agenda social, adicione eventos específicos ao seu perfil e acompanhe a sua participação.

---

## Qual a nossa Missão?

Nossa missão é criar uma ponte entre cidadãos, voluntários e ONGs, incentivando a participação em ações sociais de forma organizada e eficiente. Queremos:

- **Capacitar cidadãos** para organizar, participar e engajar outras pessoas em ações sociais em grupo.
- **Facilitar a busca** por oportunidades de voluntariado e ONGs na sua cidade.
- **Motivar novos participantes** por meio de um sistema de recompensas gamificado, alcançando até mesmo aqueles que não têm interesse inicial em ativismo comunitário.
- **Conectar pessoas** com valores e paixões em comum, fortalecendo laços e comunidades.
- **Preencher uma lacuna de mercado**.

---

## Como faremos isso?

Desenvolveremos uma plataforma com funcionalidades essenciais para otimizar a experiência de voluntariado.

### Funcionalidades - Fase 1 (AV1)

- **Cadastro e Login**: Permite que usuários e ONGs criem contas na plataforma.
- **Perfis**: Usuários podem criar e editar seus perfis, indicando seus interesses.
- **Notificações**: Um sistema de notificações mantém os usuários informados.
- **Eventos**: ONGs e usuários podem criar eventos de voluntariado.
- **Calendário Pessoal**: Os usuários podem salvar e gerenciar os eventos nos quais planejam participar.

### Funcionalidades - Fase 2 (AV2)

- **Busca Avançada**: Os usuários podem procurar por oportunidades de voluntariado por tipo de ação ou localização.
- **Gamificação**: Um sistema de pontos e missões (individuais e em grupo) oferece benefícios não monetários e recompensa a participação.
- **Avaliações**: Usuários, ONGs e eventos podem ser avaliados para garantir transparência.
- **Portal de Transparência**: Um portal dedicado à transparência para fortalecer a confiança na plataforma.
- **Ranking**: Um sistema de ranking com pontuações, medalhas e títulos reconhece os voluntários mais engajados.

---

## Área de Aplicação e Público-Alvo

O **Canto do Bem** é um projeto de Tecnologia Social. Inicialmente, o projeto será lançado na cidade de Recife, com potencial de expansão para todo o Brasil. A plataforma interagirá com os usuários de forma dinâmica e intuitiva.

Nosso público-alvo é dividido em três grupos:

- **Cidadãos Comuns**: Aqueles que desejam iniciar suas próprias ações sociais ou ter sua primeira experiência com o serviço social.
- **Voluntários Desmotivados**: Pessoas que buscam oportunidades e benefícios não monetários para retomar o interesse no trabalho voluntário.
- **ONGs e Empresas**: Organizações que precisam de uma plataforma para gerenciar sua força de trabalho voluntária, conseguir mais engajamento e focar em suas missões.

### 📂 Arquitetura e Organização dos Módulos

O sistema segue uma arquitetura modular para facilitar a manutenção:

```text
codigos_canto_do_bem/
│
├── main.py                  # Ponto de entrada e Menu Principal
├── auxiliares/              # Camada de Persistência
│   └── json_auxiliares.py   # Leitura/Escrita no JSON
│
├── modulos/                 # Regra de Negócio
│   ├── cadastro.py          # Validações e registo
│   ├── login.py             # Autenticação
│   ├── eventos.py           # Gestão de eventos
│   ├── calendario.py        # Agenda pessoal
│   └── perfil.py            # Edição de utilizador
│
└── base_de_dados/           # Dados
    └── dados.json           # Armazenamento

