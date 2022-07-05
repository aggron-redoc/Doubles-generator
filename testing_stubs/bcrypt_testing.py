import bcrypt

passwd = b's$cret12'

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd, salt)

p = hashed.decode('utf-8')
print(bcrypt.checkpw(passwd, bytes(p, 'utf-8')))
