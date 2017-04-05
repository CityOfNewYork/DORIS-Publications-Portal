/**
 * Wrapper functions for the Fetch API
 */
import {readCookie} from './cookie'

/**
 * Returns a fetch() promise after sending a request
 * including the csrf token header.
 */
function csrfFetch(url, options={}) {
  return fetch(url, {  // TODO: needs polyfill https://github.com/github/fetch
    ...options,
    credentials: "same-origin",  // automatically send cookies for the current domain
    headers: {
      "X-CSRFToken": readCookie("csrf_token")
    }
  })
}

export {csrfFetch};
