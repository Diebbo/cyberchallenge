from base64 import b64decode

a = 'ZmxhZ3t3NDF0XzF0c19hbGxfYjE='
b = 664813035583918006462745898431981286737635929725

res = b64decode(a).decode('ascii')
res += b.to_bytes(24, 'big').decode('ascii')
print(res)
