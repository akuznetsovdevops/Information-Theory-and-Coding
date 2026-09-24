text = 'Nursultan'
shift = 2
result = ''
for char in text:
    result += chr(ord(char) + shift)

print(result)
text = result
result = ''
for char in text:
        result += chr(ord(char) - shift)

print(result)
