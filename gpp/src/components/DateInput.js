import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {MaskedInput} from 'react-text-mask';
import {Form} from 'semantic-ui-react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import './DateInput.css';

class Input extends Component {  // Must be a class; DatePicker gives its customInput prop a ref
  render() {
    const {error, onClick, onChange, value, label, name} = this.props;
    return (
      <Form.Input
        error={error}
        required
        label={label}
        name={name}
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
  static propTypes = {
    label: PropTypes.oneOfType([
      PropTypes.string.isRequired,
      PropTypes.element.isRequired
    ]),
    name: PropTypes.string.isRequired,
    maxDate: PropTypes.object
  };

  state = {
    date: undefined,
    moment: this.props.maxDate || null,
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
        (this.state.moment && this.state.moment.diff(parsedDate, 'days') < 0)
      )
    });
  };

  render() {
    const {date, moment, error} = this.state;
    const {label, name} = this.props;
    return <DatePicker
      maxDate={moment}
      selected={date}
      customInput={
        <Input
          onChange={this.handleChange}
          error={error}
          label={label}
          name={name}
        />
      }
      onChange={this.handleChange}
      onChangeRaw={this.handleChangeRaw}
    />;
  }
}

export default DateInput;