export default function dateFilter(value) {
  const options = {
      day: "numeric",
      month: "short",
      year: "numeric"
  }
  const LOCALE = navigator.language || navigator.userLanguage
  return new Intl.DateTimeFormat(LOCALE, options).format(new Date(value))
}
