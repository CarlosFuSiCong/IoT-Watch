export const DEG_C = '\u00B0C'

/** HH:MM:SS — for telemetry rows */
export const fmtTime = (iso: string) =>
  new Date(iso).toLocaleTimeString('en-GB', {
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  })

/** DD/MM HH:MM:SS — compact date+time for device context */
export const fmtDateTime = (iso: string) =>
  new Date(iso).toLocaleString('en-GB', {
    month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  })

/** YY/MM/DD HH:MM:SS — full date+time for list views */
export const fmtDateTimeFull = (iso: string) =>
  new Date(iso).toLocaleString('en-GB', {
    year: '2-digit', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
  })
