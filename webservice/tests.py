from mail import send_mail
from consts import *


def test():
    try:
        send_mail(issue_type,
                  test_title,
                  test_sender,
                  test_sender_url,
                  test_event_url,
                  test_body
                  )
    except BaseException:
        print('Okay')


if __name__ == '__main__':
    test()