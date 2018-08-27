from multiprocessing import Value
from multiprocessing import Process

class Driver(object):

    LINEAR = 'linear'
    ANGULAR = 'angular'

    #STEP
    LINEAR_STEP_SPEED = 0.05
    ANGULAR_STEP_SPEED = 0.2

    #MAX
    MAX_LINEAR_SPEED = 0.5
    MAX_ANGULAR_SPEED = 1

    def __init__(self):
        self.linear = Value('d', 0.0)
        self.angular = Value('d', 0.0)

    def move_forward(self):
        self.linear.value = self.MAX_LINEAR_SPEED

    def move_backward(self):
        self.linear.value = -self.MAX_LINEAR_SPEED

    def move_right(self):
        self.angular.value = -self.MAX_ANGULAR_SPEED

    def move_left(self):
        self.angular.value = self.MAX_ANGULAR_SPEED

    def stop(self, direction=None):
        if direction == self.LINEAR:
            self.linear.value = 0
        elif direction == self.ANGULAR:
            self.angular.value = 0
        else:
            self.angular.value = 0
            self.linear.value = 0

    def start(self):
        self.publisher_process = Process(target=self.publish_message, args=())
        self.publisher_process.start()

    @staticmethod
    def acceleration(current_speed, desired_speed, step_speed):
        if current_speed == desired_speed:
            pass
        elif current_speed < desired_speed:
            current_speed += step_speed
            if current_speed > desired_speed:
                current_speed = desired_speed
        elif current_speed > desired_speed:
            current_speed -= step_speed
            if current_speed < desired_speed:
                current_speed = desired_speed
        return current_speed

    def publish_message(self):
        import rospy
        from rospy import Publisher
        from geometry_msgs.msg import Twist

        rospy.init_node('move')
        rospy.loginfo("About to be moving!")
        publisher = Publisher('mobile_base/commands/velocity', Twist)
        twist = Twist()
        while True:
            rospy.loginfo("Current/Desired/Step Linear Speed: " +  str(twist.linear.x) + "/" + str(self.linear.value) +"/"+ str(self.LINEAR_STEP_SPEED))
            rospy.loginfo("Current/Desired/Step Angular Speed: " +  str(twist.angular.z) + "/" + str(self.angular.value) +"/"+ str(self.ANGULAR_STEP_SPEED))
            twist.linear.x = Driver.acceleration(current_speed=twist.linear.x, desired_speed=self.linear.value, step_speed=self.LINEAR_STEP_SPEED)
            twist.angular.z = Driver.acceleration(current_speed=twist.angular.z, desired_speed=self.angular.value, step_speed=self.ANGULAR_STEP_SPEED)
            publisher.publish(twist)
            rospy.sleep(0.1)
