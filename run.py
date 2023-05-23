from main import MyView, app
import threading

from static_space_handlers import avatars_size

if __name__ == '__main__':
    general_view = MyView('flask.db')
    general_view.associate_funcs()

    threading.Timer(600, avatars_size, ['/static/avatars', 5]).start()

    app.run(debug=True)
