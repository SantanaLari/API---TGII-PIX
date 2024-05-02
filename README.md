API - Coleta Chave Pix

## Link Para Acessar a API
https://api-pix-7t33.onrender.com/

## Principal Funcionalidade
Essa API tem como objetivo simular a filtragem e contabilização de chaves Pix encontradas em um arquivo JSON. 

## Exemplo de uso
|Endpoint|Tipo|Funcionalidade|
|:-------|:---|:-------------:|
|/|GET|Exibe uma tela que permite o envio de um arquivo json.|
|/upload_arquivo/|POST|Retorna um aviso sobre o arquivo json que foi enviado.|
|/exibe_contagem/{chave_json}|GET|Retorna a quantidade de chaves Pix identificadas no arquivo JSON correspondente à {chave_json} especificada na URL. A {chave_json} deve ser o nome de uma chave que tem como valor uma possível chave Pix."|


