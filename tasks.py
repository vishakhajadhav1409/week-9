from flask import Blueprint, request, jsonify
from app.models import Task
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

task_bp = Blueprint("tasks", __name__)

@task_bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()

    query = Task.query.filter_by(user_id=user_id)

    status = request.args.get("status")
    if status:
        query = query.filter_by(status=status)

    tasks = query.all()

    return jsonify([{"id": t.id, "title": t.title} for t in tasks])


@task_bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    data = request.get_json()
    user_id = get_jwt_identity()

    task = Task(
        title=data["title"],
        description=data.get("description"),
        priority=data.get("priority"),
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({"msg": "Task created"}), 201


@task_bp.route("/tasks/<int:id>", methods=["PUT"])
@jwt_required()
def update_task(id):
    task = Task.query.get_or_404(id)

    data = request.get_json()
    task.title = data.get("title", task.title)
    task.status = data.get("status", task.status)

    db.session.commit()

    return jsonify({"msg": "Updated"})


@task_bp.route("/tasks/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"msg": "Deleted"})