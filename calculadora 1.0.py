import curses
import sys

def menu_principal(stdscr):
    curses.curs_set(1)

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

    stdscr.refresh()

    num1, op, num2 = ler_operandos_decimal(quantidade_bits, stdscr)

    bin1, bin2 = converter_em_binário(num1, num2, quantidade_bits)

    try:
        if op == "+":
            resultado = somar(bin1, bin2)
        elif op == "-":
            bin2_negado = somar(inverter_bits(bin2), '0' * (quantidade_bits - 1) + '1')
            resultado = somar(bin1, bin2_negado)
        elif op == "*":
            resultado = multiplicar(bin1, bin2)
        elif op == "/":
            resultado = dividir(bin1, bin2)
        else:
            raise ValueError

        mostrar_resultado(bin1, bin2, resultado[-quantidade_bits:], stdscr)

    except ValueError:
        erro = 'Entrada inválida'
        mostrar_erro(erro, stdscr)

def mostrar_erro(erro, stdscr, linha=0):
    limpar_tela(stdscr)
    stdscr.addstr(linha-1, 0, f"Erro: {erro}")
    stdscr.refresh()

def limpar_tela(stdscr):
    stdscr.clear()
    stdscr.refresh()

def escolher_bits(stdscr):
    linha = 2
    stdscr.addstr(linha, 3, "8, 16, 32:")
    curses.echo()
    bits = stdscr.getstr(linha, len('8, 16, 32: ')+2, 2).decode("utf-8")

    match bits:
        case '8': quantidade_bits = 8
        case '16': quantidade_bits = 16
        case '32': quantidade_bits = 32
        case _: 
            erro = 'Escolha uma quantidade de bits válida (8, 16 ou 32):'
            mostrar_erro(erro, stdscr, linha)
            return escolher_bits(stdscr)

    return quantidade_bits

def sinal_magnitude_para_complemento2(binario):
    if binario[0] == '0':
        return binario
    invertido = inverter_bits(binario)
    return somar(invertido, '0' * (len(binario) - 1) + '1')

def inverter_bits(binario):
    return ''.join('1' if b == '0' else '0' for b in binario)

def ler_operandos_decimal(quantidade_bits, stdscr):
    linha = 6
    stdscr.addstr(0, 0, "*--**--Calculadora Binária--**--*")

    limite_inferior = -(2 ** (quantidade_bits - 1))
    limite_superior = (2 ** (quantidade_bits - 1)) - 1

    try:
        stdscr.addstr(linha, 2, f"Digite o primeiro número entre {limite_inferior} e {limite_superior}: ")
        curses.echo()
        num1 = int(stdscr.getstr(linha, len(f"Digite o primeiro número entre {limite_inferior} e {limite_superior}: ") + 2, 20).decode("utf-8"))
        if not (limite_inferior <= num1 <= limite_superior): raise ValueError

        stdscr.addstr(linha + 1, 2, "Digite o operador (+, -, *, /): ")
        op = stdscr.getstr(linha + 1, len("Digite o operador (+, -, *, /): ") + 2, 1).decode("utf-8")

        stdscr.addstr(linha + 2, 2, f"Digite o segundo número entre {limite_inferior} e {limite_superior}: ")
        num2 = int(stdscr.getstr(linha + 2, len(f"Digite o segundo número entre {limite_inferior} e {limite_superior}: ") + 2, 20).decode("utf-8"))
        if not (limite_inferior <= num2 <= limite_superior): raise ValueError

    except ValueError:
        erro = 'Valor fora do intervalo ou inválido, tente novamente:'
        mostrar_erro(erro, stdscr, linha)
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
    curses.endwin()
    sys.exit(0)

def pressione_tecla(stdscr):
    stdscr.addstr(5, 0, "Pressione a tecla Enter para calcular ou ESC para sair.")
    stdscr.refresh()

    tecla = stdscr.getch()

    try:
        if tecla == 13:
            limpar_tela(stdscr)
            menu_principal(stdscr)
        elif tecla == 27:
            finalizar(stdscr)
        else:
            raise ValueError
    except ValueError:
        erro = 'Tecla inválida'
        mostrar_erro(erro, stdscr)

def somar(smag1, smag2):
    resultado = ''
    carry = 0
    for i in range(len(smag1) - 1, -1, -1):
        total = carry
        total += smag1[i] == '1'
        total += smag2[i] == '1'
        resultado = ('1' if total % 2 else '0') + resultado
        carry = 1 if total > 1 else 0
    return resultado[-len(smag1):]

def subtrair(*args, **kwargs):
    pass

def multiplicar(*args, **kwargs):
    return '0' * len(args[0])

def dividir(*args, **kwargs):
    return '0' * len(args[0])

def mostrar_resultado(bin1, bin2, resultado, stdscr):
    limpar_tela(stdscr)
    stdscr.addstr(8, 0, f"Primeiro número em binário: {bin1}")
    stdscr.addstr(9, 0, f"Segundo número em binário:  {bin2}")
    stdscr.addstr(10, 0, f"Resultado em binário:      {resultado}")
    stdscr.refresh()
    pressione_tecla(stdscr)

if __name__ == "__main__":
    try:
        curses.wrapper(menu_principal)
    except Exception as e:
        print("Erro ao iniciar a interface curses:", e)
        sys.exit(1)
