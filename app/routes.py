from flask import render_template, request, redirect, url_for

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/translate', methods=['POST'])
    def translate():
        # Here you would integrate your translation logic
        language = request.form['language']
        # Call to your translation function
        return redirect(url_for('index'))
