import pdb
from typing import Dict, List, Tuple, Union

########################################################################################################
# Flip-flop modules (prefix %) are either on or off; they are initially off.                           #
# If a flip-flop module receives a high pulse, it is ignored and nothing happens.                      #
# However, if a flip-flop module receives a low pulse, it flips between on and off.                    #
# If it was off, it turns on and sends a high pulse. If it was on, it turns off and sends a low pulse. #
########################################################################################################

##################################################################################################################################
# Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected input modules; #
# they initially default to remembering a low pulse for each input.                                                              #
# When a pulse is received, the conjunction module first updates its memory for that input.                                      #
# Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.                      #
##################################################################################################################################

########################################################################################
# There is a single broadcast module (named broadcaster).                              #
# When it receives a pulse, it sends the same pulse to all of its destination modules. #
########################################################################################


TEST = True

if TEST:
    _raw = [
        "button -> broadcaster",
        "broadcaster -> a, b, c",
        "%a -> b",
        "%b -> c",
        "%c -> inv",
        "&inv -> a",
    ]

    __raw = [
        "button -> broadcaster",
        "broadcaster -> a",
        "%a -> inv, con",
        "&inv -> b",
        "%b -> con",
        "&con -> output",
    ]

else:
    with open("./input.txt", "r") as txtin:
        _raw = [ln.strip() for ln in txtin]


__data = [map(str.strip, _.split("->")) for _ in _raw]
_data = {k: list(map(str.strip, v.split(","))) for k, v in __data}


class LowPulse:
    created = None

    def __new__(cls):
        if cls.created is None:
            cls.created = super(LowPulse, cls).__new__(cls)
        return cls.created


class HighPulse:
    created = None

    def __new__(cls):
        if cls.created is None:
            cls.created = super(HighPulse, cls).__new__(cls)
        return cls.created


class Button:
    def __init__(self):
        pass

    def press(self) -> List[Tuple[str, str, LowPulse]]:
        return [("button", "broadcaster", LowPulse())]


class BroadCaster:
    def __init__(self, destinations: List[str]):
        self.destinations = destinations

    def process(
        self,
        input_pulse: Tuple[str, Union[HighPulse, LowPulse]],  # Origin and Pulse type
    ) -> List[Tuple[str, str, LowPulse]]:
        return [("broadcaster", dest, LowPulse()) for dest in self.destinations]


class FlipFlop:
    def __init__(self, name: str, destinations: List[str]):
        self.name = name
        self.state = False
        self.destinations = destinations

    def process(
        self,
        input_pulse: Tuple[str, Union[HighPulse, LowPulse]],  # Origin and Pulse type
    ) -> List[Tuple[str, str, Union[HighPulse, LowPulse]]]:
        # Ignore High pulses
        if isinstance(input_pulse, HighPulse):
            return []

        self.state = not self.state
        if self.state:
            return [(self.name, dest, HighPulse()) for dest in self.destinations]
        return [(self.name, dest, LowPulse()) for dest in self.destinations]


class Conjunction:
    def __init__(self, name: str, sources: List[str], destinations: List[str]):
        self.name = name
        self.destinations = destinations
        self.sources = {_: LowPulse() for _ in sources}

    def process(
        self,
        input_pulse: Tuple[str, Union[HighPulse, LowPulse]],  # Origin and Pulse type
    ) -> List[Tuple[str, str, Union[HighPulse, LowPulse]]]:
        self.sources[input_pulse[0]] = input_pulse[1]

        if all((isinstance(_, HighPulse) for _ in self.sources.values())):
            return [(self.name, dest, LowPulse()) for dest in self.destinations]
        return [(self.name, dest, HighPulse()) for dest in self.destinations]


def create_network(input_data: Dict[str, List[str]]):
    network = {}

    conjunctions = {}

    for k, v in input_data.items():
        if k.startswith("&"):
            conjunctions[k[1:]] = {"sources": set(), "destinations": v}

    for k, v in input_data.items():
        if k == "broadcaster":
            name = k
        elif k.startswith("&") or k.startswith("%"):
            name = k[1:]

        for dest in v:
            if dest in conjunctions:
                conjunctions[dest]["sources"].add(name)

        if k.startswith("&") or k == "button":
            continue

        network[name] = v

    return {
        "button": Button(),
        "broadcaster": BroadCaster(network["broadcaster"]),
        **{k: FlipFlop(k, v) for k, v in network.items() if k != "broadcaster"},
        **{
            k: Conjunction(k, list(v["sources"]), v["destinations"])
            for k, v in conjunctions.items()
        },
    }


NETWORK = create_network(_data)


LOW_COUNT = 0
HIGH_COUNT = 0


def state_hash(network: dict) -> tuple:
    done = list()
    for k, v in sorted(network.items()):
        sublist = []

        if isinstance(v, FlipFlop):
            sublist.append(v.name)
            sublist.append(v.state)

        if isinstance(v, Conjunction):
            sublist.append(v.name)
            sublist.append(tuple(sorted(v.sources.items())))

        if len(sublist) > 0:
            done.append(tuple(sublist))

    return tuple(done)


for _ in range(1):
    stack = NETWORK["button"].press()
    state_memory = []

    signal_count = 0

    while len(stack) > 0:
        network_state = state_hash(NETWORK)
        # print(network_state)
        if network_state in state_memory and signal_count > 2:
            print("Hello")
            break
        state_memory.append(network_state)

        for signal in stack.copy():
            print(f"Signal: {signal}")
            # pdb.set_trace()

            if isinstance(signal[2], LowPulse):
                LOW_COUNT += 1
            else:
                HIGH_COUNT += 1

            stack.remove(signal)
            if signal[1] == "output":
                continue

            substack = NETWORK[signal[1]].process((signal[0], signal[2]))
            print(f"Stack: {stack}")
            print(f"Substack: {substack}")
            print()

            stack = substack + stack
            signal_count += 1
