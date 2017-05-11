import React, {Component} from 'react';
import {Dropdown, Form, Input} from 'semantic-ui-react';

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
      {key: 'fis', text: 'Fiscal', value: 'fiscal'}
    ];

    const {isCalendar, value} = this.state;

    return (
        <Form.Field>
          <label htmlFor='year'>Year</label>
          <Input
            name='year'
            label={<Dropdown defaultValue='calendar' options={options} onChange={this.onDropdownChange} />}
            labelPosition='left'
            maxLength='4'
            value={value}
            onChange={this.onInputChange}
          />
          {!isCalendar && value.length === 4 && `(July 1, ${value} – June 30, ${parseInt(value, 10) + 1})`}
        </Form.Field>
    )
  }
}

export default YearInput;
