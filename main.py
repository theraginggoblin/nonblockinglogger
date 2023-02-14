from logger import logger_singleton
from time import sleep

if __name__ == "__main__":
    print("Logging 20 messages")
    for num in range(0, 20):
        logger_singleton.log_message(f"{str(num)}")

    exception_test = False

    if exception_test:
        try:
            raise Exception
        except Exception as e:
            print("caugth exception")

        raise Exception

    print("Sleeping for 3 seconds")
    sleep(3)

    for num in range(0, 10000):
        logger_singleton.log_message(f"{str(num)}")
