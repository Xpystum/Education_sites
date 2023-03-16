from flask import Flask, render_template, request  # requst and render html pages
from vsearch import search_4_letters  # my func - using my func in project
# Экранирование что бы браузер не воспринимал текст как теги например "< or >"
from flask import escape
import pymysql
from db.config import host, user, password, db_name
from ua_parser import user_agent_parser

app = Flask(__name__)

#Функции
def log_request_text(req, res: str) -> None:
    with open('vsearch.log', 'a') as log:
         req_user_browser = user_agent_parser.Parse(req.user_agent.string)['user_agent']['family']
         print(req.form, req.remote_addr, req_user_browser, res, file=log, sep = "|")

def log_request(req, res: str) -> None:  # записать в лог (работает с бд)

    try:
        # Подключаемся к Mysql с помощью драйвера
        connection = pymysql.connect(
        host = host,
        port = 3306,
        user = user,
        password = password,
        database = db_name,
        # это нужно для того, чтобы получить результат в виде словаря, где ключами будут названия колонок.
        cursorclass = pymysql.cursors.DictCursor)
        print("Successfully connected")
        print('"#' * 20)


    #Сделать шаблонную функцию в функции

        try:
            with connection.cursor() as cursor: #автоматически закрое соединение с cursor
                _SQL = "insert into log (`phrase`, `letters`, `ip`, `browser_string`, `result`) VALUES (%s, %s, %s, %s, %s)"
                print(type(req_user_browser = user_agent_parser.Parse(req.user_agent.string)['user_agent']['family']))
                cursor.execute(_SQL, (req.form['phrase'],
                                      req.form['letters'],
                                      req.remote_addr,
                                      req.user_agent.string,
                                      req_user_browser,))
                connection.commit()  # принудительное сохранение в БД

        except Exception as ex:  # Ловим ошибку при покдлючении к бд
            print("Error cursor - execute")
            print(ex)

        finally:
            connection.close()  # закрываем соединение с бд

    except Exception as ex:  # Ловим ошибку при покдлючении к бд
        print("Connection refused")
        print(ex)

    # Старая запись в лог
    # with open('vsearch.log', 'a') as log:
    #      print(req.form, req.remote_addr, req.user_agent, res, file=log, sep = "|")
#Конец блоков Функций

@app.route('/search4', methods=['POST'])
def do_search() -> str:
    """Функция для вывода и постановки в шаблон наших значений в html шаблоне
    с помощью junja2
    """
    log_request_text(request, str(search_4_letters(
        request.form['phrase'], request.form['letters']))) # запись в лог
    
    log_request(request, str(search_4_letters(
        request.form['phrase'], request.form['letters'])))  # вызываем функция которая будет записывать в бд

    return render_template('result.html',
                           the_title='Here are you result:',
                           the_phrase=request.form['phrase'],
                           the_letters=request.form['letters'],
                           the_result=str(search_4_letters(request.form['phrase'], request.form['letters'])), )

    # return render_template('result.html',
    #                        the_title = 'Here are you result:',
    #                        the_phrase = request.form['phrase'],
    #                        the_letters = request.form['letters'],
    #                        the_result = str(search_4_letters(request.form['phrase']
    #                                                          ,request.form['letters'])), )  #рендеринг нашей html страницы


@app.route('/')
@app.route('/entry')
def entry_page() -> 'str':
    return render_template('entry.html',
                           the_title='Welcome to search4letterson the web')


@app.route('/viewlog')
def view_the_log() -> 'str':
    contents = []
    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            # сделано под escape (чтбы у нас был список из escape)
            for item in line.split('|'):
                contents[-1].append(escape(item))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Result',)
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
