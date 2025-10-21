import os
from flask import Flask, render_template, redirect, url_for, flash, abort
from config import Config
from models import db, Project, Comment
from forms import NewProjectForm, CommentForm

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()
    os.makedirs(app.config['PROJECTS_DIR'], exist_ok=True)


@app.route('/')
def index():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('index.html', projects=projects)


@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    form = NewProjectForm()
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            author_name=form.author_name.data,
            filepath=''
        )
        db.session.add(project)
        db.session.flush()

        filename = f'project_{project.id}.md'
        filepath = os.path.join(app.config['PROJECTS_DIR'], filename)

        with open(filepath, 'w') as f:
            f.write(form.description.data)

        project.filepath = filename
        db.session.commit()

        flash('Project created successfully!', 'success')
        return redirect(url_for('view_project', project_id=project.id))

    return render_template('new_project.html', form=form)


@app.route('/projects/<int:project_id>')
def view_project(project_id):
    project = Project.query.get_or_404(project_id)

    filepath = os.path.join(app.config['PROJECTS_DIR'], project.filepath)
    try:
        with open(filepath, 'r') as f:
            description = f.read()
    except FileNotFoundError:
        description = 'Project description file not found.'

    comments = Comment.query.filter_by(project_id=project_id).order_by(Comment.created_at).all()
    form = CommentForm()

    return render_template('project.html',
                         project=project,
                         description=description,
                         comments=comments,
                         form=form)


@app.route('/projects/<int:project_id>/comment', methods=['POST'])
def add_comment(project_id):
    project = Project.query.get_or_404(project_id)
    form = CommentForm()

    if form.validate_on_submit():
        parent_id = form.parent_comment_id.data
        quoted = form.quoted_text.data

        comment = Comment(
            project_id=project_id,
            student_name=form.student_name.data,
            comment_text=form.comment_text.data,
            parent_comment_id=int(parent_id) if parent_id else None,
            quoted_text=quoted if quoted else None
        )
        db.session.add(comment)
        db.session.commit()

        flash('Comment added!', 'success')
    else:
        flash('Please fill in all required fields.', 'error')

    return redirect(url_for('view_project', project_id=project_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
