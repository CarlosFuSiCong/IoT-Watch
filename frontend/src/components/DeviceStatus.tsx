interface Props {
  status: 'online' | 'offline'
}

export default function DeviceStatus({ status }: Props) {
  return (
    <>
      <span className={`status-dot ${status}`} />
      <span className={status === 'online' ? 'txt-online' : 'txt-offline'}>
        {status.toUpperCase()}
      </span>
    </>
  )
}
