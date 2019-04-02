from communication import Communication
from encoder import Encoder


# enc = Encoder('s')
com = Communication(port='/dev/ttyUSB1')
com.write(b'dupa')
