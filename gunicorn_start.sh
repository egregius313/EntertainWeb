NAME="entertainweb"                               # Name of the the application
VIRTENVDIR=/webapps/virtenv                       # Which virtual environment to use 
DJANGODIR=/webapps/entertainweb                   # Django project directory
SOCKFILE=/webapps/virtenv/run/gunicorn.sock       # we will communicte using this unix socket
USER=michael                                      # the user to run as
GROUP=webapps                                     # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=entertainweb.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=entertainweb.wsgi                     # WSGI module name

echo "Starting $NAME as $(whoami)"

# Activate the virtual environment
cd $VIRTENVDIR
. bin/activate

cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
cd $VIRTENVDIR
exec bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
