import {Validator} from "jsonschema";

function validate_json(data, schema) {
  let v = new Validator();
  return v.validate(data, schema).errors
}

function validate_property(data, schema, name) {
  const errors = validate_json(data, schema);
  return errors.filter(
    (error) => error.property === "instance." + name || error.argument === Object.keys(data)[0]
  ).map((error) => schema.properties[name].error[error.name] || error.message);
}

export {validate_json, validate_property};
