from flask import Flask, render_template, request #requst and render html pages
from vsearch import search_4_letters #my func - using my func in project 
from flask import escape #Экранирование что бы браузер не воспринимал текст как теги например "< or >"

app = Flask(__name__)

def log_request(req, res: str) -> None:
    with open('vsearch.log', 'a') as log:
        print(req.form, file=log , end="|")
        print(req.remote_addr, file=log , end="|")
        print(req.user_agent, file=log , end="|")
        print(res, file=log)
        # print(req.form, req.remote_addr, req.user_agent, res, file=log, sep = "|")

@app.route('/search4', methods = ['POST'])
def do_search() -> str:
    """Функция для вывода и постановки в шаблон наших значений в html шаблоне
    с помощью junja2
    """
    log_request(request, str(search_4_letters(request.form['phrase'], request.form['letters']))) #записать в лог (делает файл в корне)
    return render_template('result.html',
                           the_title = 'Here are you result:',
                           the_phrase = request.form['phrase'],
                           the_letters = request.form['letters'],
                           the_result = str(search_4_letters(request.form['phrase']
                                                             ,request.form['letters'])), )  #рендеринг нашей html страницы

@app.route('/')
@app.route('/entry')
def entry_page() -> 'str':
    return render_template('entry.html',
                           the_title = 'Welcome to search4letterson the web')


@app.route('/viewlog')
def view_the_log() -> 'html':
    contents = []
    with open('vsearch.log') as log:
         for line in log:
            contents.append([])
            for item in line.split('|'): #сделано под escape (чтбы у нас был список из escape)
                contents[-1].append(escape(item)) 
    titles = ('Form Data','Remote_addr','User_agent','Result',)
    return render_template('viewlog.html',
                            the_title='View_Log',
                            the_row_titles=titles,
                            the_data=contents,)



    # contents = []
    # with open('vsearch.log') as log:
    #     for chose in log:
    #         contents.append(escape(chose.split('|'))) 
    # return str(contents)


if __name__ == '__main__':
    app.run(debug=True)




   