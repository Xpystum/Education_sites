from flask import Flask, render_template, request  # requst and render html pages
from vsearch import search_4_letters  # my func - using my func in project
# Экранирование что бы браузер не воспринимал текст как теги например "< or >"
from flask import escape
from ua_parser import user_agent_parser
from db.DBcm import DbConfing, UseDatabase



app = Flask(__name__)

#Функции
def log_request_text(req, res: str) -> None:
    with open('vsearch.log', 'a') as log:
         req_user_browser = user_agent_parser.Parse(req.user_agent.string)['user_agent']['family']
         print(req.form, req.remote_addr, req_user_browser, res, file=log, sep = "|")

def log_request(req, res: str) -> None:  # Работа с Базой данных

    app.config['DbConfing'] = DbConfing("127.0.0.1", "root", 3306 ,"1911" , "vsearchlogdb") # поместили данные о подключении в объект
    #Для гибкости лучше использовать паттерн абстрактная фабрика (Что бы мы могли менять субд не переписывая наши объекты)
    

    try:
           
        with UseDatabase(app.config['DbConfing']) as cursor: #Организовали наш класс с менеджером контекста к бд
            print("Successfully connected")
            print('"#' * 20)
            _SQL = "insert into log (`phrase`, `letters`, `ip`, `browser_string`, `result`) VALUES (%s, %s, %s, %s, %s)"
            req_user_browser = user_agent_parser.Parse(req.user_agent.string)['user_agent']['family']
            cursor.execute(_SQL, (req.form['phrase'],
                                        req.form['letters'],
                                        req.remote_addr,
                                        req.user_agent.string,
                                        req_user_browser,))
            print("Commit - is add in Date Base")


    except Exception as ex:  # Ловим ошибку при покдлючении к бд или при работе
        print("Connection refused Date Base or inside the context manager `with` ")
        print(ex)



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

  

@app.route('/')
@app.route('/entry')
def entry_page() -> 'str':
    return render_template('entry.html',
                           the_title='Welcome to search4letterson the web')


@app.route('/viewlog')
def view_the_log() -> 'str':

    with UseDatabase(app.config['DbConfing']) as cursor:
        _SQL = "select phrase, letters, ip, browser_string, result from log"

                   
        cursor.execute(_SQL)
        result = cursor.fetchall() #возвращает данные в зависимости от запроса (в данном примере словарь)

        lits_result = [] 
        for a in result:
            lits_result.append(escape(list(a.values()))) #нужно для того т.к fetchall() - теперь возвращает словарь
            

    titles = ('Phrase','Letters', 'Remote_addr', 'User_agent', 'Result',)
    return render_template('viewlog.html',
                           the_title='View_Log',
                           the_row_titles=titles,
                           the_data = lits_result,)

         

if __name__ == '__main__':
    app.run(debug=True)
