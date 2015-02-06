from constants import *
import parameters as params
import numpy as np

# state machine for slotted CSMA-CA algorithm
class csma_slotted:
    def __init__(self, parameters):
        self.p = parameters

        self.csma_statemachine = {"initialize": self.initialize, "apply_backoff": self.apply_backoff, "CCA": self.CCA,
                                  "increase_ctr": self.increase_ctr, "decrease_ctr": self.decrease_ctr,
                                  "success": self.success, "failure": self.failure, "done": self.done}
        self.next_state = "initialize"

        self.t_sym = 0  # always in [0, self.beacon_interval)
        self.t_total_sym = 0  # total elapsed symbols since start
        self.delay = 0  # backoff delay for current transmission
        self.is_successful = False

        self.NB = NB0
        self.BE = aMacMinBE
        self.CW = CW0

    def increment_time(self, increment):
        t_old = self.t_total_sym
        self.delay += increment
        self.t_sym += increment
        self.t_total_sym += increment
        if self.t_sym >= self.p.macSuperframeDuration:
            wait_time = self.p.macBeaconInterval - self.p.macSuperframeDuration
            self.delay += wait_time
            self.t_sym = (self.t_sym + wait_time) % self.p.macBeaconInterval
            self.t_total_sym += wait_time
        # print "\tinc time from", t_old * vPhySymbolDurationSec[self.p.phy_mode] * 1000, "ms by", \
        #     (self.t_total_sym - t_old) * vPhySymbolDurationSec[self.p.phy_mode] * 1000, "ms to", \
        #     self.t_total_sym*vPhySymbolDurationSec[self.p.phy_mode] * 1000, "ms"

    def channel_idle(self):
        fac = 1e9
        tmp = np.random.randint(0, fac)
        if self.t_sym < self.p.phyBeaconDuration:
            # print "\tMedium busy during beacon duration"
            return False
        else:
            if tmp < self.p.p_col * fac:
                # print "\tMedium busy"
                return False
            else:
                # print "\tMedium idle"
                return True

    def run(self):
        # print "run"
        self.delay = 0
        self.is_successful = False

        # run state machine
        # print "--- start CSMA"
        while self.next_state != "done":
            self.csma_statemachine[self.next_state]()
        self.next_state = "initialize"
        # print "--- finished CSMA"
        return self.is_successful, self.delay

    def initialize(self):
        # print "initialize"
        self.NB = NB0
        self.BE = aMacMinBE if not self.p.macBatteryLifeExtension else min(2, aMacMinBE)
        self.CW = CW0

        # synchronize to next backoff period boundary
        if self.t_sym % aUnitBackoffPeriod != 0:
            # print "align to next backoff period boundary"
            self.increment_time(aUnitBackoffPeriod - (self.t_sym % aUnitBackoffPeriod))

        self.next_state = "apply_backoff"

    def apply_backoff(self):
        # print "apply_backoff"
        rand_backoff_sym = np.random.randint(0, 2 ** self.BE) * aUnitBackoffPeriod
        remaining_backoff_sym = self.p.macSuperframeDuration - self.t_sym

        if rand_backoff_sym > remaining_backoff_sym:  # continue backoff in next superframe
            # print "backoff continues in next superframe, inc by (at least) backoff"
            self.increment_time(rand_backoff_sym)
        else:
            if rand_backoff_sym + self.p.phyTransmissionWithAckDuration > remaining_backoff_sym:
                # print "transmission cannot be completed in current CAP, wait for next superframe, inc by (at least) rem. sym and backoff"
                # wait for next frame and backoff anew
                rand_backoff_sym = np.random.randint(0, 2 ** self.BE) * aUnitBackoffPeriod  # this is assumed to always fit into the next frame
                self.increment_time(remaining_backoff_sym + rand_backoff_sym)
            else:  # transmission fits into remaining superframe
                # print "transmission in current CAP possible, inc by backoff"
                self.increment_time(rand_backoff_sym)

        self.next_state = "CCA"

    def CCA(self):
        # print "CCA"
        if self.channel_idle():
            self.next_state = "decrease_ctr"
        else:
            self.next_state = "increase_ctr"

    def increase_ctr(self):
        # print "increase_ctr"
        self.NB += 1
        self.CW = CW0
        self.BE = min(self.BE + 1, aMacMinBE)
        if self.NB > aMacMaxCSMABackoffs:
            self.next_state = "failure"
        else:
            self.next_state = "apply_backoff"

    def decrease_ctr(self):
        # print "decrease_ctr"
        self.CW -= 1
        if self.CW == 0:
            self.next_state = "success"
        else:
            self.next_state = "CCA"

    def success(self):
        # print "success"
        self.is_successful = True
        self.next_state = "done"

    def failure(self):
        # print "failure"
        self.is_successful = False
        self.next_state = "done"

    def done(self):
        print "this is unreachable"
