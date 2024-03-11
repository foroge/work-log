from flask import Flask, render_template, redirect, request, make_response
from data.users import User
from forms.user import RegisterForm, LoginForm
from forms.job import JobsForm
from forms.department import DepartmentForm
from data.jobs import Jobs
from data.department import Department
from data import db_session, jobs_api, jobs_resources, users_resources, users_api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import reqparse, abort, Api, Resource



app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/department_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def department_delete(id):
    db_sess = db_session.create_session()
    deps = db_sess.query(Department).filter(Department.id == id).filter(
        (Department.chief == current_user.id | current_user.id == 1)).first()
    if deps:
        for user in dep.members:
            user.dep_id = None
            db_sess.commit()
        db_sess.delete(deps)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/department')


@app.route('/department_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def department_edit(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        deps = db_sess.query(Department).filter(Department.id == id).filter(
            (Department.chief == current_user.id | current_user.id == 1)).first()
        if deps:
            members = ", ".join([str(user.id) for user in deps.members])
            form.members.data = members
            form.title.data = deps.title
            form.chief.data = deps.chief
            form.email.data = deps.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        deps = db_sess.query(Department).filter(Department.id == id).filter(
            (Department.chief == current_user.id | current_user.id == 1)).first()
        if deps:
            members = form.members.data.split(", ")
            for i in members:
                try:
                    user = db_sess.query(User).filter(User.id == i).first()
                    if user.dep_id != deps.id:
                        user.dep_id = deps.id
                        db_sess.commit()
                except Exception:
                    pass
            deps.title = form.title.data
            deps.chief = form.chief.data
            deps.email = form.email.data
            db_sess.commit()
            return redirect('/department')
        else:
            abort(404)
    return render_template('department.html', title='Редактирование новости', form=form)


@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        dep = Department(
            title=form.title.data,
            chief=form.chief.data,
            email=form.email.data
        )
        db_sess.add(dep)
        db_sess.commit()
        dep = db_sess.query(Department).filter(Department.email == form.email.data).first()
        members = form.members.data.split(", ")
        for i in members:
            try:
                user = db_sess.query(User).filter(User.id == i).first()
                if user.dep_id != dep.id:
                    user.dep_id = dep.id
                    db_sess.commit()
            except Exception:
                pass
        db_sess.close()
        return redirect('/department')
    return render_template('department.html', title='Add department', form=form)


@app.route("/department")
def index_dep():
    db_sess = db_session.create_session()
    deps = db_sess.query(Department).all()
    list_deps = list()
    for dep in deps:
        members = ", ".join([str(user.id) for user in dep.members]) if dep.members else "No members"
        chief = db_sess.query(User).filter(User.id == dep.chief).first()
        chief = f"{chief.name} {chief.surname}"
        list_deps.append([dep.id, dep.title, chief, members, dep.email, dep.chief])
    return render_template("department_index.html", deps=list_deps)


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
        list_works.append([work.id, work.job, team_leader, work_size, collaborators, is_finished, work.team_leader])
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
            address=form.address.data,
            dep_id=form.dep_id.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    # для списка объектов
    api.add_resource(jobs_resources.JobsListResource, '/api/v2/jobs')

    # для одного объекта
    api.add_resource(jobs_resources.JobsResource, '/api/v2/jobs/<int:jobs_id>')

    # для списка объектов
    api.add_resource(users_resources.UserListResource, '/api/v2/users')

    # для одного объекта
    api.add_resource(users_resources.UserResource, '/api/v2/users/<int:users_id>')

    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()