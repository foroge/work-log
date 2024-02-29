from flask import Flask, render_template
from data.users import User
from data.jobs import Jobs
from data.department import Departments
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    db_sess = db_session.create_session()
    works = db_sess.query(Jobs).all()
    list_works = list()
    for work in works:
        team_leader = db_sess.query(User).filter(User.id == work.team_leader).first()
        team_leader = f"{team_leader.name} {team_leader.surname}"
        is_finished = "Is not finished"
        if work.is_finished:
            is_finished = "Is finished"
        work_size = f"{work.work_size} hours"
        list_works.append([work.id, work.job, team_leader, work_size, work.collaborators, is_finished])
    return render_template("index.html", works=list_works)


def main():
    job = Jobs()
    job.team_leader = 2
    job.job = "gdfjgjdslgs;lj"
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    # cap = User()
    # cap.surname = "Scott"
    # cap.name = "Ridley"
    # cap.age = 21
    # cap.position = "captain"
    # cap.speciality = "research engineer"
    # cap.address = "module_1"
    # cap.email = "scott_chief@mars.org"
    #
    # db_sess.add(cap)
    # db_sess.commit()
    #
    # for i in range(4):
    #     user = User()
    #     user.surname = "Alex"
    #     user.name = f"Forward_{i}"
    #     user.age = 24
    #     user.position = "Privat"
    #     user.speciality = "research engineer"
    #     user.address = f"module_{i}"
    #     user.email = f"basic_{i}@mars.org"
    #     user.hashed_password = f"basic_{i}"
    #
    #     db_sess.add(user)
    #     db_sess.commit()
    #
    # dep = Departments()
    # dep.title = "research engineer"
    # dep.members = [user]
    #
    db_sess.add(job)
    db_sess.commit()
    db_sess.close()
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()