from requests import get, post, delete


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
    print(get('http://127.0.0.1:8080/api/jobs').json())


one = ('http://127.0.0.1:8080/api/jobs/1', "Correct")
two = ('http://127.0.0.1:8080/api/jobs/999', "Non-existent id")
three = ('http://127.0.0.1:8080/api/jobs/str', "Id - string")
four = ('http://127.0.0.1:8080/api/jobs/', "no id")
tests = (one, two, three, four)
test_del(tests)
