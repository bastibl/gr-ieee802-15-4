import numpy as np

NB0 = 0 # start value for number of backoffs
CW0 = 2 # start value for contention window length
macMinBE = 3 # default value in the standard
macMaxBE = 5 # default value in the standard
macMaxCSMABackoffs = 4 # default value in the standard
aUnitBackoffPeriod = 20 # number of symbols per backoff period

SEND_SUCCESS = True
SEND_FAILURE = False

class csma_unslotted:
    def medium_busy(self, p_col):
        fac = 1e12
        tmp = np.random.randint(0,fac)
        if tmp < p_col*fac:
            # print "\tMedium busy"
            return True
        else:
            # print "\tMedium idle"
            return False

    def run(self, p_col):
        # reset everything
        NB = NB0
        BE = macMinBE
        backoff_units_elapsed = 0

        while NB <= macMaxCSMABackoffs:
            # random backoff
            backoff_units_elapsed += np.random.randint(0,2**BE)

            # CCA
            if self.medium_busy(p_col):
                NB += 1
                BE = min(BE+1, macMaxBE)
                if NB > macMaxCSMABackoffs:
                    return (SEND_FAILURE, backoff_units_elapsed*aUnitBackoffPeriod)
            else:
                return (SEND_SUCCESS, backoff_units_elapsed*aUnitBackoffPeriod)

class csma_slotted:
    def __init__(self, beacon_interval, superframe_duration, battery_life_extension, beacon_duration_sym):
        self.beacon_interval_sym = beacon_interval
        self.superframe_duration_sym = superframe_duration
        self.beacon_duration_sym = beacon_duration_sym
        self.BLE = battery_life_extension
        if self.BLE != False:
            raise NotImplementedError()

    def channel_idle(self, p_col, t_sym):
        tmp = np.random.randint(0,fac)
        if tmp < p_col*fac or t < (t_sym % self.beacon_duration_sym):
            # print "\tMedium busy"
            return False
        else:
            # print "\tMedium idle"
            return True

    def run(self, p_col, initial_sym_elapsed):
        # reset everything
        NB = NB0
        BE = macMinBE if self.BLE == False else min(2,macMinBE)
        CW = CW0
        backoff_units_elapsed = 0

        # synchronize to next backoff period boundary
        if intial_sym_elapsed % aUnitBackoffPeriod != 0:
            backoff_units_elapsed += \
                float(aUnitBackoffPeriod - (initial_sym_elapsed % aUnitBackoffPeriod))/aUnitBackoffPeriod

        while True:
            # random backoff
            backoff_units_elapsed += np.random.randint(0,2**BE)

            while True:
                # CCA
                if self.channel_idle(p_col, back_off_units_elapsed*aUnitBackoffPeriod + initial_sym_elapsed):
                    CW -= 1
                    if CW == 0:
                        return (SEND_SUCCESS, backoff_units_elapsed*aUnitBackoffPeriod)
                else:
                    break

        #
        #     NB += 1
        #     CW = CW0
        #     BE = min(BE+1, macMaxBE)
        #     if NB > macMaxCSMABackoffs:
        #         return (SEND_FAILURE, backoff_units_elapsed*aUnitBackoffPeriod)

