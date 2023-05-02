import pstats

p = pstats.Stats("profiles/turn_execution_service_profile.bulk")
p.sort_stats(pstats.SortKey.TIME).print_stats(.3)
