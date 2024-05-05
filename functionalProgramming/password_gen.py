import random
import string


class PasswordGenerator:
    def __init__(self, length, count, charset=None):
        self.length = length
        self.count = count
        if charset is None:
            self.charset = string.ascii_letters + string.digits
        else:
            self.charset = charset

        self.generated_passwords = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.generated_passwords >= self.count:
            raise StopIteration
        password = ''.join(random.choice(self.charset) for _ in range(self.length))
        self.generated_passwords += 1
        return password


passwords_generator = PasswordGenerator(12, 5)
for pswd in passwords_generator:
    print(pswd)

print('\n')

passwords_generator = PasswordGenerator(8, 4, "abcd")
it = iter(passwords_generator)
while True:
    try:
        print(next(it))
    except StopIteration:
        break

