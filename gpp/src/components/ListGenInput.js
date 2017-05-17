import React, {Component} from 'react';
import {Form, Icon, List, Segment} from 'semantic-ui-react';

class ListGenInput extends Component {
  state = {
    items: [],
    value: ''
  };

  onAdd = () => {
    if (this.state.value.replace(/^\s+|\s+$/g, '')) {
      this.setState({
        items: [this.state.value, ...this.state.items],
        value: ''
      });
    }
  };

  onRemove = (index) => (e) => {
    e.preventDefault();
    this.setState({
      items: [...this.state.items.slice(0, index), ...this.state.items.slice(index + 1)]
    })
  };

  handleChange = (e, {value}) => {
    this.setState({
      value: value
    })
  };


  render() {
    const items = this.state.items.length > 0 &&
      <List divided relaxed>
        {this.state.items.map((item, index) => (
          <List.Item key={index}>
            <List.Content verticalAlign="middle">
              <Icon
                link
                name="remove"
                onClick={this.onRemove(index)}
              /> {item}
            </List.Content>
          </List.Item>
        ))}
      </List>;

    return (
      <Form.Field>
        <Segment>
          <Form.Input
            {...this.props}
            icon={<Icon name="add" inverted circular link onClick={this.onAdd}/>}
            onChange={this.handleChange}
            value={this.state.value}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                this.onAdd();
              }
            }}
          />
          {items}
        </Segment>
      </Form.Field>
    )
  }
}

export default ListGenInput;
