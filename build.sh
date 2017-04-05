#!/usr/bin/env bash

# build.sh
# --------
#
# Must be run from project root.
#
# After running this script you should be able to run the entire application through Flask.
# You will not longer need to have the react app running (i.e. npm start) to interact with
# the Government Publications Portal in the state of its latest build.

command -v npm >/dev/null 2>&1 || { echo >&2 "npm not installed.  Aborting."; exit 1; }
cd gpp/
npm run build
cd ../
if [ -d app/static ]; then
    rm -rf app/static
fi
mv gpp/build/* app/
mkdir app/static/img/
mv app/favicon.ico app/static/img/
mv app/index.html app/templates/index.html
rmdir gpp/build/
