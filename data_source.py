from typing import Dict, List, Tuple
import random
import numpy as np
#random.seed(43)
# random.randrange(0, 10)

class DataSource:

    def __init__(self, PB_coordinates, households_connected):
        self.PB_coordinates = PB_coordinates
        self.households_connected_to_PB = households_connected
        pass

    def get_details(self, PB_id):
        """zwraca listę domów podpiętą do danego PB"""
        return self.households_connected_to_PB[PB_id]


    def get_distance(self, PB_id1, PB_id2):
        """wylicza dystans pitagorasowy między dwoma PB, a następnie
        dodaje losowy narzut reprezentujący przeszkody na drodze światłowodu"""

        a=self.PB_coordinates[PB_id1][0]**2 + self.PB_coordinates[PB_id2][0]**2
        b=self.PB_coordinates[PB_id1][1]**2 + self.PB_coordinates[PB_id2][1]**2
        c=random.randrange(-7,7)
        return np.sqrt(a+b) + c






