import time

cpu_15 = None
cpu_10 = None
cpu_5 = None

def get_cpu_stats():
  global cpu_5, cpu_10, cpu_15
  stats_file = open('/os_proc/stat','r')

  cpus = dict()
  stats = dict()
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
      
  stats['cpus'] = cpus
  stats['cpu_5'] = cpu_5
  stats['cpu_10'] = cpu_10
  stats['cpu_15'] = cpu_15

  cpu_15 = cpu_10
  cpu_10 = cpu_5
  cpu_5 = cpus
  
  return stats

def get_mem_stats():
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

def get_stats():
  return {'mem': get_mem_stats(),
          'cpu': get_cpu_stats()}

