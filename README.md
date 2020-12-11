

# sysinfo

## Python based scripts for obtaining system information from Linux.

* Python2 and Python3 compatible
* Output in JSON format
* Simple scripts and extensible structure
* Parallel commands execution
* Output to stdout or file
* Output can be processed by jq

## Command-line arguments
```
usage: sysinfo.py [-h] [--all] [--error] [--info] [--list] [--output OUTPUT]
                  [--pool POOL] [--verbose]
                  [commands [commands ...]]

positional arguments:
  commands              Commands

optional arguments:
  -h, --help            show this help message and exit
  --all, -a             Execute all commands.
  --error, -e           Show only error outputs from commands.
  --info, -i            List all commands with command line arguments.
  --list, -l            List all commands.
  --output OUTPUT, -o OUTPUT
                        Path to the output file.
  --pool POOL, -p POOL  Pool size for parallel execution of commands. (default
                        value is 5)
  --verbose, -v         Add more info to output - options, commands, raw
                        command result.
```

## Examples

### Standart JSON output
```
python2 sysinfo.py lscpu
```
```json
{
    "lscpu": {
        "output": {
            "architecture": "armv6l",
            "bogomips": "996.14",
            "byteOrder": "Little Endian",
            "coresPerSocket": "1",
            "cpuMaxMhz": "1000.0000",
            "cpuMinMhz": "700.0000",
            "cpus": "1",
            "flags": "half thumb fastmult vfp edsp java tls",
            "model": "7",
            "modelName": "ARM1176",
            "onLineCpusList": "0",
            "sockets": "1",
            "stepping": "r0p7",
            "threadsPerCore": "1",
            "vendorId": "ARM"
        }
    }
}
```

### Get single value
```
python2 sysinfo.py lscpu | jq -r ".lscpu.output.modelName"
```
```
ARM1176
```

### Output in CSV format
```
python2 sysinfo.py lsblk | jq -r ".lsblk.output[] | [.name, .label, .size,
.mountpoint] | @csv"
```

```
"mmcblk0","","14.6G",""
"mmcblk0boot0","","4M",""
"mmcblk0boot1","","4M",""
"mmcblk0p1","boot","256M","/boot"
"mmcblk0p2","rootfs","14.3G","/"
```

## Resources

* [jq](https://stedolan.github.io/jq/)

## Available commands
```
blkid                     - Block device attributes
blockdev                  - Block device ioctls
busctl                    - Introspect the bus
chrt                      - Scheduling attributes of all the tasks (threads)
dev_disk                  - Disk devices mapping
df                        - Report file system disk space usage
dmidecode                 - Dumping all information from DMI (SMBIOS)
dmidecode_baseboard       - Dumping BASEBOARD information from DMI (SMBIOS)
dmidecode_bios            - Dumping BIOS information from DMI (SMBIOS)
dmidecode_cache           - Dumping CACHE information from DMI (SMBIOS)
dmidecode_chassis         - Dumping CHASSIS information from DMI (SMBIOS)
dmidecode_connector       - Dumping CONNECTOR information from DMI (SMBIOS)
dmidecode_memory          - Dumping MEMORY information from DMI (SMBIOS)
dmidecode_processor       - Dumping CHASSIS information from DMI (SMBIOS)
dmidecode_slot            - Dumping SLOT information from DMI (SMBIOS)
dmidecode_system          - Dumping SYSTEM information from DMI (SMBIOS)
dnf_installed             - DNF - list installed packages
dnf_repolist              - DNF - defined repositories
env                       - Environment variables
etc_default               - Default configuration for programs
etc_fstab                 - Filesystems mounted on boot
etc_group                 - Groups essential information
etc_hosts                 - Maps hostnames to IP addresses
etc_locale_gen            - Configuration file for locale-gen
etc_mtab                  - Currently mounted filesystems
etc_passwd                - Attributes of each user or account on a computer
etc_release               - OS release info
etc_shadow                - Shadow database of the passwd file
etc_timezone              - Timezone settings
fbset                     - Show frame buffer device settings
fbset_info                - Show frame buffer device information
findmnt                   - List all mounted filesytems
free                      - Amount of free and used memory in the system
getconf                   - Configuration variables for the current system and their values
groups                    - Group names
hardware_platform         - Hardware platform
hostnamectl               - Current system hostname and related information
ifconfig                  - List all interfaces which are currently available, even if down
jobs                      - Job names, if job control is active
kernel_name               - Kernel name
kernel_release            - Kernel release
kernel_version            - Kernel version
lsblk                     - Lists information about all block devices
lscpu                     - Information about the CPU architecture
lsmod                     - Show the status of modules in the Linux Kernel
lsns                      - Block device ioctls
lsof                      - Information about files opened by processes
lspci                     - List all PCI devices
lsusb                     - List USB devices
machine                   - Machine hardware name
modinfo                   - Information about a Linux Kernel modules
nodename                  - Network node hostname
operating_system          - Operating system
parted                    - Lists partition layout on all block devices
proc_cmdline              - Parameters passed to the kernel at the time it is started
proc_consoles             - Information about current consoles including tty
proc_cpuinfo              - Type of processor used by your system
proc_crypto               - Installed cryptographic ciphers used by the Linux kernel
proc_devices              - Installed cryptographic ciphers used by the Linux kernel
proc_diskstats            - I/O statistics of block devices
proc_dma                  - List of the registered ISA DMA channels in use
proc_filesystems          - List of the file system types currently supported by the kernel
proc_fs                   - File system parameters
proc_iomem                - Map of the system's memory for each physical device
proc_ioports              - List of currently registered port regions used for input or output communication with a device
proc_loadavg              - Load average in regard to both the CPU and IO over time
proc_locks                - Files currently locked by the kernel
proc_meminfo              - Reports a large amount of valuable information about the systems RAM usage
proc_modules              - List of all modules loaded into the kernel
proc_mounts               - List mounted filesystems (info provides from kernel)
proc_partitions           - Partition block allocation information
proc_scsi                 - List of every recognized SCSI device
proc_swaps                - Measures swap space and its utilization
proc_sys                  - Information about the system and kernel features
proc_uptime               - Information detailing how long the system has been on since its last restart
proc_version              - Version of the Linux kernel, the version of gcc used to compile the kernel, and the time of kernel compilation
proc_vmstat               - Detailed virtual memory statistics from the kernel
processor                 - Processor type
prtstat                   - Print statistics of a processes
ps                        - Report a snapshot of the current processes
rpm                       - Querying all RPM packages
services                  - Service names
services_list             - Displays services with status
services_params           - Displays services with status
shell_alias               - Shell alias names
shell_all_commands        - Shell command names
shell_builtins            - Names of shell builtin commands
shell_exported_variables  - Names of exported shell variables
shell_variables           - Names of all shell variables
sysctl                    - Runtime kernel parameters
sysctl_system             - Runtime kernel parameters from all system configuration files
timedatectl               - System time and date
udevadm                   - Queries the udev database for device information stored in the udev database
udevadm_block_devices     - Queries the udev database for block device information stored in the udev database
users                     - User names
vmstat_disk               - Report disk statistics
vmstat_disk_sum           - Report some summary statistics about disk activity
vmstat_forks              - Displays the number of forks since boot
vmstat_stats              - Displays a table of various event counters and memory statistics
yum_installed             - YUM - list installed packages
yum_repolist              - YUM - defined repositories
```
