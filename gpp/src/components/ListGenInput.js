import React, {Component} from 'react';
import {Form, Icon, List, Segment} from 'semantic-ui-react';

class ListGenInput extends Component {
  state = {
    items: [],
    value: ''
  };

  onAdd = () => {
    this.setState({
      items: [this.state.value, ...this.state.items],
      value: ''
    });
  };

  handleChange = (e, {value}) => {
    this.setState({
      value: value
    })
  };


  render() {
    const items = this.state.items.length > 0 &&
      <Segment>
        <List divided relaxed>
          {this.state.items.map((item, index) => (
            <List.Item
              key={index}
              content={item}
            />
          ))}
        </List>
      </Segment>;

    return (
      <Form.Field>
        <Form.Input
          {...this.props}
          icon={<Icon name="add" inverted circular link onClick={this.onAdd}/>}
          onChange={this.handleChange}
          value={this.state.value}
          onKeyDown={(e) => {
            if (e.key === 'Enter'){
              e.preventDefault();
              this.onAdd();
            }
          }}
        />
        {items}
      </Form.Field>
    )
  }
}

export default ListGenInput;
