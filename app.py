from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///classes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Class model
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# API to get all classes
@app.route('/api/classes', methods=['GET'])
def get_classes():
    classes = Class.query.all()
    class_list = [{"id": cls.id, "name": cls.name} for cls in classes]
    return jsonify(class_list)

# API to add a new class
@app.route('/api/classes', methods=['POST'])
def add_class():
    data = request.json
    new_class = Class(name=data['name'])
    db.session.add(new_class)
    db.session.commit()
    return jsonify({"id": new_class.id, "name": new_class.name}), 201

# API to update a class
@app.route('/api/classes/<int:id>', methods=['PUT'])
def update_class(id):
    data = request.json
    cls = Class.query.get_or_404(id)
    cls.name = data['name']
    db.session.commit()
    return jsonify({"id": cls.id, "name": cls.name})

# API to delete a class
@app.route('/api/classes/<int:id>', methods=['DELETE'])
def delete_class(id):
    cls = Class.query.get_or_404(id)
    db.session.delete(cls)
    db.session.commit()
    return jsonify({"message": "Class deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)