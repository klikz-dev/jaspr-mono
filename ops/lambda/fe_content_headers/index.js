"use strict";
exports.handler = (event, context, callback) => {
  //Get contents of response
  const request = event.Records[0].cf.request;
  const response = event.Records[0].cf.response;
  const headers = response.headers;
  const customHeaders = request.origin.s3.customHeaders;

  const JASPR_CDN = customHeaders["x-env-jaspr-cdn"][0].value;
  const API_ROOT = customHeaders["x-env-api-root"][0].value;
  const SENTRY_ROOT = customHeaders["x-env-sentry-root"][0].value;
  const SENTRY_REPORT = customHeaders["x-env-sentry-report"][0].value;

  const CSP_POLICY =
    "default-src 'self'; " +
    "script-src 'self' cdn.segment.com; " +
    "style-src 'self'; " +
    `img-src 'self' data: ${JASPR_CDN}; ` +
    "font-src 'self'; " +
    `connect-src 'self' ${API_ROOT} api.segment.io ${SENTRY_ROOT} ${JASPR_CDN}; ` +
    "object-src 'none'; " +
    `media-src 'self' ${JASPR_CDN}; ` +
    "upgrade-insecure-requests; " +
    "block-all-mixed-content; " +
    `report-uri ${SENTRY_REPORT}`;

  const PERMISSION_POLICY =
    "geolocation 'none'; " +
    "notifications 'none'; " +
    "push 'none'; " +
    "midi 'none'; " +
    "camera 'none'; " +
    "microphone 'none'; " +
    "speaker-selection 'none'; " +
    "device-info 'none'; " +
    "background-fetch 'none'; " +
    "background-sync 'none'; " +
    "bluetooth 'none'; " +
    "persistent-storage 'none'; " +
    "ambient-light-sensor 'none'; " +
    "accelerometer 'none'; " +
    "gyroscope 'none'; " +
    "magnetometer 'none'; " +
    "clipboard-read 'none'; " +
    "clipboard-write 'self'; " +
    "display-capture 'none'; " +
    "nfc 'none'; " +
    `report-uri ${SENTRY_REPORT}`;

  //Set new headers
  headers["strict-transport-security"] = [
    {
      key: "Strict-Transport-Security",
      value: "max-age=31536000; includeSubdomains; preload",
    },
  ];
  headers["x-content-type-options"] = [
    { key: "X-Content-Type-Options", value: "nosniff" },
  ];
  headers["x-xss-protection"] = [
    { key: "X-XSS-Protection", value: "1; mode=block" },
  ];
  headers["referrer-policy"] = [
    { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  ];
  headers["feature-policy"] = [
    {
      key: "Feature-Policy",
      value:
        "geolocation 'none';midi 'none';sync-xhr 'none';microphone 'none';camera 'none';magnetometer 'none';gyroscope 'none';fullscreen 'self';payment 'none';",
    },
  ];
  headers["permissions-policy"] = [
    { key: "Permissions-Policy", value: PERMISSION_POLICY },
  ];
  headers["Content-Security-Policy-Report-Only"] = [
    { key: "Content-Security-Policy-Report-Only", value: CSP_POLICY },
  ];

  //Return modified response
  callback(null, response);
};
