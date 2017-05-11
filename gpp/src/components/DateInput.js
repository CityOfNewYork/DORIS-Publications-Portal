import React, {Component} from 'react';
import {MaskedInput} from 'react-text-mask';
import {Form} from 'semantic-ui-react';
import DatePicker from 'react-datepicker';
import moment from 'moment';
import 'react-datepicker/dist/react-datepicker.css';
import './DateInput.css';

class Input extends Component {  // Must be a class; DatePicker gives its customInput prop a ref
  render() {
    const {error, onClick, onChange, value} = this.props;
    return (
      <Form.Input
        error={error}
        required
        label="Date Published"
        name="date"
        children={
          <MaskedInput
            mask={[/\d/, /\d/, '/', /\d/, /\d/, '/', /\d/, /\d/, /\d/, /\d/]}
            placeholder="MM/DD/YYYY"
            required
            pattern="(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.]\d\d\d\d"
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
    date: undefined,
    moment: moment().startOf('day'),
    error: false
  };

  handleChange = (date) => {
    this.setState({
      date: date,
      error: false
    });
  };

  static isValidDate(month, day, year) {
    const date = new Date(year, month - 1, day);
    // eslint-disable-next-line
    return date && date.getMonth() + 1 == month;  // this is a perfectly reasonable use of type coercion
  }

  handleChangeRaw = (e) => {
    const value = e.target.value,
      // .match returns null if value is not in the format: DD/DD/DDDD
      dateMatch = (value).match(/^(\d{2})\/(\d{2})\/(\d{4})$/),
      parsedDate = Date.parse(value);
    this.setState({
      // .diff will return negative values if the parsedDate is greater than today
      error: (
        dateMatch === null ||
        !DateInput.isValidDate(...value.split("/")) ||
        this.state.moment.diff(parsedDate, 'days') < 0
      )
    });
  };

  render() {
    const {date, moment, error} = this.state;
    return <DatePicker
      maxDate={moment}
      selected={date}
      customInput={<Input onChange={this.handleChange} error={error}/>}
      onChange={this.handleChange}
      onChangeRaw={this.handleChangeRaw}
    />;
  }
}

export default DateInput;
