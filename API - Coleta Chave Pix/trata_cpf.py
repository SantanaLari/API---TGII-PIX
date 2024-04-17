import re

class TrataCpf:
    def __init__(self, cpf):
        self.cpf = cpf
    
    def valida_cpf(self, cpf):
        base, digitos_verificadores = self.formata_cpf(cpf)
        digito = ''
        cont = 10
        resultado = 0
        for n in base:
            if cont == 1:
                break
            num_convertido = int(n)
            resultado += (num_convertido*cont)
            cont -= 1
        
        resto = resultado % 11
        if resto == 0 or resto == 1:
            digito += '0'
        else:
            res_digito = 11 - resto
            digito += str(res_digito)

        cont = 10
        resultado = 0

        cpf_alterado = base[1:] + digito
        for n in cpf_alterado:
            if cont == 1:
                break
            num_convertido = int(n)
            resultado += (num_convertido*cont)
            cont -= 1

        resto = resultado % 11
        if resto == 0 or resto == 1:
            digito += '0'
        else:
            res_digito = 11 - resto
            digito += str(res_digito)

        if digito == digitos_verificadores:
            return 'Valido'
        else:
            return 'Invalido'

    def formata_cpf(self, cpf):
        tam_cpf = len(cpf)
        base_cpf = ''
        digitos_verificadores = ''

        if tam_cpf == 14:
            digitos_verificadores = cpf[-2:]
            if '.' in cpf:
                base_cpf = str(cpf).replace(".", "")
            else:
                base_cpf = str(cpf).replace("-", "")
            base_cpf = base_cpf[0:9]
        elif tam_cpf == 12 or tam_cpf == 11:
            digitos_verificadores = cpf[-2:]
            base_cpf = cpf[0:9]
        else:
            pass
        
        return base_cpf, digitos_verificadores
