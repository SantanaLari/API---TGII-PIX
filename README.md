
API - Coleta Chave Pix

# Aviso
Essa API está em fase de desenvolvimento. Posteriormente algumas funções são corrigidas.

## Principal Funcionalidade
Essa API tem como objetivo simular a filtragem e contabilização de chaves Pix encontradas em um arquivo JSON. 

## Exemplo de uso
- Enviar um arquivo .json:
    - Endpoint: http://127.0.0.1:8000/ 
    - Somente envie arquivos json, qualquer outro tipo de arquivo não dará certo.

- Confirmar a validação do arquivo:
    - Endpoint: http://127.0.0.1:8000/upload_arquivo/ 
    - Você será direcionado para essa página após o envio do arquivo. Nela você confirmará se o arquivo foi aceito.

- Exibir a contagem das chaves Pix:
    - http://127.0.0.1:8000/exibe_contagem/{chave_json}
    - Substitua {chave_json} pela chave correta presente no seu arquivo json. Exemplo:
[
    {
        "nome": "Fulano",
        "contato": "1191234-1234",
        "data_nasc": "22/06/1945"
    }
]
Nesse exemplo, a chave correta seria "contato", porque o valor associado a ela é uma possível chave Pix. 
