from flask import render_template, request, redirect, url_for
import Utility

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/translate', methods=['POST'])
    def translate():
        Utility.process_srt_file()
        return redirect(url_for('index'))
