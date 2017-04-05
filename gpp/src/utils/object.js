/**
 * Object utilities
 */

/**
 * Returns a copy of an object excluding one property.
 *
 * Credit: just-boris
 * http://stackoverflow.com/questions/34698905/clone-a-js-object-except-for-one-key
 */
function omit(obj, omitKey) {
  return Object.keys(obj).reduce((result, key) => {
    if(key !== omitKey) {
       result[key] = obj[key];
    }
    return result;
  }, {});
}

export { omit };
