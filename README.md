# POS-testes

#Dupla: Flavia e Ester

## Rotas Públicas
- POST /auth/login
- POST /auth/refresh
- POST /users
- GET /messages

## Rotas Protegidas com JWT
- GET/PUT/DELETE /users/{id}
- POST/PUT/DELETE /comments
- DELETE /messages

## Perfis:
- ADMIN: pode tudo
- USER: só modifica seus próprios dados e mensagens