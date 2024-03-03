from flask import Flask, render_template, redirect, request
from data.users import User
from forms.user import RegisterForm, LoginForm
from forms.job import JobsForm
from data.jobs import Jobs
from data.department import Departments
from data import db_session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id).filter(
        (Jobs.team_leader == current_user.id | current_user.id == 1)).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).filter(
            (Jobs.team_leader == current_user.id | current_user.id == 1)).first()
        if jobs:
            form.team_leader.data = jobs.team_leader
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.start_date.data = jobs.start_date
            form.end_date.data = jobs.end_date
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).filter(
                                          (Jobs.team_leader == current_user.id | current_user.id == 1)).first()
        if jobs:
            jobs.team_leader = form.team_leader.data
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.start_date = form.start_date.data
            jobs.end_date = form.end_date.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('job.html', title='Редактирование новости', form=form)


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data,
        )
        db_sess = db_session.create_session()
        db_sess.add(job)
        db_sess.commit()
        db_sess.close()
        return redirect('/')
    return render_template('job.html', title='Add job', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


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
        collaborators = "No members"
        if work.collaborators:
            collaborators = work.collaborators
        list_works.append([work.id, work.job, team_leader, work_size, collaborators, is_finished])
    return render_template("index.html", works=list_works)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            age = int(form.age.data)
        except ValueError:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Возраст не является числом")
        if not (0 <= age <= 130):
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Возраст не является реальным")
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            hashed_password=form.password.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()