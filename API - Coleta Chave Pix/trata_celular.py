import re

class TrataCelular:
    def __init__(self, celular):
        self.celular = celular

    def valida_celular(self, celular):
        celular_formatado = self.formata_celular(celular)
        situacao = 'Invalido'
        ddd_valido = ['11', '12', '13', '14', '15', '16', '17', '18', '19', '21', '22', '24', '27', '28', '31', '32', '33', '34', '35', '37', '38', '41', '42', '42', '43', '44', '45', '46', '47', '48', '49', '49', '51', '53', '54', '55', '61', '62', '63', '64', '65', '66', '67', '68', '69', '71', '73', '74', '75', '77', '79', '81', '82', '83', '84', '85', '86', '87', '88', '89', '91', '92', '93', '94', '95', '96', '97', '98', '99']

        if len(celular_formatado) >= 11:
            nono_digito = celular_formatado[-9]
            ddd_detectado = celular_formatado[-11:-9]

            if nono_digito == '9':
                for ddd in ddd_valido:
                    if ddd == ddd_detectado:
                        situacao = 'Valido'
                        break

        return situacao

    def formata_celular(self, celular):
        formata_numero = r"\d+"

        numero_formatado = re.findall(formata_numero, celular)
        numero_formatado = "".join(numero_formatado)
        
        return numero_formatado