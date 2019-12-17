export default function roundFilter(value, decimals) {

  if(!value) {
    value = 0;
  }

  if(!decimals) {
    decimals = 2;
  }

  value = Math.round(value * Math.pow(10, decimals)) / Math.pow(10, decimals);
  return value;
}
