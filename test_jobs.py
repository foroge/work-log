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
    print(get('http://127.0.0.1:8080/api/jobs').json())


def test_edit(tests):
    for test in tests:
        print(f"{test[2]}: {put(test[0], json=test[1])}")


char = list()
one = dict(job="okkk")
char.append((f'http://127.0.0.1:8080/api/jobs/7', one, "correct"))
two = dict(name="xxxx")
char.append((f'http://127.0.0.1:8080/api/jobs/5', two, "non-existent parameter"))
three = dict()
char.append((f'http://127.0.0.1:8080/api/jobs/9', three, "empty dictionary"))
four = dict(team_leader=9, job="okkkk", work_size=24, collaborators="1, 3, 4", is_finished=0)
char.append((f'http://127.0.0.1:8080/api/jobs/10', four, "all parameters"))
test_edit(char)
# correct: <Response [200]>
# non-existent parameter: <Response [400]>
# empty dictionary: <Response [400]>
# all parameters: <Response [200]>