# Introduction to Gitlib.py

## Basic configure in config.ini
```ini
[git]
; source can only use 'git@.....'
source = 
branch = 
; target backup file name
filename = sq.sql
; you own ssh key
ssh_key = data/hksd
ssh_passwd = 
```

## Usage

To use this library, please setting global git username and user email.

```bash
git --config global user.name "Your name"
git --config global user.email "Your email address"
```
