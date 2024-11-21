seeds = []

# seed-to-soil map:
seed_2_soil = {}
# soil-to-fertilizer map:
soil_2_fertilizer = {}
# fertilizer-to-water map:
fertilizer_2_water = {}
# water-to-light map:
water_2_light = {}
# light-to-temperature map:
light_2_temperature = {}
# temperature-to-humidity map:
temperature_2_humidity = {}
# humidity-to-location map:
humidity_2_location = {}
current = None

with open("./input.txt", "r") as txtin:
    for ln in txtin:

        if ln == "\n":
            continue

        if "seeds:" in ln:
            seeds = list(map(int, ln.replace("seeds:", "").strip().split(" ")))
            continue
        if "seed-to-soil map:" in ln:
            current = seed_2_soil
            continue
        if "soil-to-fertilizer map:" in ln:
            current = soil_2_fertilizer
            continue
        if "fertilizer-to-water map:" in ln:
            current = fertilizer_2_water
            continue
        if "water-to-light map:" in ln:
            current = water_2_light
            continue
        if "light-to-temperature map:" in ln:
            current = light_2_temperature
            continue
        if "temperature-to-humidity map:" in ln:
            current = temperature_2_humidity
            continue
        if "humidity-to-location map:" in ln:
            current = humidity_2_location
            continue

        parts = map(int, map(str.strip, ln.split(" ")))
        dst_start, src_start, _range = parts
        src_end = src_start + _range - 1

        current[(src_start, src_end)] = dst_start - src_start


def map_seed_to_loc(seed_number: int) -> int:
    num = seed_number
    for _map in (
        seed_2_soil,
        soil_2_fertilizer,
        fertilizer_2_water,
        water_2_light,
        light_2_temperature,
        temperature_2_humidity,
        humidity_2_location,
    ):
        for k, v in _map.items():
            if k[0] <= num <= k[1]:
                num = num + v
                break
    return num


seed_tuples = sorted(
    [(seeds[idx], seeds[idx] + seeds[idx + 1]) for idx in range(0, len(seeds), 2)]
)

# 3249904174 is too high
# 309796150
