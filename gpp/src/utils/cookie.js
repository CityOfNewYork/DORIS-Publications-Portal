/**
 * Helpers for managing cookies.
 */

/**
 * Returns the value of a cookie or null if not found.
 * Provided by http://www.quirksmode.org/js/cookies.html
 * @param {string} name The name of the cookie
 */
function readCookie(name) {
  let nameEQ = name + "=";
  let ca = document.cookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1, c.length);
    }
    if (c.indexOf(nameEQ) === 0) {
      return c.substring(nameEQ.length, c.length);
    }
  }
  return null;
}

export {readCookie};
