from flask import Flask, render_template, url_for, request, redirect, json,jsonify
from flask_restful import Resource, Api, reqparse
from googletrans import Translator

app = Flask(__name__)
api = Api(app)

class TranslatorSimple(Resource):
    def get(self):
        pass

    def post(self):
        data = request.json
        translator = Translator()
        keyword = data.get('keyword')
        lang = data.get('lang')
        if len(data.get('lang')) == 0 or data.get('lang') == None:
            lang="en"
        t = translator.translate(keyword,lang)
        res = {'text':t.text}
        return jsonify(res)

api.add_resource(TranslatorSimple, '/translate')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)

