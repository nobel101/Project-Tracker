from flask import Flask,render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:admin@localhost:5432/project_tracker'
app.config['SECRET_KEY'] = '\x9bF\x91\xe9\xba\xd9G\x96\x1a1\x82YX\xe0\x08\x8e+\x1fVK?\x8e\x85\xdb'
db = SQLAlchemy(app)

class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=50))


class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    description = db.Column(db.String(length=50))

    project = db.relationship("Project")


@app.route("/")
def show_projects():
    return render_template('index.html', projects=Project.query.all())

@app.route("/project/<project_id>")
def show_tasks(project_id):
    return render_template('project-tasks.html',
            project=Project.query.filter_by(project_id=project_id).first(),
            tasks = Task.query.filter_by(project_id=project_id).all())
@app.route("/add/project", methods=['POST'])
def add_project():
    #Add project
    #retrieving the user input from the html form
    if not request.form['project-title']:
        flash("PLease Enter a title for the project","red")
    else:
        project = Project(title=request.form['project-title'])
        db.session.add(project)
        db.session.commit()
        flash("Project has been created successfully", 'green')
    return redirect(url_for('show_projects'))

@app.route("/add/task/<project_id>", methods=['POST'])
def add_task(project_id):
    #add task
    if not request.form['task-description']:
        flash("Please Enter a task name","red")
    else:
        task = Task(description=request.form["task-description"],
                project_id=project_id)
        db.session.add(task)
        db.session.commit()
        flash("the task has been added successfully","green")
    return redirect(url_for('show_tasks', project_id=project_id))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)
