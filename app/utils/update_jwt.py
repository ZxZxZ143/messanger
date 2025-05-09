from flask_jwt_extended import set_refresh_cookies, set_access_cookies, create_access_token, create_refresh_token, \
    get_jwt_identity, get_jwt


def set_jwt_cookies(res):
    # Генерация access и refresh токенов
    access_token = create_access_token(identity=get_jwt_identity(), additional_claims={"id": get_jwt().get("id")})
    refresh_token = create_refresh_token(identity=get_jwt_identity(), additional_claims={"id": get_jwt().get("id")})

    # Установка токенов в cookies
    set_access_cookies(res, access_token)
    set_refresh_cookies(res, refresh_token)
    return res