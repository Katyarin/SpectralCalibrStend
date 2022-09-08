


for i in range(100):
    with open('test.txt', 'a') as file:
        file.write(str(i))
        file.write('\n')

with open('test.txt', 'a') as file:
    file.write(str(10))