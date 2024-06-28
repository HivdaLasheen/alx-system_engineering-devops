exec { 'kill_process':
  command     => 'pkill -f killmenow',
  path        => ['/bin', '/usr/bin', '/usr/local/bin'],
  refreshonly => true,
}

# Notify the exec resource to run
notify { 'trigger_kill':
  notify => Exec['kill_process'],
}
