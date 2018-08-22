from threading import Thread, Lock
import time

cpu_15 = None
cpu_10 = None
cpu_5 = None

class Stats(Thread):
 
  def __init__(self):
    self.daemon = True
    self._lock = Lock()

    self.stats = {}
  def get_cpu_stats(self):
    stats_file = open('/os_proc/stat','r')

    cpus = dict()
    for line in stats_file:
      if 'cpu' in line:
        sp = line.strip().split(' ')
        spl = [x for x in sp if x]
        cpu = {'user': float(spl[1]),
               'nice': float(spl[2]),
               'system': float(spl[3]),
               'idle': float(spl[4]),
               'iowait': float(spl[5]),
               'irq': float(spl[6]),
               'softirq': float(spl[7]),
               'steal': float(spl[8])}
        total = cpu['user'] + cpu['nice'] + cpu['system'] + cpu['idle'] + cpu['iowait'] + cpu['irq'] + cpu['softirq'] + cpu['steal']
        total_idle = cpu['idle'] + cpu['iowait']
        cpu['total'] = total
        cpu['total_idle'] = total_idle
        cpu['avg'] = 1 - total_idle / total
        if cpu_5:
          cpu['5_avg'] = 1 - (total_idle - cpu_5[spl[0]]['total_idle']) / (total - cpu_5[spl[0]]['total'])
        if cpu_10:
          cpu['10_avg'] = 1 - (total_idle - cpu_10[spl[0]]['total_idle']) / (total - cpu_10[spl[0]]['total'])
        if cpu_15:
          cpu['15_avg'] = 1 - (total_idle - cpu_15[spl[0]]['total_idle']) / (total - cpu_15[spl[0]]['total'])
        cpus[spl[0]] = cpu
      
    self.cpu_15 = cpu_10
    self.cpu_10 = cpu_5
    self.cpu_5 = cpus
  
    return cpus

  def get_mem_stats(self):
    mem_file = open('/os_proc/meminfo', 'r')
    mem = dict()

    for line in mem_file:
      spl = [x for x in line.split(' ') if x]
      mem[spl[0][:-1]] = float(spl[1])
    return {'total_used': mem['MemTotal'] - mem['MemFree'],
          'non_trivial': mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached'] - mem['SReclaimable'] - mem['Shmem'],
            'buffers': mem['Buffers'],
            'cached': mem['Cached'] + mem['SReclaimable'] + mem['Shmem'],
            'pct_used': 1 - mem['MemFree'] / mem['MemTotal'],
            'pct_real': 1 - (mem['MemFree'] + mem['Buffers'] + mem['Cached'] + mem['SReclaimable'] + mem['Shmem']) / mem['MemTotal']
            }

  def run(self):
    while True:
      self.update_stats()
      time.sleep(5)

  def update_stats(self):
    with self._lock:
      self.stats = {'mem': get_mem_stats(),
                    'cpu': get_cpu_stats()}
  def get_stats(self):
    with self._lock:
      return self.stats

