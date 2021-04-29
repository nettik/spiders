import time
from functools import wraps
from source2.different_type_data.extreme_temperature import main_extreme_temperature
from source2.different_type_data.average_rainfall import main_average_rainfall
from source2.different_type_data.max_rainfall import  main_max_rainfall
from source2.different_type_data.average_pressure import main_average_pressure
from source2.different_type_data.average_temperature import main_average_temperature
from source2.different_type_data.average_humidity import main_average_humidity


def timer(func):
    @wraps(func)
    def wrapper():
        start = time.time()
        func()
        print("\r" + str(round((time.time() - start) / 60, 1)) + "分钟")

    return wrapper


@timer
def main():
    main_average_humidity()


if __name__ == '__main__':
    main()
