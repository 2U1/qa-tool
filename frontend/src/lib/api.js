import qs from "qs";

const fastapi = (
  operation,
  url,
  params,
  success_callback,
  failure_callback
) => {
  let method = operation;
  let headers = {};
  let body;

  if (params instanceof FormData) {
    // When using FormData, the browser will automatically set the Content-Type to 'multipart/form-data'
    // with the boundary parameter, so we don't set it manually.
    body = params;
  } else {
    // For JSON or URL-encoded content, set the Content-Type header accordingly
    if (operation === "login") {
      headers["Content-Type"] = "application/x-www-form-urlencoded";
      body = qs.stringify(params);
    } else {
      headers["Content-Type"] = "application/json";
      body = JSON.stringify(params);
    }
  }

  let _url = import.meta.env.VITE_SERVER_URL + url;

  if (method === "get") {
    _url += "?" + new URLSearchParams(params);
  }

  let options = {
    method: method,
    headers: headers,
  };

  if (method !== "get") {
    options["body"] = body;
  }
  fetch(_url, options).then((response) => {
    if (response.status === 204) {
      // No content
      if (success_callback) {
        success_callback();
      }
      return;
    }
    response
      .json()
      .then((json) => {
        if (response.status >= 200 && response.status < 300) {
          // 200 ~ 299
          if (success_callback) {
            success_callback(json);
          }
        } else {
          if (failure_callback) {
            failure_callback(json);
          } else {
            alert(JSON.stringify(json));
          }
        }
      })
      .catch((error) => {
        alert(JSON.stringify(error));
      });
  });
};

export default fastapi;
