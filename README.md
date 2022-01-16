# RobotNavegacion
Simulación de un Turtlebot navegando por calles con señales simuladas con números

---------- FOLLOWBOT -------------------

Este robot detectará y seguirá las lineas amarillas que encuentre en el suelo.
 
Puede ser ejecutado utilizando el world course que viene incluido en la carpeta o utilizar el mapa autorace.launch 
del paquete del turtlebot3_gazebo, que también dispone de una línea amarilla.

Para ejecutar el algoritmo de detección y seguimiento, utilizar el comando:
  python follower.py
dentro de la carpeta follower una vez lanzado el gazebo con el mapa.

------------ MAPA -------------------

Esta carpeta contiene el mapa utilizado para el robot navegacion

----------ROBOT_NAVEGACION---------------

Este robot circulará por un escenario simulado en el que habrán números que simulen señales de tráfico, que el robot respetará.

Para ejecutar estos paquetes:

instalar los programas necesarios dentro de requirements.txt utilizando el comando:
  pip install -r requirements.txt
Para poder ejecutar este comando, se debe tener pip instalado previamente.

Una vez instalar los paquetes necesarios, dentro de la carpeta Robot_navegacion se encuentran 3 ficheros de python:

  - deteccion_color.py --> Este código realiza la deteccion y umbralización del color azul en HSV.
  - deteccion_numeros.py --> Este código realiza la detección y clasificación de los números del mapa.
  - navegacion.py --> Este código combina los dos anteriores junto a una máquina de estados para realizar la nacegación por el mapa.

Para lanzar cualquiera de los 3 anteriores códigos, primero se debe lanzar el mapa en gazebo, utilizando el siguiente comando
  roslaunch turtlebot_gazebo turtlebot_world.launch world_file:=(ruta al mapa)/mapa
Una vez lanzado el entorno, y dentro de la carpeta Robot_navegacion, podemos lanzar cualquiera de los algoritmos anteriores utilizando:
  python (nombre fichero.py)
