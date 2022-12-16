#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
# set static and template folders
app.template_folder = 'frontend'
app.static_folder = 'frontend/assets'


#----------------------------------------------------------------------------#
# Routes.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/uses')
def uses():
    return render_template('uses.html')


@app.route('/post')
def post():
    return render_template('post.html')


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.config.update(
        DEBUG=True,
        TEMPLATES_AUTO_RELOAD=True,
    )
    app.run()
