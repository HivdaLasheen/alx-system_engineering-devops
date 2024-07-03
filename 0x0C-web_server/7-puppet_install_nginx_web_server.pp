# Install and configure Nginx server using Puppet

# Add stable version of Nginx repository
exec { 'add nginx stable repo':
  command => 'sudo add-apt-repository -y ppa:nginx/stable',
  path    => '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
  unless  => 'apt-cache policy | grep -q nginx/stable',
}

# Update software packages list
exec { 'update packages':
  command => 'apt-get update',
  path    => '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
  require => Exec['add nginx stable repo'],
}

# Install Nginx
package { 'nginx':
  ensure  => installed,
  require => Exec['update packages'],
}

# Allow HTTP traffic
exec { 'allow HTTP':
  command => "ufw allow 'Nginx HTTP'",
  path    => '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
  unless  => 'ufw status | grep -q "Nginx HTTP"',
}

# Change folder permissions for /var/www
exec { 'chmod www folder':
  command => 'chmod -R 755 /var/www',
  path    => '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
  require => Package['nginx'],
}

# Create index file
file { '/var/www/html/index.html':
  content => "Hello World!\n",
  require => Exec['chmod www folder'],
}

# Create custom 404 error page
file { '/var/www/html/404.html':
  content => "Ceci n'est pas une page\n",
  require => Exec['chmod www folder'],
}

# Nginx default configuration file
file { '/etc/nginx/sites-enabled/default':
  content => "
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;

    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location / {
        try_files \$uri \$uri/ =404;
    }

    error_page 404 /404.html;

    location /404.html {
        internal;
    }

    if (\$request_filename ~ redirect_me) {
        rewrite ^ https://www.youtube.com/watch?v=QH2-TGUlwu4 permanent;
    }
}
",
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# Ensure Nginx service is running and enabled
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-enabled/default'],
}
