from io import BytesIO
from flask import Blueprint, current_app
from flask import flash, send_file, render_template, request, redirect, url_for, abort
from autoconstruccion.models import Project, db, Event, User, Skill, SkillLevel
from autoconstruccion.web.forms import ProjectForm, UserForm, EventForm, SkillForm
from .utils import get_image_from_file_field
from flask.ext.login import login_required, current_user
from autoconstruccion.login.auth import is_admin


bp = Blueprint('web', __name__,
               template_folder='templates',
               static_folder='static',
               static_url_path='static/web')


@bp.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)


@bp.route('projects')
def project_index():
    projects = Project.query.all()
    return render_template('projects/index.html', projects=projects)


@bp.route('projects/add', methods=['GET', 'POST'])
@login_required
@is_admin
def project_add():

    # Don't pass request.form as flask_wtf do it automatically, and
    # if request.form is passed it won't load the images!!!!
    project_form = ProjectForm()

    if project_form.validate_on_submit():
        project = Project()
        project_form.populate_obj(project)
        project.image = get_image_from_file_field(project_form.image, request)
        db.session.add(project)
        db.session.commit()

        flash('Project created', 'success')
        return redirect(url_for('web.project_index'))
    return render_template('projects/add.html', form=project_form)


@bp.route('projects/<int:project_id>')
def project_view(project_id):
    project = Project.query.get(project_id)
    return render_template('projects/view.html', project=project)


@bp.route('projects/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
@is_admin
def project_edit(project_id):
    project = Project.query.get(project_id)
    form = ProjectForm(obj=project)

    if form.validate_on_submit():
        form.populate_obj(project)
        project.image = get_image_from_file_field(form.image, request)
        db.session.commit()

        flash('Project edited', 'success')
        return redirect(url_for('web.project_index'))
    return render_template('projects/edit.html', form=form, project_id=project_id)


@bp.route('projects/<int:project_id>/join', methods=['GET', 'POST'])
@login_required
def project_join(project_id):
    project = Project.query.get(project_id)
    user = User.query.get(current_user.id)
    skills = Skill.query.all()
    if request.method == 'POST':
        skills_result = request.form
        for skill_id in skills_result:
            if skill_id != 'csrf_token':
                skill_level = SkillLevel()
                skill_level.project_id = project_id
                skill_level.user_id = user.id
                skill_level.skill_id = int(skill_id)
                skill_level.level = int(skills_result[skill_id])
                db.session.add(skill_level)
        user.projects.append(project)
        db.session.commit()

        flash('Data saved successfully', 'success')
        return redirect(url_for('web.project_view', project_id=project_id))
    return render_template('projects/join_skills.html', project=project, skills=skills)


@bp.route('projects/<int:project_id>/image')
def get_project_image(project_id):
    project = Project.query.get(project_id)
    if project.image:
        return send_file(BytesIO(project.image), mimetype='image/jpg')
    else:
        # return default image for a project
        return send_file('static/img/project_default.jpg', mimetype='image/jpg')


@bp.route('projects/<int:project_id>/events/add', methods=['GET', 'POST'])
@login_required
@is_admin
def event_add(project_id):
    form = EventForm(request.form)
    if request.method == 'POST':
        if form.validate():
            event = Event()
            form.populate_obj(event)
            event.project_id = project_id
            db.session.add(event)
            db.session.commit()

            flash('Data saved successfully', 'success')
            return redirect(url_for('web.project_events', project_id=project_id))

        flash('Data not valid, please review the fields')

    return render_template('events/add.html', project_id=project_id, form=form)


@bp.route('projects/<int:project_id>/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
@is_admin
def event_edit(project_id, event_id):
    event = Event.query.get(event_id)

    form = EventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        db.session.commit()

        flash('Data saved successfully', 'success')
        return redirect(url_for('web.project_events', project_id=project_id))

    return render_template('events/edit.html', project_id=project_id, event_id=event_id, form=form)


@bp.route('projects/<int:project_id>/events/<int:event_id>', methods=['GET'])
def event_view(project_id, event_id):
    conditions = (Event.id == event_id,
                  Event.project_id == project_id)
    event = Event.query.filter(*conditions).first()
    return render_template('events/view.html', event=event) if event else abort(404)


@bp.route('projects/<int:project_id>/events/<int:event_id>/join')
@login_required
def event_join(project_id, event_id):
    user_id = current_user.get_id()
    user = User.query.get(user_id)
    event = Event.query.get(event_id)
    user.events.append(event)
    db.session.commit()

    flash('Joined to event successfully', 'success')
    return redirect(url_for('web.event_view', project_id=project_id, event_id=event_id))


@bp.route('projects/<int:project_id>/events/<int:event_id>/volunteers', methods=['GET', 'POST'])
@login_required
@is_admin
def event_volunteers(project_id, event_id):
    event = Event.query.get(event_id)

    return render_template('events/volunteers.html', users=event.users)


@bp.route('projects/<int:project_id>/events/<int:event_id>/reminder', methods=['GET', 'POST'])
@login_required
@is_admin
def event_reminder(project_id, event_id):
    event = Event.query.get(event_id)

    text = "Recuerda que hay un evento {} el dia {} ".format (event.name, event.start_date)
    subject = "Recordatorio cita {}".format(event.start_date)
    for user in event.users:
        message = {  'to': user.email, 'subject': subject, 'text': text  }
        current_app.notifier.send(**message)

    return redirect(url_for('web.event_view', project_id=project_id, event_id=event_id))


@bp.route('projects/<int:project_id>/events', methods=['GET'])
def project_events(project_id):
    conditions = (Event.project_id == project_id,)
    events = Event.query.filter(*conditions).all()

    return render_template('projects/events.html', events=events, project_id=project_id)


@bp.route('projects/<int:project_id>/volunteers', methods=['GET'])
@login_required
@is_admin
def project_volunteers(project_id):
    project = Project.query.get(project_id)
    return render_template('projects/volunteers.html', project_id=project_id, users=project.users)


@bp.route('users', methods=['GET', 'POST'])
@login_required
@is_admin
def user_index():
    users = User.query.all()
    return render_template('users/index.html', users=users)


@bp.route('users/add', methods=['GET', 'POST'])
@login_required
@is_admin
def user_add():
    form = UserForm(request.form)
    if request.method == 'POST':
        if form.validate():
            user = User()
            form.populate_obj(user)
            user.store_password_hashed(form.password.data)
            db.session.add(user)
            db.session.commit()

            flash('Data saved successfully', 'success')
            return redirect(url_for('web.user_index'))

        flash('Data not valid, please review the fields')

    return render_template('users/add.html', form=form)


@bp.route('users/<int:user_id>', methods=['GET', 'POST'])
@login_required
@is_admin
def user_edit(user_id):
    user = User.query.get(user_id)
    form = UserForm(request.form, user)
    if request.method == 'POST':
        if form.validate():
            form.populate_obj(user)
            if current_user.is_admin():
                user._is_admin = form.is_admin.data
            user.store_password_hashed(form.password.data)
            db.session.commit()

            flash('Data saved successfully', 'success')
            return redirect(url_for('web.user_index'))
        flash('Data not valid, please review the fields')

    return render_template('users/edit.html', form=form, user_id=user_id)


@bp.route('users/account', methods=['GET', 'POST'])
@login_required
def user_account():
    user_id = current_user.get_id()
    user = User.query.get(user_id)
    if not user:
        raise Exception('User not found')

    form = UserForm(request.form, user)
    if request.method == 'POST':
        if form.validate():
            form.populate_obj(user)
            user.store_password_hashed(form.password.data)
            db.session.commit()

            flash('Data saved successfully', 'success')
            return redirect(url_for('web.user_index'))

        flash('Data not valid, please review the fields')

    return render_template('users/account.html', form=form, user_id=user_id)


@bp.route('skills')
@login_required
def skill_index():
    skills = Skill.query.all()
    return render_template('skills/index.html', skills=skills)


@bp.route('skills/add', methods=['GET', 'POST'])
@login_required
def skill_add():
    form = SkillForm(request.form)
    if request.method == 'POST':
        if form.validate():
            skill = Skill()
            form.populate_obj(skill)
            skill.image = get_image_from_file_field(form.image, request)
            db.session.add(skill)
            db.session.commit()

            flash('Skill saved successfully', 'success')
            return redirect(url_for('web.skill_add'))

        flash('Data not valid, please review the fields')

    return render_template('skills/add.html', form=form)


@bp.route('skills/edit/<int:skill_id>', methods=['GET', 'POST'])
@login_required
def skill_edit(skill_id):
    skill = Skill.query.get(skill_id)
    form = SkillForm(obj=skill)

    if form.validate_on_submit():
        form.populate_obj(skill)
        skill.image = get_image_from_file_field(form.image, request)
        db.session.commit()

        flash('Skill edited', 'success')
        return redirect(url_for('web.skill_index'))
    return render_template('skills/edit.html', form=form, skill_id=skill_id)