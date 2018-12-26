from Crypto.Cipher import AES

key = 'FE5A10236842EF551087301E8B17EEFB'
iv = '1337133713371337BAADF0000DAAAAAA'
encrypted = '6f4e8fff1523407fabf1e6ba7abcc585129e3802f785a75f28b0e63482449f5347501f6b38f014ae4f51e37ffb9b323b'

key = bytes([int(key[i:i+2], 16) for i in range(0, len(key), 2)])
iv = bytes([int(iv[i:i+2], 16) for i in range(0, len(iv), 2)])
encrypted = bytes([int(encrypted[i:i+2], 16) for i in range(0, len(encrypted), 2)])

cipher = AES.new(key, AES.MODE_CBC, iv)
decrypted = cipher.decrypt(encrypted)
decrypted = decrypted[:-1 * decrypted[-1]].decode()
print(decrypted)
