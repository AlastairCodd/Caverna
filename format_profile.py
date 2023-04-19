import pstats

p = pstats.Stats("turn_execution_service_profile.1")
p.sort_stats(pstats.SortKey.TIME).print_stats(.3)
