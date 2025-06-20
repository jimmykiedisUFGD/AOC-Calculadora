import curses
import sys

def menu_principal(stdscr):
    curses.curs_set(1)

    # Exibe o menu principal usando curses e lê a escolha do usuário

    linha = 0
    stdscr.addstr(linha, 0, "*--**--Calculadora Binária--**--*")
 
    stdscr.addstr(linha+1, 2, "Escolha a quantidade de bits:")
    quantidade_bits = escolher_bits(stdscr)

    limpar_tela(stdscr)
    stdscr.addstr(linha+1, 2, "Operações disponíveis:")
    stdscr.addstr(linha+2, 3, "+ : Adição")
    stdscr.addstr(linha+3, 3, "- : Subtração")
    stdscr.addstr(linha+4, 3, "* : Multiplicação")
    stdscr.addstr(linha+5, 3, "/ : Divisão")

    # Ecreve o menu na tela
    stdscr.refresh()

    # Lê quais serão os operandos e qual será o operador
    num1, op, num2 = ler_operandos_decimal(quantidade_bits, stdscr)

    bin1, bin2 = converter_em_binário(num1, num2, quantidade_bits)

    smag1, smag2 = sinal_magnitude_para_complemento2(bin1), sinal_magnitude_para_complemento2(bin2)

    # Converte os números decimais para binários

    try:
        if op == "+":
            somar(bin1, bin2, smag1, smag2, stdscr)
        elif op == "-":
            subtrair(bin1, bin2, quantidade_bits, stdscr)
        elif op == "*":
            multiplicar(bin1, bin2, quantidade_bits, stdscr)
        elif op == "/":
            dividir(bin1, bin2, quantidade_bits, stdscr)
        else:
            raise ValueError  # Se for qualquer tecla inválida, levanta um erro manualmente

    except ValueError:
        erro = 'Entrada inválida'
        mostrar_erro(erro, stdscr)

def mostrar_erro(erro, linha, stdscr):
    limpar_tela(stdscr)
    stdscr.addstr(linha-1, 0, f"Erro: {erro}")
    stdscr.refresh()
    
    return

def limpar_tela(stdscr):

    # Limpa a tela e exibe o menu principal novamente
    stdscr.clear()
    stdscr.refresh()
    
    return
    
def escolher_bits(stdscr):

    linha = 2
    # Definindo se serão 8, 16, 32 bits
    stdscr.addstr(linha, 3, "8, 16, 32:")
    curses.echo()
    bits = stdscr.getstr(linha, len('8, 16, 32: ')+2, 2).decode("utf-8")
    
    match bits:
        case '8':
            quantidade_bits = 8
        case '16':
            quantidade_bits = 16
        case '32':
            quantidade_bits = 32
        case _:
            erro = 'Escolha uma quantidade de bits válida (8, 16 ou 32):'
            mostrar_erro(erro, linha, stdscr)
            return escolher_bits(stdscr)

    return quantidade_bits

def sinal_magnitude_para_complemento2(binario):
    if binario[0] == '0':
        return binario
    invertido = ''.join('1' if b == '0' else '0' for b in binario)
    return somar(invertido, '0' * (len(binario) - 1) + '1')

def ler_operandos_decimal(quantidade_bits, stdscr):
    linha = 6
    stdscr.addstr(0, 0, "*--**--Calculadora Binária--**--*")

    # Calcula os limites com sinal (complemento de dois)
    limite_inferior = -(2 ** (quantidade_bits - 1))
    limite_superior = (2 ** (quantidade_bits - 1)) - 1

    try:
        stdscr.addstr(linha, 2, f"Digite o primeiro número entre {limite_inferior} e {limite_superior}: ")
        curses.echo()
        num1 = int(stdscr.getstr(linha, len(f"Digite o primeiro número entre {limite_inferior} e {limite_superior}: ") + 2, 20).decode("utf-8"))
        if not (limite_inferior <= num1 <= limite_superior):
            raise ValueError

        stdscr.addstr(linha + 1, 2, "Digite o operador (+, -, *, /): ")
        op = stdscr.getstr(linha + 1, len("Digite o operador (+, -, *, /): ") + 2, 1).decode("utf-8")

        stdscr.addstr(linha + 2, 2, f"Digite o segundo número entre {limite_inferior} e {limite_superior}: ")
        num2 = int(stdscr.getstr(linha + 2, len(f"Digite o segundo número entre {limite_inferior} e {limite_superior}: ") + 2, 20).decode("utf-8"))
        if not (limite_inferior <= num2 <= limite_superior):
            raise ValueError

    except ValueError:
        erro = 'Valor fora do intervalo ou inválido, tente novamente:'
        mostrar_erro(erro, linha, stdscr)
        return ler_operandos_decimal(quantidade_bits, stdscr)

    return num1, op, num2

def converter_em_binário(num1, num2, quantidade_bits):
    def para_binario_complemento_dois(n, bits):
        if n >= 0:
            return format(n, f'0{bits}b')
        else:
            return format((1 << bits) + n, f'0{bits}b')

    bin1 = para_binario_complemento_dois(num1, quantidade_bits)
    bin2 = para_binario_complemento_dois(num2, quantidade_bits)

    return bin1, bin2

def finalizar(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, "Encerrando o programa... ")
    stdscr.refresh()

    curses.endwin()  # Encerra o modo curses (importante!)
    sys.exit(0)

def pressione_tecla(stdscr):
    stdscr.addstr(5, 0, "Pressione a tecla Enter para calcular ou ESC para sair.")
    stdscr.refresh()

    tecla = stdscr.getch()

    try:
        if tecla == 13:  # Enter
            limpar_tela(stdscr)
            menu_principal(stdscr)
        elif tecla == 27:  # ESC
            finalizar(stdscr)
        else:
            raise ValueError  # Se for qualquer tecla inválida, levanta um erro manualmente
    except ValueError:
        erro = 'Tecla inválida'
        mostrar_erro(erro, stdscr)

def somar(bin1, bin2, smag1, smag2, stdscr):
    resultado = ''
    carry = 0

    for i in range(len(smag1) - 1, -1, -1):
        total = carry
        total += smag1[i] == '1'
        total += smag2[i] == '1'
        resultado = ('1' if total % 2 else '0') + resultado
        carry = 1 if total > 1 else 0

    mostrar_resultado(bin1, bin2, resultado[-len(smag1):], stdscr)

def subtrair(bin1, bin2, quantidade_bits, stdscr):
    pass

def multiplicar(bin1, bin2, quantidade_bits, stdscr):
    pass

def dividir(bin1, bin2, quantidade_bits, stdscr):
    pass

def mostrar_resultado(bin1, bin2, resultado, stdscr):
    # Exibe o resultado na tela (binário + decimal)

    limpar_tela(stdscr)

    #aqui começamos a exibir a tela de resultador
    stdscr.addstr(8, 0, f"Primeiro número em binário: {bin1}")
    stdscr.addstr(9, 0, f"Segundo número em binário:  {bin2}")
    stdscr.addstr(10, 0, f"Resultado em binário:      {resultado}")
    stdscr.refresh()

    pressione_tecla(stdscr)

if __name__ == "__main__":
    curses.wrapper(menu_principal)
