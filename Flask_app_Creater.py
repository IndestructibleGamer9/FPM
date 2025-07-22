import os
import shutil

class FlaskAppCreator:
    def __init__(self):
        self.models_cont ="""from extensions import db
from flask_login import UserMixin
from datetime import datetime, date 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    joined = db.Column(db.Date, default=date.today)
    admin = db.Column(db.Boolean, default=False)
"""
        self.index_cont ="""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Index</title>
</head>

<body>
    <h1>This is the index page!</h1>
</body>

</html>
"""
        self.base_cont = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">

    <!-- Title -->
    <title>{% block title %}My Flask App{% endblock %}</title>

    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.ico') }}">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

    <!-- Font Awesome -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <!-- Feather Icons -->
    <script src="https://unpkg.com/feather-icons"></script>

    <!-- Custom Styles Block -->
    {% block styles %}{% endblock %}

    <!-- Mobile Web App -->
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
</head>

<body>
    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
    <div class="container mt-3">
        {% for category, message in messages %}
        <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show"
            role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endfor %}
    </div>
    {% endif %}
    {% endwith %}

    <!-- Main Content -->
    <main>
        {% block content %}{% endblock %}
    </main>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

    <!-- Feather Icons Initialization -->
    <script>
        feather.replace();
    </script>

    <!-- Custom Scripts Block -->
    {% block scripts %}{% endblock %}
</body>

</html>
"""

    def warning(self, message, degree=1):
        YELLOW = "\033[93m"
        RESET = "\033[0m"
        RED = "\033[91m"
        GREEN = "\033[92m"
        if degree == 1:
            print(f"{YELLOW}Warning: {message}{RESET}")
        elif degree == 2:
            print(f"{RED}Error: {message}{RESET}")
        elif degree == 0:
            print(f"{GREEN}Success: {message}{RESET}")
        else:
            print(f"{YELLOW}Warning: {message}{RESET}")
            print(f"{YELLOW}Warning: {message}{RESET}")

    def copy_file(self, orig, dest):
        try:
            shutil.copytree(orig, dest)
            print(f"File '{orig}' copied to '{dest}' successfully.")
            return True
        except FileNotFoundError:
            print(f"Error: Source file '{orig}' not found.")
            return False
        except PermissionError:
            print("Error: Permission denied to copy the file.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False         

    def create_scr(self, file_path, cont=None):
        with open(file_path, "w") as file:
            if cont:
                file.write(cont)

    def app_cont(self, database, blueprint_names):
        if database:
            if blueprint_names:
                imp = []
                code = []
                for blueprint in blueprint_names:
                    imp.append(f'from {blueprint} import {blueprint}_bp')
                    code.append(f'app.register_blueprint({blueprint}_bp)')
                imp_string = "\n".join(imp)  
                code_string = "\n".join(code)
                if 'auth' in blueprint_names:
                    return """from flask import Flask, render_template
import os
from extensions import db, migrate, login_manager, bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UserData.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
bootstrap.init_app(app)

# Configure login manager
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'
from models import User
"""+"\n"+imp_string+"\n"+code_string+"\n"+"""
@app.route('/')
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=3001)
"""
                else:
                    return """from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UserData.db'

db = SQLAlchemy()
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)"""+"\n"+imp_string+"\n"*2+""""""+"\n"*2+code_string+"\n"*2+"""@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=3001) 
"""
            else:
                return """from flask import Flask, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UserData.db'

db = SQLAlchemy()
migrate = Migrate()
db.init_app(app)
migrate.init_app(app, db)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=3001) 
"""
        else:
            if blueprint_names:
                imp = []
                code = []
                for blueprint in blueprint_names:
                    imp.append(f'from {blueprint} import {blueprint}_bp')
                    code.append(f'app.register_blueprint({blueprint}_bp)')
                imp_string = "\n".join(imp)  
                code_string = "\n".join(code)  
                a= """from flask import Flask, render_template
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)"""+"\n"+imp_string+"\n"+""""""+"\n"*2+code_string+"\n"*2+"""@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=3001)
"""
                return a
            else:
                return """from flask import Flask, render_template
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=3001)
"""  

    def get_req(self):
        self.proj_name = str(input("Enter the project name: "))
        self.database = input("Do you want to use a database? (y/n): ")
        if self.database.lower() == 'y':
            self.warning("Database will be created.", 0)
            self.database = True
        elif self.database.lower() == 'n':
            self.warning("No database will be created.", 1)
            self.database = False    
        else:
            self.warning("Unknown input, no database will be created.", 1)
            self.database = False   

        self.forms = input("Do you want to use Flask forms? (y/n): ")
        if self.forms.lower() == 'y':
            self.warning("Forms will be created.", 0)
            self.forms = True
        elif self.forms.lower() == 'n':
            self.warning("No forms will be created.", 1)
            self.forms = False    
        else:
            self.warning("Unknown input, no forms will be created.", 1)
            self.forms = False 

        self.blueprints = int(input("How many blueprints do you want to create within(0,100)? "))
        if self.blueprints < 0:
            self.warning("Blueprints cannot be negative, setting to 0.", 2)
            self.blueprints = 0
            self.blueprint_names = None
        elif self.blueprints == 0:
            self.warning("No blueprints will be created.", 1) 
            self.blueprint_names = None   
        elif self.blueprints >= 0: 
            if self.blueprints >= 101:
                self.warning('Too many blueprints, creating 100.', 1) 
                self.blueprints= 100  
            self.blueprint_names = []
            for blueprint in range(0, self.blueprints):
                name = input(f'Blueprint name {blueprint+1}: ')
                if name != 'null' and name != '' and name != None and name != 'None' and name != 'none' and name not in self.blueprint_names:
                    self.blueprint_names.append(name)
                else:
                    if name in self.blueprint_names:
                        self.warning('cannot create 2 blueprints with same name', 1)   


        else:
            self.warning("Unknown input no blueprints will be created.", 1)

    def copy_auth(self):
        if self.copy_file('./data/auth', f"./{self.proj_name}/auth"):
            self.warning("Auth files copied successfully.", 0)
        else:
            self.warning("Failed to copy auth files.", 2)

    def copy_extensions(self):
        if shutil.copy2('./data/extensions.py', f"./{self.proj_name}/extensions.py"):
            self.warning("Extensions file copied successfully.", 0)
        else:
            self.warning("Failed to copy extensions file.", 2)

    def init_cont(self, name):
        return f"""from flask import Blueprint

{name}_bp = Blueprint('{name}', __name__, template_folder='templates', static_folder='static', static_url_path='/{name}/static')

from . import routes  # Import routes to register them with the blueprint
"""

    def create_bp(self, blueprint_name):
        os.mkdir(self.path+f'/{blueprint_name}')
        bp_path = self.path+f'/{blueprint_name}'
        os.mkdir(bp_path+'/templates')
        os.mkdir(bp_path+'/static')
        tempath = f"./{bp_path}/templates"
        os.mkdir(tempath+f'/{blueprint_name}')
        self.create_scr((tempath+'/index.html'), cont=self.index_cont)
        statpath = f"./{bp_path}/static"
        os.mkdir(statpath+'/scripts')
        os.mkdir(statpath+'/styles')
        os.mkdir(statpath+'/img')
        self.create_scr((bp_path+'/__init__.py'), cont=self.init_cont(blueprint_name))
        self.create_scr((bp_path+'/routes.py'))            

    def create_fldr_str(self):

        os.mkdir(self.path+'/templates')
        os.mkdir(self.path+'/static')
        tempath = f"./{self.proj_name}/templates"
        statpath = f"./{self.proj_name}/static"
        os.mkdir(statpath+'/scripts')
        os.mkdir(statpath+'/styles')
        os.mkdir(statpath+'/img') 
        self.create_scr((tempath+'/index.html'), cont=self.index_cont)
        self.create_scr((tempath+'/base.html'), cont=self.base_cont)                  

    def create_app(self):
        self.get_req()
        if not os.path.exists(self.proj_name):
            os.makedirs(self.proj_name)
            self.path = f'./{self.proj_name}'
            self.warning(f"Project directory '{self.proj_name}' created.", 0)
        else:
            self.warning(f"Project directory '{self.proj_name}' already exists.", 2)
            return False
        
        self.create_scr((self.path+'/app.py'), cont=self.app_cont(self.database, self.blueprint_names))
        if self.database:
            self.warning('remember to populate models.py initalize migrate and upgrade to make database work!!!')
            self.create_scr((self.path+'/models.py'), cont=self.models_cont)

        if self.forms:
            self.create_scr((self.path+'/forms.py'))

        self.create_fldr_str()
        if self.blueprint_names:
            for blueprint_name in self.blueprint_names:
                if blueprint_name.lower() == 'auth':
                    if self.database:
                        self.copy_auth()
                        self.copy_extensions()
                    else:
                        self.warning("Auth blueprint requires a database, skipping.", 1)
                else:
                    self.create_bp(blueprint_name)

        if self.database:
            import subprocess
            try:
                result1 = subprocess.run(
                    ["flask", "db", "init"],
                    cwd=f"C:\\Users\\Will\\Documents\\GitHub\\Flask_Project_Setup\\{self.proj_name}",
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(result1.stdout)
            except subprocess.CalledProcessError as e:
                print("Error initializing database:", e.stderr)

            try:
                result2 = subprocess.run(
                    ["flask", "db", "migrate", "-m", "initialization"],
                    cwd=f"C:\\Users\\Will\\Documents\\GitHub\\Flask_Project_Setup\\{self.proj_name}",
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(result2.stdout)
            except subprocess.CalledProcessError as e:
                print("Error during migration:", e.stderr)

            try:
                result3 = subprocess.run(
                    ["flask", "db", "upgrade"],
                    cwd=f"C:\\Users\\Will\\Documents\\GitHub\\Flask_Project_Setup\\{self.proj_name}",
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(result3.stdout)
            except subprocess.CalledProcessError as e:
                print("Error during upgrade:", e.stderr)
            # except Exception as e:
            #     self.warning(f'Database Initalizing FAILED error: {e}', 2) 
        self.warning("Initialization Sucess!", 0)               

        self.warning("Flask app structure created successfully.", 0)
        return True       
        
    def run(self):
        self.create_app()

if __name__ == '__main__':
    fap = FlaskAppCreator()  
    fap.run()
