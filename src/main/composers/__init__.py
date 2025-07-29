"""
Composers
=========

Este módulo contém funções composer para cada endpoint da aplicação. Um composer é responsável por montar a cadeia de dependências (Controller, UseCase, Repository, etc.) de cada caso de uso, retornando um handler pronto para ser utilizado nas rotas HTTP.

Cada função composer:
- Instancia o repositório e o use case necessários
- Injeta as dependências corretas
- Retorna o método handle do controller, que recebe um HttpRequest e retorna um HttpResponse

Exemplo de uso:
    from src.main.composers.create_fiscal_composer import create_fiscal_composer
    handler = create_fiscal_composer()
    response = handler(HttpRequest(...))

Documentação individual de cada composer está presente em seus respectivos arquivos.
"""