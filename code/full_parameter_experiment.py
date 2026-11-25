
import csv
import hashlib
import hmac
import os
import statistics
import time
from pathlib import Path

import bcrypt
from argon2 import PasswordHasher

from resource_monitor import ResourceMonitor


# Paths
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

RAW_FILE = DATA_DIR / "parameter_sweep_results.csv"
SUMMARY_FILE = DATA_DIR / "parameter_sweep_summary.csv"


# Experiment settings
PASSWORD = "ResearchPassword123!"
PASSWORD_BYTES = PASSWORD.encode("utf-8")

REPETITIONS = 30
SALT_LENGTH = 16
DKLEN = 32

# Argon2id: memory cost in KiB
ARGON2_MEMORY_COSTS = [19456, 32768, 65536]

# bcrypt: cost factor
BCRYPT_ROUNDS = [10, 11, 12]

# PBKDF2: iteration count
PBKDF2_ITERATIONS = [300000, 600000, 900000]


def measure_operation(operation):
    monitor = ResourceMonitor()
    monitor.start()

    start = time.perf_counter()
    result = operation()
    elapsed_ms = (time.perf_counter() - start) * 1000

    cpu, ram = monitor.stop()

    return result, elapsed_ms, cpu, ram


def run_argon2(memory_cost):
    hasher = PasswordHasher(
        time_cost=2,
        memory_cost=memory_cost,
        parallelism=1
    )

    # Warm-up
    warm_hash = hasher.hash(PASSWORD)
    hasher.verify(warm_hash, PASSWORD)

    return hasher


def run_bcrypt(rounds):
    # Warm-up
    salt = bcrypt.gensalt(rounds=rounds)
    warm_hash = bcrypt.hashpw(PASSWORD_BYTES, salt)
    bcrypt.checkpw(PASSWORD_BYTES, warm_hash)


def run_pbkdf2(iterations):
    # Warm-up
    salt = os.urandom(SALT_LENGTH)
    warm_hash = hashlib.pbkdf2_hmac(
        "sha256", PASSWORD_BYTES, salt, iterations, dklen=DKLEN
    )
    hmac.compare_digest(
        warm_hash,
        hashlib.pbkdf2_hmac(
            "sha256", PASSWORD_BYTES, salt, iterations, dklen=DKLEN
        )
    )


def experiment_argon2(memory_cost):
    hasher = run_argon2(memory_cost)

    for repetition in range(1, REPETITIONS + 1):
        print(
            f"Argon2id | memory={memory_cost} KiB | "
            f"{repetition}/{REPETITIONS}"
        )

        hashed, hash_time, hash_cpu, hash_ram = measure_operation(
            lambda: hasher.hash(PASSWORD)
        )

        _, verify_time, verify_cpu, verify_ram = measure_operation(
            lambda: hasher.verify(hashed, PASSWORD)
        )

        save_result(
            "Argon2id",
            "memory_cost_kib",
            memory_cost,
            repetition,
            hash_time,
            hash_cpu,
            hash_ram,
            verify_time,
            verify_cpu,
            verify_ram
        )


def experiment_bcrypt(rounds):
    run_bcrypt(rounds)

    for repetition in range(1, REPETITIONS + 1):
        print(
            f"bcrypt | rounds={rounds} | "
            f"{repetition}/{REPETITIONS}"
        )

        salt = bcrypt.gensalt(rounds=rounds)

        hashed, hash_time, hash_cpu, hash_ram = measure_operation(
            lambda: bcrypt.hashpw(PASSWORD_BYTES, salt)
        )

        _, verify_time, verify_cpu, verify_ram = measure_operation(
            lambda: bcrypt.checkpw(PASSWORD_BYTES, hashed)
        )

        save_result(
            "bcrypt",
            "rounds",
            rounds,
            repetition,
            hash_time,
            hash_cpu,
            hash_ram,
            verify_time,
            verify_cpu,
            verify_ram
        )


def experiment_pbkdf2(iterations):
    run_pbkdf2(iterations)

    for repetition in range(1, REPETITIONS + 1):
        print(
            f"PBKDF2 | iterations={iterations} | "
            f"{repetition}/{REPETITIONS}"
        )

        salt = os.urandom(SALT_LENGTH)

        hashed, hash_time, hash_cpu, hash_ram = measure_operation(
            lambda: hashlib.pbkdf2_hmac(
                "sha256",
                PASSWORD_BYTES,
                salt,
                iterations,
                dklen=DKLEN
            )
        )

        def verify():
            calculated = hashlib.pbkdf2_hmac(
                "sha256",
                PASSWORD_BYTES,
                salt,
                iterations,
                dklen=DKLEN
            )
            return hmac.compare_digest(hashed, calculated)

        _, verify_time, verify_cpu, verify_ram = measure_operation(verify)

        save_result(
            "PBKDF2",
            "iterations",
            iterations,
            repetition,
            hash_time,
            hash_cpu,
            hash_ram,
            verify_time,
            verify_cpu,
            verify_ram
        )


def save_result(
    algorithm,
    parameter_name,
    parameter_value,
    repetition,
    hash_time,
    hash_cpu,
    hash_ram,
    verify_time,
    verify_cpu,
    verify_ram
):
    row = {
        "algorithm": algorithm,
        "parameter_name": parameter_name,
        "parameter_value": parameter_value,
        "repetition": repetition,
        "hashing_time_ms": hash_time,
        "hashing_cpu_percent": hash_cpu,
        "hashing_ram_increase_mb": hash_ram,
        "verification_time_ms": verify_time,
        "verification_cpu_percent": verify_cpu,
        "verification_ram_increase_mb": verify_ram
    }

    with open(RAW_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(row)


def create_summary():
    with open(RAW_FILE, newline="") as file:
        rows = list(csv.DictReader(file))

    groups = {}

    for row in rows:
        key = (
            row["algorithm"],
            row["parameter_name"],
            row["parameter_value"]
        )
        groups.setdefault(key, []).append(row)

    summary_rows = []

    for (algorithm, parameter_name, parameter_value), group in groups.items():

        def values(column):
            return [float(row[column]) for row in group]

        hash_times = values("hashing_time_ms")
        verify_times = values("verification_time_ms")
        hash_ram = values("hashing_ram_increase_mb")
        verify_ram = values("verification_ram_increase_mb")

        summary_rows.append({
            "algorithm": algorithm,
            "parameter_name": parameter_name,
            "parameter_value": parameter_value,
            "repetitions": len(group),

            "hashing_time_avg_ms": statistics.mean(hash_times),
            "hashing_time_sd_ms": statistics.stdev(hash_times),
            "hashing_time_min_ms": min(hash_times),
            "hashing_time_max_ms": max(hash_times),

            "verification_time_avg_ms": statistics.mean(verify_times),
            "verification_time_sd_ms": statistics.stdev(verify_times),
            "verification_time_min_ms": min(verify_times),
            "verification_time_max_ms": max(verify_times),

            "hashing_cpu_avg_percent": statistics.mean(
                values("hashing_cpu_percent")
            ),
            "verification_cpu_avg_percent": statistics.mean(
                values("verification_cpu_percent")
            ),

            "hashing_ram_avg_mb": statistics.mean(hash_ram),
            "verification_ram_avg_mb": statistics.mean(verify_ram),
            "hashing_ram_max_mb": max(hash_ram),
            "verification_ram_max_mb": max(verify_ram)
        })

    with open(SUMMARY_FILE, "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=summary_rows[0].keys()
        )
        writer.writeheader()
        writer.writerows(summary_rows)


def main():
    # Start a fresh raw-results file
    if RAW_FILE.exists():
        RAW_FILE.unlink()

    print("STARTING PARAMETER EXPERIMENT")
    print("=============================")

    for memory_cost in ARGON2_MEMORY_COSTS:
        experiment_argon2(memory_cost)

    for rounds in BCRYPT_ROUNDS:
        experiment_bcrypt(rounds)

    for iterations in PBKDF2_ITERATIONS:
        experiment_pbkdf2(iterations)

    create_summary()

    print("\nEXPERIMENT COMPLETED")
    print(f"Raw results: {RAW_FILE}")
    print(f"Summary: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
