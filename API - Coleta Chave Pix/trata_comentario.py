import re
import json
import emoji
from trata_email import TrataEmail
from trata_chave_aleatoria import TrataChaveAleatoria
from trata_cpf import TrataCpf
from trata_celular import TrataCelular

class TrataComentario:

    qtd_comentarios = 0
    qtd_cpf = 0
    qtd_chave_aleatoria = 0
    qtd_email = 0
    qtd_celular = 0

    def __init__(self, link, chave):
        self.link = link
        self.chave = chave

    def coleta_comentario(self):
        lista_comentarios = []
        
        for dado in self.link:
            comentario_coletado = dado.get(self.chave)
            if comentario_coletado:
                lista_comentarios.append(comentario_coletado)
        
        self.qtd_comentarios = len(lista_comentarios)

        return lista_comentarios

    def verifica_email(self, comentario):
        email_localizado = TrataEmail(comentario)
        email_limpo = email_localizado.localiza_posicao_email()
        email_limpo = email_localizado.limpa_email(email_limpo)
        situacao = email_localizado.valida_email(email_limpo)

        return situacao

    def verifica_chave_aleatoria(self, comentario):
        chave_aleatoria_localizada = TrataChaveAleatoria(comentario)
        chave_aleatoria_limpa = chave_aleatoria_localizada.localiza_posicao_chave_aleatoria()
        chave_aleatoria_limpa = chave_aleatoria_localizada.limpa_chave_aleatoria(chave_aleatoria_limpa)
        situacao = chave_aleatoria_localizada.valida_chave_aleatoria(chave_aleatoria_limpa)

        return situacao

    def verifica_chave_cpf(self, comentario):
        possivel_cpf_localizado = TrataCpf(comentario)
        situacao = possivel_cpf_localizado.valida_cpf(comentario)
        
        return situacao

    def verifica_chave_celular(self, comentario):
        possivel_celular_localizado = TrataCelular(comentario)
        situacao = possivel_celular_localizado.valida_celular(comentario)

        return situacao

    def verifica_consecutividade(self, comentario, numero_detectado):
        posicao_elementos = []
        numero_formatado = ''
        maior_valor = ''
        
        for pos, texto in enumerate(comentario):
            for num in numero_detectado:
                if num in texto:
                    posicao_elementos.append(pos)
        
        tamanho_lista = len(posicao_elementos)
        lista_comparacao = [posicao_elementos[0]]
        
        for indice in range(0, tamanho_lista-1):
            lista_comparacao.append(lista_comparacao[indice] + 1)

        
        for n in posicao_elementos:
            if len(comentario[n]) > len(maior_valor):
                maior_valor = comentario[n]
            else:
                maior_valor = maior_valor

        if lista_comparacao == posicao_elementos:
            numeros_unidos = ''.join(re.findall(r'[\d]+', str(numero_detectado)))  
            maior_formatado = ''.join(re.findall(r'[\d]+', str(maior_valor)))
            tamanho_maior = len(maior_formatado)
            tamanho_numeros_unidos = len(numeros_unidos)

            if tamanho_maior == 12 and maior_valor[0] == '0':
                numero_formatado = maior_valor
            elif tamanho_maior == 11:
                numero_formatado = maior_valor
            elif tamanho_maior == 9:
                numero_formatado = numeros_unidos
            elif tamanho_maior == 8  and tamanho_numeros_unidos == 11 or tamanho_numeros_unidos == 12:
                numero_formatado = numeros_unidos
            else:
                numero_formatado = -1  
        else:
            numero_formatado = maior_valor
    
        return numero_formatado
        
    def analisa_chave_celular_ou_cpf(self, comentario):
        possivel_chave_coletada = '-1'
        valido = ''
        tipo = ''

        comentario = emoji.replace_emoji(comentario, replace='')
        comentario_separado = comentario.replace('\n', ' ').split(' ')
        numeros_identificados = re.findall(r'[\d\-\.]+', comentario)
        tamanho_numero_capturado = len(numeros_identificados)

        if tamanho_numero_capturado == 1 and len(numeros_identificados[0]) >= 11:
            regex_cpf = r"^[0-9]{3}\.[0-9]{3}\.[0-9]{3}-[0-9]{2}$"
            regex_celular = r"^[0-9]{2}[9]{1}[0-9]{4}-[0-9]{4}$"
            numeros_identificados = numeros_identificados[0]

            if re.findall(regex_cpf, numeros_identificados):
                possivel_chave_coletada = numeros_identificados
                valido = self.verifica_chave_cpf(numeros_identificados)
                tipo = 'Cpf'
            elif re.findall(regex_celular, numeros_identificados):
                possivel_chave_coletada = numeros_identificados
                valido = self.verifica_chave_celular(numeros_identificados)
                tipo = 'celular'
            else:
                formata_numero = r"\d+"

                numeros_identificados_formatados = re.findall(formata_numero, numeros_identificados)
                numeros_identificados_formatados = "".join(numeros_identificados_formatados)
                
                valido = self.verifica_chave_cpf(numeros_identificados_formatados)        

                if valido == 'Valido':
                    possivel_chave_coletada = numeros_identificados_formatados[:3] +'.'+ numeros_identificados_formatados[3:6] + '.' + numeros_identificados_formatados[6:9] + '-' + numeros_identificados_formatados[9:11]
                    tipo = 'Cpf'
                else:
                    valido = self.verifica_chave_celular(numeros_identificados_formatados)
                    if valido == 'Valido':
                        possivel_chave_coletada = '(' + numeros_identificados_formatados[:-9] + ') ' + numeros_identificados_formatados[-9:-4] + '-' + numeros_identificados_formatados[-4:]
                        tipo = 'celular'
        else:
            if len(numeros_identificados[0]) >= 11:
                numeros_identificados = self.verifica_consecutividade(comentario_separado, numeros_identificados)
                numeros_identificados_formatados = re.findall(r'\d+', numeros_identificados)
                numeros_identificados_formatados = "".join(numeros_identificados_formatados)
                
                valido = self.verifica_chave_cpf(numeros_identificados_formatados)

                if valido == 'Valido':
                    possivel_chave_coletada = numeros_identificados_formatados[:3] +'.'+ numeros_identificados_formatados[3:6] + '.' + numeros_identificados_formatados[6:9] + '-' + numeros_identificados_formatados[9:11]
                    tipo = 'Cpf'
                else:
                    valido = self.verifica_chave_celular(numeros_identificados_formatados)
                    if valido == 'Valido':
                        possivel_chave_coletada = '(' + numeros_identificados_formatados[:-9] + ') ' + numeros_identificados_formatados[-9:-4] + '-' + numeros_identificados_formatados[-4:]
                        tipo = 'celular'
            
        return possivel_chave_coletada, valido, tipo

    def filtra_comentario(self, lista_comentarios):
        nome = 'chaves'
        dict_chave_coletada = {}
        dict_chave_coletada[nome] = []
        situacao = ''

        for comentario in lista_comentarios:
            
            if '@' in comentario: 
                situacao = self.verifica_email(comentario)
                dict_chave_coletada['chaves'].append({'tipo':'e-mail', 'situacao':situacao})
            elif str(comentario).count('-') == 4:
                situacao = self.verifica_chave_aleatoria(comentario)
                dict_chave_coletada['chaves'].append({'tipo':'chave aleatoria', 'situacao':situacao})
            elif re.search(r'\d+', comentario):
                chave_desconhecida, situacao, tipo = self.analisa_chave_celular_ou_cpf(comentario)
             
                if chave_desconhecida != '-1':
                    dict_chave_coletada['chaves'].append({'tipo':tipo, 'situacao':situacao})
            else:
                pass
            
        return dict_chave_coletada

    def contabiliza_chave(self, dicionario):
        dicionario_coletado = dicionario['chaves']
        for item in dicionario_coletado:
            if item['situacao'] == 'Valido':
                if item['tipo'] == 'e-mail':
                    self.qtd_email += 1
                elif item['tipo'] == 'Cpf':
                    self.qtd_cpf += 1
                elif item['tipo'] == 'celular':
                    self.qtd_celular += 1
                elif item['tipo'] == 'chave aleatoria':
                    self.qtd_chave_aleatoria += 1
                else:
                    pass
        
        return {'Comentarios coletados':self.qtd_comentarios,
                'CPF': self.qtd_cpf,
                'E-mail': self.qtd_email,
                'Celular': self.qtd_celular,
                'Chave aleatoria': self.qtd_chave_aleatoria}





    