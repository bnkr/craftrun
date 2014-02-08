#! /bin/sh
### BEGIN INIT INFO
# Provides:          minecraft-server
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Craftrun based init script.
# Description:       Run a minecraft server.
### END INIT INFO

# Author: James Webber <bunkerprivate@gmail.com>

# Do NOT "set -e"

# PATH should only include /usr/* if it runs after the mountnfs.sh script
PATH=/sbin:/usr/sbin:/bin:/usr/bin

##############################################################################
## You should change these variables if you have multiple minecraft servers ##
##############################################################################

DESC="Minecraft server"
NAME=minecraft
CRAFTRUN=/usr/bin/craftrun
CRAFTRUN_CONF=/etc/minecraft/craftrun.yml

#########
## END ##
#########

SCRIPTNAME=/etc/init.d/$NAME

# Exit if the package is not installed
[ -x "$CRAFTRUN" ] || exit 0

# Read configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

# Load the VERBOSE setting and other rcS variables
. /lib/init/vars.sh

# Define LSB log_* functions.
# Depend on lsb-base (>= 3.2-14) to ensure that this file is present
# and status_of_proc is working.
. /lib/lsb/init-functions

OUTPUT=""
STATUS=0

craftrun()
{
  $CRAFTRUN -c $CRAFTRUN_CONF "$*"
}

do_status()
{
  craftrun status
}

#
# Function that starts the daemon/service
#
do_start()
{
  # Return
  #   0 if daemon has been started
  #   1 if daemon was already running
  #   2 if daemon could not be started
  craftrun status && return 1
  craftrun start || return 2

  # Add code here, if necessary, that waits for the process to be ready
  # to handle requests from services started subsequently which depend
  # on this one.  As a last resort, sleep for some time.
  # (craftrun will do this for us)
}

#
# Function that stops the daemon/service
#
do_stop()
{
  # Return
  #   0 if daemon has been stopped
  #   1 if daemon was already stopped
  #   2 if daemon could not be stopped
  #   other if a failure occurred
  craftrun status && return 1
  craftrun stop || return 2

  # Wait for children to finish too if this is a daemon that forks
  # and if the daemon is only ever run from this initscript.
  # If the above conditions are not satisfied then add some other code
  # that waits for the process to drop all resources that could be
  # needed by services started subsequently.  A last resort is to
  # sleep for some time.
  # (craftrun will handle this)

  # Many daemons don't delete their pidfiles when they exit.
  # (we don't have one)
}

#
# Function that sends a SIGHUP to the daemon/service
#
do_reload() {
  #
  # If the daemon can reload its configuration without
  # restarting (for example, when it is sent a SIGHUP),
  # then implement that here.
  #
  # (no such operation)
  return 0
}

case "$1" in
  start)
  [ "$VERBOSE" != no ] && log_daemon_msg "Starting $DESC" "$NAME"
  do_start
  case "$?" in
    0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
    2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
  esac
  ;;
  stop)
  [ "$VERBOSE" != no ] && log_daemon_msg "Stopping $DESC" "$NAME"
  do_stop
  case "$?" in
    0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
    2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
  esac
  ;;
  status)
  do_status
  exit $?
  ;;
  #reload|force-reload)
  #
  # If do_reload() is not implemented then leave this commented out
  # and leave 'force-reload' as an alias for 'restart'.
  #
  #log_daemon_msg "Reloading $DESC" "$NAME"
  #do_reload
  #log_end_msg $?
  #;;
  restart|force-reload)
  #
  # If the "reload" option is implemented then remove the
  # 'force-reload' alias
  #
  log_daemon_msg "Restarting $DESC" "$NAME"
  do_stop
  case "$?" in
    0|1)
    do_start
    case "$?" in
      0) log_end_msg 0 ;;
      1) log_end_msg 1 ;; # Old process is still running
      *) log_end_msg 1 ;; # Failed to start
    esac
    ;;
    *)
    # Failed to stop
    log_end_msg 1
    ;;
  esac
  ;;
  *)
  #echo "Usage: $SCRIPTNAME {start|stop|restart|reload|force-reload}" >&2
  echo "Usage: $SCRIPTNAME {start|stop|status|restart|force-reload}" >&2
  exit 3
  ;;
esac

:
