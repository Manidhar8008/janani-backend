from memory import save_identity, get_latest_identity, save_daily_log, get_latest_log

save_identity("4:00 AM", "No phone before work", "Disciplined builder")

print(get_latest_identity())

save_daily_log("Today I worked 3 hours but got distracted twice.")

print(get_latest_log())