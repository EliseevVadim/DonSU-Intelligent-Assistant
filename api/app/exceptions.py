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
