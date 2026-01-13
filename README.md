# bipedal_sw

Software for bipedal robot.

## Contents

- calibrate.py — centers motors for easier assembly
- read_motor_positions.py — read motor positions  
- write_motor_positions.py — command motor positions  
- playback.py — replay recorded motion  
- gaits/ — gait and motion data  

## Setup

Clone the repository with submodules:

    git clone --recurse-submodules https://github.com/rubieluo/bipedal_sw.git
    cd bipedal_sw

Virtual environment:

```
    python3 -m venv .venv
    source .venv/bin/activate
```

Install the submodule

    `pip install st-3215`

## Usage
Use calibrate to center the motors and assemble the robot in its zero position. Read and write motor positions is used for testing to make sure motors and communication is working. Playback is used to run a gait from the `gait` folder on the robot. The gaits are generated using [this repo](https://github.com/rubieluo/bipedal_reference_motion). 
```
    python calibrate.py
    python read_motor_positions.py
    python write_motor_positions.py
    python playback.py
```
