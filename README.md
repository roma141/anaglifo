# anaglifo
Google Earth y otros servicios gratuitos proveen curvas de nivel promedio, es decir aproximadas para la resoluciòn que ellos manejan
Con otros servicios se pueden conseguir fotografías aéreas que pueden dar mayor resolución a estas curvas.
Un programa como Qgis permite obtener estas curvas.

Hay programas que permiten crear modelos 3D a partir de varias fotografías o de un video, pero no he encontrado que lo hagan a partir de un solo un par.
El problema de hacerlo automáticamente creando uno programa similar es que es necesario establecer los puntos correspondientes en cada foto y no se como hacerlo.

Con esa nube de puntos se utilizan programas stándar para generar las curvas. Luego hay que corregirlas mirando las fotos.

O se puede con esos puntos en 3D armar una mesh, luego corregirla mirando la foto, luego cortala en tajadas horizontales para obtener las curvas, después proyectar los bordes
de estas tajadas en el plano horizontal y al fin obtener las curvas. Es un proceso largo y complicado.

Con este programa estoy ensayando la idea de tomar las curvas generadas por estos programas y montarlas en las fotografías aéreas, ajustando las fotos
con las curvas que ya están georeferenciadas.
Esto se hace generando un anaglifo donde se hace este ajuste.
Luego de que estén ajustadas se procede a mover las curvas para que se ajusten al terreno visto en las fotos.
Como las fotos tienen mayor detalle toca agregar puntos a las curvas y tambien agregar otras curvas.
Las curvas mantienen su altura, lo que cambia es su posición horizontal

En este sistema se obtienen las curvas ya corregidas con la foto. Me parece como más simple y rápido este camino, por esto lo estoy haciendo.

Las curvas se graban en .ply para ser leídas por los progamas estándar com Qgis
