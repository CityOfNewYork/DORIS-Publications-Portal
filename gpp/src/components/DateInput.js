import React, {Component} from 'react';
import {MaskedInput} from 'react-text-mask';
import {Form} from 'semantic-ui-react';
import DatePicker from 'react-datepicker';
import moment from 'moment';

import 'react-datepicker/dist/react-datepicker.css';

class Input extends Component {
  state = {
    value: this.props.value
  };

  handleChange = (e) => {
    this.setState({
      value: e.target.value
    })
  };

  render() {
    return (
      <Form.Input
        required
        label="Date Published"
        name="date"
        children={
          <MaskedInput
            mask={[/\d/, /\d/, '/', /\d/, /\d/, '/', /\d/, /\d/, /\d/, /\d/]}
            placeholder="MM/DD/YYYY"
            required
            pattern=""
            onClick={this.props.onClick}
            value={this.state.value}
            onChange={this.handleChange}
          />
        }
      />
    )
  }
}

class DateInput extends Component {
  constructor(props) {
    super(props);
    this.state = {
      startDate: moment()
    };
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(date) {
    this.setState({
      startDate: date
    });
  }

  render() {
    return <DatePicker
      selected={this.state.startDate}
      customInput={<Input />}
      onChange={this.handleChange}
    />;
  }
}

export default DateInput;
