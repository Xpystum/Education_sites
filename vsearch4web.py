from flask import Flask, render_template, request, session,  copy_current_request_context  # requst and render html pages
from vsearch import search_4_letters  # my func - using my func in project
# Экранирование что бы браузер не воспринимал текст как теги например "< or >"
from flask import escape
from ua_parser import user_agent_parser
from db.DBcm import DbConfing, UseDatabase, ConnectionError, CredentialsError, SQLError
import os #Для рамнонизации секретного ключа
from threading import Thread
import time




app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(
    SECRET_KEY = os.urandom(24)
)



app.secret_key = app.config['SECRET_KEY'];


#region Функции Логирования и работы с бд

def log_request_text(req, res: str) -> None:
    with open('vsearch.log', 'a') as log:
         req_user_browser = user_agent_parser.Parse(req.user_agent.string)['user_agent']['family']
         print(req.form, req.remote_addr, req_user_browser, res, file=log, sep = "|")


# def log_request(req, res: str) -> None:  # Работа с Базой данных

    # app.config['DbConfing'] = DbConfing("127.0.0.1", "root", 3306, "1911", "vsearchlogdb") # поместили данные о подключении в объект
    # #Для гибкости лучше использовать паттерн абстрактная фабрика (Что бы мы могли менять субд не переписывая наши объекты)
   

    # try:
        
    #     time.sleep(10) #сделано для тестирование многопоточности
    #     with UseDatabase(app.config['DbConfing']) as cursor: #Организовали наш класс с менеджером контекста к бд
    #         print("Successfully connected")
    #         print('"#' * 20)
    #         _SQL = "insert into log (`phrase`, `letters`, `ip`, `browser_string`, `result`) VALUES (%s, %s, %s, %s, %s)"
    #         req_user_browser = user_agent_parser.Parse(req.user_agent.string)['user_agent']['family']
    #         cursor.execute(_SQL, (req.form['phrase'],
    #                                     req.form['letters'],
    #                                     req.remote_addr,
    #                                     req.user_agent.string,
    #                                     req_user_browser,))
    #         print("Commit - is add in Date Base")


    # except Exception as ex:  # Ловим ошибку при покдлючении к бд или при работе
    #     print("Connection refused Date Base or inside the context manager `with` ")
    #     print(ex)
#endregion


@app.route('/search4', methods=['POST'])
def do_search() -> str:
    """Функция для вывода и постановки в шаблон наших значений в html шаблоне
    с помощью junja2
    """

    #region Функции Логирования и работы с бд
    log_request_text(request, str(search_4_letters(
        request.form['phrase'], request.form['letters']))) # запись в лог
   
    @copy_current_request_context 
    def log_request(req, res: str) -> None:  # Работа с Базой данных
        #Мы добавили определение и код функции для работы с бд в do_search(), т.к декоратор фласка

        app.config['DbConfing'] = DbConfing("127.0.0.1", "root", 3306, "1911", "vsearchlogdb") # поместили данные о подключении в объект
        #Для гибкости лучше использовать паттерн абстрактная фабрика (Что бы мы могли менять субд не переписывая наши объекты)
    
        try:
            
            time.sleep(10) #сделано для тестирование многопоточности
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
    #endregion

    try: #ловим ошибку при работе с БД
        th = Thread(target=log_request, args=(request, str(search_4_letters(
                                                        request.form['phrase'], 
                                                        request.form['letters'])))) #Записываем в объект многопоточность и функцию с которой будем работать
        th.start() #Запуск многопоточности
        # log_request(request, str(search_4_letters(
        #     request.form['phrase'], request.form['letters'])))  # вызываем функция которая будет записывать в бд
    except Exception as err:
        print(f"********************* \n Ошибка при подключении к БД: {err}")

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
# @checkk_logged_in
def view_the_log() -> 'str':

    try:
        with UseDatabase(app.config['DbConfing']) as cursor:
            _SQL = "select phrase, letters, ip, browser_string, result from log"

                    
            cursor.execute(_SQL)
            result = cursor.fetchall() #возвращает данные в зависимости от запроса (в данном примере словарь)

            lits_result = []
            for a in result:
                lits_result.append(list(a.values())) #нужно для того т.к fetchall() - теперь возвращает словарь

        titles = ('Phrase','Letters', 'Remote   _addr', 'User_agent', 'Result',)
        return render_template('viewlog.html',  
                            the_title='View_Log',
                            the_row_titles=titles,
                            the_data = lits_result,)

    except ConnectionError as err:
        print("Ошибка к подключении к БД: Мы обратились к БД ещё не подключившийся к ней.")
        print(err)
    except SQLError as err:
        print('Is your query correct? Error:', str(err))
    except CredentialsError as err:
        print("User-id/Password issues. Error:", )
    except Exception as err:
        print("Something went wrong:", str(err))
    return 'Eror'
  
@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are now logged in.'

@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out.'



app.secret_key = app.config['SECRET_KEY'];

if __name__ == '__main__':
     app.run(debug=True)
