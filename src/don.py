
def deco(func):
    def inner(*args, **kwargs):
        new_args = tuple(
            arg.strip().lower() if isinstance(arg, str) else arg.lower() for arg in args
        )
        return func(*new_args, **kwargs)
    return inner

@deco
def doan(text=''):
    print(f"'{text}'")

if __name__ == "__main__":
    doan(" te  ")