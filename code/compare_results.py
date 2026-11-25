
import pandas as pd
import matplotlib.pyplot as plt


# Load experimental data
argon2 = pd.read_csv("../data/argon2_results.csv")
bcrypt_data = pd.read_csv("../data/bcrypt_results.csv")
pbkdf2 = pd.read_csv("../data/pbkdf2_results.csv")


datasets = {
    "Argon2id": argon2,
    "bcrypt": bcrypt_data,
    "PBKDF2": pbkdf2
}


# Calculate statistics
results = []

for algorithm, data in datasets.items():

    results.append({
        "Algorithm": algorithm,

        "Hashing average (ms)": data["hashing_time_ms"].mean(),
        "Hashing std (ms)": data["hashing_time_ms"].std(),
        "Hashing min (ms)": data["hashing_time_ms"].min(),
        "Hashing max (ms)": data["hashing_time_ms"].max(),

        "Verification average (ms)": data["verification_time_ms"].mean(),
        "Verification std (ms)": data["verification_time_ms"].std(),
        "Verification min (ms)": data["verification_time_ms"].min(),
        "Verification max (ms)": data["verification_time_ms"].max(),

        "Hashing CPU (%)": data["hashing_cpu_percent"].mean(),
        "Verification CPU (%)": data["verification_cpu_percent"].mean(),

        "Hashing RAM increase (MB)": data["hashing_ram_increase_mb"].mean(),
        "Verification RAM increase (MB)": data["verification_ram_increase_mb"].mean(),

        "Hashing maximum RAM (MB)": data["hashing_ram_increase_mb"].max(),
        "Verification maximum RAM (MB)": data["verification_ram_increase_mb"].max()
    })


summary = pd.DataFrame(results)


# Display results
print("\nEXPERIMENTAL COMPARISON")
print("-----------------------")

print(summary.round(2).to_string(index=False))


# Save summary
summary.to_csv("../data/comparison_summary.csv", index=False)


# 1. Execution time comparison
summary.plot(
    x="Algorithm",
    y=[
        "Hashing average (ms)",
        "Verification average (ms)"
    ],
    kind="bar",
    figsize=(10, 6)
)

plt.title("Password Hashing Algorithms - Execution Time")
plt.ylabel("Time (milliseconds)")
plt.xlabel("Algorithm")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("../graphs/comparison_time.png", dpi=300)
plt.close()

# 2. CPU usage comparison
summary.plot(
    x="Algorithm",
    y=[
        "Hashing CPU (%)",
        "Verification CPU (%)"
    ],
    kind="bar",
    figsize=(10, 6)
)

plt.title("Password Hashing Algorithms - CPU Usage")
plt.ylabel("Average CPU usage (%)")
plt.xlabel("Algorithm")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("../graphs/comparison_cpu.png", dpi=300)
plt.close()



# 3. RAM usage comparison

# Chart 1: Argon2id
argon2_summary = summary[
    summary["Algorithm"] == "Argon2id"
]

argon2_summary.plot(
    x="Algorithm",
    y=[
        "Hashing RAM increase (MB)",
        "Verification RAM increase (MB)"
    ],
    kind="bar",
    figsize=(8, 6)
)

plt.title("Argon2id - RAM Usage")
plt.ylabel("Average RAM increase (MB)")
plt.xlabel("Algorithm")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("../graphs/comparison_ram_argon2id.png", dpi=300)
plt.close()


# Chart 2: bcrypt and PBKDF2
other_algorithms = summary[
    summary["Algorithm"].isin(["bcrypt", "PBKDF2"])
]

other_algorithms.plot(
    x="Algorithm",
    y=[
        "Hashing RAM increase (MB)",
        "Verification RAM increase (MB)"
    ],
    kind="bar",
    figsize=(8, 6)
)

plt.title("bcrypt and PBKDF2 - RAM Usage")
plt.ylabel("Average RAM increase (MB)")
plt.xlabel("Algorithm")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("../graphs/comparison_ram_other.png", dpi=300)
plt.close()


#plt.savefig("comparison_ram.png", dpi=300)
#plt.close()


# Finished
print("\nFiles saved:")
print("- comparison_summary.csv")
print("- comparison_time.png")
print("- comparison_cpu.png")
print("- comparison_ram_argon2id.png")
print("- comparison_ram_other.png")