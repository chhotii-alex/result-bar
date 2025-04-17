export function URLforEndpoint(endpointName) {
  let [protocol, path, port] = window.location.origin.split(":");
  let urlPrefix = `${protocol}:${path}:8000`;
  return `${urlPrefix}/${endpointName}`;
}
