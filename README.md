# Robot Arm Control
Intended to run on a Raspberry Pi (any version)

## Setup

To install required packages:
```
pip3 install -r requirements.txt
```

## Implemented Control Devices
### Motor
Used to communicate with a DC motor driver (__DRV8838__ in my case), controlling it's `phase` pin for direction and PWM'ing it's `enable` pin to get speed control

### Stepper
Used to communicate with a stepper motor driver (__A4988__ in my case), controlling it's `dir` pin for direction and alternating it's `step` pin within a thread to get speed control (currently speed is hardcoded; the switching rate is given by `dutySleep`)
