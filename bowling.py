#!/usr/bin/python

""" A bowling game/score modeling. """

# A player a described by his name and his strike, spare skills

# the spare prob is the probability that the player make a spare given that
# he already missed the strike (for more fan we can also model the spare
# probability in function of the number if left pins but also in function of
# their configuration if we store this information)

class Frame(object):

    def sanity_check(self):
        assert len(self.throws) <= self.throws_nbr
        assert sum(self.throws) <= self.pins_nbr

    def __init__(self, pins_nbr=10, throws_nbr=2, throws=None):
        """ Init a frame with the number of initial wooden pins and the
        maximum number of tries (throws) """
        self.pins_nbr = pins_nbr
        self.throws_nbr = throws_nbr

        if throws is None:
            self.throws = []
        else:
            self.throws = throws
            if len(self.throws):
                self.sanity_check() # runs sanity_check
                assert self.complete() # assert completeness


    def __str__(self):
        return '({}, {}) [{}]'.format(self.throws_nbr, self.pins_nbr ,
            ', '.join(map(str, self.throws)))


    def add_throw(self, down_pins=0):
        """ adds a try to the frame """
        current_score = sum(self.throws)
        if len (self.throws) < self.throws_nbr and current_score<self.pins_nbr:
            assert down_pins <= self.pins_nbr
            if (current_score + down_pins) <= self.pins_nbr:
                self.throws.append(down_pins)

    def is_strike(self):
        return 1 == len(self.throws) and sum(self.throws) == self.pins_nbr

    def is_spare(self):
        return len(self.throws)>1 and sum(self.throws) == self.pins_nbr

    def is_new(self):
        return len(self.throws) == 0

    def get_score(self):
        # if not self.complete():
        #     print "partial score !"
        return sum(self.throws)

    def get_throws_nbr(self):
        return len (self.throws)

    def get_throws(self):
        return self.throws

    def set_strike(self):
        self.throws = [self.pins_nbr]

    def set_throws(self, throws):
        """ Set complete frame throws (alternative to add them one by one) """
        if len(throws) <= self.throws_nbr and sum(throws)<=self.pins_nbr:
            if len(throws) == 1 :
                if not sum(throws) == self.pins_nbr:
                    return False
            if throws[0] == self.pins_nbr:
                if not len(throws) == 1 :
                    return False
            self.throws = throws
            return True
        return False

    def complete(self):
       return self.get_throws_nbr() == self.throws_nbr or self.get_score() == self.pins_nbr

class Ball(Frame):
    def __init__(self, pins_nbr=10):
        super(self.__class__, self).__init__(pins_nbr=pins_nbr, throws_nbr=1)


from random import random, randint

class Player:

    def __init__(self, n_name, strike_prob=0.7, spare_prob=0.5):
        self.n_name = n_name
        self.frames = []
        self.strike_prob = strike_prob
        self.spare_prob = spare_prob

    def play_frame(self, frame):
        assert issubclass(frame.__class__, Frame) # to play also extra Ball(s)
        assert frame.is_new()
        if self.strike_prob > random():
            frame.set_strike() # it's a strike
            self.frames.append(frame)
            return frame.complete()

        else:
            frame.add_throw(randint(1, frame.pins_nbr-1))
            while not frame.complete():
                if self.spare_prob > random():
                    frame.add_throw(frame.pins_nbr-frame.get_score())
                else:
                    frame.add_throw(randint(0, frame.pins_nbr-frame.get_score()-1))
            self.frames.append(frame)
            return frame.complete()

    def add_frame(self, frame):
        assert issubclass(frame.__class__, Frame) # to add also extra Ball(s)
        self.frames.append(frame)

    def print_frames(self):
        print 'Frames:'
        for frame in self.frames:
            print frame

    def score_frames(self, frame_length):
        scores = []
        score = 0
        for idx in range(min(len(self.frames), frame_length)):
            frame = self.frames[idx]
            score += frame.get_score()
            if frame.is_strike():
                bonus = []
                for frame_ in self.frames[idx+1:idx+3]:
                    bonus.extend(frame_.get_throws())
                score += sum(bonus[:2])
            else:
                if frame.is_spare():
                    if idx + 1 <len(self.frames):
                        bonus = self.frames[idx+1].get_throws()[0]
                        score += bonus
            scores.append(score)
        print 'scoring details,', scores
        return score


class Bowling(object):
    def __init__(self, players, frames_nbr=10, pins_nbr=10, throws_nbr=2):
        """ init a bowling game """
        self.pins_nbr = pins_nbr
        self.throws = []
        self.throws_nbr = throws_nbr
        self.frames_nbr = frames_nbr
        self.players = players

    def run(self):
        """ Dynamically generates a Game (random game) """
        for frm_idx in range(self.frames_nbr):
            for player in self.players:
                assert isinstance(player, Player)
                player.play_frame(Frame(pins_nbr=self.pins_nbr))

        # Check the last frame for each player
        for player in self.players:
            if player.frames[self.frames_nbr-1].is_strike():
                for _ in range(2):
                    player.play_frame(Ball(pins_nbr=self.pins_nbr))
            if player.frames[self.frames_nbr-1].is_spare():
                player.play_frame(Ball(pins_nbr=self.pins_nbr))


    def display(self):
        for player in self.players:
            print "--- {} ---".format(player.n_name)
            print "{} scores {}".format(player.n_name,\
                                         player.score_frames(self.frames_nbr))
            player.print_frames()


def main():
    players = [ Player('Perfect Striker', strike_prob=1),
                Player('Spare Genuis', strike_prob=0, spare_prob=1),
                Player('Striker', strike_prob=0.8),
                Player('Newbie', strike_prob=0.5),
                Player('Bad player', strike_prob=0.3, spare_prob=0.3) ]

    bowl = Bowling(players, frames_nbr=10)
    bowl.run()
    bowl.display()

if __name__ == "__main__":
    main()
