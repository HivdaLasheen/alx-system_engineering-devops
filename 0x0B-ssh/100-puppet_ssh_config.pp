# Ensure the .ssh directory exists for the user
file { '/home/ubuntu/.ssh':
  ensure => directory,
  mode   => '0700',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Manage the SSH client configuration file
file { '/home/ubuntu/.ssh/config':
  ensure => file,
  mode   => '0600',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  content => "\
Host your_server_ip_or_hostname
    User ubuntu
    IdentityFile ~/.ssh/school
    PreferredAuthentications publickey
    PasswordAuthentication no
",
}
