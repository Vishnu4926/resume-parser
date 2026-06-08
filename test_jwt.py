from auth.jwt_handler import create_access_token

token = create_access_token(
    {
        "sub": "vishnu@gmail.com"
    }
)

print(token)
