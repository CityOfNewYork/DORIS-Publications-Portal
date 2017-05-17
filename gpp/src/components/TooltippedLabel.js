import React from 'react';
import PropTypes from 'prop-types';
import {Popup, Icon} from 'semantic-ui-react';


const TooltippedLabel = ({tooltipContent, labelContent, position}) => (
  <label>
    <Popup
      trigger={<Icon name="question" link circular />}
      content={tooltipContent}
      position={position}
    /> {labelContent}
  </label>
);

TooltippedLabel.propTypes = {
  tooltipContent: PropTypes.string.isRequired,
  labelContent: PropTypes.string.isRequired,
  position: PropTypes.string
};

TooltippedLabel.defaultProps = {
  position: 'top center'
};

export default TooltippedLabel;
