import functools


def save_log(kwargs, res, e_obj, func_name):
    print('save_log')
    print(kwargs)
    print(res)
    print(e_obj)
    print(func_name)


def decorate(_func=None, **options):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            e_obj = res  = None
            try:
                new_args = [a.strip() for a in args]
                res = func(*new_args, **kwargs)
            except Exception as e:
                e_obj = e
                raise e
            finally:
                try:
                    save_log(kwargs, res, e_obj, func.__name__)
                except Exception as e:
                    print(e)

            return res
        return wrapper

    if _func is None:
        print('decorator no _func')
        return decorator
    else:
        print('decorator _func')
        return decorator(_func)


def decorator(func):
    def inner(*args, **kwargs):
        new_args = [a.strip() for a in args]
        res = func(*new_args, **kwargs)
        return res

    return inner


@decorator
def print_don(name: str =''):
    print(f'{name}')

print_don('  don  ')
