import sys


class Parameters:
    def __init__(self, file_name):
        # Abrindo Arquivo .cvs do Altium
        self.altium_output_file = open(file_name, "r")
        pickPlace = self.altium_output_file.read()
        self.altium_output_file.close()

        # Verificar com o Desenvolvedor o tamanho da placa no eixo X
        x_size = float(input("informe o tamanho da placa em X\n"))

        # Removendo Cabecalho do Altium e Linha em Branco no Final
        pickPlace = pickPlace.split("\n")[13:-1]
        buffer = []

        # Removendo aspas
        for col in range(len(pickPlace)):
            pickPlace[col] = (pickPlace[col].split(',"'))
            for lin in range(len(pickPlace[col])):
                pickPlace[col][lin] = pickPlace[col][lin].replace('"', '')

            # Tratando informações do Bottom
            if pickPlace[col][-3] == "BottomLayer":
                pickPlace[col][2] = str("%.4f" % (x_size - float(pickPlace[col][2])))
                pickPlace[col][4] = str("%.4f" % (x_size - float(pickPlace[col][4])))
                pickPlace[col][6] = str("%.4f" % (x_size - float(pickPlace[col][6])))

            # Tratando a rotação
            pickPlace[col][-2] = str((int(pickPlace[col][-2]) - 90))

            # Removendo componentes N/M e TP's
            if pickPlace[col][-1] != "N/M" and pickPlace[col][-1] != "VALUE":
                buffer.append(pickPlace[col])

        outline = ""
        # Juntando as linhas em um único vetor
        for i in range(len(buffer)):
            buffer[i] = ",".join(buffer[i]) + "\n"

        # Ordenando
        buffer.sort()

        # Adicionando o cabeçalho
        buffer.insert(0, ",".join(['Designator', 'Footprint', 'Mid X', 'Mid Y', 'Ref X', 'Ref Y',
                                   'Pad X', 'Pad Y', 'Layer', 'Rotation', 'Comment']) + "\n")

        # Juntando as informações a serem gravadas em uma única variável
        for i in range(len(buffer)):
            outline += buffer[i]

        # Exportando as informações tratadas para um novo arquivo .csv
        output_file = open(self.altium_output_file.name.replace(".csv", "_m.csv"), "w")
        output_file.write(outline)
        output_file.close()


if sys.argv[1]:
    Converter = Parameters(sys.argv[1])
