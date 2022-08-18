# Robot Navegation
Simulation of an autonomous algorithm that navegates around the streets. The simulation uses a turtlebot and the traffic signals are emulated with numbers. The turtlebot has a vision algorithm that detects the numbers and decide its actions.

---------- FOLLOWBOT -------------------

This robot will detect and follow yellow lines painted on the ground
 
 This can be executed using the map world course inside the folder or using the autorace.launch map from gazebo.

To execute the number detection algorithm, use this command:
  python follower.py
 inside the follower folder once Gazebo is launched.

------------ MAPA -------------------

This folder contains the map used by the robot.

----------ROBOT_NAVEGACION---------------

This robot will drive around a simulated scenario where there will numbers emulating traffic signals.

To execute this packages:

Install the required programs inside requirements.txt this way:
  pip install -r requirements.txt
In order to execute this command, you'll need to have pip previously installed.

Once required packages are installed, inside Robot_navegacion folder, you'll find 3 Python scripts:

  - deteccion_color.py --> This code detects and umbralises blue color in HSV.
  - deteccion_numeros.py --> This code detects and classifies the numbers in the map.
  - navegacion.py --> This code combines the previous 2 with a state machine in order to do the navegation.

To launch this 3 codes, first you have to launch the map on Gazebo, using the next command:
  roslaunch turtlebot_gazebo turtlebot_world.launch world_file:=(ruta al mapa)/mapa
Once the invironment is launched, we are able to launch any of the previous scripts using:
  python (nombre fichero.py)
