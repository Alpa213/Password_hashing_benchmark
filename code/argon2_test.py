
import time
import statistics
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

from argon2 import PasswordHasher
from resource_monitor import ResourceMonitor


# Experiment configuration
password = "ResearchPassword123!"

hasher = PasswordHasher(
    time_cost=2,
    memory_cost=19456,
    parallelism=1
)

REPETITIONS = 30

hashing_times = []
verification_times = []

hashing_cpu = []
verification_cpu = []

hashing_ram = []
verification_ram = []


# Warm-up
hashed_password = hasher.hash(password)
hasher.verify(hashed_password, password)


# Main experiment
for i in range(REPETITIONS):

    print(f"Repetition {i + 1}/{REPETITIONS}")

    # Hashing measurement
    monitor = ResourceMonitor()
    monitor.start()

    start = time.perf_counter()

    hashed_password = hasher.hash(password)

    hashing_time = (
        time.perf_counter() - start
    ) * 1000

    cpu, ram = monitor.stop()

    hashing_times.append(hashing_time)
    hashing_cpu.append(cpu)
    hashing_ram.append(ram)


    # Verification measurement
    monitor = ResourceMonitor()
    monitor.start()

    start = time.perf_counter()

    hasher.verify(hashed_password, password)

    verification_time = (
        time.perf_counter() - start
    ) * 1000

    cpu, ram = monitor.stop()

    verification_times.append(verification_time)
    verification_cpu.append(cpu)
    verification_ram.append(ram)


# Save raw measurements
with open(DATA_DIR / "argon2_results.csv", "w", newline="") as file:

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

    for i in range(REPETITIONS):

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
print("\nARGON2ID EXPERIMENT RESULTS")
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

print("\nData saved to argon2_results.csv")
