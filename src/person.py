
import random
import statistics
import time

import utils
import data as DATA

class Person:

    def __init__(self, id, game, type='random', parent_1=None, parent_2=None):
        self.id = id
        self.game = game
        self.type = type
        self.parent_1 = parent_1
        self.parent_2 = parent_2
        self.kids = list()
        self.is_alive = True
        self.relationships = dict()
        self.in_love_with = None
        self.job = None
        self.company = None
        self.education_level = 0
        self.school_sucess = 0
        self.timeline = list()
        self.add_to_timeline(type='birth', data={'date': self.game.days})

        self.gender = "M" if utils.boolean_from_random(DATA.STAT_MEN) else "F"
        sexuality_index = utils.index_from_random([d['percentage'] for d in DATA.STAT_SEXUALITY[self.gender]])
        self.sexuality = DATA.STAT_SEXUALITY[self.gender][sexuality_index]['name']

        self.firstname = random.choice(DATA.FIRSTNAMES[self.gender])

        if self.type is 'random':
            self.initialize_from_nothing()
        elif self.type is 'genetic':
            self.initialize_from_parents()
        elif self.type is 'adoption': 
            self.initialize_from_adoption()

        self.generate_interests_from_traits()

        # setTimeout(
        # function() {
        #     self.live_day();
        # }.bind(self.,
        # 5000
        # );


    def add_to_timeline(self, type, data):
        self.timeline.append({'type': type, 'data': data})

    def generate_interests_from_traits(self):
        self.interests = sorted(
                            utils.profile_distances_from_array(self.traits, DATA.INTERESTS),
                            key=lambda o: o['distance']
                            )[:2]


    def initialize_from_nothing(self):
        self.age = 9125 # Is equal à 25 years old
        self.stage_of_life = "adult"
        self.remaining_days = DATA.MAX_AGE - 9125
        self.lastname = random.choice(DATA.LASTNAMES)
        # self.city = random.choice(DATA.CITIES);
        self.city = DATA.CITIES[0]
        self.traits = {
            'logic': random.randint(1, 10),
            'creativity': random.randint(1, 10),
            'sociability': random.randint(1, 10),
            'kindness': random.randint(1, 10),
            'joviality': random.randint(1, 10),
            'humour': random.randint(1, 10), # humor a la base (err?)
            'romantism': random.randint(1, 10),
            'spontaneity': random.randint(1, 10),
            'dynamism': random.randint(1, 10),
            'ego': random.randint(1, 10),
            'sanity': random.randint(1, 10),
            'perfectionism': random.randint(1, 10),
            'openness': random.randint(1, 10)
        }
        self.education_level = random.randint(0, 5)

    def initialize_from_adoption(self):
        self.initialize_from_nothing()
        self.age = 1642 # Is equal à 25 years old
        self.stage_of_life = "child"
        self.lastname = self.game.characters[self.parent_1].lastname
        self.city = self.game.characters[self.parent_1].city

    def initialize_from_parents(self):
        self.age = 0
        self.stage_of_life = "baby"
        self.remaining_days = DATA.MAX_AGE
        self.lastname = self.game.characters[self.parent_1].lastname
        # self.city = random.choice(DATA.CITIES)
        self.city = self.game.characters[self.parent_1].city
        self.traits = {
            'logic': statistics.mean([
                self.game.characters[self.parent_1].traits['logic'],
                self.game.characters[self.parent_2].traits['logic']
            ]),
            'creativity': statistics.mean([
                self.game.characters[self.parent_1].traits['creativity'],
                self.game.characters[self.parent_2].traits['creativity']
            ]),
            'sociability': statistics.mean([
                self.game.characters[self.parent_1].traits['sociability'],
                self.game.characters[self.parent_2].traits['sociability']
            ]),
            'kindness': statistics.mean([
                self.game.characters[self.parent_1].traits['kindness'],
                self.game.characters[self.parent_2].traits['kindness']
            ]),
            'joviality': statistics.mean([
                self.game.characters[self.parent_1].traits['joviality'],
                self.game.characters[self.parent_2].traits['joviality']
            ]),
            'humour': statistics.mean([
                self.game.characters[self.parent_1].traits['humour'],
                self.game.characters[self.parent_2].traits['humour']
            ]),
            'romantism': statistics.mean([
                self.game.characters[self.parent_1].traits['romantism'],
                self.game.characters[self.parent_2].traits['romantism']
            ]),
            'spontaneity': statistics.mean([
                self.game.characters[self.parent_1].traits['spontaneity'],
                self.game.characters[self.parent_2].traits['spontaneity']
            ]),
            'dynamism': statistics.mean([
                self.game.characters[self.parent_1].traits['dynamism'],
                self.game.characters[self.parent_2].traits['dynamism']
            ]),
            'ego': statistics.mean([
                self.game.characters[self.parent_1].traits['ego'],
                self.game.characters[self.parent_2].traits['ego']
            ]),
            'sanity': statistics.mean([
                self.game.characters[self.parent_1].traits['sanity'],
                self.game.characters[self.parent_2].traits['sanity']
            ]),
            'perfectionism': statistics.mean([
                self.game.characters[self.parent_1].traits['perfectionism'],
                self.game.characters[self.parent_2].traits['perfectionism']
            ]),
            'openness': statistics.mean([
                self.game.characters[self.parent_1].traits['openness'],
                self.game.characters[self.parent_2].traits['openness']
            ])
        }

    #@utils.timer
    def compute_age(self):
        self.age += 1
        if self.age < 3 * 365:
            self.stage_of_life = "baby"
        elif self.age < 12 * 365:
            self.stage_of_life = "child"
        elif self.age < 18 * 365:
            self.stage_of_life = "teen"
        elif self.age < 25 * 365:
            self.stage_of_life = "young_adult"
        elif self.age < 70 * 365:
            self.stage_of_life = "adult"
        else:
            self.stage_of_life = "elder"
    
    #@utils.timer
    def compute_job(self):
        if self.stage_of_life in ['adult', 'young_adulte'] and not self.job:
            employed = utils.boolean_from_random(DATA.STAT_EMPLOYMENT[self.education_level])
            if employed:
                job = random.choice(DATA.JOBS[self.education_level])
                self.job = job[self.gender]
                self.company = random.choice(job['companies'])
                self.add_to_timeline('new_job', {'age': self.age, 'job': self.job, 'company': self.company})

    #@utils.timer
    def compute_studies(self):
        pass

    #@utils.timer
    def compute_new_relationships(self):
        #persons_pool = random.choices(self.game.characters, k=10)
        for _, person in self.game.characters.items():
            if self.id != person.id and person.id not in self.relationships.keys() and person.is_alive and self.city == person.city:
                bonus_job = DATA.BONUS_MEET_JOB if not self.job and self.job == person.job else 0
                bonus_company = DATA.BONUS_MEET_COMPANY if not self.company and self.company == person.company else 0
                bonus_interest = len([i for i in self.interests if i in person.interests]) * DATA.BONUS_MEET_INTEREST
                chance_to_meet = utils.boolean_from_random(DATA.STAT_MEET + bonus_job + bonus_company + bonus_interest)
                if chance_to_meet:
                    self.add_new_relationship(person)

    #@utils.timer
    def add_new_relationship(self, person):
        if person.id not in self.relationships.keys():
            self.relationships[person.id] = {
                'started': self.age,
                'type': 'acquaintance',
                'level': 0,
                'person': person.id,
                'bonus': 0,
            }
            person.add_new_relationship(self)

    #@utils.timer
    def compute_social_contacts(self):
        for id, relation in self.relationships.items():
            person = self.game.characters[id]
            if relation['bonus'] == 0:
                bonus_job = DATA.BONUS_CONTACT_JOB if self.job and self.job == person.job else 0
                bonus_company = DATA.BONUS_CONTACT_COMPANY if self.company and self.company == person.company else 0
                bonus_interest =  len([i for i in self.interests if i in person.interests]) * DATA.BONUS_CONTACT_INTEREST
                relation['bonus'] = DATA.STAT_CONTACT + bonus_job + bonus_company + bonus_interest
            chance_to_contact = utils.boolean_from_random(relation['bonus'])
            if chance_to_contact:
                relation['level'] += 1 if relation['level'] < 100 else 0
            if relation['type'] == 'loved_one':
                if relation['level'] == 100:
                    self.have_child(person)
            else:
                if relation['level'] > 80:
                    if self.compute_sexual_compatibility(person):
                        relation['type'] = 'loved_one'
                        self.in_love_with = id
                        person.in_love_with = self.id
                        self.add_to_timeline(type='found_love', data={
                            'age': self.age,
                            'person': {
                                'id': self.in_love_with,
                                'firstname': person.firstname,
                                'lastname': person.lastname
                            }
                        })
                        person.add_to_timeline(type='found_love', data={
                            'age': person.age,
                            'person': {
                                'id': self.id,
                                'firstname': self.firstname,
                                'lastname': self.lastname
                            }
                        })
                    else:
                        relation['type'] = 'best_friend'
                elif relation['level'] > 60:
                    relation['type'] = 'friend'
                elif relation['level'] > 40:
                    relation['type'] = 'buddy'
                elif relation['level'] < 0:
                    relation['type'] = 'enemy'

    def have_child(self, person):
        if len(self.kids) < 2:
            id = "%s+%s#%d" % (self.id, person.id, len(self.kids))
            genetic = self.gender != person.gender
            type = 'genetic' if genetic else 'adoption'
            p = Person(id=id, parent_1=self.id, parent_2=person.id, type=type, game=self.game)
            self.game.characters[id] = p
            self.add_child(p)
            person.add_child(p)

    def add_child(self, child):
        self.kids.append(child.id)
        self.add_to_timeline(type='new_child', data={
            'age': self.age,
            'child': {
                'id': child.id,
                'firstname' : child.firstname,
                'lastname' : child.lastname
            }
        })

    def compute_sexual_compatibility(self, person):
        if self.in_love_with or person.in_love_with or self.stage_of_life not in ["young_adult", "adult", "elder"]:
            return False
        else:
            same_gender = self.gender == person.gender
            if self.sexuality is 'hetero':
                compatibility = not same_gender and person.sexuality in ['hetero', 'bi']
            elif self.sexuality is 'homo':
                compatibility = same_gender and person.sexuality in ['homo', 'bi']
            elif self.sexuality is 'bi':
                compatibility = (not same_gender and person.sexuality in ['hetero', 'bi']) or (same_gender and person.sexuality in ['homo', 'bi'])
            else:
                raise Exception('Sexuality unknown: %s' % self.sexuality)
            return compatibility

    #@utils.timer
    def compute_death(self):
        self.remaining_days -= self.random_life_shit() # at least 1 days or more because life is a bitch
        self.is_alive = self.remaining_days > 0
        if not self.is_alive:
            self.add_to_timeline(type='death', data={'age': self.age})

    def random_life_shit(self):
        shit_chance = random.random()
        if shit_chance < 0.0001:
            if self.age < 25 * 365:
                shit = 5
                shit_gravity = random.random() * 50
            elif self.age < 50 * 365:
                shit = 15
                shit_gravity = random.random() * 150
            elif self.age < 80 * 365:
                shit = 50
                shit_gravity = random.random() * 500
            else:
                shit = 100
                shit_gravity = random.random() * 100
            return 1 + (shit * shit_gravity)
        else:
            return 1

    #@utils.timer
    def live_day(self):
        if self.is_alive:
            self.compute_age()
            self.compute_job()
            self.compute_studies()
            self.compute_new_relationships()
            self.compute_social_contacts()
            self.compute_death()

    def to_json(self):
        invalid = ['game']
        return {x: self.__dict__[x] for x in self.__dict__ if x not in invalid}