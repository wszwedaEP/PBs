import numpy as np
from mock_data.mock_data import PB_coordinates, households_connected_to_PB
from data_source import DataSource
# from copy import copy

data=DataSource(PB_coordinates,households_connected_to_PB)

class singleHouseholdRearranger:
    def __init__(self, data):
        self.PB_coords = data.PB_coordinates
        self.households_connected_to_PB = data.households_connected_to_PB
        self.single_hh_PB_ids = [PB_id for PB_id in self.households_connected_to_PB.keys()
                                 if len(data.get_details(PB_id))==1]
        self.available_PB_ids = [PB_id for PB_id in self.households_connected_to_PB.keys()
                                 if len(data.get_details(PB_id))<6]

    def is_full(self, PB_id):
        if len(data.get_details(PB_id))<5:
            return False
        else:
            return True

    def rearrange(self):
        while len(set(self.single_hh_PB_ids)) > 1:

            for PB_single_hh in self.single_hh_PB_ids:

                print('Single_PBs {}'.format(self.single_hh_PB_ids))
                temp_available_PB_ids=self.available_PB_ids.copy()
                temp_available_PB_ids.remove(PB_single_hh)

                temp_matrix = np.zeros((len(temp_available_PB_ids), 2))

                for iter_num, PB_candidate in enumerate(temp_available_PB_ids):
                    temp_matrix[iter_num][0]=PB_candidate
                    temp_matrix[iter_num][1]=data.get_distance(PB_candidate, PB_single_hh)

                lowest_distance_row = int(np.where(temp_matrix[:,1]==np.amin(temp_matrix[:,1]))[0])
                best_candidate = int(temp_matrix[lowest_distance_row][0])

                print('curr_single_PB_id {}'.format(PB_single_hh))
                print(temp_matrix)
                print('best_candidate: {}'.format(best_candidate))

                house_id=self.households_connected_to_PB[PB_single_hh][0]
                print('houseID = {}'.format(house_id))

                self.single_hh_PB_ids.remove(PB_single_hh)
                self.available_PB_ids.remove(PB_single_hh)
                self.single_hh_PB_ids.insert(0, 'X')

                print('singleHH after removal = {}'.format(self.single_hh_PB_ids))

                if self.is_full(best_candidate):
                    print('best_candidate {} is full and will not be considered next iteration'.format(best_candidate))
                    self.available_PB_ids.remove(best_candidate)

                print('PBs_available  {}'.format(self.available_PB_ids))

                print('old_image {}'.format(self.households_connected_to_PB))
                self.households_connected_to_PB[best_candidate].append(house_id)
                del self.households_connected_to_PB[PB_single_hh]
                print('new image:  {}'.format(self.households_connected_to_PB))

        return self.households_connected_to_PB


singleHouseholdRearranger(data).rearrange()


