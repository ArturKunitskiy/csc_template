"""Скопіюйте як student/routes.py"""

from flask import Flask


def register(app: Flask) -> None:
    @app.route("/hello")
    def hello():
        return "Привіт з вашого Flask-роуту!"
