from utils.volume_lookup import VolumeLookup

lookup = VolumeLookup()

print(
    lookup.get_volume(524.05)
)

print(
    lookup.get_volume(524.50)
)

print(
    lookup.get_volume(526.70)
)
