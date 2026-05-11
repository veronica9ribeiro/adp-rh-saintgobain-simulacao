from src.workers.buscar   import buscar_todos, buscar_por_matricula
from src.workers.exportar import para_excel


def main():
    print("=== Sync ADP → RH Saint-Gobain ===\n")

    print("Buscando funcionários...")
    df = buscar_todos()
    print(f"Total: {len(df)} registros\n")

    print("Exportando para Excel...")
    para_excel(df, "funcionarios")

    print("\nBuscando funcionário 00001...")
    worker = buscar_por_matricula("00001")
    if worker:
        nome = worker["person"]["legalName"]["formattedName"]
        print(f"Encontrado: {nome}")
    else:
        print("Funcionário não encontrado.")

    print("\nConcluído.")


if __name__ == "__main__":
    main()
