import threading
import time

from ThreadResource import ThreadResource

class ArmJoint(ThreadResource):
    """
    Controls a joint on the arm. A joint is a combination of a JointController (to move the joint) and an encoder
    (to determine relative movement of the JointController).

    The ArmJoint begins in an indeterminate state where you may move the joint relatively using `setSpeed`, but since no
    absolute position is available you must initialise it by moving the joint to a known angle and calling `initCurrentAngle`.
    After this the joint tracks its position relative to the encoder turn value taken when `initCurrentAngle` was called 
    and will enforce the min and max angles so the JointController will stay within them.

    `encoderAngleRatio` is the number of encoder turn counts that correspond to 360deg rotation of the joint. A negative
    value represents the encoder and JointController speed being opposite polarity to one another.

    TODO: impl moveToAngle (or is this part of some higher controller - moves multiple joint in unison)
    """

    minPosition = None

    def __init__(self, jointController, encoder, encoderValueIndex: int, maxAngle: int, encoderAngleRatio: float):
        super().__init__()

        self.jointController = jointController
        self.encoder = encoder
        self.encoderValueIndex = encoderValueIndex

        self.maxAngle = maxAngle
        self.encoderAngleRatio = encoderAngleRatio

    def loop(self):
        if self.minPosition:
            currentAngle = self.getAngle()
            controllerSpeed = self.jointController.getSpeed()

            # limit is breached if position is outside boundary and controller is actively
            # taking it further out (as opposed to it trying to come back inside the limits)
            lowerLimitBreach = currentAngle <= 0 and controllerSpeed < 0
            upperLimitBreach = currentAngle >= self.maxAngle and controllerSpeed > 0

            if lowerLimitBreach or upperLimitBreach:
                self.jointController.setSpeed(0)
            
        time.sleep(0.1)

    """
    Set the speed of the underlying JointController
    """
    def setSpeed(self, speed: float):
        self.jointController.setSpeed(speed)

    # def moveToAngle(self, angle: float):
    #     pass # TODO: impl me!

    """
    Given the angle and the current encoder turn value, set the minimum position of this joint 
    """
    def initCurrentAngle(self, angle):
        self.minPosition = self.encoder.getTurns(self.encoderValueIndex) - ((self.encoderAngleRatio * angle) / 360)

    """
    Get the current angle of this joint based on the current turn value take nfrom the encoder.
    Note that the minimum position must be set using `setMinPosition` otherwise None is returned.
    """
    def getAngle(self):
        if self.minPosition is None:
            return None
        
        return (self.encoder.getTurns(self.encoderValueIndex) - self.minPosition) / self.encoderAngleRatio * 360

    def __str__(self):
        angle = self.getAngle()

        return 'ARMJOINT({0}): thread={1} ang={2}deg maxAng={3}'.format(
            self.jointController,
            "Alive" if self.thread.is_alive() else "DEAD",
            "{:.1f}".format(angle) if not angle is None else "-",
            self.maxAngle
        )
