import numpy as np
from mock_data.mock_data import PB_coordinates, households_connected_to_PB
from data_source import DataSource
# from copy import copy

data=DataSource(PB_coordinates,households_connected_to_PB)

class singleHouseholdRearranger:
    def __init__(self, data):
        """wczytuje do klasy dane, kolejno:
        * słownik koordynat PB
        * słownik domostw podłączonych do PB
        * tworzy listę PB obsługujących pojedyncze domostwo
        * tworzy listę PB, które mogą obsłużyć dodatkowe domostwa"""
        self.PB_coords = data.PB_coordinates
        self.households_connected_to_PB = data.households_connected_to_PB
        self.single_hh_PB_ids = [PB_id for PB_id in self.households_connected_to_PB.keys()
                                 if len(data.get_details(PB_id))==1]
        self.available_PB_ids = [PB_id for PB_id in self.households_connected_to_PB.keys()
                                 if len(data.get_details(PB_id))<6]

    def is_full(self, PB_id):
        """podczas działanie pętli w metodzie rearrange sprawdza
        czy dany PB będzie w stanie obsłużyć dodatkowe domostwo
        w następnej iteracji"""
        if len(data.get_details(PB_id))<5:
            return False
        else:
            return True

    def rearrange(self):
        '''gdy pętla nie składa się z samych znaków 'X' (zawiera jeszcze pojedyncze PB):
        Podczas iterowania po single_hh_PB_ids ta lista ulega modyfikacji,
        tj. wyrzucane są z niej na bieżąco PB, które już nie są single.
        W związku z tym lista po której iterujemy skraca się i iteracja
        wykonywana jest nieprawidłowo.
        Rozwiązaniem tego problemu jest dostawienie znaku 'X' na początku listy
        gdy usunięty z niej został pojedynczy PB.
        '''
        while len(set(self.single_hh_PB_ids)) > 1:
            'iteruj po liście single PB'
            for PB_single_hh in self.single_hh_PB_ids:

                print('Single_PBs {}'.format(self.single_hh_PB_ids))
                'stwórz tymczasową kopię rozpatrywanych PB, tak żeby nie zawierała id PB który chcemy podłączyć'
                temp_available_PB_ids=self.available_PB_ids.copy()
                temp_available_PB_ids.remove(PB_single_hh)
                'zainicjuj tymczasową macierz, gdzie pierwsza kolumna jest PB id'
                'a druga kolumna jest dystans między rozważanym PB,'
                'a tym dla którego szukamy nowego miejsca'
                temp_matrix = np.zeros((len(temp_available_PB_ids), 2))
                'wypelnij tymczasową macierz wg powyższego'
                for iter_num, PB_candidate in enumerate(temp_available_PB_ids):
                    temp_matrix[iter_num][0]=PB_candidate
                    temp_matrix[iter_num][1]=data.get_distance(PB_candidate, PB_single_hh)
                'znajdz wiersz o najmniejszym dystansie i na tej podstawie'
                'wytypuj najlepszego kandydata, do ktorego podłaczony bedzie single PB'
                lowest_distance_row = int(np.where(temp_matrix[:,1]==np.amin(temp_matrix[:,1]))[0])
                best_candidate = int(temp_matrix[lowest_distance_row][0])

                print('curr_single_PB_id {}'.format(PB_single_hh))
                print(temp_matrix)
                print('best_candidate: {}'.format(best_candidate))

                'wyswietl houseID ktory zmieni swoje miejsce'
                house_id=self.households_connected_to_PB[PB_single_hh][0]
                print('houseID = {}'.format(house_id))

                'usun z listy single PB ten, ktory zostal przepięty do innego PB'
                self.single_hh_PB_ids.remove(PB_single_hh)
                'usun z listy dostępnych PB ten, który własnie zostal przepiety do innego PB'
                self.available_PB_ids.remove(PB_single_hh)
                'aby zachowac dlugosc listy po której iterujemy, dostaw na początek X'
                self.single_hh_PB_ids.insert(0, 'X')

                print('singleHH after removal = {}'.format(self.single_hh_PB_ids))

                'sprawdz czy w nastepnej iteracji PB do którego własnie przypielismy nowe'
                'domostwo, będzie w stanie pomieścić kolejne domostwa'
                if self.is_full(best_candidate):
                    print('best_candidate {} is full and will not be considered next iteration'.format(best_candidate))
                    self.available_PB_ids.remove(best_candidate)

                print('PBs_available  {}'.format(self.available_PB_ids))

                'jak wyglądał słownik PB i domostw przed iteracją'
                print('old_image {}'.format(self.households_connected_to_PB))
                'podepnij domostwo do nowego PB'
                self.households_connected_to_PB[best_candidate].append(house_id)
                'usun ze slownika PB i domostw ten PB, który w tej iteracji zniknął z mapy'
                del self.households_connected_to_PB[PB_single_hh]
                'jak wyglada słownik PB i domostw po iteracji'
                print('new image:  {}'.format(self.households_connected_to_PB))

        'zwroc słownik PB i podpiętych do nich domostw po przejściu całego algorytmu'
        'tj gdy nie ma już single PB'
        return self.households_connected_to_PB

'wykonaj algorytm'
singleHouseholdRearranger(data).rearrange()


