from werkzeug.security import generate_password_hash
i = input("pwd:")
i_s = generate_password_hash(i)
print(i_s)