import argparse


def ler_header_ppm(f):
    tipo = f.readline().strip()
    if tipo != b'P6':
        raise ValueError("Formato não suportado. Esperado PPM P6.")

    linha = f.readline().strip()
    while linha.startswith(b'#'):
        linha = f.readline().strip()

    largura, altura = map(int, linha.split())

    linha = f.readline().strip()
    while linha.startswith(b'#'):
        linha = f.readline().strip()

    valor_maximo = int(linha)
    if valor_maximo != 255:
        raise ValueError("Somente PPM com max=255 suportado.")

    offset_dados = f.tell()
    return largura, altura, valor_maximo, offset_dados, tipo


def dividir_ppm(arquivo_entrada, num_partes):
    with open(arquivo_entrada, "rb") as f:
        largura, altura, valor_maximo, offset_dados, tipo = ler_header_ppm(f)

        print(f"Imagem: {largura}x{altura}")
        print(f"Dividindo em {num_partes} partes...\n")

        linhas_base = altura // num_partes
        resto = altura % num_partes

        partes_info = []

        f.seek(offset_dados)

        for i in range(num_partes):
            linhas = linhas_base + (1 if i < resto else 0)

            nome_arquivo = f"parte_{i}.ppm"
            partes_info.append((nome_arquivo, linhas))

            with open(nome_arquivo, "wb") as out:
                # escrever header
                out.write(tipo + b"\n")
                out.write(f"{largura} {linhas}\n".encode())
                out.write(f"{valor_maximo}\n".encode())

                # copiar dados linha por linha
                for _ in range(linhas):
                    linha_bytes = f.read(largura * 3)
                    out.write(linha_bytes)

            print(f"✅ Criado: {nome_arquivo} ({linhas} linhas)")

    print("\n🎉 Divisão concluída!")
    return partes_info


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dividir imagem PPM em partes")

    parser.add_argument("arquivo_entrada", help="Arquivo PPM de entrada")
    parser.add_argument("partes", type=int, help="Número de partes: 2, 4, 8 ou 12")

    args = parser.parse_args()

    if args.partes not in [2, 4, 8, 12]:
        print("⚠️ Use apenas: 2, 4, 8 ou 12 partes")
        exit()

    dividir_ppm(args.arquivo_entrada, args.partes)