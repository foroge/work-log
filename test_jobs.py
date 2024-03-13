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


# test get()
# one = ('http://127.0.0.1:8080/api/jobs/3', "correct")
# two = ('http://127.0.0.1:8080/api/jobs/999', "non-existent id")
# three = ('http://127.0.0.1:8080/api/jobs/str', "id - string")
# four = ('http://127.0.0.1:8080/api/jobs/', "no id")
# five = 'http://127.0.0.1:8080/api/jobs', "correct"
# tests = [one, two, three, four, five]
# test_get(tests)
# correct: <Response [200]>
# non-existent id: <Response [404]>
# id - string: <Response [404]>
# no id: <Response [404]>
# correct: <Response [200]>

# test post
# one = ('http://127.0.0.1:8080/api/jobs', {'team_leader': 2, 'job': 'gdsfgd', 'work_size': 1,
#                                           "collaborators": "1, 2, 3", 'is_finished': 0}, "Correct")
# two = ('http://127.0.0.1:8080/api/jobs', {'team_leader': 2, 'job': 'gdsfgd', 'work_size': 1,
#                                           "collaborators": "1, 2, 3"}, "Not all parameters")
# three = ('http://127.0.0.1:8080/api/jobs', {'team_leader': 2, 'job': 'gdsfgd', 'work_size': 1,
#                                           "collaborators": "1, 2, 3", 'is_finished': "fsfds"},
#        "Not that type of parameter")
# four = ('http://127.0.0.1:8080/api/jobs', {}, "Empty dict")
# tests = [one, two, three, four]
# test_post(tests)
# Correct: <Response [200]>
# Not all parameters: <Response [400]>
# Not that type of parameter: <Response [500]>
# Empty dict: <Response [400]>

# test_del(tests)
# one = ('http://127.0.0.1:8080/api/jobs/3', "correct")
# two = ('http://127.0.0.1:8080/api/jobs/999', "non-existent id")
# three = ('http://127.0.0.1:8080/api/jobs/str', "id - string")
# four = ('http://127.0.0.1:8080/api/jobs/', "no id")
# tests = [one, two, three, four]
# test_del(tests)
# correct: <Response [200]>
# non-existent id: <Response [404]>
# id - string: <Response [404]>
# no id: <Response [404]>