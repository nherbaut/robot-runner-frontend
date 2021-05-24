import json
import pika
import uuid
from app.main import app
from flask import render_template, request
import os


def get_api_root():
    return os.getenv("API_ROOT", "dummy://")


@app.route("/robot/<robot_id>", methods=["GET"])
def welcome_robot(robot_id):
    return render_template('robot.html')

@app.route("/robot/<robot_id>", methods=["POST"])
def trigger_robot(robot_id):
    broker_user = os.getenv("BROKER_USER")
    broker_password = os.getenv("BROKER_PASSWORD")
    broker_host = os.getenv("BROKER_HOST")

    credentials = pika.PlainCredentials(broker_user, broker_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(broker_host, 5672, "/", credentials))
    channel = connection.channel()
    channel.queue_declare(queue='celery', durable=True)
    channel.queue_declare(queue='robot-response', durable=True)

    id = str(uuid.uuid4())
    task_name = "youtube.run_robot"

    payload = json.loads(request.form["robotcommand"])
    message = [["youtube-robot", payload], {}, {"callbacks": None, "errbacks": None, "chain": None, "chord": None}]

    channel.basic_publish('celery',
                          'celery',
                          body=json.dumps(message),
                          properties=pika.BasicProperties(
                              headers={"id": id,
                                       "root_id": id,
                                       "origin": "robot-runner",
                                       "task": task_name, },
                              content_type='application/json',
                              content_encoding="utf-8",
                              correlation_id=id,
                              reply_to="robot-response",
                              delivery_mode=2))
    return "ok"
