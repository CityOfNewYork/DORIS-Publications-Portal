import React, {Component} from 'react';
import {MaskedInput} from 'react-text-mask';
import {Form} from 'semantic-ui-react';
import DatePicker from 'react-datepicker';
import moment from 'moment';
import 'react-datepicker/dist/react-datepicker.css';


class Input extends Component {  // Must be a class; DatePicker gives its customInput prop a ref
  render() {
    const {onClick, onChange, value} = this.props;
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
            pattern=""  // TODO: pattern for dates
            onClick={onClick}
            value={value}
            onChange={onChange}
          />
        }
      />
    )
  }
}


class DateInput extends Component {
  state = {
    date: moment()
  };

  handleChange = (date) => {
    this.setState({
      date: date
    });
  };

  render() {
    return <DatePicker
      selected={this.state.date}
      customInput={<Input onChange={this.handleChange}/>}
      onChange={this.handleChange}
    />;
  }
}

export default DateInput;
