import pstats

p = pstats.Stats("profiles/turn_execution_service_profile.configurable")
p.sort_stats(pstats.SortKey.TIME).print_stats(.1)
