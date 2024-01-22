# resp_parser.py

class RespParser:
    @staticmethod
    def parse_command(data):
        # Verifica se o primeiro caractere indica o tipo de dado
        if data[0] == b'*':
            return RespParser._parse_array(data[1:])
        elif data[0] == b'$':
            return RespParser._parse_bulk_string(data[1:])
        else:
            raise ValueError("Comando RESP inválido")

    @staticmethod
    def _parse_array(data):
        # Extrai o número de elementos no array
        num_elements, rest_data = RespParser._parse_integer(data)
        elements = []

        # Itera sobre os elementos do array
        for _ in range(num_elements):
            element, rest_data = RespParser.parse_command(rest_data)
            elements.append(element)

        return elements, rest_data

    @staticmethod
    def _parse_bulk_string(data):
        # Extrai o comprimento da string a ser lida
        length, rest_data = RespParser._parse_integer(data)

        # Se o comprimento for -1, representa um valor nulo
        if length == -1:
            return None, rest_data

        # Lê a string do restante dos dados
        bulk_string = rest_data[:length]
        return bulk_string.decode('utf-8'), rest_data[length:]

    @staticmethod
    def _parse_integer(data):
        # Encontra o índice do caractere de quebra de linha
        crlf_index = data.index(b'\r\n')

        # Extrai o valor do inteiro e o restante dos dados
        integer_value = int(data[:crlf_index])
        rest_data = data[crlf_index + 2:]

        return integer_value, rest_data
