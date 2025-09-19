# ⚽ Scoutify - Automação de Vagas de Prática

**Scoutify** é uma automação em Python que monitora vagas de prática em clubes de futebol do portal [Futebol Interativo](https://praticas.futebolinterativo.com/).  
O sistema roda em segundo plano, acessa clubes específicos, registra todas as vagas disponíveis e envia uma **notificação no computador** quando encontra a vaga desejada.

---

## ✨ Funcionalidades

- 🔄 Executa automaticamente (pode ser configurado para iniciar junto com o PC).  
- 🌐 Abre a página de clubes pré-definidos (ex.: Portuguesa-RJ, Madureira).  
- 📊 Identifica as áreas de atuação disponíveis (ex.: Comunicação e Marketing, Análise, Gestão e Negócios, Saúde e Performance).  
- 📝 Registra um **histórico em CSV** com:
  - Data e hora da verificação
  - Clube consultado
  - Área da vaga
  - Status (disponível ou não)
- 🔔 Envia uma **notificação no Windows** quando encontra a vaga de **Análise**.  

---

## 🛠️ Tecnologias utilizadas

- [Python](https://www.python.org/)  
- [Playwright](https://playwright.dev/python/) – automação de navegador  
- [Plyer](https://plyer.readthedocs.io/en/latest/#notification) – notificações desktop  
- [CSV](https://docs.python.org/3/library/csv.html) – para salvar histórico  

