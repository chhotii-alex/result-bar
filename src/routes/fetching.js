import { urlPrefix } from "./server_url.js";

export function URLforEndpoint(endpointName) {
  return `${urlPrefix}/${endpointName}`;
}
