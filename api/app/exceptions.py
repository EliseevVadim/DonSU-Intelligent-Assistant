from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь уже существует')

IncorrectEmailOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail='Неверная почта или пароль')

TokenNoFound = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail='Токен не найден')

NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                               detail='Токен не валиден')

NoUserIdException = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail='Пользователь с заданным ID не найден')

ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                   detail='Недостаточно прав')

CantResetPasswordException = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                           detail='Невозможно обновить пароль')

PasswordResetLinkInvalid = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                         detail='Недействительная или устаревшая ссылка для сброса пароля.')

PasswordsMismatch = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                  detail='Указанные пароли не совпадают')

ChatNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Чат не найден')

NoAccessToChat = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                               detail='У Вас нет прав управлять этим чатом')

AppNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Приложение не найдено')

NoAccessToApp = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                              detail='У Вас нет прав управлять этим приложением')
