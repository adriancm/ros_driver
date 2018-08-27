from mock import MagicMock
from kobuki.driver import Driver
import pytest

class FakePublisher(object):

    def __init__(self, *args):
        pass

    def publish(self, msg):
        pass


def test_move_forward():
    driver = Driver()
    driver.move_forward()
    assert driver.linear.value == 0.2

def test_move_right():
    driver = Driver()
    driver.move_forward()
    assert driver.linear.value == 0.2

def test_move_left_right():
    driver = Driver()
    driver.move_left()
    driver.move_right()
    assert driver.angular.value == -0.8

def test_move_backward_left():
    driver = Driver()
    driver.move_backward()
    driver.move_left()
    assert driver.angular.value == 0.8
    assert driver.linear.value == -0.2
    
def test_stop():
    driver = Driver()
    driver.angular.value = 1
    driver.linear.value = 1
    driver.stop()
    assert driver.angular.value == 0
    assert driver.linear.value == 0

def test_stop_linear():
    driver = Driver()
    driver.angular.value = 1
    driver.linear.value = 1
    driver.stop(Driver.LINEAR)
    assert driver.angular.value == 1
    assert driver.linear.value == 0

def test_stop_angular():
    driver = Driver()
    driver.angular.value = 1
    driver.linear.value = 1
    driver.stop(Driver.ANGULAR)
    assert driver.angular.value == 0
    assert driver.linear.value == 1
