from requests import get, post, delete, put


def test_get(tests):
    for test in tests:
        print(f"{test[1]}: {get(test[0])}")


def test_post(tests):
    for test in tests:
        print(test[0])
        print(f"{test[2]}: {post(test[0], json=test[1])}")
    print(get(tests[0][0]).json())


def test_del(tests):
    for test in tests:
        print(f"{test[1]}: {delete(test[0])}")
    print(get('http://127.0.0.1:8080/api/users').json())


def test_edit(tests):
    for test in tests:
        print(f"{test[2]}: {post(test[0], json=test[1])}")


char = list()
for i in range(3, 7):
    one = dict(surname=f"Gen{i + 1}", name=f"Alex{i}", age=20, position="chief", speciality="biolog", address="module_1",
               email=f"{i}@x", hashed_password=123, dep_id=3, city_from="Москва")
    char.append((f'http://127.0.0.1:8080/api/users', one, "correct"))
test_post(char)
# char = list()
# for i in range(3):
#     one = dict(surname=f"Gen{i + 3}")
#     char.append((f'http://127.0.0.1:8080/api/users/{i + 1}', one, "correct"))
# test_edit(char)

