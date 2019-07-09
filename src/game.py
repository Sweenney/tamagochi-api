
import logging
import time
from concurrent.futures import ThreadPoolExecutor
import threading

from person import Person

class Game:

    def __init__(self):
        self.simulation_time_start = time.clock()
        self.simulation_time_end = None
        self.has_ended = False
        self.days = 730000
        self.days_max = 800000
        self.characters_count = 100
        # //self.watching_index = utils.random_integer(0, this.characters_count - 1);
        self.watching_index = None
        self.characters = dict()
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('Game')
        self.generate_random_characters()
        self.play()

    def reset():
        self.simulation_time_start = time.clock()
        self.simulation_time_end = None
        self.has_ended = False
        self.days = 730000
        self.characters = dict()
        self.generate_random_characters()
        self.play()

    def generate_random_characters(self):
        for i in range(self.characters_count):
            p = Person(id=i, game=self, type='random')
            self.characters[i] = p

    def play(self):
        while( self.days < self.days_max ):
            for _, char in self.characters.copy().items():
                # print('Live day %d with [%d/%s]\r' % (self.days, id, len(self.characters)), end="")
                char.live_day()
            self.days += 1
        self.simulation_time_end = time.clock()
        self.has_ended = True
        logging.info("Personnes totales générées: %s en %s s" 
                    % (
                        len(self.characters),
                        (self.simulation_time_end - self.simulation_time_start)
                      )
                    )

    def to_json(self):
        result = dict()
        for id, char in self.characters.items():
            result[id] = char.to_json()
        return result