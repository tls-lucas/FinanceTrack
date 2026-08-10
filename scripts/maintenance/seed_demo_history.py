from datetime import date
from pathlib import Path
import sys
import argparse

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app import Category, Transaction, User, app, db


DEFAULT_EMAIL = "demo@financetrack.local"


SEED_CATEGORIES = [
    ("Freelance", True),
    ("Investimentos", True),
    ("Assinaturas", True),
    ("Educacao", True),
    ("Viagem", True),
    ("Presentes", True),
]


SEED_TRANSACTIONS = [
    ("2024-02-05", "income", 4200.00, "Salário", "Salario base fevereiro 2024"),
    ("2024-02-07", "expense", 1450.00, "Moradia", "Aluguel fevereiro 2024"),
    ("2024-02-12", "expense", 680.00, "Alimentação", "Supermercado fevereiro 2024"),
    ("2024-04-10", "income", 1100.00, "Freelance", "Projeto web abril 2024"),
    ("2024-04-15", "expense", 210.00, "Transporte", "Combustivel abril 2024"),
    ("2024-04-22", "expense", 320.00, "Saúde", "Consulta abril 2024"),
    ("2024-09-02", "income", 4800.00, "Salário", "Salario base setembro 2024"),
    ("2024-09-05", "expense", 1600.00, "Moradia", "Aluguel setembro 2024"),
    ("2024-09-18", "expense", 240.00, "Lazer", "Cinema setembro 2024"),
    ("2024-12-03", "income", 5000.00, "Salário", "Salario base dezembro 2024"),
    ("2024-12-10", "expense", 890.00, "Alimentação", "Mercado dezembro 2024"),
    ("2024-12-20", "expense", 470.00, "Presentes", "Presentes fim de ano 2024"),
    ("2025-01-15", "income", 2500.00, "Salário", "Salario extra janeiro 2025"),
    ("2025-01-19", "expense", 500.00, "Saúde", "Medicamentos janeiro 2025"),
    ("2025-03-08", "income", 2600.00, "Freelance", "Consultoria marco 2025"),
    ("2025-03-10", "expense", 980.00, "Moradia", "Aluguel marco 2025"),
    ("2025-05-19", "income", 2500.00, "Salário", "Salario maio 2025"),
    ("2025-05-22", "expense", 760.00, "Alimentação", "Supermercado maio 2025"),
    ("2025-06-19", "income", 2000.00, "Salário", "Salario junho 2025"),
    ("2025-06-20", "expense", 310.00, "Transporte", "Transporte junho 2025"),
    ("2025-08-14", "income", 5100.00, "Salário", "Salario agosto 2025"),
    ("2025-08-18", "expense", 1250.00, "Moradia", "Aluguel agosto 2025"),
    ("2025-10-09", "income", 1400.00, "Investimentos", "Rendimento outubro 2025"),
    ("2025-10-17", "expense", 180.00, "Lazer", "Saida outubro 2025"),
    ("2025-11-19", "expense", 250.98, "Saúde", "Consulta novembro 2025"),
    ("2025-12-05", "income", 5300.00, "Salário", "Salario dezembro 2025"),
    ("2025-12-11", "expense", 970.00, "Alimentação", "Mercado dezembro 2025"),
    ("2026-01-05", "income", 5600.00, "Salário", "Salario janeiro 2026"),
    ("2026-01-08", "expense", 1720.00, "Moradia", "Aluguel janeiro 2026"),
    ("2026-01-13", "expense", 845.00, "Alimentação", "Mercado janeiro 2026"),
    ("2026-01-20", "expense", 129.00, "Assinaturas", "Servicos recorrentes janeiro 2026"),
    ("2026-02-05", "income", 1900.00, "Freelance", "Projeto fevereiro 2026"),
    ("2026-02-10", "expense", 260.00, "Transporte", "Transporte fevereiro 2026"),
    ("2026-02-18", "expense", 210.00, "Saúde", "Exame fevereiro 2026"),
    ("2026-03-03", "income", 5600.00, "Salário", "Salario marco 2026"),
    ("2026-03-11", "expense", 1720.00, "Moradia", "Aluguel marco 2026"),
    ("2026-03-16", "expense", 310.00, "Lazer", "Cinema marco 2026"),
    ("2026-03-28", "expense", 760.00, "Alimentação", "Mercado marco 2026"),
    ("2026-04-10", "income", 850.00, "Freelance", "Landing page abril 2026"),
    ("2026-04-22", "expense", 39.00, "Assinaturas", "Ferramenta abril 2026"),
    ("2026-05-06", "income", 5650.00, "Salário", "Salario maio 2026"),
    ("2026-05-12", "expense", 1750.00, "Moradia", "Aluguel maio 2026"),
    ("2026-05-18", "expense", 320.00, "Educacao", "Curso maio 2026"),
    ("2026-05-25", "expense", 910.00, "Alimentação", "Mercado maio 2026"),
    ("2026-06-04", "income", 5700.00, "Salário", "Salario junho 2026"),
    ("2026-06-09", "income", 900.00, "Freelance", "Bico junho 2026"),
    ("2026-06-14", "expense", 2400.00, "Viagem", "Viagem junho 2026"),
    ("2026-06-19", "expense", 420.00, "Lazer", "Passeio junho 2026"),
    ("2026-06-27", "expense", 275.00, "Transporte", "Transporte junho 2026"),
]


def get_or_create_category(user, name, user_scoped=False):
    category = Category.query.filter_by(name=name).first()
    if category is None:
        user_id = user.id if user_scoped else None
        category = Category(name=name, user_id=user_id)
        db.session.add(category)
        db.session.flush()
    return category


def main():
    parser = argparse.ArgumentParser(description="Populate test transactions for a user.")
    parser.add_argument("email", nargs="?", default=DEFAULT_EMAIL, help="Target user email")
    args = parser.parse_args()

    with app.app_context():
        user = User.query.filter_by(email=args.email).first()
        if user is None:
            raise SystemExit(f"Usuario {args.email} nao encontrado.")

        category_cache = {}
        for name, user_scoped in SEED_CATEGORIES:
            category_cache[(name, user_scoped)] = get_or_create_category(user, name, user_scoped=user_scoped)

        added = 0
        skipped = 0

        for raw_date, tx_type, amount, category_name, description in SEED_TRANSACTIONS:
            tx_date = date.fromisoformat(raw_date)
            category = category_cache.get((category_name, True))
            if category is None:
                category = category_cache.get((category_name, False))
            if category is None:
                category = get_or_create_category(user, category_name, user_scoped=True)
                category_cache[(category_name, True)] = category

            existing = Transaction.query.filter_by(
                user_id=user.id,
                category_id=category.id,
                type=tx_type,
                amount=amount,
                date=tx_date,
                description=description,
            ).first()

            if existing is not None:
                skipped += 1
                continue

            db.session.add(
                Transaction(
                    user_id=user.id,
                    category_id=category.id,
                    type=tx_type,
                    amount=amount,
                    date=tx_date,
                    description=description,
                )
            )
            added += 1

        db.session.commit()

        print(f"Usuario: {user.email} (id={user.id})")
        print(f"Categorias garantidas: {len(SEED_CATEGORIES)}")
        print(f"Transacoes adicionadas: {added}")
        print(f"Transacoes ja existentes e ignoradas: {skipped}")


if __name__ == "__main__":
    main()