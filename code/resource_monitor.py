
import time
import psutil
import threading


class ResourceMonitor:

    def __init__(self):
        self.process = psutil.Process()
        self.running = False

        self.cpu_samples = []
        self.memory_samples = []

        self.start_memory = 0
        self.thread = None

    def monitor(self):

        while self.running:

            cpu = self.process.cpu_percent(interval=None)

            memory = (
                self.process.memory_info().rss
                / (1024 * 1024)
            )

            self.cpu_samples.append(cpu)
            self.memory_samples.append(memory)

            time.sleep(0.01)

    def start(self):

        self.cpu_samples.clear()
        self.memory_samples.clear()

        self.start_memory = (
            self.process.memory_info().rss
            / (1024 * 1024)
        )

        self.process.cpu_percent(interval=None)

        self.running = True

        self.thread = threading.Thread(
            target=self.monitor
        )

        self.thread.start()

    def stop(self):

        self.running = False
        self.thread.join()

        average_cpu = (
            sum(self.cpu_samples) / len(self.cpu_samples)
            if self.cpu_samples else 0
        )

        peak_ram_increase = (
            max(self.memory_samples) - self.start_memory
            if self.memory_samples else 0
        )

        return average_cpu, max(0, peak_ram_increase)
