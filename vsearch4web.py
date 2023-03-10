from flask import Flask, render_template,request
from vsearch import search_4_letters

app = Flask(__name__)


@app.route('/search4', methods = ['POST'])
def do_search() ->str:
    """Функция для вывода и постановки в iаблон наших значений в htrml шаблоне
    с помощью junja2
    """
    
    return render_template('result.html',
                           the_title = 'Here are you result:',
                           the_phrase = request.form['phrase'],
                           the_letters = request.form['letters'],
                           the_result = str(search_4_letters(request.form['phrase']
                                                             ,request.form['letters'])), )   

@app.route('/')
@app.route('/entry')
def entry_page() -> 'str':
    return render_template('entry.html',
                           the_title = 'Welcome to search4letterson the web')

if __name__ == '__name__':
    app.run(debug=True)