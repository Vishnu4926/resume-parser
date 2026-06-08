from auth.security import (
    hash_password,
    verify_password
)

password = "vishnu123"

hashed = hash_password(password)

print(hashed)

print(
    verify_password(
        "vishnu123",
        hashed
    )
)
