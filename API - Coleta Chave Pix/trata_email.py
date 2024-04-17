import emoji

class TrataEmail:
    def __init__(self, email):
        self.email = str(email).replace('\n', '')

    def valida_email(self, email):
        dominios = ['gmail', 'hotmail', 'outlook', 'yahoo']
        situacao = ''

        for dominio in dominios:
            if dominio in email:
                if '.com.br' in email or '.com' in email:
                    situacao = 'Valido'
                    break
                else:
                    situacao = 'Invalido'
                    break
            else:
                situacao = 'Invalido'
        
        return situacao

    def limpa_email(self, email):
        email_sem_emoji = emoji.replace_emoji(email, replace='')
        email_formatado = ''
        posicao_palavra = 0

        if '.com.br' in email_sem_emoji:
            posicao_palavra = email_sem_emoji.find('.com.br') + len('.com.br')
        elif '.com' in email_sem_emoji and not '.br' in email_sem_emoji:
            posicao_palavra = email_sem_emoji.find('.com') + len('.com')

        palavra_posterior = email_sem_emoji[posicao_palavra:]
        email_formatado = email_sem_emoji.replace(palavra_posterior, '')

        if ':' in email_formatado:
            posicao_dois_pontos = email_formatado.find(':') + 1
            email_formatado = email_formatado[posicao_dois_pontos:]

        return email_formatado

    def localiza_posicao_email(self):
        chave_separada = str(self.email).split(' ')
        posicao_email = 0

        for pos, palavra in enumerate(chave_separada):
            if '@' in palavra:
                posicao_email = pos

        email_localizado = chave_separada[posicao_email]

        return email_localizado
        
        