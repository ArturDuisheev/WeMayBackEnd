### Документация к авторизации/регистрации
***
Из-за того что **токены**  из `rest_framework_simple_jwt` конфликтуют с токенами из библиотеки `drf-social-oauth`, на **back-end**'e используются вторые. Работа с ними в том числе со стороны **front-end**'а отличается от токенов из первой библиотеки, поэтому была создана данная документация. 

*Примечание:* В **request**'ах, практически везде используется `client_id` и `client_secret`. Это специальные поля приложения (таблица **application** в *admin'ке* `django`), создаваемого в *БД*.

***
#### Как получить поля `client_id` и `client_secret`:
1. Добавляем в админ-панели `django` новое приложение в таблице **application**.
2. При добавлении приложения `client_id` и `client_secret` генерируются автоматически, при этом требуется **сразу же** скопировать `client_secret`, так как позже его значение *зашифруется* и уже не будет подходить для последующих операций. Значение поля `client_id` можно скопировать позже, он не изменяется.
3. Дальше необходимо выбрать `client_type` (выбираем пункт *confidential*) и 'authorization_grand_type' (выбираем пункт *Resource owner password-based*).
4. Также следует назначить `user'а` для данного приложения, желательно `admin'а` и 
`redirect_urls` (Можно добавить несколько путей, разделенных пробелом).   
5. Поле `algorithm` не следует трогать, поле `name` является опциональным.
***
#### Регистрация

**Request:**
``` json
{
    "client_id": "osjlnnJR2wR2jfsfr1yYg8S5aGemCYN5UyrfZRVX",
    "client_secret":"wUeCX5yDN95qxsFx0jh3A8esNncx0M1znevUOsok3riQDtPXOpOtJtpAqkaDJ6R68g3ekVHd1qJwlo8iCF4hysUGET7mqWrjcXA94ln7EKmL3vEavGkCeoUqhIWZAfpy",
    "grant_type": "password",
    "email": "<your email>",
    "password": "<your password"
}
```
**End-Point**

#### [https://{domain-name}/api/v1/users/register/]()


**Response**
``` json
{
    "access_token": "XWrwl6B5aVTKXUi6GeSx8SSE4ZTRfw",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "V649fDhvaG7f52nBb9jwtl49QrBxSM"
}
```
**Access** токен имеет тип **Bearer** 
***

#### Логин

**Request:**

*Примечание*: В качестве `username` необходимо использовать `email` 
``` json
{
    "client_id": "osjlnnJR2wR2jfsfr1yYg8S5aGemCYN5UyrfZRVX",
    "client_secret":"wUeCX5yDN95qxsFx0jh3A8esNncx0M1znevUOsok3riQDtPXOpOtJtpAqkaDJ6R68g3ekVHd1qJwlo8iCF4hysUGET7mqWrjcXA94ln7EKmL3vEavGkCeoUqhIWZAfpy",
    "grant_type": "password",
    "username": "<your email>",
    "password": "<your password"
}
```
**End-Point**

#### [https://{domain-name}/api/v1/oauth/token/]()


**Response**
``` json
{
    "access_token": "XWrwl6B5aVTKXUi6GeSx8SSE4ZTRfw",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "V649fDhvaG7f52nBb9jwtl49QrBxSM"
}
```
**Access** токен имеет тип **Bearer** 
***

#### Логаут

**Request:**

``` json
{
    "token": "OyGusmeIjYkkoej8p0r0Pw08DWMcBS", 
    "client_id": "osjlnnJR2wR2jfsfr1yYg8S5aGemCYN5UyrfZRVX",
    "client_secret":"wUeCX5yDN95qxsFx0jh3A8esNncx0M1znevUOsok3riQDtPXOpOtJtpAqkaDJ6R68g3ekVHd1qJwlo8iCF4hysUGET7mqWrjcXA94ln7EKmL3vEavGkCeoUqhIWZAfpy"
}
```

*Примечание:* В поле `token` можно передавать как `access_token` так и `refresh_token`

**End-Point**

#### [https://{domain-name}/api/v1/oauth/revoke-token/]()


**Response**
``` json
""
```
*No Content*
***

#### oAuth Facebook

**Request:**

``` json
{
    "token": "EAAagtl0iQcoBO02hZBNTZCxYjultZAclv8p5HKUTK4OqZAZBfW7vLgU8ouspI4FJmsA3a703zbOaNSyddF94czgoNu6t96SKIMtWdY8aO5ZCGmIXJTNGhiPvu5eGFZCUjPCZBTMUQNzylLZAhf6LJ4NvVYDPel0By4zVOY0D0yp7nN3YgdxDlZCzcAIZB6ZCDAuRQH5FIwZDZD",
    "backend": "facebook",
    "grant_type": "convert_token",
    "client_id": "osjlnnJR2wR2jfsfr1yYg8S5aGemCYN5UyrfZRVX",
    "client_secret":"wUeCX5yDN95qxsFx0jh3A8esNncx0M1znevUOsok3riQDtPXOpOtJtpAqkaDJ6R68g3ekVHd1qJwlo8iCF4hysUGET7mqWrjcXA94ln7EKmL3vEavGkCeoUqhIWZAfpy"
}
```

*Примечание:* В поле `token` можно необходимо передать токен, полученный от приложения **Facebook**.

**End-Point**

#### [https://{domain-name}/api/v1/oauth/convert-token/]()


**Response**
``` json
{
    "access_token": "1rfU9lAfOHSH1CuI2qIDlHA57swUAC",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "FFCZYryOddKQ9Xc8E056COxpYOSFBl"
}
```
***
#### oAuth Google 

``` json
{
    "token": "ya29.a0AfB_byDBWT7rOK5wmdDfX9XYTSzuupj5C9uY5aUmONA9dACreQsTggagA5zxa-XiLYThO-Kx5LhApqo7srxR4egcP-QpFAyc7OnFWFSWKNCbUkQyknYZJG0wIeekOgvIS9gGpFiT-LMEPd0WrcFz7QUozWX95Y5pUG2IaCgYKAfsSARISFQHGX2MiNX9DRXCWZQ4rLgxLPJ0H_A0171",
    "backend": "google-oauth2",
    "grant_type": "convert_token",
    "client_id": "osjlnnJR2wR2jfsfr1yYg8S5aGemCYN5UyrfZRVX",
    "client_secret":"wUeCX5yDN95qxsFx0jh3A8esNncx0M1znevUOsok3riQDtPXOpOtJtpAqkaDJ6R68g3ekVHd1qJwlo8iCF4hysUGET7mqWrjcXA94ln7EKmL3vEavGkCeoUqhIWZAfpy"
}
```

*Примечание:* В поле `token` можно необходимо передать токен, полученный от приложения **Google**.

**End-Point**

#### [https://{domain-name}/api/v1/oauth/convert-token/]()

**Response**
``` json
{
    "access_token": "1rfU9lAfOHSH1CuI2qIDlHA57swUAC",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "FFCZYryOddKQ9Xc8E056COxpYOSFBl"
}
```
***
