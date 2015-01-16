from constants import *
import parameters as params
import numpy as np

# state machine for slotted CSMA-CA algorithm
class mac_slotted:
    def __init__(self,parameters):
        self.p = parameters

        self.csma_statemachine = {"initialize": self.initialize, "apply_backoff": self.apply_backoff, "CCA": self.CCA,
                                  "increase_ctr": self.increase_ctr, "decrease_ctr": self.decrease_ctr,
                                  "success": self.success, "failure": self.failure, "done": self.done}
        self.next_state = "initialize"

        self.t_sym = 0  # always in [0, self.beacon_interval)
        self.delay = 0  # overall time elapsed
        self.bytes_transmitted = 0

        self.NB = NB0
        self.BE = aMacMinBE
        self.CW = CW0

    def increment_time(self, increment):
        print "inc time by", increment
        self.delay += increment
        self.t_sym += increment
        if self.t_sym >= self.p.macSuperframeDuration:
            wait_time = self.p.macBeaconInterval - self.p.macSuperframeDuration
            self.delay += wait_time
            self.t_sym = (self.t_sym + wait_time) % self.p.macBeaconInterval

    def channel_idle(self):
        fac = 1e9
        tmp = np.random.randint(0,fac)
        if tmp < self.p.p_col*fac or self.t_sym < (self.t_sym % self.p.phyBeaconDuration):
            # print "\tMedium busy"
            return False
        else:
            # print "\tMedium idle"
            return True

    def run(self):
        print "run"
        self.delay = 0
        self.bytes_transmitted = 0

        # run state machine
        while self.next_state != "done":
            self.csma_statemachine[self.next_state]()

        return self.delay, self.bytes_transmitted

    def initialize(self):
        print "initialize"
        self.NB = NB0
        self.BE = aMacMinBE if not self.p.macBatteryLifeExtension else min(2, aMacMinBE)
        self.CW = CW0

        # synchronize to next backoff period boundary
        if self.t_sym % aUnitBackoffPeriod != 0:
            self.increment_time(aUnitBackoffPeriod - (self.t_sym % aUnitBackoffPeriod))

        self.next_state = "apply_backoff"

    def apply_backoff(self):
        print "apply_backoff"
        rand_backoff_units = np.random.randint(0, 2 ** self.BE)
        remaining_backoff_units = self.p.macSuperframeDuration - self.t_sym

        if rand_backoff_units > remaining_backoff_units:  # continue backoff in next superframe
            self.increment_time(rand_backoff_units * aUnitBackoffPeriod)
        else:
            if rand_backoff_units * aUnitBackoffPeriod + self.p.phyTransmissionWithAckDuration > remaining_backoff_units*aUnitBackoffPeriod:
                # wait for next frame and backoff anew
                self.increment_time(remaining_backoff_units * aUnitBackoffPeriod)
                rand_backoff_units = np.random.randint(0, 2 ** self.BE)  # this is assumed to always fit into the next frame
                self.increment_time(rand_backoff_units * aUnitBackoffPeriod)
            else:  # transmission fits into remaining superframe
                self.increment_time(rand_backoff_units * aUnitBackoffPeriod)

        self.next_state = "CCA"

    def CCA(self):
        print "CCA"
        if self.channel_idle():
            self.next_state = "decrease_ctr"
        else:
            self.next_state = "increase_ctr"

    def increase_ctr(self):
        print "increase_ctr"
        self.NB += 1
        self.CW = CW0
        self.BE = min(self.BE+1, aMacMinBE)
        if self.NB > aMacMaxCSMABackoffs:
            self.next_state = "failure"
        else:
            self.next_state = "apply_backoff"

    def decrease_ctr(self):
        print "decrease_ctr"
        self.CW -= 1
        if self.CW == 0:
            self.next_state = "success"
        else:
            self.next_state = "CCA"

    def success(self):
        print "success"
        self.bytes_transmitted += self.p.nbytes_mac_payload
        self.next_state = "done"

    def failure(self):
        print "failure"
        self.next_state = "done"

    def done(self):
        print "done"
