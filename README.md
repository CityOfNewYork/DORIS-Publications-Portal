# Government Publications Portal

The Unholy Union of Alan Chen's Government Publications Sumissions Portal WIP and 
the Government Publications Portal developed in the Summer of 2014.

> Flask + React & Redux, using the [JSend](https://labs.omniti.com/labs/jsend) specification
and the [Semantic-UI](http://react.semantic-ui.com/introduction) framework

## Development Process Notes

- The following directories and files in `app/` should **not** be altered manually:

    - `templates/`
    - `static/`
    - `asset-manifest.json`
    - `favicon.ico`
    - `package.json`
    
- Changes made during frontend development should only affect the `gpp/` directory.

- In order to run the Government Publications Portal without having to launch the React app
(i.e. Flask only), run `./build.sh`.
  - This script will produce a build of the React app optimized for production--using
  `npm run build`--and will transfer it to `app/`.
  - Since **`master`** should always be in a production-ready state, `build.sh` should 
  be executed before pushing to the branch whenever any frontend changes are made.


### Redux Usage

- Currently, Redux is only being used to manage pseudo-user authentication. Since
Flask-Login is handling user state on the server, the Redux store simply consists 
of a toggleable boolean: `authenticated`.
- [Redux Persist](https://github.com/rt2zz/redux-persist#why-redux-persist) is used to maintain
application state across a browser refresh.

### How To: Forms

#### Part 1 - BE

1. Create a `forms.py` file in the corresponding resource package 
(e.g. `app/resources/v1/publications/`) if the file does not yet exist.
2. In `forms.py`, use WTForms to create a form class with fields that mostly will only consist of validators.
3. In your resource api, use the newly-created form to validate request data.

#### Part 2 - FE

- Please refer to http://react.semantic-ui.com/collections/form
- A [higher-order component](https://facebook.github.io/react/docs/higher-order-components.html), `withValidation`, 
is provided in `gpp/src/custom.js` to aid the form creation process. It handles the collection, updating, and 
submission of form data and will populate its state's `error` property if there are issues during submission or 
if the server responds with any errors.
    
## Development Environment Setup

1. Make sure you have the latest version of VirtualBox.

2. Copy `rhel-6.8.virtualbox.box` from `smb://nas2012server03.records.nycnet/public/webdev` 
into your project root or any desired directory.

3. Run `./setup.sh` from within your project root directory.

    - This script will attempt to:
    
        - Add the *rhel-6.8* vagrant box
        - Install the vagrant plugins *vagrant-reload* and *vagrant-vbguest*
        - Copy `Vagrantfile.example` into `Vagrantfile`
        - Prompt you for your RedHat Developer Account credentials
            - If you do not have a developer account, [create one](https://www.redhat.com/en/developers).
        - Build your development VM
        
    - If you experience build errors, try re-provisioning:

            RH_USER=<Your RedHat Username> RH_PASS=<Your Redhat Password> vagrant provision
    
    - If you do not want to set the `RH_` environment variables and you don't mind having 
    your RedHat credentials stored in your `Vagrantfile`, you can add them on lines 4 and 5.

4. Run `vagrant ssh` to connect to your development environment.

5. Run `python manage.py runserver` to start the app.
You can access it on your browser at `https://10.0.0.2`

    - You can also run `python manage.py runserver -host 0.0.0.0` to access the app at `localhost:8000`
    
#### You can stop here if you're only doing backend development. Otherwise, you will need to do the following:

6. In the settings of your preferred project editor, set the *Tab Size* and *Indent* to 2.
If you are using PyCharm (2016.3), these settings can be found in `Preferences > Editor > Code Styles`.

7. Install npm (or yarn)

    OS X: `brew install npm`
    
    RedHat: `sudo yum -y install rh-nodejs4; scl enable rh-nodejs4 bash`

      - It might be a good idea to make an alias for that second command as 
        you will need to execute it before running any npm command: `alias enable_node="scl enable rh-nodejs4 bash"`

8. Navigate to `gpp/` and run `npm install`

9. Run `npm start`
       
   - The application that has been started is the only one you need to access via browser 
     (see table below) in order to test any changes. The Flask app will serve as your 
     backend so make sure that is running as well!

| Environment | Browser Address | `package.json` proxy | hot reload? |
|---|---|---|---|
| Local | http://localhost:4000 | http://localhost:8000 | Yes |
| Vagrant | http://localhost:5000 | http://localhost:5000 | No :( |