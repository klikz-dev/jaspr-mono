"use strict";

const remove_suffix = ".app.jaspr-development.com";

exports.handler = (event, context, callback) => {
  const response = event.Records[0].cf.response;
  const request = event.Records[0].cf.request;
  const headers = request.headers;
  const host_header = headers.host[0].value;

  if (host_header.endsWith(remove_suffix)) {
    const wildcard_subdomain = host_header.substring(
      0,
      host_header.length - remove_suffix.length
    );

    if (wildcard_subdomain.indexOf("--") > -1) {
      // new fangled URL
      const subdomain = wildcard_subdomain.substring(
        wildcard_subdomain.indexOf("--") + 2
      );
      // prepend '/' + the subdomain onto the existing request path ("uri")
      request.uri = "/" + subdomain + request.uri;
    } else {
      // old school URL
      // prepend '/' + the subdomain onto the existing request path ("uri")
      request.uri =
        "/" +
        host_header.substring(0, host_header.length - remove_suffix.length) +
        request.uri;
    }

    const re = /(?:\.([^.]+))?$/; // Regex checks for file extension
    request.uri = request.uri.replace(/\/$/, "/index.html");
    if (request.uri.endsWith("index.html") || !re.exec(request.uri)[1]) {
      // URI's without file extensions are routes and should point to index.html
      request.uri = request.uri
        .split("/")
        .slice(0, 2)
        .concat("index.html")
        .join("/");
    }
  }

  // return control to CloudFront with the modified request
  return callback(null, request);
};
