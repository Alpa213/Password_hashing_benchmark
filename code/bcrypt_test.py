
import time
import statistics
import csv
import bcrypt

from resource_monitor import ResourceMonitor
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)


password = b"ResearchPassword123!"
iterations = 30

hashing_times = []
verification_times = []

hashing_cpu = []
verification_cpu = []

hashing_ram = []
verification_ram = []

# Resource monitor
monitor = ResourceMonitor()


# Warm-up
warmup_salt = bcrypt.gensalt(rounds=10)
warmup_hash = bcrypt.hashpw(password, warmup_salt)
bcrypt.checkpw(password, warmup_hash)


# 30 repetitions
for i in range(iterations):

    print(f"Repetition {i + 1}/{iterations}")

    # HASHING
    monitor.start()
    start = time.perf_counter()

    # Salt generation is included in hashing time
    salt = bcrypt.gensalt(rounds=10)
    hashed_password = bcrypt.hashpw(password, salt)

    hashing_times.append(
        (time.perf_counter() - start) * 1000
    )

    cpu, ram = monitor.stop()

    hashing_cpu.append(cpu)
    hashing_ram.append(ram)


    # VERIFICATION
    monitor.start()
    start = time.perf_counter()

    valid = bcrypt.checkpw(password, hashed_password)

    verification_times.append(
        (time.perf_counter() - start) * 1000
    )

    cpu, ram = monitor.stop()

    verification_cpu.append(cpu)
    verification_ram.append(ram)


# Save raw measurements
with open(DATA_DIR / "bcrypt_results.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "repetition",
        "hashing_time_ms",
        "hashing_cpu_percent",
        "hashing_ram_increase_mb",
        "verification_time_ms",
        "verification_cpu_percent",
        "verification_ram_increase_mb"
    ])

    for i in range(iterations):

        writer.writerow([
            i + 1,
            hashing_times[i],
            hashing_cpu[i],
            hashing_ram[i],
            verification_times[i],
            verification_cpu[i],
            verification_ram[i]
        ])


# Display results
print("\nBCRYPT EXPERIMENT RESULTS")
print("---------------------------")

print("\nHASHING")
print(f"Average time: {statistics.mean(hashing_times):.2f} ms")
print(f"Average CPU: {statistics.mean(hashing_cpu):.2f}%")
print(f"Average RAM increase: {statistics.mean(hashing_ram):.2f} MB")
print(f"Maximum RAM increase: {max(hashing_ram):.2f} MB")

print("\nVERIFICATION")
print(f"Average time: {statistics.mean(verification_times):.2f} ms")
print(f"Average CPU: {statistics.mean(verification_cpu):.2f}%")
print(f"Average RAM increase: {statistics.mean(verification_ram):.2f} MB")
print(f"Maximum RAM increase: {max(verification_ram):.2f} MB")

print(f"\nPassword verified: {valid}")
print("\nData saved to bcrypt_results.csv")
