JWT_LIFITIME_SECONDS = 3600
PASSWORD_MIN_LEN = 3

DONATE_DISTRIBUTION_ATTEMPTS = 100

NAME_MAX_LEN = 100


CHARITY_NAME_EXISTS = 'Проект с таким именем уже существует!'
CHARITY_NAME_INCORRECT = 'Некорректное наименование проекта!'
CHARITY_DESCRIPTION_INCORRECT = 'Некорректное описание проекта!'
CHARITY_SUM_MIN_THEM_INVESTED = 'Сумма не может быть меньше внесённой!'
CHARITY_NOT_FOUND = 'Проект не найден!'
CHARITY_WAS_INVESTED = 'В проект были внесены средства, не подлежит удалению!'
CHARITY_CLOSED = 'Закрытый проект нельзя редактировать!'
CHARITY_EMPTY_NAME = 'Имя не может быть пустым!'
CHARITY_EMPTY_DESCRIPTION = 'Описание не может быть пустым!'

DONATION_ZERRO_ERROR = 'Сумма пожертвования должна быть больше 0'

USER_REMOVE_EXCEPTION = 'Удаление запрещено'


PASSWORD_LENGTH_ERROR = ('Пароль должен быть не меньше '
                         f'{PASSWORD_MIN_LEN} символов')
PASSWORD_CONTAIN_EMAIL_ERROR = 'Пароль не может содержать e-mal'
PASSWORD_ALREADY_REGISTERED = 'Пользователь зарегистрирован.'