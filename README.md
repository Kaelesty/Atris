# Atris
Проект основан на PYGAME.
# Main.py
Main.py включает основной игровой цикл и вторичные функции.
В зависимости от текущего глобального статуса, вызывается соответствующая функция обьекта класса MenuPainter(по факту он все отрисовывает, а не только меню.), выполняющая отрисовку интерфейса.
Глобальные статусы:
	# omm - on main menu
	# wfa - wait for activity
	# gmc - game mode choosing
	# ig-cl - in game classic
	# ig-bt - in game btris
	# ig-wt - in game welltris
	# nts - notes
Main.py также исполняет первичную обработку событий клавиатуры.Вне игр, единственное обрабатываемое событие - нажатие "X"(key=120), исполняющее роль универсальной кнопки возврата.Внутри игр также обрабатываются "A","D","SPACE","ESC","S".При "поимке" этих событий, Main.py вызывает функцию catch экземпляра текущей игры.
Main.py также обрабатывает нажатия на графические кнопки(класса Button), вызывая функцию button_reaction, выполняющуя смену глобального статуса.

# Menu_painter.py
Menu_painter.py занимается отрисовкой интерфейса и хранением экземпляров игровых классов.
При изменении глобального статуса, извне вызываются функции из группы "init", выполняющие настройку MenuPainter для текущего глобального статуса.Далее, при каждом проходе основного игрового цикла, вызывается соответствующая функция отрисовки(группа "draw").
При инициализации глобальных статусов из группу "ig" также создается экземпляр класса соответствующей игры.

# Button.py
Button является наследником pygame.sprites.Sprite.Выполняет функцию экранной кнопки.При наведении/нажатии автоматически меняет внешний вид по средством изменения статуса.
Статусы:
	ps - pressed
	uw - under view
	st - standart
При нажатии, через Main.py вызывается button_reaction, получающая имя Button.

# Игровые режимы Tetris/Welltris
	# GAME MODES:
	# easy : показывается след. фигура, можно вращать фигуры на паузе
	# normal : нельзя вращать фигуры на паузе
	# hard : след. фигура не показывается

# Tetris.py
Tetris храниться в MenuPainter, при каждой отрисовке себя также выполняет шаг, включающий проверку возможности спуска, выполняет спуск.
При нажатии "A","D" выполняется проверка на сдвиг, сдвиг
При нажатии "S" выполняется сброс, вызывающий шаг пока возможен спуск.
При нажатии "ESC" игра ставится на паузу/снимается с паузы
При нажатии "SPACE" выполняет проверка на поворот, поворот

# Welltris.py 
Механика аналогична Tetris.
Отрисовка поля выполняется автоматически, с понижаюими коэфицентами.

# Btris.py
При "взятии" фигуры в Main.py меняет значение флаг _follow_bt.При его значении True, каждый проход цикла в Btris передается положение мыши.
