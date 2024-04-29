from client.exceptions import CannotReadAccessToken


def set_access_token(token: str):
    with open("token.txt", "w") as file:
        file.write(token)


def get_access_token():
    try:
        with open("token.txt") as file:
            return file.read()
    except IOError as e:
        raise CannotReadAccessToken from e
