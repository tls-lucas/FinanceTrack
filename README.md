# FinanceTrack

Aplicação web de controle financeiro pessoal, construída com Flask.

## Stack

- Flask + Flask-SQLAlchemy
- MySQL
- APScheduler (tarefas agendadas)
- fpdf (geração de relatórios em PDF)

## Rodando localmente

```bash
pip install -r requirements.txt
python app.py
```

Configure as credenciais do banco em um arquivo `.env` (veja `.gitignore`).
