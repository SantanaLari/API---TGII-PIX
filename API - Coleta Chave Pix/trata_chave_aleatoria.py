import emoji
import re

class TrataChaveAleatoria:
    def __init__(self, chave_aleatoria):
        self.chave_aleatoria = str(chave_aleatoria)

    def valida_chave_aleatoria(self, chave_aleatoria):
        situacao = ''
        padrao =  re.compile(r"^[a-zA-Z0-9]{8}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{4}-[a-zA-Z0-9]{12}$")

        if padrao.match(chave_aleatoria) and len(chave_aleatoria) == 36:
            situacao = 'Valido'
        else:
            situacao = 'Invalido'

        return situacao

    def limpa_chave_aleatoria(self, chave_aleatoria):
        chave_aleatoria_sem_emoji = emoji.replace_emoji(chave_aleatoria, replace='')
        chave_aleatoria_formatada = chave_aleatoria_sem_emoji.replace('\n', '')
        
        if len(chave_aleatoria_formatada) > 36:
            primeira_ocorrencia = chave_aleatoria_formatada.find("-")
            ultima_ocorrencia = chave_aleatoria_formatada.rfind("-")
            qtd_primeira_parte = len(chave_aleatoria_formatada[:primeira_ocorrencia])
            qtd_ultima_parte = len(chave_aleatoria_formatada[ultima_ocorrencia:]) - 1
    
            if qtd_primeira_parte > 8 and qtd_ultima_parte == 12:
                tirar = qtd_primeira_parte - 8
                chave_aleatoria_formatada = chave_aleatoria_formatada[tirar:]
            elif qtd_ultima_parte > 12 and qtd_primeira_parte == 8:
                tirar = qtd_ultima_parte - 12
                chave_aleatoria_formatada = chave_aleatoria_formatada[:-tirar]  
            elif qtd_primeira_parte > 8 and qtd_ultima_parte > 12:
                tirar_primeira = qtd_primeira_parte - 8
                tirar_ultima = qtd_ultima_parte - 12
                chave_aleatoria_formatada = chave_aleatoria_formatada[tirar_primeira:]
                chave_aleatoria_formatada = chave_aleatoria_formatada[:-tirar_ultima]
                  
        return chave_aleatoria_formatada

    def localiza_posicao_chave_aleatoria(self):
        chave_separada = self.chave_aleatoria.split(' ')
        posicao_chave_aleatoria = 0

        for pos, palavra in enumerate(chave_separada):
            if '-' in palavra:
                posicao_chave_aleatoria = pos
        
        chave_aleatoria_localizada = chave_separada[posicao_chave_aleatoria]

        return chave_aleatoria_localizada