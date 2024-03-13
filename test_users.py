from requests import get, post, delete, put


def test_get(tests):
    for test in tests:
        print(f"{test[1]}: {get(test[0])}")


def test_post(tests):
    for test in tests:
        print(f"{test[2]}: {post(test[0], json=test[1])}")
    print(get(tests[0][0]).json())


def test_del(tests):
    for test in tests:
        print(f"{test[1]}: {delete(test[0])}")
    print(get('http://127.0.0.1:8080/api/users').json())


def test_edit(tests):
    for test in tests:
        print(f"{test[2]}: {put(test[0], json=test[1])}")


# test get
# tests = (('http://127.0.0.1:8080/api/users', "All jobs"), ('http://127.0.0.1:8080/api/users/1', "One job"),
#          ('http://127.0.0.1:8080/api/users/999', "ID is not correct"), ('http://127.0.0.1:8080/api/users/str', "id - string"))
# test_get(tests)
# All jobs: <Response [200]>
# One job: <Response [200]>
# ID is not correct: <Response [404]>
# id - string: <Response [404]>

# test post
# char = list()
# one = dict(surname=f"Gen11", name=f"Alex11", age=20, position="chief", speciality="biolog", address="module_1",
#            email=f"11@x", hashed_password=123, dep_id=3)
# char.append((f'http://127.0.0.1:8080/api/users', one, "correct"))
# two = dict(surname=f"Gen8", name=f"Alex8", age=20, position="chief", speciality="biolog", address="module_1",
#            email=f"8@x", hashed_password=123, dep_id=3)
# char.append((f'http://127.0.0.1:8080/api/users', two, "email not unique"))
# three = dict(surname=f"Gen8", name=f"Alex8", age=20, position="chief", speciality="biolog", address="module_1")
# char.append((f'http://127.0.0.1:8080/api/users', three, "not full parameters"))
# four = dict()
# char.append((f'http://127.0.0.1:8080/api/users', four, "dict is empty"))
# test_post(char)
# correct: <Response [200]>
# email not unique: <Response [500]>
# not full parameters: <Response [400]>
# dict is empty: <Response [400]>

# test edit
# char = list()
# one = dict(surname=f"Gen1111")
# char.append((f'http://127.0.0.1:8080/api/users/1', one, "correct"))
# two = dict(email=f"19@x", dep_id=7)
# char.append((f'http://127.0.0.1:8080/api/users/2', two, "correct"))
# three = dict(surrrname=f"Gen8")
# char.append((f'http://127.0.0.1:8080/api/users/3', three, "non-existent parameter"))
# four = dict(email=f"19@x", dep_id=7)
# char.append((f'http://127.0.0.1:8080/api/users/str', four, "wrong id"))
# five = dict(email=f"19@x", dep_id=7)
# char.append((f'http://127.0.0.1:8080/api/users/999', five, "non-existent id"))
# test_edit(char)
# correct: <Response [200]>
# correct: <Response [200]>
# non-existent parameter: <Response [400]>
# wrong id: <Response [404]>
# non-existent id: <Response [500]>

# test del
# tests = (('http://127.0.0.1:8080/api/users/4', "correct"), ('http://127.0.0.1:8080/api/users/1', "correct"),
#          ('http://127.0.0.1:8080/api/users/999', "ID is not correct"), ('http://127.0.0.1:8080/api/users/str', "id - string"))
# test_del(tests)
# correct: <Response [200]>
# correct: <Response [200]>
# ID is not correct: <Response [404]>
# id - string: <Response [404]>