import React from 'react';
import {Popup} from 'semantic-ui-react';
import './Nyc4dHeader.css'


const Nyc4dHeader = () => (
  <div className="nycidm-header">
    <div className="upper-header-black">
      <div className="container-nycidm">
        <span className="upper-header-left">
          <a href="https://www1.nyc.gov">
            <img className="small-nyc-logo" alt=""
                 src="http://nyc4d.nycnet/assets/images/pages/intergration/nyc_white@x2.png"/>
          </a>
          <img className="vert-divide" alt=""
               src="http://nyc4d.nycnet/assets/images/pages/intergration/upper-header-divider.gif"/>
          <span className="upper-header-black-title">
            DORIS Government Publications Portal
          </span>
        </span>
        <span className="upper-header-right">
          <span className="upper-header-a">
            <Popup
              inverted
              trigger={<a href="">Log In</a>}
              content='Only NYC agency employees can be granted authorization to submit documents.
              If you are not employed by a city agency, please do not attempt to log in.'
            />
          </span>
        </span>
      </div>
    </div>
  </div>
);

export default Nyc4dHeader;
