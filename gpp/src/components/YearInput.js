import React, {Component} from 'react';
import {Select, Form, Label, Popup, Icon} from 'semantic-ui-react';
import TooltippedLabel from './TooltippedLabel';

class YearInput extends Component {
  state = {
    isCalendar: true,
    value: ''
  };

  onDropdownChange = (e, {value}) => {
    this.setState({
      isCalendar: value === 'calendar'
    })
  };

  onInputChange = (e, {value}) => {
    if (/^[0-9]+$/.test(value.slice(-1)) || value === '') {
      this.setState({
        value: value
      })
    }
  };

  render() {
    const options = [
      {key: 'cal', text: 'Calendar', value: 'calendar'},
      {key: 'fis', text: 'NYC Fiscal', value: 'fiscal'}
    ];

    const {isCalendar, value} = this.state;

    return (
      <div>
        <Form.Input
          label={<TooltippedLabel tooltipContent="Testing 1 2 3" labelContent="Associated Year" />}
          name='year'
          action={
            <Select
              compact
              defaultValue='calendar'
              options={options}
              onChange={this.onDropdownChange}
            />
          }
          maxLength='4'
          value={value}
          onChange={this.onInputChange}
        />
        {
          !isCalendar && value.length === 4 &&
          <Label pointing>
            July 1, {value} – June 30, {parseInt(value, 10) + 1}
          </Label>
        }
      </div>
    )
  }
}

export default YearInput;
