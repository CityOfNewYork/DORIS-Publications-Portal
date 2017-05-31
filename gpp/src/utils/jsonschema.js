import {Validator} from "jsonschema";

function validate_json(data, schema, propertyName) {
    let v = new Validator();
    const validation = v.validate(data, schema, {propertyName});
    debugger;
}

export {validate_json};
